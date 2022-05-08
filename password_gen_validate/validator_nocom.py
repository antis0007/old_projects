import secrets
def secure(password):
    special = "!-$%&'()*+,./:;<=>?_[]^`{|}~"
    contains_lower = False
    contains_upper = False
    contains_digit = False
    contains_special = False
    for i in password:
        if i.islower() == True:
            contains_lower = True
        elif i.isupper() == True:
            contains_upper = True
        elif i.isdigit() == True:
            contains_digit = True
    for i in special:
        if i in password:
            contains_special = True
            break
    if(contains_lower==True and contains_upper==True and contains_digit==True and contains_special==True):
        return(True)
def validate(password):
    special = "!-$%&'()*+,./:;<=>?_[]^`{|}~"
    forbidden = [" ","@","#"]
    for i in forbidden:
        if i in password:
            return("Invalid")
    if len(password)<8:
        return("Invalid")
    if secure(password) == True:
        return("Secure")
    return("Insecure")
def generate(n):
    special = "!-$%&'()*+,./:;<=>?_[]^`{|}~"
    all_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!-$%&'()*+,./:;<=>?_[]^`{|}~"
    while True:
        password = ("").join(secrets.choice(all_characters) for i in range(n))
        if secure(password) == True:
            break
    return(password)
if __name__ == "__main__":
        test = generate(8)
        print(test)
        print(validate(test))
        
