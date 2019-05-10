<p align="center">
  <img src="DEMO.gif" height="150">
</p>

# Snake X

Snake X is an arcade snake game written in Python using [pyxel](https://github.com/kitao/pyxel). X stands for the functionality to move in "X" directions.

## Build and Play

```
git clone git@github.com:balloonio/snakex.git
cd snakex
python3 -m venv myvenv
source myvenv/bin/activate
pip3 install -r requirements.txt
./snakex.py
```

## Controls and Keys

| Control         | Key                            |
|-----------------|--------------------------------|
| Move up         | `UP arrow key` or `W`          |
| Move down       | `DOWN arrow key` or `S` or `X` |
| Move left       | `LEFT arrow key` or `A`        |
| Move right      | `RIGHT arrow key` or `D`       |
| Move up right   | `E`                            |
| Move up left    | `Q`                            |
| Move down right | `C`                            |
| Move down left  | `Z`                            |
| Restart         | `G`                            |
| Quit            | `ESC`                          |

## Features

- Snake can move along eight directions.
- Snake grows longer and moves faster after it consumes apples; the length to grow depends on the apple color while the acceleration is the same for all apples.
- Clicking direction keys while snake is already moving in that direction will make snake temporarily speed up.
- The score is shown upon death as of how many apple was consumed.
- There are sound effects for apple eating and death screen
