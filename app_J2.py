from flask import Flask, render_template, url_for, request
import socket
import pandas as pd

app = Flask(__name__)

host = socket.gethostname()
port = 4000
server = ("DESKTOP-G530RU6", 4005) #le host name du serveur (host si on travail sur le même PC | "DESKTOP-G530RU6" si on travail avec mon PC perso | "PO-7545" si on travail avec mon PC pro)

your_board, his_board = pd.DataFrame([[0]*9]*9, columns=["A","B","C","D","E","F","G","H","I"], index=range(1,10)), pd.DataFrame([[0]*9]*9, columns=["A","B","C","D","E","F","G","H","I"], index=range(1,10))
your_boat, his_boat = [], []
your_action, his_action = [], []
your_reward, his_reward = [], []

@app.route('/')
def init():
    return render_template("init.html")

@app.route('/home', methods=['POST', 'GET'])
def home():
    output = request.form.to_dict()
    for k in output.keys():
        your_board.loc[int(k[1]),k[0]] = 1
        your_boat.append(k)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))

    message, addr = s.recvfrom(1024)
    message = message.decode('utf-8')
    his_action.append(message)

    if his_action[-1] in your_boat:
        reward = "Touché"
    else:
        reward = "Tombé"
    his_reward.append(reward)

    return render_template("index.html", your_boat=your_boat, your_action=your_action, your_reward=your_reward, his_action=his_action, his_reward=his_reward, win="En cours")


@app.route('/result', methods=['POST', 'GET'])
def result():
    

    output = request.form.to_dict()
    action = list(output.keys())[0]
    your_action.append(action)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))

    s.sendto(his_reward[-1].encode('utf-8') + ";".encode('utf-8') + action.encode('utf-8'), server)
    
    reponse, addr = s.recvfrom(1024)
    reponse = reponse.decode('utf-8')
    
    your_reward.append(reponse.split(";")[0])
    if your_reward.count("Touché") == 3:
        return render_template("index.html", your_boat=your_boat, your_action=your_action, your_reward=your_reward, his_action=his_action, his_reward=his_reward, win="Gagné")

    his_action.append(reponse.split(";")[1])

    if his_action[-1] in your_boat:
        reward = "Touché"
    else:
        reward = "Tombé"
    his_reward.append(reward)

    if his_reward.count("Touché") == 3:
        s.sendto(his_reward[-1].encode('utf-8') + ";".encode('utf-8') + "Fin".encode('utf-8'), server)
        return render_template("index.html", your_boat=your_boat, your_action=your_action, your_reward=your_reward, his_action=his_action, his_reward=his_reward, win="Perdu")

    return render_template("index.html", your_boat=your_boat, your_action=your_action, your_reward=your_reward, his_action=his_action, his_reward=his_reward, win="En cours")
    
if __name__ == "__main__":
    app.run(debug=True, port=5000)
