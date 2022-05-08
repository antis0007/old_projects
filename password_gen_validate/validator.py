#Password Validator + Generator
#By Andrew Tischenko
#2021-09-15

#import random #basic pseudo-random python module
#random.seed will be omitted or None, so system time will be used

#random.seed(a=None,version=2) #I will leave this line in incase we want a specific seed
import secrets #Cryptographically strong RNG, much more secure than random
#import string #for string operations
#alphabet_lower = "abcdefghijklmnopqrstuvwxyz"
#all_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!-$%&’()*+,./:;<=>?_[]^‘{|}~"


#Ideas for password generation:
#(n is password length)

#Novel Method 1 for password generation:
#step1: loop n times and set the index of password string to a random index character from a string/list of all usable characters
#Novel Method 1 has no guarantee that the password output would be secure, moving on...

#Novel Method 2 for password generation: (May be more secure and difficult to RE, because of multiple random number generation?)
#step1: Generate a base string of length n consisting of lowercase string characters only. This can be done with a random number for an index between (0,25) looped n times, or using 
#step2: Generate a random number between 1 and n, lets call it x
#step3: loop x times through password, generate a random number between 1 and n each loop, and replace that index with the capital letter of that character
#step4: Generate a random number between 1 and n, lets call it y
#step5: loop y times through password, generate a random number between 1 and n each loop, and replace that index with a random symbol from special characters
#step6: repeat for digits and end.
#This method guarantees a secure password, and is tunable if x and y were not to be random, meaning a fixed number of special characters or uppercase letters upon request
#I noticed that there is a rare chance that the symbol generation will overwrite all capitals, so put it in a while loop like method 3


#Method 2 does not always work, and had MANY edge cases, was too complex, and took more time as passwords got larger, so I have removed it and decided to implement Method 3
##password = ""
##alphabet_lower = "abcdefghijklmnopqrstuvwxyz"
##special = "!-$%&’()*+,./:;<=>?_[]^‘{|}~"
##digit = "0123456789"
###random implementation:
##for i in range(n):
##    password.join(alphabet_lower[random.randint(0,n)])
##
###secrets implementation:
###Store already changed character indexes (workaround):
###stores at least 1 index that has lower, upper, digit and symbol
###this means no regeneration, works first try but slower
##    
##min_list = [0,0,0,0]
##
##password = password.join(secrets.choice(alphabet_lower) for i in range(n))
##password = list(password) #Have to make password a list temporarily bc strings are immutable
##x = secrets.randbelow(n)+1 #at least 1
##for i in range(0,x):
##    o = secrets.randbelow(n)
##    password[o] = password[o].upper()
##y = secrets.randbelow(n)+1 #at least 1
##for i in range(0,y):
##    o = secrets.randbelow(n)
##    password[o] = secrets.choice(special)
##password = ("").join(password) #Convert password from a list to a string


#Method 3 for password generation: (Shortest code secure method)
#This method was inspired by recipes and best practices on the secrets module documentation
#https://docs.python.org/3/library/secrets.html
#step1: Create a string/list with all allowable characters
#step2: Create a while loop where passwords are generated over and over from all available characters, loop x number of times and pick random characters using an index and randint or secrets.choice(all_characters)
#step3: Before end of every loop, do a secure check to make sure it has the minimum requirements
#step4: if it is secure, break loop and use password. If not secure, loop again and generate randomly until password fits criteria
#This method always works, but there is no guarantee that it will be secure on the first loop through, and may take several loops to generate a random secure password.

#Method 3 will be implemented for now

def secure(password):
    #This code used to be part of validate
    #I needed to use it in generate as well, and wanted to make it shorter
    
    #Secure check
    #Uppercase + Lowercase + Digit check loop:
    #Could have used a shorter python "any" or "all" through the digits, but would have to do several
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
    #Special Character Check:
    for i in special:
        if i in password:
            contains_special = True
            break
    #print(contains_lower)
    #print(contains_upper)
    #print(contains_digit)
    #print(contains_special)
    #considering using list comprehension? Supposedly more efficient
    #Final Secure Check:
    if(contains_lower==True and contains_upper==True and contains_digit==True and contains_special==True):
        return(True)

def validate(password):
    special = "!-$%&'()*+,./:;<=>?_[]^`{|}~"
    forbidden = [" ","@","#"]
    #Invalid check
    for i in forbidden:
        if i in password:
            return("Invalid")
    if len(password)<8:
        return("Invalid")
    #past this point we know that password must technically be valid
    if secure(password) == True:
        return("Secure")
    
    #Insecure - (if Secure check not met)
    return("Insecure")

def generate(n):
    #secret implementation:
    special = "!-$%&'()*+,./:;<=>?_[]^`{|}~"
    all_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!-$%&'()*+,./:;<=>?_[]^`{|}~"
    while True:
        password = ("").join(secrets.choice(all_characters) for i in range(n))
        if secure(password) == True:
            break
    return(password)

if __name__ == "__main__":
        #input_password = str(input())
        #print(validate(input_password))
        #print(generate(10))
        test = generate(1000000)
        print(test)
        print(validate(test))
        
