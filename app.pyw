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
        # Register Window
        super().__init__(master)
        self.master = master
        self.winfo_toplevel().title("Add Creature")

        # Create Top Frame
        self._topFrame = Frame(self.master)
        self._topFrame.pack()

        # Create Bottom Frame
        self._bottomFrame = Frame(self.master)
        self._bottomFrame.pack(fill=X, side=BOTTOM, pady=(10,0))

        # Load Contents of Window
        self.render_options()

    def render_options(self):
        # Add Top Text to Window
        self._title = Label(self._topFrame, text="Create Creature", font=titleFont)
        self._title.pack(pady=(10,10))

        # Make New Creature Frame
        creatureFrame = Frame(self._topFrame)
        creatureFrame.pack(pady=(10,10), padx=(10,10))

        # Make Input Label
        name_label = Label(creatureFrame, text="Creature Name", font=baseFont)
        name_label.pack(side=LEFT)

        # Make Creature Name Input
        self._entry = Entry(creatureFrame, font=baseFont)
        self._entry.pack(side=LEFT, padx=(10, 0))

        # Button to Submit Form
        button = Button(self._bottomFrame, text="Add Creature", font=baseFont)
        button['command'] = lambda: self._add()
        button.pack(fill=X)

        button = Button(self._bottomFrame, text="Cancel", font=baseFont)
        button['command'] = lambda: self._close()
        button.pack(fill=X)

    def _add(self):
        creature_name = self._entry.get()
        if creature_name and creature_name.strip():
            # Add New Creature Name to Initiative as Current
            game_tracker.add(creature_name)

        self._close()

    def _close(self):
        # Close Current Window
        self.master.destroy()

        # Open Game Tracker Window
        game_window = Tk()
        gw = InitTracker(master=game_window)
        gw.mainloop()


class InsertSelection(Frame):
    def __init__(self, master=None):
        # Register Window
        super().__init__(master)
        self.master = master
        self.winfo_toplevel().title("Insert Selection")

        # Render Buttons for each Hold Creature
        self.render_options()

    def render_options(self):
        # Add Top Text to Window
        self._title = Label(self.master, text="Available Creatures", font=titleFont)
        self._title.pack(pady=(10,10))

        # Get List of Cretures
        creatures = game_tracker.get_insert_options()
        key = 0
        for creature in creatures:
            # Add Button for Creature
            button = Button(self.master, text=creature['name'], font=baseFont)
            button['command'] = lambda key=key: self._insert(key)
            button.pack(fill=X)
            key += 1

        button = Button(self.master, text="Cancel", font=baseFont)
        button['command'] = lambda: self._close()
        button.pack(fill=X)
    
    def _insert(self, key):
        # Move Creature from Hold List to Initiative as Current
        game_tracker.insert(key)

        self._close()

    def _close(self):
        # Close Current Window
        self.master.destroy()

        # Open Game Tracker Window
        game_window = Tk()
        gw = InitTracker(master=game_window)
        gw.mainloop()


class InitTracker(Frame):
    def __init__(self, master=None):
        # Register Window
        super().__init__(master)
        self.master = master
        self.winfo_toplevel().title("Initiative Tracker")

        # Create Frame 1
        self._topFrame = Frame(self.master)
        self._topFrame.pack()

        # Create Frame 2
        self._roundFrame = Frame(self.master)
        self._roundFrame.pack()

        # Create Frame 3
        self._currentFrame = Frame(self.master)
        self._currentFrame.pack()

        # Create Frame 4
        self._nextFrame = Frame(self.master)
        self._nextFrame.pack()

        # Create Frame 5
        self._bottomFrame = Frame(self.master)
        self._bottomFrame.pack(fill=X, side=BOTTOM, pady=(10,0))

        # Render Info Displays
        self.render_text_frames()

        # Render Action Buttons
        self.render_bottom_frame()

    def render_text_frames(self):
        # Add Add Top Text
        self._title = Label(self._topFrame, text="Game Tracker", font=titleFont)
        self._title.pack(pady=(10, 10))

        # Add Label with Dynamic Var
        self._round = StringVar()
        _round_label = Label(self._roundFrame, text="Round: ", font=baseFont)
        _round_label.pack(side=LEFT)
        _round_text = Label(self._roundFrame, textvariable=self._round, font=baseFont)
        _round_text.pack(side=LEFT, padx=(10,0))

        # Add Label with Dynamic Var
        self._current_player = StringVar()
        _current_player_label = Label(self._currentFrame, text="Current: ", font=baseFont)
        _current_player_label.pack(side=LEFT)
        _current_player_text = Label(self._currentFrame, textvariable=self._current_player, font=baseFont)
        _current_player_text.pack(side=LEFT, padx=(10,0))

        # Add Label with Dynamic Var
        self._next_player = StringVar()
        _next_player_label = Label(self._nextFrame, text="Next:", font=baseFont)
        _next_player_label.pack(side=LEFT)
        _next_player_text = Label(self._nextFrame, textvariable=self._next_player, font=baseFont)
        _next_player_text.pack(side=LEFT, padx=(10,0))

        # Update Display
        self._update_text()

    def render_bottom_frame(self):
        # Add Button to Bottom Frame
        next_button = Button(self._bottomFrame, text="Next Character", font=baseFont)
        next_button['command'] = lambda: self._next()
        next_button.pack(fill=X)

        # Add Button to Bottom Frame
        hold_button = Button(self._bottomFrame, text="Hold Initiative", font=baseFont)
        hold_button['command'] = lambda: self._hold()
        hold_button.pack(fill=X)

        # Add Button to Bottom Frame
        remove_button = Button(self._bottomFrame, text="Remove Character", font=baseFont)
        remove_button['command'] = lambda: self._remove()
        remove_button.pack(fill=X)

        # Add Button to Bottom Frame
        insert_button = Button(self._bottomFrame, text="Insert Into Initiative", font=baseFont)
        insert_button['command'] = lambda: self._insert()
        insert_button.pack(fill=X)

        # Add Button to Bottom Frame
        add_button = Button(self._bottomFrame, text="Add Character", font=baseFont)
        add_button['command'] = lambda: self._add()
        add_button.pack(fill=X)

    def _next(self):
        # Move to Next Creature
        game_tracker.next()

        # Update Display
        self._update_text()

    def _hold(self):
        # Add Creature to Hold List
        game_tracker.hold()

        # Update Display
        self._update_text()

    def _remove(self):
        # Remove Creature from Tracker
        game_tracker.remove()

        # Update Display
        self._update_text()

    def _insert(self):
        if game_tracker.has_insert_options():
            # Close Current Window
            self.master.destroy()

            # Open Insert Creature Window
            insert_window = Tk()
            iw = InsertSelection(master=insert_window)
            iw.mainloop()

    def _add(self):
        # Close Current Window
        self.master.destroy()

        # Open New Creature Window
        add_window = Tk()
        aw = AddCreature(master=add_window)
        aw.mainloop()

    def _update_text(self):
        # Update StringVars
        self._current_player.set(game_tracker.get_current())
        self._next_player.set(game_tracker.get_next())
        self._round.set(game_tracker.get_round())


class PlayerInit(Frame):
    _players = []
    _entries = {}

    def __init__(self, master=None):
        # Register Window
        super().__init__(master)
        self.master = master
        self.winfo_toplevel().title("Player Initiative")

        # Create Top Frame
        self._topFrame = Frame(self.master)
        self._topFrame.pack()

        # Create Bottom Frame
        self._bottomFrame = Frame(self.master)
        self._bottomFrame.pack(fill=X, side=BOTTOM, pady=(10,0))

        # Render Player Init Form
        self.render_form()

    def render_form(self):
        # Add Top Text to Window
        self._title = Label(self._topFrame, text="Player Initiative", font=titleFont)
        self._title.pack(pady=(10, 10))

        # Get List of Players from File
        self._players = game_tracker.get_players()
        for player in self._players:
            # Make Input Frame
            player_frame = Frame(self._topFrame)
            player_frame.pack(pady=(10,10), padx=(10,10))

            # Add Text to Frame
            label = Label(player_frame, text=player['name'], font=baseFont)
            label.pack(side=LEFT)

            # Add Input to Frame
            self._entries[player['name']] = Entry(player_frame, font=baseFont)
            self._entries[player['name']].pack(side=LEFT, padx=(10,0))

        # Add Button to Process Form
        button = Button(self._bottomFrame, text="Run Encounter", font=baseFont)
        button['command'] = lambda: self.run_encounter()
        button.pack(fill=X)

    def run_encounter(self):
        errors = False
        for entry in self._entries:
            # Verify Initiative has Init and is Number
            player = self._entries[entry].get()
            if not (player and re.match(r'^[0-9]*$', player)):
                errors = True

        if not errors:
            for player in self._players:
                # Save Player Initiative to Tracker
                init_roll = self._entries[player['name']].get()
                game_tracker.set_player_initiative(player, init_roll)

            # Organize Order by Initiative
            game_tracker.set_order()

            # Close Current Window
            self.master.destroy()

            # Open Game Tracker Window
            game_window = Tk()
            gw = InitTracker(master=game_window)
            gw.mainloop()


class EncounterSelection(Frame):
    def __init__(self, master=None):
        # Register Window
        super().__init__(master)
        self.master = master
        self.winfo_toplevel().title("Encounter Selection")

        # Render Encounter Buttons
        self.render_options()

    def render_options(self):
        # Add Top Text to Window
        self._title = Label(self.master, text="Available Encounters", font=titleFont)
        self._title.pack(pady=(10,10))

        # Get List of Encounters from Directory
        encounters = game_tracker.get_encounters()
        for encounter in encounters:
            # Convert from Path to String
            path = str(encounter)

            # Handle Windows vs Unix
            if isinstance(encounter, pathlib.WindowsPath):
                file = path.split('\\')
            elif isinstance(encounter, pathlib.PosixPath):
                file = path.split('/')

            # Get File Name
            name = file[len(file)-1].replace(".csv", "").replace("-", " ")

            # Create Button for Encounter
            button = Button(self.master, text=name, font=baseFont)
            button['command'] = lambda encounter=encounter: self.set_encounter(encounter)
            button.pack(fill=X)

    def set_encounter(self, file_name):
        # Save Selected Encounter
        game_tracker.set_encounter(file_name)

        # Close Current Window
        self.master.destroy()

        # Open Player Initiative Window
        player_window = Tk()
        pw = PlayerInit(master=player_window)
        pw.mainloop()

# Load Encounter Picker Window
encounter_window = Tk()
ew = EncounterSelection(master=encounter_window)
ew.mainloop()