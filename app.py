# Load File/Directory Handlers
import pathlib

# Load GUI System
from tkinter import *

# Load Game Class
from tracker import game_tracker

# Set Font Styles
titleFont = ("Verdana", 22)
baseFont = ("Verdana", 14)


class AddCreature(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.winfo_toplevel().title("Add Creature")

        self.render_options()

    def render_options(self):
        self._title = Label(self.master, text="Create Creature", font=titleFont)
        self._title.pack(pady=(10,10))

        creatureFrame = Frame(self.master)
        creatureFrame.pack(pady=(10,10))
        name_label = Label(creatureFrame, text="Creature Name", font=baseFont)
        name_label.pack(side=LEFT)
        self._entry = Entry(creatureFrame, font=baseFont)
        self._entry.pack(side=LEFT, padx=(10, 0))

        button = Button(self.master, text="Add Creature", font=baseFont)
        button['command'] = lambda: self._add()
        button.pack(fill=X)

    def _add(self):
        creature_name = self._entry.get()
        if creature_name and creature_name.strip():
            game_tracker.add(creature_name)

            self.master.destroy()

            game_window = Tk()
            gw = InitTracker(master=game_window)
            gw.mainloop()


class InsertSelection(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.winfo_toplevel().title("Insert Selection")

        self.render_options()

    def render_options(self):
        self._title = Label(self.master, text="Available Creatures", font=titleFont)
        self._title.pack(pady=(10,10))

        creatures = game_tracker.get_insert_options()
        key = 0
        for creature in creatures:
            button = Button(self.master, text=creature['name'], font=baseFont)
            button['command'] = lambda key=key: self._insert(key)
            button.pack(fill=X)
            key += 1
    
    def _insert(self, key):
        game_tracker.insert(key)

        self.master.destroy()

        game_window = Tk()
        gw = InitTracker(master=game_window)
        gw.mainloop()


class InitTracker(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.winfo_toplevel().title("Initiative Tracker")

        self._topFrame = Frame(self.master)
        self._topFrame.pack()

        self._roundFrame = Frame(self.master)
        self._roundFrame.pack()
        self._currentFrame = Frame(self.master)
        self._currentFrame.pack()
        self._nextFrame = Frame(self.master)
        self._nextFrame.pack()

        self._bottomFrame = Frame(self.master)
        self._bottomFrame.pack(side=BOTTOM, pady=(10,0))

        self.render_text_frames()
        self.render_bottom_frame()

    def render_text_frames(self):
        self._title = Label(self._topFrame, text="Game Tracker", font=titleFont)
        self._title.pack(pady=(10, 10))

        self._round = StringVar()
        _round_label = Label(self._roundFrame, text="Round: ", font=baseFont)
        _round_label.pack(side=LEFT)
        _round_text = Label(self._roundFrame, textvariable=self._round, font=baseFont)
        _round_text.pack(side=LEFT, padx=(10,0))

        self._current_player = StringVar()
        _current_player_label = Label(self._currentFrame, text="Current: ", font=baseFont)
        _current_player_label.pack(side=LEFT)
        _current_player_text = Label(self._currentFrame, textvariable=self._current_player, font=baseFont)
        _current_player_text.pack(side=LEFT, padx=(10,0))

        self._next_player = StringVar()
        _next_player_label = Label(self._nextFrame, text="Next:", font=baseFont)
        _next_player_label.pack(side=LEFT)
        _next_player_text = Label(self._nextFrame, textvariable=self._next_player, font=baseFont)
        _next_player_text.pack(side=LEFT, padx=(10,0))

        self._update_text()

    def render_bottom_frame(self):
        next_button = Button(self._bottomFrame, text="Next Character", font=baseFont)
        next_button['command'] = lambda: self._next()
        next_button.pack(side=LEFT)

        hold_button = Button(self._bottomFrame, text="Hold Initiative", font=baseFont)
        hold_button['command'] = lambda: self._hold()
        hold_button.pack(side=LEFT)

        remove_button = Button(self._bottomFrame, text="Remove Character", font=baseFont)
        remove_button['command'] = lambda: self._remove()
        remove_button.pack(side=LEFT)

        insert_button = Button(self._bottomFrame, text="Insert Into Initiative", font=baseFont)
        insert_button['command'] = lambda: self._insert()
        insert_button.pack(side=LEFT)

        add_button = Button(self._bottomFrame, text="Add Character", font=baseFont)
        add_button['command'] = lambda: self._add()
        add_button.pack(side=LEFT)

    def _next(self):
        game_tracker.next()

        self._update_text()

    def _hold(self):
        game_tracker.hold()

        self._update_text()

    def _remove(self):
        game_tracker.remove()

        self._update_text()

    def _insert(self):
        if game_tracker.has_insert_options():
            self.master.destroy()

            insert_window = Tk()
            iw = InsertSelection(master=insert_window)
            iw.mainloop()

    def _add(self):
        self.master.destroy()

        add_window = Tk()
        aw = AddCreature(master=add_window)
        aw.mainloop()

    def _update_text(self):
        self._current_player.set(game_tracker.get_current())
        self._next_player.set(game_tracker.get_next())
        self._round.set(game_tracker.get_round())


class PlayerInit(Frame):
    _players = []
    _entries = {}

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.winfo_toplevel().title("Player Initiative")

        self.render_form()

    def render_form(self):
        self._title = Label(self.master, text="Player Initiative", font=titleFont)
        self._title.pack(pady=(10, 10))

        self._players = game_tracker.get_players()
        for player in self._players:
            player_frame = Frame(self.master)
            player_frame.pack(pady=(10,10), padx=(10,10))

            label = Label(player_frame, text=player['name'], font=baseFont)
            label.pack(side=LEFT)

            self._entries[player['name']] = Entry(player_frame, font=baseFont)
            self._entries[player['name']].pack(side=LEFT, padx=(10,0))

        button = Button(self.master, text="Run Encounter", font=baseFont)
        button['command'] = lambda: self.run_encounter()
        button.pack(fill=X)

    def run_encounter(self):
        errors = False
        for entry in self._entries:
            player = self._entries[entry].get()
            if not (player and re.match(r'^[0-9]*$', player)):
                errors = True

        if not errors:
            for player in self._players:
                init_roll = self._entries[player['name']].get()
                game_tracker.set_player_initiative(player, init_roll)

            game_tracker.set_order()
            self.master.destroy()

            game_window = Tk()
            gw = InitTracker(master=game_window)
            gw.mainloop()


class EncounterSelection(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.winfo_toplevel().title("Encounter Selection")

        self.render_options()

    def render_options(self):
        self._title = Label(self.master, text="Available Encounters", font=titleFont)
        self._title.pack(pady=(10,10))

        encounters = game_tracker.get_encounters()
        for encounter in encounters:
            path = str(encounter)
            if isinstance(encounter, pathlib.WindowsPath):
                file = path.split('\\')
            elif isinstance(encounter, pathlib.PosixPath):
                file = path.split('/')
            name = file[len(file)-1].replace(".csv", "").replace("-", " ")
            button = Button(self.master, text=name, font=baseFont)
            button['command'] = lambda encounter=encounter: self.set_encounter(encounter)
            button.pack(fill=X)

    def set_encounter(self, file_name):
        game_tracker.set_encounter(file_name)
        self.master.destroy()

        player_window = Tk()
        pw = PlayerInit(master=player_window)
        pw.mainloop()

encounter_window = Tk()
ew = EncounterSelection(master=encounter_window)
ew.mainloop()