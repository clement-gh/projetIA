from security import *

if __name__ == '__main__':
    # entrer un nom d'utilisateur et un mot de passe
    print("Entrez un nom d'utilisateur et un mot de passe:")
    username = input("Username: ")
    password = input("Password: ")

    # hashage du mot de passe
    hashed_password = hash_password(password)
    print("Le mot de passe hashé est: " + hashed_password)
    print ("dans le .env vous devez mettre le mot de passe hashé")
