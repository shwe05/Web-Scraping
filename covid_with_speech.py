import requests 
import json 
import pyttsx3
import speech_recognition as sr
import re
import threading
import time




API_KEY = "tK_TX2T6D4kz"
PROJECT_TOKEN = "tXzK_eFxB15Y"
RUN_TOKEN = "t2oeD61dA0Mk"



class Data:
    def __init__(self,api_key,project_token):
        self.api_key = api_key
        self.project_token = project_token
        self.params = {
            "api_key" : self.api_key
            }  #This is for authentication
        self.data = self.get_data() 

    def get_data(self): #Can keep gettingand updating the latest data and call it at any point 
        #last_ready_run means i can extract that latest data 
        response = requests.get(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/last_ready_run/data',params=self.params)
        data = json.loads(response.text)
        return data 
        
    def get_total_cases(self):
        data = self.data['total']
        for content in data:
            if content['name'] == "Coronavirus Cases:":
                return content['value']
            
            
    def get_total_deaths(self):
        data = self.data['total']
        for content in data:
            if content['name'] == "Deaths:":
                return content['value']


    def get_country_data(self,country):
        data = self.data["country"]
        for content in data:
            if content['name'].lower() == country.lower():
                return content

        return "0" 


    def get_list_of_countries(self):
        countries  = []
        for country in self.data['country']:
            countries.append(country['name'].lower())
        return countries 


    def update_data(self):
        response = requests.post(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/run',params=self.params)


        def poll():
            time.sleep(0.1)
            old_data = self.data
            while True:
                new_data = self.get_data()
                if new_data != old_data:
                    self.data = new_data
                    print("Data updated")
                    break
                time.sleep(5) 
                


        
        t = threading.Thread(target=poll) #Helps with waiting time, so you dont have to wait and it wont take over while ur running
        t.start() 



def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

'''Function that defines our audio'''
def get_audio():
    r = sr.Recognizer()  #1. Recognize 
    with sr.Microphone() as source: 
        audio = r.listen(source)
        said = "" #Get the recording 

        try:
            said = r.recognize_google(audio) #Send to this recognizer
        except Exception as e:
            print("Exception:", str(e)) #When there is error
    return said.lower()
    

def main():
    print("Started Program")
    data = Data(API_KEY, PROJECT_TOKEN)
    END_PHRASE = "stop"
    country_list = data.get_list_of_countries()

    TOTAL_PATTERNS = {
        re.compile("[\w\s]+ total [\w\s]+ cases"): data.get_total_cases,
        re.compile("[\w\s]+ total cases"): data.get_total_cases,
        re.compile("[\w\s]+ total [\w\s]+ deaths"): data.get_total_deaths,
        re.compile("[\w\s]+ total deaths"): data.get_total_deaths}#w\s means, "any number of words"

    COUNTRY_PATTERNS = {
        re.compile("[\w\s]+ cases [\w\s]+"): lambda country: data.get_country_data(country)['total_cases'],
        re.compile("[\w\s]+ deaths [\w\s]+"): lambda country: data.get_country_data(country)['total_deaths']
        }#lambda takes in the variable country  

    
    UPDATE_COMMAND = "update" 
                             
    while True:
        print("Listening...")
        text = get_audio()
        print(text) 
        result = None 

        for pattern, func in COUNTRY_PATTERNS.items():
            if pattern.match(text):
                words = set(text.split(" ")) #Eg. "How many cases in Myanmar" ---> {"how", "many"} ... 
                for country in country_list:
                    if country in words:
                        result = func(country) 
                        break


        for pattern, func in TOTAL_PATTERNS.items():
            if pattern.match(text):
                result = func() #store the value
                break
        if text == UPDATE_COMMAND:
            result = "Data is being updated. This may take a moment!"
            data.update_data() 
            
        if result:
            speak(result)

        if text.find(END_PHRASE) != -1:
            print('Exit') 
            break
            
main()
            
