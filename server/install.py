import os
print("INSTALLING DEPENDENCIES")
choice = input("Do you want to install dependencies?(y/n): ")
if choice == 'y':
    cuda = input("Do you want to install dependencies for CUDA?(y/n): ")
    if cuda == 'y':
        print("Installing dependencies with CUDA")
        os.system("pip install -r for_install/requirements(CUDA).txt")
        print("Dependencies installed")
        print("After installing CUDA dependencies, you need to install CUDA Toolkit with CUDA support")
        print(r"You can download it from https://developer.nvidia.com/cuda-12-4-0-download-archive/")
    elif cuda == 'n':
        os.system("pip install -r for_install/requirements.txt")
        print("Dependencies installed")
    else:
        print("Invalid input")
else:
    print("Please install dependencies manually")
    print("Exiting...")