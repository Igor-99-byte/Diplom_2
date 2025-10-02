import random


class GenerateDataUser:
    def generate_email(self):
        number = random.randint(1, 1000)
        email = f'wildhant{number}@mail.ru'
        return email
    
    def generate_password(self):
        password = ''.join(str(random.randint(0, 9)) for _ in range(7))
        return password
    
    def generate_name(self):
        number_2 = random.randint(1, 1000)
        name = f'elf{number_2}'
        return name