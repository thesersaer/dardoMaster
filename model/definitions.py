import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)).strip('\\model')

grid_cols = [15, 16, 17, 18, 19, 20, 25]
display_grid_cols = ['J', 'PTS', '15', '16', '17', '18', '19', '20', '🎯']
grid_keys = ['J', 'PTS'] + [str(number) for number in grid_cols]

dartboard_numbers = [number for number in range(1, 21, 1)]

cricket_scoring_numbers = [15, 16, 17, 18, 19, 20, 25]

foul_penalty_rounds = 2
