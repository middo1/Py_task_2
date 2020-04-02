import random

first_name = input("Enter your first name :")
last_name = input("Enter your name :")
email = input("Enter your email address :")
ran = "" 
password = first_name[0:2] + last_name[len(last_name)-2 :]
container = {} 
while len(ran) < 5:
    i = random.randint(0, len(email) - 1)
    ran += email[i] 
    if len(ran) == 5:
        password += ran
check_pass = input("Is this password okay with you? " + password + "  Please enter(yes/no): ") 
if check_pass == "yes":
    container["Name"] = first_name + " " + last_name 
    container["Email"] = email
    container["Password"] = password
    print("NAME:", container["Name"], "\n" + "EMAIL:", container["Email"],"\n" + "PASSWORD:", container["Password"]) 
elif check_pass == "no":
    password = input("Enter your password which is not less than seven characters : ")
    while len(password) < 7:
        password = input("Your password's characters are less than seven. Please re-enter password : ") 
    container["Name"] = first_name + " " + last_name 
    container["Email"] = email
    container["Password"] = password
    print("NAME:", container["Name"],"\n" +"EMAIL:", container["Email"],"\n" + "PASSWORD:", container["Password"])









