import random


class GenerateDataUser:
    def generate_email(self):
        number = ''.join([str(random.randint(0, 9)) for _ in range(7)])
        email = f'wildhant{number}@mail.ru'
        return email
    
    def generate_password(self):
        password = ''.join([str(random.randint(0, 9)) for _ in range(7)])
        return password
    
    def generate_name(self):
        number_2 = ''.join([str(random.randint(0, 9)) for _ in range(7)])
        name = f'elf{number_2}'
        return name