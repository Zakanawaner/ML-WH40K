

# Battlefield secondary class with all the info from the disposition of the board and so on.
class BattleField:
    def __init__(self):
        super(BattleField, self).__init__()
        # Board initializations
        self.objectTerrain = 0
        self.objectBuiltin = 0
        self.objectUnassigned = 0
        self.rawObjects = []
        self.rawSoldiers = []
        self.terrain = []
        self.builtin = []
        self.unassigned = []
        self.endScan = False

    # Function called by the client with /new-model
    def first_scan(self, obj):  # V1.0
        if not self.endScan:
            if obj['Name'] == 'Custom_Model' and obj['Nickname'] != '':
                self.rawSoldiers.append(obj)
            else:
                self.classify_not_unit_objects(obj)

    # Function for handling the units of the board that are not models
    def classify_not_unit_objects(self, obj):  # Not implemented
        self.builtin.append(obj) if not obj['Locked'] else self.terrain.append(obj)
