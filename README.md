# Sudoku-Solver

Generator to create and/or solver Sudoku puzzles

## Table of Contents
1. [Description](#description)
2. [Getting Started](#getting-started)
    * [Technologies and Libraries](#technologies-and-libraries)
    * [How to Run](#how-to-run)
    * [Usage](#usage)
3. [RoadMap](#roadmap)
4. [Acknowledgements](#acknowledgements)

## Description
A solver which uses a backtracking algorithm that is used to find solutions to 
generated or user-provided Sudoku puzzles. The solver has different modes that 
an user can choose for difficulty and/or assistance.

## Getting Started
### Technologies and Libraries
* Python 3.8
* Pygame
* Numpy
### How to Run
#### Clone Repository
<ins>Go to terminal and paste</ins>: git clone https://github.com/nrudeys/Sudoku-Solver.git

#### To run EXE
Go to dist directory in cloned folder and double click on sudoku-solver
application

#### NOTE: to create EXE application
pyinstaller -F --noconsole --add-data "instructions.txt;." --add-data "background.png;." sudoku_solver.py

### Usage
The game has two start modes START and ENTER. Additional information such as
rules, controls, and notes can be found in INFO.

<p align="center">
    <img src="https://github.com/nrudeys/Sudoku-Solver/blob/fec704913523408788eb4a3e284b04c530d60f79/start_game.png" width="350" height="350">
</p>

#### START mode
Before clicking START, an user can also choose a difficulty and assist mode. However, this is
optional. If assist mode is not chosen its default is to be off but if a difficulty mode is not chosen,
one is selected randomly. 

<p align="center">
    <img src="https://github.com/nrudeys/Sudoku-Solver/blob/452a257be55c632b60f5cf717a5a85ccffcf4193/start_modes.png" width="350" height="350">
</p>

##### Difficulty modes
EASY: 39 - 49 given clues          
MEDIUM: 28 - 38 given clues
HARD: 17 - 27 given clues  

Examples:  
<p float="left">
  <img src="https://github.com/nrudeys/Sudoku-Solver/blob/f4707b95ca6bf9aae30c3ad152baa717c341b740/easy.png" width="250">
  <img src="https://github.com/nrudeys/Sudoku-Solver/blob/f4707b95ca6bf9aae30c3ad152baa717c341b740/med.png"     width="250">
  <img src="https://github.com/nrudeys/Sudoku-Solver/blob/f4707b95ca6bf9aae30c3ad152baa717c341b740/hard.png" width="250">
</p>


##### Assist modes
If on, the game will indicate cells that have conflicting entries with one another





#### ENTER mode

In START mode, an user can ch
incompleted
Sudoku puzzle is generated 


## RoadMap
## Acknowledgements
