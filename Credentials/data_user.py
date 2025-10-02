from helpers import GenerateDataUser

generator = GenerateDataUser()

class DataUser:
    emailPasswordName = [
        ((email := generator.generate_email()), (password := generator.generate_password()), (name := generator.generate_name())),
        (email, password, name),
        ('', 'witcher55', 'Gerald')
    ]