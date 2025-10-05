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


class DataUserPassedFailedDublicate:
    create_dublicate_user = {
                "email": "qwerty130@mail.ru",
                "password": "123456", 
                "name": "Duplicate User"
            }
    
class LoginPassedUser:
    email = 'qwerty14@mail.ru'
    password = '123456'
    name = 'qwerty14'

class LoginFailedUser:
    email = 'failed.ru'
    password = 'failed12'

    