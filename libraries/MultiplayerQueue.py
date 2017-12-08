from collections import deque

class MultiplayerQueue():
    def __init__(self):
        self.line = deque()
        self.in_game = []
        
    def add_player(self, player):
        self.line.append(player)
        print "Added player: ", self.line
        return len(self.line)

    def map_line_players(self, fn):
        for player in self.line:
            fn(player)

    def map_game_players(self, fn):
        for player in self.in_game:
            fn(player)

    def set_game_size(self, size):
        self.in_game = [None]*size

    def start_player(self, number):
        """ Returns the ID of the new player"""
        try:
            player = self.line.popleft() 
            self.in_game[number] = player
            return player
        except IndexError:
            return None

    def fill_players(self):
        for idx, val in enumerate(self.in_game):
            if val is None:
                self.start_player(idx)

    def remove_player(self, clientID):
        print "Kicking player ", clientID
        for player in self.in_game:
            if player['id'] == clientID:
                self.line.remove(player)
                return True

        for idx, val in enumerate(self.in_game):
            if player['id'] == clientID:
                print "Kicking current player ", idx
                self.in_game[idx] = None
                return True
        return False

    def clear_players(self):
        for player in self.in_game:
            player = None