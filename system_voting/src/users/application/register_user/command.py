class RegisterUserCommand:
    def __init__(self, email:str, password: str, role:str):
        self.email = email
        self.password = password
        self.role = role