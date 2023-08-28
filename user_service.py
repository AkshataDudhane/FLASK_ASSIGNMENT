from datetime import datetime, date
import re
class User:
    def __init__(self,name, birthday, email, state, zipcode):

        self.name = name
        self.birthday = self.parse_date(birthday)
        self.email = email
        self.state = state
        self.zipcode = zipcode

    def parse_date(self, date_str):

        if isinstance(date_str, str):
            return datetime.strptime(date_str, '%m/%d/%Y')
        elif isinstance(date_str, date):
            return date_str
        else:
            raise ValueError("Invalid date format")

#writing a function for : No wine can ship to New Jersey, Connecticut, Pennsylvania, Massachusetts, Illinois, Idaho or Oregon
    def check_state(self):

        if self.state not in ['NJ','CT','PA','MA','IL','ID','OR']:
            return True
        else:
            return False
        

    #2)writing the function for: Wine can not ship to any zipcode that has two consecutive numbers next to each other


    #it takes zipcode as an input and converts it into a string.
    def check_zip(self):

        zip_str=str(self.zipcode)
        for i in range(len(zip_str)-1): #iterating through the characters
            if (int(zip_str[i])+1==int(zip_str[i+1]) or int(zip_str[i+1])+1==int(zip_str[i])): #checking if the current character and next character if find return true else false
                return False
        return True


    #3) writing a function to return wine not sold to anyone born on the first Monday of the month.

    def val_weekday(self):

        # weekday=datetime.strptime(self.birthday, '%m/%d/%Y') #converting weekday to a datetime object and matching the date format
        return self.birthday.weekday()!=0 or self.birthday.day>7
    #returns true if the particular day is not the first monday(0) or day should be greater than 7.


    #4) writing a function for email validation
    def check_email(self):

        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b' #regex pattern
        if re.fullmatch(pattern, self.email): #match the entire input string against the regular expression 
            return True
        else:
            return False

    #21 years 
    def calculateAge(self):
        
        # birth=datetime.strptime(self.birthday, '%m/%d/%Y')
        today = date.today()
        age = today.year - self.birthday.year
        if(today.month<self.birthday.month or (today.month==self.birthday.month and today.day<self.birthday.day)):
            '''to check if person's is birth month or date falls after the current month or date
            if birth year=2002 age will be considered as 21.
            if birthday is on 26th july 2023, present month=birth month and present date(25)<birth date(26)
            '''
            age-=1
            #we need to subtract age by 1 so actual age will be 20
        return age>=21