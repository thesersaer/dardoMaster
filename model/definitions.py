import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)).strip('\\model')

# GENERAL

dartboard_numbers = [number for number in range(1, 21, 1)]

foul_penalty_rounds = 2

min_players = 2

max_players = 6

# CRICKET

cricket_scoring_numbers = [15, 16, 17, 18, 19, 20, 25]

cricket_row_header = ['J', 'PTS'] + [str(number) for number in cricket_scoring_numbers]

cricket_number_0_str = '○○○'
cricket_number_1_str = '●○○'
cricket_number_2_str = '●●○'
cricket_number_3_str = '●●●'
