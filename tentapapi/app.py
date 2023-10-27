from app import create_app
from config import IP, PORT

if __name__ == '__main__':
    create_app().run(host=IP, port=PORT)