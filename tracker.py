# Load File/Directory Handlers
from os import listdir
from os.path import isfile, join

# Load Randomizer
from random import randrange

class GameTracker:
    _round = 1
    _current_index = 0
    _current_key = ''
    _next_key = ''

    _creatures = {}
    _init_order = []
    _hold_list = []

    def __init__(self):
        pass

    def get_encounters(self):
        # Return List of Files in Directory
        return [f for f in listdir("encounters") if isfile(join("encounters", f))]

    def set_encounter(self, file_name):
        # Open File
        efile = open("encounters/" + file_name, 'r')

        # Skip File Labels
        next(efile)

        # Read File Line by Line
        for line in efile:
            # Turn Line String into Lists
            mob = line.rstrip().split(",")

            # Calculate Initiative
            initiative = randrange(1, 20) + int(mob[2])

            # Remove Dup Risk
            if int(mob[2]) < 10:
                mob[2] = '0' + mob[2]
            key = float(str(initiative) + '.' + mob[2] + str(randrange(10, 99)))

            # Save to Creature Dict
            self._creatures[key] = mob[0] + " (cr " + mob[1] + ")"

        # Close File
        efile.close()

    def get_players(self):
        # Define Return Object
        players = []

        # Open Players File
        pfile = open("players.csv", 'r')

        # Skip File Labels
        next(pfile)

        # Read File Line by Line
        for line in pfile:
            # Turn Line String into Lists
            line_list = line.rstrip().split(",")

            # Add Player Dict to Players List
            player = {
                'name': line_list[0],
                'init_mod': line_list[1]
            }
            players.append(player)

        # Close File
        pfile.close()

        # Return Players List
        return players

    def set_player_initiative(self, player, init_roll):
        # Remove Dup Risk
        if int(player['init_mod']) < 10:
            player['init_mod'] = '0' + player['init_mod']
        key = float(str(init_roll) + '.' + player['init_mod'] + str(randrange(10, 99)))

        # Save to Creature Dict
        self._creatures[key] = player['name']

    def set_order(self):
        # Organize Creatures by Initiative
        self._init_order = sorted(self._creatures, reverse=True)

        # Set Reference Keys
        self._set_keys()

    def get_current(self):
        # Get Creature Name
        return self._creatures[self._current_key]

    def get_next(self):
        # Get Creature Name
        return self._creatures[self._next_key]

    def get_round(self):
        # Get Round #
        return self._round

    def next(self):
        # Set Next Creature
        self._current_index += 1

        # Check for Index Loop
        self._check_for_new_round()

    def remove(self):
        # Remove Creature from List
        self._init_order.pop(self._current_index)

        # Check for Index Loop
        self._check_for_new_round()

    def hold(self):
        # Add Creature to Hold List
        creature = {
            'name': self._creatures[self._current_key],
            'key': self._current_key
        }
        self._hold_list.append(creature)

        # Remove Creature from List
        self.remove()

    def has_insert_options(self):
        # Verify Hold List not Empty
        if len(self._hold_list) > 0:
            return True

        return False

    def get_insert_options(self):
        # Get Hold List
        return self._hold_list

    def insert(self, key):
        # Add Creature to Init List
        index = int(key)
        self._init_order.insert(self._current_index, self._hold_list[index]['key'])

        # Remove Creature from Hold List
        self._hold_list.pop(index)

        # Set Reference Keys
        self._set_keys()

    def add(self, creature):
        # Add Creature to Creatures Dict
        new_key = randrange(111, 999)
        self._creatures[new_key] = creature

        # Add Creature to Init List
        self._init_order.insert(self._current_index, new_key)

        # Set Reference Keys
        self._set_keys()

    def _check_for_new_round(self):
        # Check if End of Loop
        if self._current_index == len(self._init_order):
            self._current_index = 0
            self._round += 1

        # Set Reference Keys
        self._set_keys()

    def _set_keys(self):
        # Set Reference Keys
        self._set_current_key()
        self._set_next_key()

    def _set_current_key(self):
        # Set Current Key
        self._current_key = self._init_order[self._current_index]

    def _set_next_key(self):
        # Set Next Index
        next_index = self._current_index + 1
        if next_index == len(self._init_order):
            next_index = 0

        # Sent Next Key
        self._next_key = self._init_order[next_index]

game_tracker = GameTracker()