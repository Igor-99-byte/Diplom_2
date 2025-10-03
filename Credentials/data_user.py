from helpers import GenerateDataUser

generator = GenerateDataUser()

class DataUser:
    def create_email(self):
        email = generator.generate_email()
        return email
    
    def create_password(self):
        password = generator.generate_email()
        return password
    
    def create_name(self):
        name = generator.generate_email()
        return name
    