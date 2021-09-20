# Sudoku-Solver

Generator to create and/or solver Sudoku puzzles

## Table of Contents
1. [Description](#description)
2. [Getting Started](#gettingstarted)
    * [Technologies and Libraries](#technologies)
    * [How to Run](#howtorun)
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
Go to terminal and paste:
git clone https://github.com/nrudeys/Sudoku-Solver.git

#### To run EXE
Go to dist directory in repository and double click on sudoku-solver
application

#### Create EXE application
pyinstaller -F --noconsole --add-data "instructions.txt;." --add-data "background.png;." sudoku_solver.py

### Usage

## RoadMap
## Acknowledgements
