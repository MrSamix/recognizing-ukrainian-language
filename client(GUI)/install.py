import os
print("INSTALLING DEPENDENCIES")
choice = input("Do you want to install dependencies?(y/n): ")
if choice == 'y':
    os.system("pip install -r requirements.txt")
    print("Dependencies installed")
else:
    print("Please install dependencies manually")
    print("Exiting...")