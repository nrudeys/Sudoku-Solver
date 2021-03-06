# Sudoku Solver
# By: Shahnur Syed

# Importing libraries
import numpy as np
import os
import pygame as py
import random
import sys
from colors import Colors
import game_helpers as gh
from game_modes import Mode
import game_setup
import gen_dataset as gen_data
import solve_dataset as solve_data

# Setting clock
fps = 5
fpsclock = py.time.Clock()

# Initializing game
py.init()

# Setting up drawing window
screen = py.display.set_mode([540, 600])

# Setup font types to use
text_font = py.font.SysFont('Monotype', 18)
num_font = py.font.SysFont('Monotype', 20, bold=True)
display_font = py.font.SysFont('Monotype', 25)

# Flags
running = True
game_started = info = generate_sol = blurred = pos = easy = medium = \
    hard = default = mode_diff = enter_board = sol_ent = False
assist = None

# Tracking records
entries_ent = dict.fromkeys([k for k in gh.get_cell_indices()], 0)
invalid = {}

input_num = 0
pg = 1

# Getting instruction lines
lines = game_setup.get_lines()

# Initial screen
game_setup.home_screen(screen, py.mouse.get_pos(), text_font)

# Setting positions for grid
# START pos: (x, y), ENTER pos: (x1, y1)
x = y = x1 = y1 = 300

while running:
    for event in py.event.get():
        if event.type == py.QUIT:
            # Exiting game
            running = False

        if event.type == py.MOUSEBUTTONUP:
            # Clicked position
            pos = curr_pos = py.mouse.get_pos()

            if (curr_pos[1] >= 180 and curr_pos[1] <= 220 and not game_started
                    and not enter_board):
                if curr_pos[0] >= 90 and curr_pos[0] <= 180:
                    # Starting game
                    if (os.path.exists("curr_grid.png") or
                            os.path.exists("curr_grid_enter.png")):
                        # Back to game screen, mode not changed
                        back_default = (
                            str(default).isnumeric() and
                            default == mode_diff and not
                            easy and not medium and not hard
                        )

                        back_easy = (str(mode_diff).isnumeric() and
                                     mode_diff == Mode.EASY and easy)

                        back_med = (mode_diff == Mode.MEDIUM and medium)

                        back_hard = (mode_diff == Mode.HARD and hard)

                        grid_saved = os.path.exists("curr_grid.png")

                        if (back_default or back_easy or back_med or
                                back_hard) and grid_saved:
                            # Load previous Sudoku puzzle
                            img = py.image.load("curr_grid.png")
                            screen.blit(img, (0, 0))

                            for k in invalid.keys():
                                val = str(invalid[k])

                                py.draw.rect(screen, Colors.WHITE,
                                             py.Rect(
                                                 k[0] + 3, k[1] + 3, 56, 56)
                                             )

                                if assist:
                                    # Red highlight incorrect entries
                                    if k == (x, y):
                                        py.draw.rect(screen,
                                                     Colors.L_RED,
                                                     py.Rect(
                                                         k[0] + 3, k[1] + 3,
                                                         56, 56)
                                                     )
                                    screen.blit(
                                        num_font.render(
                                            val, True, Colors.RED),
                                        (25 + k[0], 25 + k[1])
                                    )
                                else:
                                    # Blue highlight (no assist)
                                    if k == (x, y):
                                        py.draw.rect(screen,
                                                     Colors.L_BLUE,
                                                     py.Rect(
                                                         k[0] + 3, k[1] + 3,
                                                         56, 56)
                                                     )

                                    screen.blit(
                                        num_font.render(val, True,
                                                        Colors.BLUE),
                                        (25 + k[0], 25 + k[1])
                                    )
                        else:
                            # Check if mode was selected
                            if easy or medium or hard:
                                grid = gh.set_grid(easy, medium, hard,
                                                   default)
                            else:
                                choices = Mode.get_choices(Mode)
                                default = random.choice(choices)

                                grid = gh.set_grid(easy, medium, hard,
                                                   default)

                            game_setup.create_empty_board(screen)

                            given_clues = game_setup.insert_values(
                                screen, grid
                            )

                            entries = (
                                gh.set_ents_dicts(given_clues)
                            )
                    else:
                        # New game
                        if easy or medium or hard:
                            grid = gh.set_grid(easy, medium, hard, default)
                        else:
                            choices = Mode.get_choices(Mode)
                            default = random.choice(choices)

                            grid = gh.set_grid(easy, medium, hard, default)

                        game_setup.create_empty_board(screen)

                        given_clues = game_setup.insert_values(screen, grid)

                        entries = (
                            gh.set_ents_dicts(given_clues)
                        )

                        invalid = {}
                        x = y = 300

                    # Reset flags
                    game_started = True
                    blurred = enter_board = info = pos = False
                    input_num = 0
                elif (curr_pos[0] >= 350 and curr_pos[0] <= 440 and
                      not enter_board):
                    # Info button clicked
                    info = True
                    game_started = False
                elif (curr_pos[0] >= 220 and curr_pos[0] <= 310 and
                      not enter_board):
                    # Enter button clicked
                    if not all(x == 0 for x in entries_ent.values()):
                        # Enter board previously visited
                        img = py.image.load("curr_grid_enter.png")
                        screen.blit(img, (0, 0))
                    else:
                        indices = [k for k in gh.get_cell_indices()]
                        entries_ent = dict.fromkeys(indices, 0)

                        game_setup.create_empty_board(screen)

                    enter_board = True
                    info = pos = False
            elif (curr_pos[0] >= 420 and curr_pos[0] <= 520 and
                  curr_pos[1] >= 550 and curr_pos[1] <= 580 and info):
                # Back button in info screen clicked
                info = False
                pg = 1
            elif curr_pos[1] >= 550 and curr_pos[1] <= 590 and game_started:
                # Game started
                if curr_pos[0] >= 30 and curr_pos[0] <= 130:
                    # New game button clicked
                    game_setup.create_empty_board(screen)

                    if easy or (str(default).isnumeric() and
                                default == Mode.EASY):
                        grid = gen_data.gen_puzzle(0, 2, 4, 5, 42)
                    elif medium or default == Mode.MEDIUM:
                        grid = gen_data.gen_puzzle(3, 5, 5, 6, 53)
                    elif hard or default == Mode.HARD:
                        grid = gen_data.gen_puzzle(6, 8, 6, 7, 64)

                    given_clues = game_setup.insert_values(screen, grid)
                    entries = gh.set_ents_dicts(given_clues)

                    # Reset flags
                    blurred = generate_sol = False
                    invalid = {}
                    input_num = 0
                    x = y = 300
                elif curr_pos[0] >= 160 and curr_pos[0] <= 260:
                    # Generate solution button clicked
                    sol = solve_data.solve_puzzle(np.copy(grid))

                    game_setup.create_empty_board(screen)

                    game_setup.insert_values(screen, grid, sol)
                    entries = {(x, y): sol[(y // 60, x // 60)]
                               if (x, y) not in given_clues
                               else True for x, y in entries}

                    generate_sol = True
                    blurred = False
                elif curr_pos[0] >= 290 and curr_pos[0] <= 390:
                    # Verify button clicked

                    grid_vals = gh.get_curr_grid_vals(entries, given_clues,
                                                      grid)

                    if gen_data.verify.verify_validness(grid_vals):
                        valid_sol = True
                    else:
                        valid_sol = False

                    if not blurred:
                        py.image.save(screen, "curr_grid.png")
                        game_setup.blur_background(screen, "curr_grid.png")
                        blurred = True

                    game_setup.display_message(screen)

                    if valid_sol:
                        screen.blit(display_font.render("You Win!", True,
                                                        Colors.BLACK),
                                    (220, 170))
                    else:
                        screen.blit(display_font.render("Try Again!", True,
                                                        Colors.BLACK),
                                    (200, 170))
                elif (curr_pos[0] >= 420 and curr_pos[0] <= 520
                      and game_started):
                    # Back button in game screen clicked

                    if not blurred:
                        py.image.save(screen, "curr_grid.png")

                    game_started = blurred = False

                    # Saving previous difficulty mode
                    if easy:
                        mode_diff = Mode.EASY
                    elif medium:
                        mode_diff = Mode.MEDIUM
                    elif hard:
                        mode_diff = Mode.HARD
                    elif default:
                        mode_diff = default
            elif curr_pos[1] >= 550 and curr_pos[1] <= 590 and enter_board:
                # Clear button clicked
                if curr_pos[0] >= 20 and curr_pos[0] <= 120:
                    game_setup.create_empty_board(screen)

                    indices = [key for key in gh.get_cell_indices()]

                    entries_ent = dict.fromkeys(indices, 0)

                    game_setup.insert_values(screen, np.reshape(
                        list(entries_ent.values()), (9, 9))
                    )

                    sol_ent = False

                # Solved button clicked
                if curr_pos[0] >= 220 and curr_pos[0] <= 320:
                    grid_vals = gh.get_curr_grid_vals(entries_ent)

                    sol_ent = error_occur = False
                    err_message = ""

                    try:
                        sol_ent = solve_data.solve_puzzle(np.copy(grid_vals))
                    except ValueError as err:
                        error_occur = True
                        err_message = str(err)

                    if type(sol_ent) == np.ndarray:
                        game_setup.create_empty_board(screen)

                        game_setup.insert_values(screen, np.copy(grid_vals),
                                                 sol_ent)

                    if error_occur:
                        if not blurred:
                            py.image.save(screen, "curr_grid_enter.png")
                            game_setup.blur_background(screen,
                                                       "curr_grid_enter.png")
                            blurred = True

                        game_setup.display_message(screen)
                        if err_message == "Has Duplicates":
                            screen.blit(display_font.render(
                                err_message, True, Colors.BLACK),
                                (175, 175)
                            )
                        elif err_message == "Not Enough Clues":
                            screen.blit(display_font.render(
                                err_message, True, Colors.BLACK),
                                (155, 175)
                            )
                        else:
                            screen.blit(display_font.render(
                                err_message, True, Colors.BLACK),
                                (190, 175)
                            )
                elif curr_pos[0] >= 420 and curr_pos[0] <= 520:
                    # Back button clicked
                    enter_board = False
                    py.image.save(screen, "curr_grid_enter.png")
            elif not (curr_pos[1] >= 550 and curr_pos[1] <= 590) and blurred:
                # Clicked outside of display message, return to
                # previous screen
                if enter_board:
                    img = py.image.load("curr_grid_enter.png")
                else:
                    img = py.image.load("curr_grid.png")

                screen.blit(img, (0, 0))

                blurred = pos = False
            elif (not game_started and curr_pos[1] >= 340 and
                  curr_pos[1] <= 380):
                # Clicked on difficulty mode
                if curr_pos[0] >= 90 and curr_pos[0] <= 180:
                    if easy:
                        # Clicking twice will undo select mode
                        easy = False
                    else:
                        easy = True

                    medium = hard = default = False
                elif curr_pos[0] >= 220 and curr_pos[0] <= 310:
                    if medium:
                        medium = False
                    else:
                        medium = True

                    easy = hard = default = False
                elif curr_pos[0] >= 350 and curr_pos[0] <= 410:
                    if hard:
                        hard = False
                    else:
                        hard = True

                    easy = medium = default = False
            elif (curr_pos[1] >= 470 and curr_pos[1] <= 510 and not
                  game_started):
                # Clicked on an assist mode
                if curr_pos[0] >= 155 and curr_pos[0] <= 245:
                    if assist:
                        assist = None
                    else:
                        assist = True
                elif curr_pos[0] >= 285 and curr_pos[0] <= 375:
                    if assist == False:
                        assist = None
                    else:
                        assist = False
            elif curr_pos[1] >= 555 and curr_pos[1] <= 575 and info:
                if curr_pos[0] >= 50 and curr_pos[0] <= 60 and pg != 1:
                    # Clicked info screen pages left arrow
                    pg -= 1
                elif curr_pos[0] >= 115 and curr_pos[0] <= 125 and pg != 2:
                    # Clicked info screen pages right arrow
                    pg += 1
        elif event.type == py.KEYDOWN:
            # Key is pressed down
            if (game_started and str(entries[(x, y)]).isnumeric() or
                    enter_board):
                input_num = event.unicode

            # Backspace key was pressed down
            if event.key == py.K_BACKSPACE:
                if assist:
                    # Get current entry
                    prev = entries[(x, y)]

                if game_started:
                    if str(entries[(x, y)]).isnumeric():
                        py.draw.rect(screen, Colors.L_BLUE,
                                     py.Rect(x + 3, y + 3, 56, 56))
                        entries[(x, y)] = 0

                        if assist:
                            # Assist is on, check if removal removed
                            # any conflicts

                            curr_vals = gh.get_curr_grid_vals(
                                entries, given_clues, grid
                            )

                            col_count, row_count, sq_count = (
                                gh.count_occurrences(curr_vals, prev, x, y)
                            )

                            if (col_count == 1):
                                # Column is valid, check row and square

                                idx = np.where(curr_vals[:, x // 60] == prev)
                                idx = idx[0][0]

                                if str(entries[x, idx * 60]).isnumeric():
                                    prev_row_cnt = np.count_nonzero(
                                        curr_vals[idx, :] == prev
                                    )

                                    sq = gh.get_square(curr_vals, x, idx)
                                    prev_sq_cnt = np.count_nonzero(sq == prev)

                                    if (not prev_row_cnt > 1 and
                                        not prev_sq_cnt > 1 and
                                            (y != idx * 60)):

                                        if (x, idx * 60) in invalid.keys():
                                            del invalid[(x, idx * 60)]

                                        py.draw.rect(
                                            screen, Colors.WHITE,
                                            py.Rect(x + 3, (idx * 60) + 3,
                                                    56, 56
                                                    )
                                        )

                                        screen.blit(num_font.render(
                                            str(entries[x, (idx * 60)]), True,
                                            Colors.BLUE),
                                            (25 + x, 25 + (idx * 60))
                                        )

                            if (row_count == 1):
                                idx = np.where(curr_vals[y // 60, :] == prev)
                                idx = idx[0][0]

                                if str(entries[(idx * 60), y]).isnumeric():
                                    prev_col_cnt = np.count_nonzero(
                                        curr_vals[:, idx] == prev
                                    )

                                    sq = gh.get_square(curr_vals, idx, y)
                                    prev_sq_cnt = np.count_nonzero(sq == prev)

                                    if (not prev_col_cnt > 1 and
                                        not prev_sq_cnt > 1 and
                                            (x != idx * 60)):

                                        if ((idx * 60), y) in invalid.keys():
                                            del invalid[(idx * 60, y)]

                                        py.draw.rect(
                                            screen, Colors.WHITE,
                                            py.Rect((idx * 60) + 3, y + 3,
                                                    56, 56)
                                        )

                                        screen.blit(num_font.render(
                                            str(entries[(idx * 60), y]), True,
                                            Colors.BLUE),
                                            (25 + (idx * 60), 25 + y)
                                        )

                            if sq_count == 1:
                                square = gh.get_square(curr_vals, x, y)
                                idx = np.where(square == prev)

                                # Locate
                                x_idx = (
                                    idx[1][0] + 3 * round(((x // 60) - 1) / 3)
                                )

                                y_idx = (
                                    idx[0][0] + 3 * round(((y // 60) - 1) / 3)
                                )

                                cell_idx = (x_idx * 60, y_idx * 60)

                                prev_col_cnt = np.count_nonzero(
                                    curr_vals[:, x_idx] == prev
                                )

                                prev_row_cnt = np.count_nonzero(
                                    curr_vals[y_idx, :] == prev)

                                if str(entries[cell_idx]).isnumeric():
                                    if (not prev_col_cnt > 1 and
                                        not prev_row_cnt > 1 and
                                            (x, y) != cell_idx):

                                        if cell_idx in invalid.keys():
                                            del invalid[cell_idx]

                                        py.draw.rect(
                                            screen, Colors.WHITE,
                                            py.Rect(
                                                cell_idx[0] + 3,
                                                cell_idx[1] + 3, 56, 56
                                            )
                                        )

                                        screen.blit(num_font.render(
                                            str(entries[cell_idx]), True,
                                            Colors.BLUE),
                                            (25 + cell_idx[0],
                                             25 + cell_idx[1])
                                        )

                        if (x, y) in invalid.keys():
                            del invalid[(x, y)]

                elif enter_board:
                    if str(entries_ent[(x1, y1)]).isnumeric():
                        py.draw.rect(screen, Colors.WHITE,
                                     py.Rect(x1 + 3, y1 + 3, 56, 56))

                        entries_ent[(x1, y1)] = 0

                        py.draw.rect(screen, Colors.L_BLUE,
                                     py.Rect(x1 + 3, y1 + 3, 56, 56))

            # Delete key was pressed down
            if event.key == py.K_DELETE:
                game_setup.create_empty_board(screen)

                indices = [key for key in gh.get_cell_indices()]

                invalid = {}

                if not enter_board:
                    entries = dict.fromkeys(indices, 0)
                    entries = {k: entries[k] if k not in given_clues else True
                               for k in entries}

                    game_setup.insert_values(screen, grid)

                    generate_sol = blurred = False
                else:
                    entries_ent = dict.fromkeys(indices, 0)

                    game_setup.insert_values(screen, np.reshape(
                        list(entries_ent.values()), (9, 9))
                    )

                    sol_ent = False

    if game_started:
        game_setup.game_screen(screen, py.mouse.get_pos())

        keys_pressed = py.key.get_pressed()

        if keys_pressed[py.K_LEFT]:
            if not blurred:
                invalid_ent = (x, y) in invalid.keys() and assist

                game_setup.advance(screen, (x, y, Colors.WHITE),
                                   grid, entries, invalid_ent)

                x = gh.set_num(x, -60)

                invalid_ent = (x, y) in invalid.keys() and assist

                if invalid_ent:
                    game_setup.advance(screen, (x, y, Colors.L_RED),
                                       grid, entries, invalid_ent)
                else:
                    game_setup.advance(screen, (x, y, Colors.L_BLUE),
                                       grid, entries, invalid_ent)

        if keys_pressed[py.K_RIGHT]:
            if not blurred:
                invalid_ent = (x, y) in invalid.keys() and assist
                game_setup.advance(screen, (x, y, Colors.WHITE),
                                   grid, entries, invalid_ent)

                x = gh.set_num(x, 60)
                invalid_ent = (x, y) in invalid.keys() and assist
                if invalid_ent:
                    game_setup.advance(screen, (x, y, Colors.L_RED),
                                       grid, entries, invalid_ent)
                else:
                    game_setup.advance(screen, (x, y, Colors.L_BLUE),
                                       grid, entries, invalid_ent)

        if keys_pressed[py.K_UP]:
            if not blurred:
                invalid_ent = (x, y) in invalid.keys() and assist
                game_setup.advance(screen, (x, y, Colors.WHITE),
                                   grid, entries, invalid_ent)

                y = gh.set_num(y, -60)

                invalid_ent = (x, y) in invalid.keys() and assist
                if invalid_ent:
                    game_setup.advance(screen, (x, y, Colors.L_RED),
                                       grid, entries, invalid_ent)
                else:
                    game_setup.advance(screen, (x, y, Colors.L_BLUE),
                                       grid, entries, invalid_ent)

        if keys_pressed[py.K_DOWN]:
            if not blurred:
                invalid_ent = (x, y) in invalid.keys() and assist

                game_setup.advance(screen, (x, y, Colors.WHITE), grid,
                                   entries, invalid_ent)

                y = gh.set_num(y, 60)

                invalid_ent = (x, y) in invalid.keys() and assist
                if invalid_ent:
                    game_setup.advance(screen, (x, y, Colors.L_RED),
                                       grid, entries, invalid_ent)
                else:
                    game_setup.advance(screen, (x, y, Colors.L_BLUE),
                                       grid, entries, invalid_ent)

        if pos and not (pos[1] >= 550 and pos[1] <= 590):
            # A cell was clicked

            idx = (gh.round_num(pos[0]), gh.round_num(pos[1]))

            curr_x = gh.round_num(pos[0])
            curr_y = gh.round_num(pos[1])

            if ((curr_x, curr_y) != (x, y) and
                str(entries[(x, y)]).isnumeric() and
                    entries[(x, y)] != 0):

                py.draw.rect(screen, Colors.WHITE,
                             py.Rect(x + 3, y + 3, 56, 56))

                if (x, y) in invalid.keys() and assist:
                    screen.blit(num_font.render(str(entries[(x, y)]), True,
                                                Colors.RED),
                                (25 + x, 25 + y))
                else:
                    screen.blit(num_font.render(str(entries[(x, y)]), True,
                                                Colors.BLUE),
                                (25 + x, 25 + y))

            if assist and str(entries[idx]).isnumeric() and entries[idx] != 0:
                curr_vals = gh.get_curr_grid_vals(entries, given_clues, grid)
                square = gh.get_square(curr_vals, curr_x, curr_y)

                num = entries[(curr_x, curr_y)]

                (col_count, row_count, sq_count) = (
                    gh.count_occurrences(curr_vals, num, curr_x, curr_y)
                )

                if col_count > 1 or row_count > 1 or sq_count > 1:
                    py.draw.rect(screen, Colors.L_RED,
                                 py.Rect(curr_x + 3, curr_y + 3, 56, 56))
                else:
                    py.draw.rect(screen, Colors.L_BLUE,
                                 py.Rect(curr_x + 3, curr_y + 3, 56, 56))
            else:
                py.draw.rect(screen, Colors.L_BLUE,
                             py.Rect(curr_x + 3, curr_y + 3, 56, 56))

                if not str(entries[(curr_x, curr_y)]).isnumeric():

                    if (x, y) in invalid.keys() and assist:
                        screen.blit(num_font.render(
                            str(grid[(curr_y // 60, curr_x // 60)]),
                            True, Colors.BLACK),
                            (25 + curr_x, 25 + curr_y)
                        )
                    else:
                        screen.blit(num_font.render(
                            str(grid[(curr_y // 60, curr_x // 60)]),
                            True, Colors.BLACK),
                            (25 + curr_x, 25 + curr_y)
                        )

            if (entries[(x, y)] == 0 or not str(entries[(x, y)]).isnumeric()):
                if (x, y) != (curr_x, curr_y):
                    py.draw.rect(screen, Colors.WHITE,
                                 py.Rect(x + 3, y + 3, 56, 56))

                if not str(entries[(x, y)]).isnumeric():
                    screen.blit(num_font.render(str(grid[(y // 60, x // 60)]),
                                                True, Colors.BLACK),
                                (25 + x, 25 + y)
                                )

            # After generating sol, only replace values w/ new entry
            if (generate_sol and entries[(x, y)] == sol[(y // 60, x // 60)]
                    and str(entries[(x, y)]).isnumeric()):
                py.draw.rect(screen, Colors.WHITE,
                             py.Rect(x + 3, y + 3, 56, 56))

                if (x, y) in invalid.keys() and assist:
                    screen.blit(num_font.render(str(entries[(x, y)]), True,
                                                Colors.RED),
                                (25 + x, 25 + y)
                                )
                else:
                    screen.blit(num_font.render(str(entries[(x, y)]), True,
                                                Colors.BLUE),
                                (25 + x, 25 + y)
                                )

            (x, y) = (curr_x, curr_y)

            if str(entries[(x, y)]).isnumeric() and entries[(x, y)] != 0:
                if (x, y) in invalid.keys() and assist:

                    screen.blit(num_font.render(str(entries[(x, y)]), True,
                                                Colors.RED),
                                (25 + x, 25 + y)
                                )
                else:
                    screen.blit(num_font.render(str(entries[(x, y)]), True,
                                                Colors.BLUE),
                                (25 + x, 25 + y)
                                )

        if (str(input_num).isnumeric() and int(input_num) >= 1 and
                int(input_num) <= 9 and str(entries[(x, y)]).isnumeric()):
            # Enter input
            py.draw.rect(screen, Colors.WHITE, py.Rect(x + 3, y + 3,
                                                       56, 56))

            prev = entries[(x, y)]
            entries[(x, y)] = num = int(input_num)

            curr_vals = gh.get_curr_grid_vals(entries, given_clues,
                                              grid)

            square = gh.get_square(curr_vals, x, y)

            (col_count, row_count, sq_count) = gh.count_occurrences(
                curr_vals, num, x, y
            )

            # Number is already used in row, col, sq (or all)
            if col_count > 1 or row_count > 1 or sq_count > 1:
                if col_count > 1:
                    idx = np.where(curr_vals[:, x // 60] == num)[0]
                    num_col_entries = [(x, idx[i] * 60) for i, val in
                                       enumerate(idx)]

                    for elem in num_col_entries:
                        if str(entries[elem]).isnumeric():
                            invalid[elem] = num
                            if assist:
                                py.draw.rect(screen, Colors.WHITE,
                                             py.Rect(
                                                 x + 3, elem[1] + 3, 56, 56)
                                             )

                                screen.blit(num_font.render(
                                    str(entries[elem]), True,
                                    Colors.RED),
                                    (25 + x, 25 + (elem[1]))
                                )

                if row_count > 1:
                    idx = np.where(curr_vals[y // 60, :] == num)[0]
                    num_row_entries = [(idx[i] * 60, y) for i, val in
                                       enumerate(idx)]

                    for elem in num_row_entries:
                        if str(entries[elem]).isnumeric():
                            invalid[elem] = num
                            if assist:
                                py.draw.rect(screen, Colors.WHITE,
                                             py.Rect(elem[0] + 3,
                                                     y + 3, 56, 56))

                                screen.blit(num_font.render(
                                    str(entries[elem]), True,
                                    Colors.RED),
                                    (25 + elem[0], 25 + y)
                                )

                if sq_count > 1:
                    idx = np.where(square == num)

                    x_idx = idx[1]
                    y_idx = idx[0]

                    num_sq_entries = [
                        (((x_idx[i] + 3 * round(((x // 60) - 1) / 3))
                          * 60), (y_idx[i] + 3 * round(((y // 60) - 1) / 3))
                         * 60)
                        for i in range(len(x_idx))
                    ]

                    for elem in num_sq_entries:
                        if str(entries[elem]).isnumeric():
                            invalid[elem] = num
                            if assist:
                                py.draw.rect(screen, Colors.WHITE,
                                             py.Rect(elem[0] + 3,
                                                     elem[1] + 3, 56, 56)
                                             )

                                screen.blit(num_font.render(
                                    str(entries[elem]), True,
                                    Colors.RED),
                                    (25 + elem[0], 25 + elem[1])
                                )
            else:
                if (x, y) in invalid.keys():
                    del invalid[(x, y)]

            # Count occurrences to check if the change to prev
            # entry make another entry valid
            (col_count, row_count, sq_count) = gh.count_occurrences(
                curr_vals, prev, x, y
            )

            if (col_count == 1) and prev != 0:
                # Change color of prev to indicate it is valid,
                # locate its position and check the sq and row
                # for duplicates
                idx = np.where(curr_vals[:, x // 60] == prev)
                idx = idx[0][0]

                if (str(entries[x, idx * 60]).isnumeric() and
                        str(prev).isnumeric()):

                    sq = gh.get_square(curr_vals, idx * 60, x)

                    if (not np.count_nonzero(curr_vals[idx, :] == prev)
                        > 1 and not np.count_nonzero(sq == prev) > 1
                            and (y != idx * 60)):

                        if (x, idx * 60) in invalid.keys():
                            del invalid[(x, (idx * 60))]

                        if assist:
                            py.draw.rect(screen, Colors.WHITE,
                                         py.Rect(x + 3,
                                                 (idx * 60) + 3, 56, 56))

                            if (x, idx * 60) in invalid.keys():
                                screen.blit(num_font.render(
                                    str(entries[x, idx * 60]), True,
                                    Colors.RED),
                                    (25 + x, 25 + (idx * 60))
                                )
                            else:
                                screen.blit(num_font.render(
                                    str(entries[x, idx * 60]), True,
                                    Colors.BLUE),
                                    (25 + x, 25 + (idx * 60))
                                )

            if (row_count == 1) and prev != 0:
                idx = np.where(curr_vals[y // 60, :] == prev)
                idx = idx[0][0]

                if (str(entries[(idx * 60), y]).isnumeric() and
                        str(prev).isnumeric()):

                    sq = gh.get_square(curr_vals, idx * 60, y)

                    if (not np.count_nonzero(curr_vals[:, idx] == prev) > 1
                        and not np.count_nonzero(sq == prev) > 1
                            and (x != idx * 60)):
                        if ((idx * 60), y) in invalid.keys():
                            del invalid[((idx * 60), y)]

                        if assist:
                            py.draw.rect(screen, Colors.WHITE,
                                         py.Rect((idx * 60) + 3,
                                                 y + 3, 56, 56)
                                         )

                            if ((idx * 60), y) in invalid.keys():
                                screen.blit(num_font.render(
                                    str(entries[(idx * 60), y]), True,
                                    Colors.RED),
                                    (25 + (idx * 60), 25 + y)
                                )
                            else:
                                screen.blit(num_font.render(
                                    str(entries[(idx * 60), y]), True,
                                    Colors.BLUE),
                                    (25 + (idx * 60), 25 + y)
                                )
            if (sq_count == 1) and prev != 0:
                idx = np.where(square == prev)
                x_idx = idx[1][0] + 3 * round(((x // 60) - 1) / 3)
                y_idx = idx[0][0] + 3 * round(((y // 60) - 1) / 3)

                cell_idx = (x_idx * 60, y_idx * 60)

                prev_col_cnt = np.count_nonzero(curr_vals[:, x_idx] == prev)
                prev_row_cnt = np.count_nonzero(curr_vals[y_idx, :] == prev)

                if (str(entries[cell_idx]).isnumeric() and
                        str(prev).isnumeric()):

                    if (not prev_row_cnt > 1 and not prev_col_cnt > 1 and
                            (x, y) != cell_idx):

                        if cell_idx in invalid.keys():
                            del invalid[cell_idx]

                        if assist:
                            py.draw.rect(screen, Colors.WHITE,
                                         py.Rect(cell_idx[0] + 3,
                                                 cell_idx[1] + 3, 56, 56
                                                 )
                                         )

                            if cell_idx in invalid.keys():
                                screen.blit(num_font.render(str(
                                    entries[cell_idx]), True,
                                    Colors.RED),
                                    (25 + cell_idx[0], 25 + cell_idx[1])
                                )
                            else:
                                screen.blit(num_font.render(str(
                                    entries[cell_idx]), True,
                                    Colors.BLUE),
                                    (25 + cell_idx[0], 25 + cell_idx[1])
                                )

            if (x, y) in invalid.keys() and assist:
                py.draw.rect(screen, Colors.L_RED,
                             py.Rect(x + 3, y + 3, 56, 56))

                screen.blit(num_font.render(input_num, True,
                                            Colors.RED),
                            (25 + x, 25 + y)
                            )
            else:
                py.draw.rect(screen, Colors.L_BLUE,
                             py.Rect(x + 3, y + 3, 56, 56))

                screen.blit(num_font.render(input_num, True,
                                            Colors.BLUE),
                            (25 + x, 25 + y)
                            )

            # Reset
            input_num = 0

        pos = False
    elif enter_board:
        game_setup.enter_board_screen(screen, py.mouse.get_pos())

        keys_pressed = py.key.get_pressed()

        if keys_pressed[py.K_LEFT]:
            if not blurred:
                # Erase previous empty square
                if type(sol_ent) == np.ndarray:
                    game_setup.enter_board_adv(screen,
                                               (x1, y1, Colors.WHITE),
                                               entries_ent, sol_ent)
                else:
                    game_setup.enter_board_adv(screen,
                                               (x1, y1, Colors.WHITE),
                                               entries_ent)

                # Advance in given dir
                x1 = gh.set_num(x1, -60)

                # Highlight new pos
                if type(sol_ent) == np.ndarray:
                    game_setup.enter_board_adv(screen,
                                               (x1, y1, Colors.L_BLUE),
                                               entries_ent, sol_ent)
                else:
                    game_setup.enter_board_adv(screen,
                                               (x1, y1, Colors.L_BLUE),
                                               entries_ent)

        if keys_pressed[py.K_RIGHT]:
            if not blurred:
                if type(sol_ent) == np.ndarray:
                    game_setup.enter_board_adv(screen,
                                               (x1, y1, Colors.WHITE),
                                               entries_ent, sol_ent)
                else:
                    game_setup.enter_board_adv(screen,
                                               (x1, y1, Colors.WHITE),
                                               entries_ent)

                x1 = gh.set_num(x1, 60)

                if type(sol_ent) == np.ndarray:
                    game_setup.enter_board_adv(screen,
                                               (x1, y1, Colors.L_BLUE),
                                               entries_ent, sol_ent)
                else:
                    game_setup.enter_board_adv(screen,
                                               (x1, y1, Colors.L_BLUE),
                                               entries_ent)

        if keys_pressed[py.K_UP]:
            if not blurred:
                if type(sol_ent) == np.ndarray:
                    game_setup.enter_board_adv(screen, (x1, y1, Colors.WHITE),
                                               entries_ent, sol_ent)
                else:
                    game_setup.enter_board_adv(screen,
                                               (x1, y1, Colors.WHITE),
                                               entries_ent)

                y1 = gh.set_num(y1, -60)

                if type(sol_ent) == np.ndarray:
                    game_setup.enter_board_adv(screen,
                                               (x1, y1, Colors.L_BLUE),
                                               entries_ent, sol_ent)
                else:
                    game_setup.enter_board_adv(screen,
                                               (x1, y1, Colors.L_BLUE),
                                               entries_ent)

        if keys_pressed[py.K_DOWN]:
            if not blurred:
                if type(sol_ent) == np.ndarray:
                    game_setup.enter_board_adv(screen,
                                               (x1, y1, Colors.WHITE),
                                               entries_ent, sol_ent)
                else:
                    game_setup.enter_board_adv(screen,
                                               (x1, y1, Colors.WHITE),
                                               entries_ent)

                y1 = gh.set_num(y1, 60)

                if type(sol_ent) == np.ndarray:
                    game_setup.enter_board_adv(screen,
                                               (x1, y1, Colors.L_BLUE),
                                               entries_ent, sol_ent)
                else:
                    game_setup.enter_board_adv(
                        screen, (x1, y1, Colors.L_BLUE), entries_ent)

        if (pos and not(pos[1] >= 550 and pos[1] <= 590)):
            curr_idx = (gh.round_num(pos[0]), gh.round_num(pos[1]))

            if type(sol_ent) == bool:
                py.draw.rect(screen, Colors.L_BLUE,
                             py.Rect(curr_idx[0] + 3, curr_idx[1] + 3, 56, 56)
                             )

                # Click
                if not curr_idx == (x1, y1):
                    py.draw.rect(screen, Colors.WHITE,
                                 py.Rect(x1 + 3, y1 + 3, 56, 56))

                    if entries_ent[(x1, y1)] != 0:
                        if (str(entries_ent[(x1, y1)]).isnumeric() and
                                entries_ent[(x1, y1)] != 0):

                            screen.blit(num_font.render(
                                str(entries_ent[(x1, y1)]),
                                True, Colors.BLACK), (25 + x1, 25 + y1)
                            )

                (x1, y1) = curr_idx

                if (str(entries_ent[curr_idx]).isnumeric() and
                        entries_ent[curr_idx] != 0):
                    screen.blit(num_font.render(
                        str(entries_ent[curr_idx]),
                        True, Colors.BLACK), (25 + x1, 25 + y1)
                    )

        if (str(input_num).isnumeric() and int(input_num) >= 1 and
                int(input_num) <= 9 and
                str(entries_ent[(x1, y1)]).isnumeric()):
            # Enter input
            if type(sol_ent) == bool:
                # Update entry for pos and display
                entries_ent[(x1, y1)] = int(input_num)

                if entries_ent[(x1, y1)] != 0:
                    py.draw.rect(screen, Colors.L_BLUE,
                                 py.Rect(x1 + 3, y1 + 3, 56, 56)
                                 )

                screen.blit(num_font.render(input_num, True,
                                            Colors.BLACK),
                            (25 + x1, 25 + y1)
                            )

            # Reset
            input_num = 0
        pos = False
    elif info:
        if pg == 1:
            game_setup.info_screen(screen, py.mouse.get_pos(), lines[:20], pg)
        elif pg == 2:
            game_setup.info_screen(screen, py.mouse.get_pos(), lines[20:], pg)
    else:
        game_setup.home_screen(screen, py.mouse.get_pos(), text_font)

        try:
            curr_pos
        except NameError:
            curr_pos = None

        # Keep highlight on clicked button

        if easy or (str(default).isnumeric() and default == Mode.EASY):
            py.draw.rect(screen, Colors.PINK, py.Rect(90, 340, 90, 40))
            py.draw.rect(screen, Colors.BLACK,
                         py.Rect(90, 340, 90, 40), 3)
            screen.blit(text_font.render(
                'EASY', True, Colors.BLACK), (110, 350))
        elif medium or (default == Mode.MEDIUM):
            py.draw.rect(screen, Colors.PINK, py.Rect(220, 340, 90, 40)
                         )
            py.draw.rect(screen, Colors.BLACK,
                         py.Rect(220, 340, 90, 40), 3)
            screen.blit(text_font.render('MEDIUM', True,
                                         Colors.BLACK), (232, 350))
        elif hard or (default == Mode.HARD):
            py.draw.rect(screen, Colors.PINK, py.Rect(350, 340, 90, 40)
                         )
            py.draw.rect(screen, Colors.BLACK,
                         py.Rect(350, 340, 90, 40), 3)
            screen.blit(text_font.render(
                'HARD', True, Colors.BLACK), (370, 350))

        if assist:
            py.draw.rect(screen, Colors.PINK, py.Rect(155, 470, 90, 40)
                         )
            py.draw.rect(screen, Colors.BLACK,
                         py.Rect(155, 470, 90, 40), 3)

            screen.blit(text_font.render(
                'On', True, Colors.BLACK), (190, 480))
            screen.blit(text_font.render(
                'Off', True, Colors.BLACK), (315, 480))
        elif assist == False or (assist is None and
                                 os.path.exists("curr_grid.png")):

            py.draw.rect(screen, Colors.PINK, py.Rect(285, 470, 90, 40)
                         )
            py.draw.rect(screen, Colors.BLACK,
                         py.Rect(285, 470, 90, 40), 3)

            screen.blit(text_font.render(
                'On', True, Colors.BLACK), (190, 480))
            screen.blit(text_font.render(
                'Off', True, Colors.BLACK), (315, 480))

    # Display
    py.display.flip()
    fpsclock.tick(fps)

# Removing screenshot as its not needed anymore
if os.path.exists("curr_grid.png"):
    os.remove("curr_grid.png")
if os.path.exists("blur_image.jpg"):
    os.remove("blur_image.jpg")
if os.path.exists("curr_grid_enter.png"):
    os.remove("curr_grid_enter.png")

py.quit()
