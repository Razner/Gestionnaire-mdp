import random
import string

def generate_mdp(longueur):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    mot_de_passe = ''.join(random.choice(caracteres) for i in range(longueur))
    return mot_de_passe
