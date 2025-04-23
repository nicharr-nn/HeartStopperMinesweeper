# HeartStopperMinesweeper
This project is an enhanced version of the Minesweeper game with new bomb mechanics and a life system. The life system consists of multiple lives, allowing the player to step on a bomb with a chance of surviving.  This project introduces two new types of bombs: the Heart Drain Bomb and the Countdown Bomb.

## Game Concept
Players start with three hearts. If a player steps on a bomb, it will cause different unique effects:
- Classic Bomb: The game is over instantly.
- Heart Drain Bomb: Reduces one heart. If the player has no remaining hearts after stepping on this bomb, the game is over.
- Countdown Bomb: Starts a countdown timer. However, if the game is not won before the countdown ends, the game is over.

To win this game, the player needs to reveal all non-bomb tiles before running out of hearts or time. The player loses if they run out of hearts or fails before the countdown bomb detonates.

## Python Version
Requires Python >= 3.10

## Current Features
- The game can be played with different bomb types (Classic Bomb, Heart Drain Bomb, and Countdown Bomb) and includes a life system with multiple hearts.
- Game-over conditions are based on hearts and a countdown timer, while win conditions are based on revealing all non-bomb tiles.

## How to run the application
1. Clone the repository
```bash
git clone https://github.com/nicharr-nn/HeartStopperMinesweeper.git
```
2. cd into the project directory
```bash
cd HeartStopperMinesweeper
```
3. Create a virtual environment by running the following command in the terminal:
```bash
python -m venv venv
```
or (MacOS)
```bash
python3 -m venv venv
```
4. Activate the virtual environment by running the following command in the terminal:

MacOS or Linux:
```bash
source venv/bin/activate
```

Windows:
```bash
venv\Scripts\activate
```
5. Install the required packages by running the following command in the terminal:
```bash
pip install -r requirements.txt
```
6. Run the application by executing the following command:
```bash
python main.py
```
