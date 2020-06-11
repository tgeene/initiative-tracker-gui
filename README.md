# Python GUI TableTop Initiative Tracker

A simple python tkinter script for tracking initiative in TableTop RPG's. Inspired by [initiative-tracker](https://github.com/tgeene/initiative-tracker).

## How To Use

### Adding Players

* Change `players-example.csv` to `players.csv`
* Add one player on each line as follows:
    * Player Name, Initiative Mod
* Leave `Line 1` Labels

### Adding Encounters

* Copy/paste `encounters/_example.csv` to `encounters` folder with a new name
* Add one mob on each line as follows:
    * Mob Name, Mob CR Level, Initiative Mod
* Leave `Line 1` Labels

### Running App

    python app.py

## Example Screenshots

#### Select Which Encounter to Run

![Encounter Selection Window](./_screenshots/encounter-selection.png?raw=true)

#### Submit Players Initiative for Encounter

![Player Initiative Window](./_screenshots/player-initiative.png?raw=true)

#### Initiative Info and Command Buttons

![Initiative Tracker Window](./_screenshots/initiative-tracker.png?raw=true)

#### Select Which Creature to Insert

![Insert Selection Window](./_screenshots/insert-selection.png?raw=true)

#### Add Creature to Current Position

![Add Creature Window](./_screenshots/add-creature.png?raw=true)