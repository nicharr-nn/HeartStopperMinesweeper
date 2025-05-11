# HeartStopperMinesweeper
This project is an enhanced version of the Minesweeper game with new bomb mechanics and a life system. The life system consists of multiple lives, allowing the player to step on a bomb with a chance of surviving.  This project introduces two new types of bombs: the Heart Drain Bomb and the Countdown Bomb.

## Game Concept
Players start with three hearts and there will be 15 bombs on the board. If a player steps on a bomb, it will cause different unique effects:
- <img src="image/classic.png" alt="Classic Bomb" width="20" height="20"> Classic Bomb: The game is over instantly.
- <img src="image/heartdrain.png" alt="Classic Bomb" width="20" height="20"> Heart Drain Bomb: Reduces one heart. If the player has no remaining hearts after stepping on this bomb, the game is over.
- <img src="image/countdown.png" alt="Classic Bomb" width="20" height="20"> Countdown Bomb: Starts a countdown timer (30 seconds). However, if the game is not won before the countdown ends, the game is over.

To win the game, the player must reveal all non-bomb tiles by clicking on them before running out of hearts or time.

## Python Version
Requires Python >= 3.10

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
or (MacOS)
```bash
python3 main.py
```