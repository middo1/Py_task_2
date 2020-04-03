import os
import json
import base64
import random
import string

def cls():
	import platform
	code = "clear"
	if platform.system().lower() == "windows":
		code = "cls"
	os.system(code)

class User:
	all = {}
	FILE = ".store"
	def __init__(self, firstname, lastname, email):
		self.firstname = firstname
		self.lastname	= lastname
		self.email		= email
		self.password	= None

	def __repr__(self):
		return f"<User {self.email}>"

	def todict(self):
		return dict(
			firstname=self.firstname,
			lastname =self.lastname,
			email		=self.email,
			password =base64.b85encode(
				bytes(self.password, "utf8")
			).decode("utf8")
		)

	def save(self):
		User.all[self.email] = self
		User.all[self.firstname] = self
		User.all[self.lastname] = self
		User.all[self.password] = self
		# serialize for json
		res = dict()
		for key in User.all:
			res[key] = User.all.get(key).todict()
		with open(User.FILE, "w") as file:
			json.dump(res, file, indent=2)

	def setpassword(self, pw):
		self.password = pw

	@staticmethod
	def exists(email):
		return User.all.get(email) is not None

	@staticmethod
	def get(email, pw):
		usr = User.all.get(email)
		if usr is not None:
			if usr.password == pw:
				return usr

	@staticmethod
	def load():
		if os.access(User.FILE, os.F_OK):
			with open(User.FILE) as file:
				res = json.load(file)
			for key in res:
				User.all[key] = User.fromdict(res[key])

	@staticmethod
	def fromdict(object:dict):
		user = User(object["firstname"],
						object["lastname"],
						object["email"]
				)
		user.setpassword(
			base64.b85decode(bytes(object["password"], "utf8")).decode("utf8")
		)
		return user

################
def genranditems(n, iterable):
	n = min(n, len(iterable)-1)
	i = list(iterable)
	random.shuffle(i)
	return i[:n]

def validateemail(email):
	return (
		"@" in email and "." in email and len(email) > 6
	)

def validatepw(pw):
	if len(pw) < 9: return False
	for char in string.digits:
		if char in pw:
			res = True
			break
		else:
			res = False
	for char in string.punctuation:
		if char in pw:
			res &= True
			return res
	return False

def genpw(key1, key2=string.ascii_letters):
	res = key1[:2]+key2[-2:]
	res += "".join(genranditems(2, string.ascii_letters))
	res += "".join(genranditems(2, string.punctuation))
	res += "".join(genranditems(1, string.digits))
	return res

def require(prompt="enter input> ", conditional_callback=None):
	valid = False
	while not valid:
		try:
			res = input(prompt)
		except (EOFError, KeyboardInterrupt) as e:
			res = ""
		if conditional_callback is None:
			valid |= True
		elif type(conditional_callback) is bool:
			valid |= conditional_callback
		else:
			valid |= conditional_callback(res)
	return res

def main():
	User.load()
	email = require("enter email: ", validateemail)
	if User.exists(email):
		# welcome user
		pw = require("enter password: ", lambda x:bool(User.get(email, x)))
		user = User.get(email, pw)
		print("Hello, %s %s." %(user.firstname.upper(), user.lastname))
	else:
		# create account
		print("You are'nt registered... fill in to create account")
		fn = require("enter first name: ", lambda text:len(text)>2)
		ln = require("enter last name: ",	lambda text:len(text)>2)
		pw = genpw(fn, ln)
		print("here's a generated password: {pw}".format(pw=pw))
		response = require("[1] use generated password\n"+\
			"[2] use another password: ", lambda num:num in ["1", "2"]
		)
		if response == "2":
			pw = require("enter password: ", validatepw)
		user = User(fn, ln, email)
		user.setpassword(pw)
		user.save()

		print("Hello, %s %s." %(user.firstname.upper(), user.lastname))

	
while True: 
 ask_user = input("Are you a new user?  Please answer (y/n): ") 
 if ask_user == "y":
     if __name__ == "__main__":
	     cls()
	     print("Use Ctrl-z to exit")
	     main() 
 elif ask_user == "n":
  container = [] 
  print("User data")
  for usr in User.all:
    container.append(usr)
    if container.index(usr) % 4 == 0:
		     print("------" + "User " + usr +"'s" + " details------" )  
		     print("Email:", usr)
    if container.index(usr) % 4 == 1:    
		     print("First name:", usr)
    if container.index(usr) % 4 == 2:    
		     print("Lastname:", usr)
    if container.index(usr) % 4 == 3:    
		     print("Password:", usr)
  print("\n")
  break
 else:
  print("please run again and enter (y/n)") 
  break
  
