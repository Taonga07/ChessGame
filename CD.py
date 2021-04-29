import os

bttnclrs = 'white', 'grey'
path = os.getcwd() + '/Chess_Resources/'
save_path = os.getcwd()

game_vars = {}

def reset_game_vars(game_vars):
    game_vars['square_clicked'] = (0, 0)
    game_vars['old_click'] = (0,0) 
    game_vars['bttnclr_turn'] = 0
    game_vars['onclick'] = 1
    game_vars['turn'] = 0