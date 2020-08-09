from flask import Flask, request, make_response
import json
from IntelligentAgent import BigPapa
from InteractiveBoard import AwesomeBoard
import os

app = Flask(__name__)

# Request of a new model
@app.route('/first-scan', methods=["GET", "POST"])
def new_model():
    # TODO Está metida aquí pero no en TTS, porque no sé cómo hacerlo en realidad.
    #  Ligado al to do de InteractiveBoard (32,11)
    if 'Done' in request.form.keys():
        ABoard.battleField.endScan = True
    else:
        ABoard.battleField.first_scan(json.loads(list(request.form.to_dict().keys())[0]))
    return make_response('Zi zenió', 200)

# Sends to TTS the rosters names from the ./Rosters directory
@app.route('/gimme-the-rosters', methods=["GET", "POST"])
def gimme_the_rosters():
    return make_response(json.dumps({'rosters': os.listdir('./Rosters/')}), 200)

# Request for making the enemy army
@app.route('/enemy-army-generation', methods=["GET", "POST"])
def enemy_army_generation():
    # TODO funciona, pero TTS se tira mucho tiempo, porque ya vimos que el servidor tarda en acceder a los datos.
    #  Hay que hacer una response rápida diciendo que el servidor está trabajando en ello, y
    #  cuando acabe avisar a TTS de alguna manera
    ABoard.ib_1_enemy_army_generation(request.form.to_dict()['Roster'])
    return make_response(json.dumps(ABoard.badArmyObject), 200)

# Request for making the friend army
@app.route('/friend-army-generation', methods=["GET", "POST"])  # Not implemented
def friend_army_generation():
    ABoard.ib_2_friend_army_generation(json.loads(list(request.form.to_dict().keys())[0]))
    return make_response('Zi zenió', 200)

# Game stats update
@app.route('/stats', methods=["GET", "POST"])  # Not implemented
def stats():
    return make_response('Zi zenió', 200)

# Game type selection from the player
@app.route('/game-type', methods=["GET", "POST"])  # Not implemented
def game_type():
    return make_response('Zi zenió', 200)


if __name__ == "__main__":
    # Initialising the IB and the IA
    ABoard = AwesomeBoard()
    # ABoard.ib_1_enemy_army_generation("Jose.html")  # A eliminar
    Zak = BigPapa()
    # Calling the server
    app.run(port=5000)
