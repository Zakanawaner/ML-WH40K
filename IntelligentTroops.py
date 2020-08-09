# An AmIThinking Class will have different networks. One for movement, One for shooting (or melee), One for charging...

# Intelligent Troops Class (IT) aka AmIThinking
class AmIThinking:
    def __init__(self, squad, guid):
        self.movementNet = self.movement_network()
        self.awareness = squad

    def movement_network(self):
        # Movement Network. This network will have the board disposition as an entry, and the target to move to,
        # sent by the IA.
        network = 0
        return network


