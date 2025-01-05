from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

def creating_env():
    if not load_dotenv(find_dotenv()):
        with open('.env', 'w') as env_file:
            env_file.write('UUID=\n')
            env_file.write('LAST_LANGUAGE=\n')
            env_file.write('LAST_MIC=\n')
            env_file.write('SERVER_IP=\n')
            env_file.write('SERVER_PORT=\n')