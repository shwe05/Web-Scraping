import requests
import json
import pyttsx3



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
    def covid_symptoms(self):
        symptoms = ' Most common symptoms: \n Fever \n Dry cough \n Tiredness \n Less common symptoms:\n \
Aches and pains \n Sore throat \n Diarrhoea \n Conjunctivitis \n Headache \n Loss of taste or smell \n A rash on skin, or discolouration of fingers or toes'
        return symptoms 


        
        t = threading.Thread(target=poll) #Helps with waiting time, so you dont have to wait and it wont take over while ur running
        t.start() 


def scraping():
    
    data = Data(API_KEY, PROJECT_TOKEN)
    print('Started Program')
    print("Hello! What will you like to find out about today's Covid-19 statistics?")
    print('-------------------------------------------------------------------------') 
    
    while True:
        print('1. Worldwide')
        print('-')
        print('2. Country')
        print('-')
        print('3. Symptoms of Covid-19')
        print('-')
        print('4. Update information to latest')
        print('-')
        print('5. Quit')
        print('-')
        
        choice = input('Please provide an option: ')



        
        if choice == '1':
            option = input('Cases or deaths?')
            option = option.lower()

            
            if option == 'cases':
                print(data.get_total_cases())

                
            if option == 'deaths':
                print(data.get_total_deaths())

                
            else:
                print('Error: Please write a valid option.') 

        if choice == '2':
            option = input('Cases or deaths?')
            option = option.lower()

            
            if option == 'cases':
                country_choice = input("Which country?")
                country_choice = country_choice.lower()
                print(data.get_country_data(country_choice)['total_cases'])

                
            if option == 'deaths':
                country_choice = input("Which country?")
                country_choice = country_choice.lower()
                print(data.get_country_data(country_choice)['total_deaths'])

                
            else:
                print('Error: Please write a valid option.')



                
        if choice == '3':
            print(data.covid_symptoms())

            
                    
        if choice == '4':
            print("Data is being updated. This may take a moment!")
            data.update_data()

            
        if choice =='5':
            print('Goodbye.')
            break

        
        else:
            print('Error: Please write a valid option.')
            
scraping() 
            
            
            
                
                
            
        
        
