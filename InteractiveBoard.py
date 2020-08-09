from bs4 import BeautifulSoup
import psycopg2
import json
import os
from IBUtilities import ib_utilities_check_names, ib_utilities_get_cylinder_bounds, ib_utilities_get_categories
from BattleField import BattleField


# Interactive Board Class (IB) aka Awesome Board
class AwesomeBoard:
    def __init__(self):
        super(AwesomeBoard, self).__init__()
        # Initialise the battlefield
        self.battleField = BattleField()
        # Enemy army
        self.badArmy = {}
        self.badArmyObject = json.load(open('./Source/army_skeleton.json'))
        # Friend army
        self.friendArmy = {}
        self.friendArmyObject = json.load(open('./Source/army_skeleton.json'))
        # Database access
        self.connection = None
        self.cursor = None
        # Game statistics
        self.stats = None

    # Function that handles the game type with the player. Called by the client with /game-type
    def ib_0_select_game_type(self):  # Not implemented
        self.badArmy = self.badArmy

    # Function that generates the enemy army given the Roster. Called by the client with /enemy-army-generation
    def ib_1_enemy_army_generation(self, bs_file=None):  # V1.0
        # TODO en la clase IA hay código que saca un army según la ingormación que recibe del tablero. Se puede adaptar
        #  para que el jugador, o bien te dé un Roster, o bien cargue su propio objeto ya guardado. De esta manera sería
        #  explorar el tablero antes de sacar mi ejército y guardar el army.
        if bs_file is None:
            self.ib_1_1_2_get_army_from_board()
        else:
            self.ib_1_1_1_get_army_from_roster(bs_file)
        self.ib_1_2_prepare_tts_army()
        self.ib_1_3_save_board()

    # Function that generates Zak's army given the player selection (recycles IB 1 functions)
    # Called by the client with /friend-army-generation
    def ib_2_friend_army_generation(self, army):  # Not implemented
        self.ib_1_1_1_get_army_from_roster(army)
        self.ib_1_2_prepare_tts_army()
        self.ib_1_3_save_board()

    # Function to be called constantly by the client to show the game statistics with /stats
    def ib_3_show_statistics(self):  # Not implemented
        self.stats = None

    # Function to store all the bonuses for the army
    def ib_4_paying_attention(self):  # Not implemented
        self.badArmy = self.badArmy

    # We fill the army dictionary with the roster selected
    def ib_1_1_1_get_army_from_roster(self, bs_file):  # V1.0
        # We get the html soup from the roster file
        with open('./Rosters/' + bs_file) as fp:
            soup = BeautifulSoup(fp, "html.parser")
        # Name of the army, force information  and rules information
        self.badArmy['Name'] = soup.find('h1').text.strip()[:soup.find('h1').text.strip().find(' [')]
        self.badArmy['Force'] = soup.find('h2').text.strip()[:soup.find('h1').text.strip().find(' [')]
        self.badArmy['Rules'] = soup.find('p', attrs={'class': 'rule-names'}).findChild('span', attrs={'class': 'italic'}).text.strip().split(', ')
        for category in soup.find_all('li', attrs={'class': 'category'}):
            # Get the army configuration
            if 'Configuration' in category.find('h3').text.strip():
                self.badArmy = ib_utilities_get_categories('Configuration', category, self.badArmy, cls=True)
            # Get the stratagems
            if 'Stratagems' in category.find('h3').text.strip():
                self.badArmy = ib_utilities_get_categories('Stratagems', category, self.badArmy, cls=True)
            # Get the HQ units
            if 'HQ' in category.find('h3').text.strip():
                self.badArmy = ib_utilities_get_categories('HQ', category, self.badArmy)
            # Get the Troops
            if 'Troops' in category.find('h3').text.strip():
                self.badArmy = ib_utilities_get_categories('Troops', category, self.badArmy)
            # Get the Elites
            if 'Elites' in category.find('h3').text.strip():
                self.badArmy = ib_utilities_get_categories('Elites', category, self.badArmy)
            # Get the Fast Attack
            if 'Fast Attack' in category.find('h3').text.strip():
                self.badArmy = ib_utilities_get_categories('Fast', category, self.badArmy)
            # Get the Heavy Support
            if 'Heavy Support' in category.find('h3').text.strip():
                self.badArmy = ib_utilities_get_categories('Heavy', category, self.badArmy)

    # Function Intelligent Agent 1: Assess board before battle
    def ib_1_1_2_get_army_from_board(self):  # Not implemented
        # TODO Esto estaba dentro el IA y hay que ponerlo bien para que lo haga el board
        # Function Intelligent Agent nº 1.1: Assign model information
        for model in self.raw_soldiers:
            if 'zak' in model['Nickname']:
                self.friendArmy.append({
                    'Nickname': model['Nickname'],
                    'Description': model['Description'],
                    'GMNotes': model['GMNotes'],
                    'Stats': json.loads(model['Description']['Stats']),
                    'Gear': json.loads(model['Description']['Gear']),
                    'Skills': json.loads(model['Description']['Skills']),
                    'Psyker': json.loads(model['Description']['Psyker']),
                    'FactionKeys': json.loads(model['Description']['FactionKeys']),
                    'Keys': json.loads(model['Description']['Keys']),
                })
            elif 'enemy' in model['Nickname']:
                self.badPeople.append({
                    'Nickname': model['Nickname'],
                    'Description': model['Description'],
                    'GMNotes': model['GMNotes'],
                    'Stats': json.loads(model['Description']['Stats']),
                    'Gear': json.loads(model['Description']['Gear']),
                    'Skills': json.loads(model['Description']['Skills']),
                    'Psyker': json.loads(model['Description']['Psyker']),
                    'FactionKeys': json.loads(model['Description']['FactionKeys']),
                    'Keys': json.loads(model['Description']['Keys']),
                })

        # Function Intelligent Agent nº 1.2: Define armies
        biggest = 0
        for model in self.friendArmy:
            index_start_squad = model['Nickname'].find('-') + 1
            index_stop_squad = model['Nickname'][index_start_squad:].find('-') + index_start_squad
            index_start_unit = index_stop_squad + 1
            squad = int(model['Nickname'][index_start_squad:index_stop_squad])
            unit = int(model['Nickname'][index_start_unit:])
            model['Squad'] = squad
            model['Unit'] = unit
            biggest = squad if squad > biggest else None
        for nb_squad in range(biggest):
            squad_list = []
            for model in self.friendArmy:
                if model['Squad'] == nb_squad + 1:
                    squad_list.append(model)
            squad_list = sorted(squad_list, key=lambda k: k['Unit'])
            self.myArmy['Squad'].append(squad_list)
        biggest = 0
        for model in self.friendArmy:
            index_start_squad = model['Nickname'].find('-') + 1
            index_stop_squad = model['Nickname'][index_start_squad:].find('-') + index_start_squad
            index_start_unit = index_stop_squad + 1
            squad = int(model['Nickname'][index_start_squad:index_stop_squad])
            unit = int(model['Nickname'][index_start_unit:])
            model['Squad'] = squad
            model['Unit'] = unit
            biggest = squad if squad > biggest else None
        for nb_squad in range(biggest):
            squad_list = []
            for model in self.badPeople:
                if model['Squad'] == nb_squad + 1:
                    squad_list.append(model)
            squad_list = sorted(squad_list, key=lambda k: k['Unit'])
            self.badArmy['Squad'].append(squad_list)

    def ib_1_2_prepare_tts_army(self):  # V1.0
        position = [0.0, 0.0]
        guid = [0, 0]
        # Open Database connection
        self.connection = psycopg2.connect(user=os.environ.get('SQL_USER'),
                                           password=os.environ.get('SQL_PASSWORD'),
                                           host=os.environ.get('SQL_HOST'),
                                           port=os.environ.get('SQL_PORT'),
                                           database=os.environ.get('SQL_NAME'))
        self.cursor = self.connection.cursor()
        self.cursor.execute("SELECT nickname "
                            "FROM models;")
        names_db = [model[0] for model in self.cursor.fetchall()]
        # HQ Units
        if 'HQ' in self.badArmy.keys():
            position, guid = self.ib_1_2_1_get_json_file('HQ', position, names_db, guid)
        # Troops Units
        if 'Troops' in self.badArmy.keys():
            position, guid = self.ib_1_2_1_get_json_file('Troops', position, names_db, guid)
        # Elite Units
        if 'Elites' in self.badArmy.keys():
            position, guid = self.ib_1_2_1_get_json_file('Elites', position, names_db, guid)
        # Fast Attack Units
        if 'Fast' in self.badArmy.keys():
            position, guid = self.ib_1_2_1_get_json_file('Fast', position, names_db, guid)
        # Heavy Support Units
        if 'Heavy' in self.badArmy.keys():
            position, guid = self.ib_1_2_1_get_json_file('Heavy', position, names_db, guid)
        self.cursor.close()
        self.connection.close()

    def ib_1_2_1_get_json_file(self, name, position, names_db, guid):  # V1.0
        y_ini = position[1]
        y_max = 0.0
        x_ini = 0.0
        for i, unit in enumerate(self.badArmy[name]['Squads']):
            guid[0] += 1
            guid[1] = 0
            position[0] = x_ini
            x_max = position[0]
            row_done = False
            for j, model in enumerate(unit['Units']):
                guid[1] += 1
                # We ge the name in the database
                nickname = ib_utilities_check_names(model['Nickname'], names_db)
                # TODO si el modelo tiene más de un nickname asociado en la base de datos, estaría bien ofrecerle al
                #  usuario cuál escoger, pero eso el algo complicado
                self.cursor.execute("SELECT skeleton "
                                    "FROM models "
                                    "WHERE nickname = %s;", (names_db[nickname[0]],))
                json_model = self.cursor.fetchone()
                if json_model is not None:
                    self.badArmy[name]['Squads'][i]['Units'][j]['bounds'] = ib_utilities_get_cylinder_bounds(json_model[0])
                    json_model[0]['Transform']['posX'] = position[0]
                    position[0] += 2 * self.badArmy[name]['Squads'][i]['Units'][j]['bounds']['radius']
                    json_model[0]['Transform']['posZ'] = position[1]
                    json_model[0]['Description'] = json.dumps({
                        'stats': self.badArmy[name]['Squads'][i]['Units'][j]['Stats'],
                        'Weapons': self.badArmy[name]['Squads'][i]['Units'][j]['Weapons'],
                        'Abilities': self.badArmy[name]['Squads'][i]['Units'][j]['Abilities'],
                        'PsychicPowers': self.badArmy[name]['Squads'][i]['Units'][j]['PsychicPowers']
                    })
                    json_model[0]['GMNotes'] = json.dumps({
                        'Rules': self.badArmy[name]['Squads'][i]['Rules'],
                        'FactionKeys': self.badArmy[name]['Squads'][i]['FactionKeys'],
                        'Keys': self.badArmy[name]['Squads'][i]['Keys']
                    })
                    json_model[0]['GUID'] = 'enemy-' + str(guid[0]) + '-' + str(guid[1])
                    self.badArmyObject['ObjectStates'].append(json_model[0])
                    self.badArmy[name]['Squads'][i]['Units'][j]['GotJson'] = True
                if (j + 1) % 5 == 0 and j != 0:
                    x_max = position[0]
                    position[0] = x_ini
                    position[1] += 2 * self.badArmy[name]['Squads'][i]['Units'][j]['bounds']['radius']
                    row_done = True
            x_max = position[0] if not row_done else x_max
            y_max = position[1]
            position[1] = y_ini
            x_ini = x_max + 3.5
        position[0] = 0.0
        position[1] = y_max + 3.5
        return position, guid

    def ib_1_3_save_board(self):  # V1.0
        # TODO aquí guardo el fichero Json que se puede cargar en TTS, pero lo guapo sería hacer el spawn directamente
        #  en el board donde se pide el Roster, y dar la opción de guardar el ejército como objeto. Hay que intentar
        #  solucionar la mierda de los nombres, pero si no se puede hay que cantarle al usuario los modelos uqe no han
        #  podido cargarse.
        # We save the json file as a TTS saved object
        with open('./Source/enemy_army.json', 'w+') as f:
            json.dump(self.badArmyObject, f, indent="\t")
        f.close()
