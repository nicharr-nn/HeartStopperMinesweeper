# Overview
This project is an enhanced version of the Minesweeper game with new bomb mechanics and a life system. The life system consists of multiple lives, allowing the player to step on a bomb with a chance of surviving.  This project introduces two new types of bombs: the Heart Drain Bomb and the Countdown Bomb.

# Game Concept
Players start with three hearts and there will be 15 bombs on the board. If a player steps on a bomb, it will cause different unique effects:
- <img src="image/classic.png" alt="Classic Bomb" width="20" height="20"> Classic Bomb: The game is over instantly.
- <img src="image/heartdrain.png" alt="Classic Bomb" width="20" height="20"> Heart Drain Bomb: Reduces one heart. If the player has no remaining hearts after stepping on this bomb, the game is over.
- <img src="image/countdown.png" alt="Classic Bomb" width="20" height="20"> Countdown Bomb: Starts a countdown timer (30 seconds). However, if the game is not won before the countdown ends, the game is over.

To win the game, the player must reveal all non-bomb tiles by clicking on them before running out of hearts or time.

# UML Class Diagram
![UML](image/UML.png)

# Class Responsibility
| **Class Name** | **Responsibilities**                                                                                     |
|----------------|----------------------------------------------------------------------------------------------------------|
| GameGUI        | Handles the user interface and game display. Manages rendering, event handling, and player interactions. |
| Player         | Tracks player hearts, interactions, and status.                                                          |
| Board          | Manage tile grid, bomb placement, and game logic.                                                        |
| Tile           | Represents a single tile in the grid. Stores bomb presence, bomb type, and number of adjacent bombs.     |
| Bomb           | Abstract base class for bomb types.                                                                      |
| Visualizer     | Generates visual summaries. Produces graphs and statistics tables.                                       |

# Youtube
[Link](https://youtu.be/at2vWlNWSYY)

# Proposal
[Link](https://drive.google.com/file/d/1AA6IrNITFUoffsFquPtr09E6GohyyJWH/view?usp=sharing)
