from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

def creating_env():
    if not load_dotenv(find_dotenv()):
        with open('.env', 'w') as env_file:
            env_file.write('IP=\n')
            env_file.write('PORT=\n')
            env_file.write('DEVICE=\n')