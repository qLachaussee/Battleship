###############################################
##### Le script du Joueur n°2 : le Serveur #####
###############################################

#########################
# Import des librairies #
#########################

from flask import Flask, render_template, request
import socket

#################
# Instanciation #
#################

# On crée l'application Flask
app = Flask(__name__)

# On spécifie notre nom d'hôte, ainsi que notre port
host = socket.gethostname()
port = 4000

# On instancie nos listes globales pour conserver en mémoire votre plateau de jeu
your_boat, his_boat = [], []

# On instancie nos listes globales pour conserver l'historique de nos actions
your_action, his_action = [], []
your_reward, his_reward = [], []

# On instancie la liste globale de server pour conserver l'IPv4 de l'adversaire
server = []

##########################################
# Spécification des pages de l'app Flask #
##########################################

# Page d'accueil
@app.route('/')
def init():
    # on retourne la page d'accueil
    return render_template("init.html")

# Page de jeu
@app.route('/home', methods=['POST', 'GET'])
def home():
    # on prend les valeurs des cases cochées de la page d'accueil
    output = request.form.to_dict()

    # pour les incorporer à nos listes global correspondant au plateau
    for k in output.keys():
        your_boat.append(k)

    # on ouvre une connexion au socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))

    # on utilise la connexion socket pour devenir Serveur et attendre le message de l'ennemi
    message, addr = s.recvfrom(1024)

    # on incorpore l'IPv4 de l'ennemi dans notre liste de server
    server.append(addr)

    # on prend le contenu du message
    message = message.decode('utf-8')

    # pour l'incorporer à notre liste globale correspondant à nos récompenses
    his_action.append(message)

    # on donne une récompense à l'action de l'ennemi en fonction de la position de vos bateaux
    if his_action[-1] in your_boat:
        reward = "Touché"
    else:
        reward = "Tombé"

    # pour l'incorporer à notre liste globale correspondant à ses récompenses
    his_reward.append(reward)

    # on retourne la page de jeu
    return render_template("index.html", your_boat=your_boat, your_action=your_action, your_reward=your_reward, his_action=his_action, his_reward=his_reward, win="En cours")

# Page de jeu après coup
@app.route('/result', methods=['POST', 'GET'])
def result():
    # on prend les valeurs de la case ciblée de la page de jeu
    output = request.form.to_dict()

    # pour l'incorporer à notre liste globale correspondant à nos actions
    action = list(output.keys())[0]
    your_action.append(action)

    # on ouvre une connexion au socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))

    # on passe de Serveur à Client
    # on envoie donc un message comprenant la récompense de l'action précédente de l'ennemi, puis votre action, séparé par un ";"
    s.sendto(his_reward[-1].encode('utf-8') + ";".encode('utf-8') + action.encode('utf-8'), server[-1])
    
    # on utilise la même connexion socket pour redevenir Serveur et attendre le message de l'ennemi
    reponse, addr = s.recvfrom(1024)

    # on prend le contenu du message
    reponse = reponse.decode('utf-8')

    # pour l'incorporer à notre liste globale correspondant à nos récompenses
    your_reward.append(reponse.split(";")[0])

    # si on a touché les 3 bateaux de l'ennemi
    if your_reward.count("Touché") == 3:
        # on met fin à la partie en retournant la valeur win="Gagné"
        return render_template("index.html", your_boat=your_boat, your_action=your_action, your_reward=your_reward, his_action=his_action, his_reward=his_reward, win="Gagné")

    # on incorpore également l'action de l'ennemi dans notre liste globale correspondant à ses actions
    his_action.append(reponse.split(";")[1])

    # on donne une récompense à l'action de l'ennemi en fonction de la position de vos bateaux
    if his_action[-1] in your_boat:
        reward = "Touché"
    else:
        reward = "Tombé"

    # pour l'incorporer à notre liste globale correspondant à ses récompenses
    his_reward.append(reward)

    # si l'ennemi a touché nos 3 bateaux
    if his_reward.count("Touché") == 3:
        # on lui envoi un message pour lui dire qu'il a gagné avec la mention "Fin" à la place de notre action
        s.sendto(his_reward[-1].encode('utf-8') + ";".encode('utf-8') + "Fin".encode('utf-8'), server[-1])
        # on met fin à la partie en retournant la valeur win="Perdu"
        return render_template("index.html", your_boat=your_boat, your_action=your_action, your_reward=your_reward, his_action=his_action, his_reward=his_reward, win="Perdu")

    # on retourne la page de jeu mise à jour
    return render_template("index.html", your_boat=your_boat, your_action=your_action, your_reward=your_reward, his_action=his_action, his_reward=his_reward, win="En cours")

# on lance notre application sur le port 5000
if __name__ == "__main__":
    app.run(debug=True, port=5000)
