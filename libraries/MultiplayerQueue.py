from collections import deque

class MultiplayerQueue():
    def __init__(self):
        self.line = deque()
        self.in_game = []
        
    def add_player(self, player):
        if player not in self.line:
            self.line.append(player)
            print "Added player: ", player['id']
            return len(self.line)
        else:
            print "Player", player['id'],  "already on list"

    def map_line_players(self, fn):
        for player in self.line:
            fn(player)

    def map_game_players(self, fn):
        for player in self.in_game:
            fn(player)

    def set_game_size(self, size):
        self.in_game = [None]*size
        print "set size", size

    def start_player(self, number):
        """ Returns the ID of the new player"""
        try:
            player = self.line.popleft() 
            print "Starting ", player['id']
            self.in_game[number] = player
            return player
        except IndexError:
            return None

    def fill_players(self):
        for idx, val in enumerate(self.in_game):
            if val is None:
                print "Filling a player ", idx
                self.start_player(idx)

    def remove_player(self, clientID):
        print "Kicking player", clientID
        try:
            client = int(clientID)
        except ValueError:
            return False

        for player in self.line:
            if player['id'] == client:
                print "Removing player in line", idx
                self.line.remove(player)
                return True

        for idx, val in enumerate(self.in_game):
            if val['id'] == client:
                print "Kicking current player ", idx
                self.in_game[idx] = None
                return True
        return False

    def clear_players(self):
        for player in self.in_game:
            player = None