from detect import *
from record import *
from database import *


if __name__=="__main__":
	print("1.Create Database")
	print("2.Register New User")
	print("3.Detect Face")
	print("4. Press 0 to Quit")
	while True:
		option=int(input("Enter Choice:").strip())
		if option==1:
			create_required()
		elif option==2:
			register()
		elif option==3:
			detect_face()
		elif option==0:
			exit(0)
