import os

turn = 0
onclick = 1
bttnclr_turn = 0
old_click = (0,0)
square_clicked = (0, 0) 
bttnclrs = 'white', 'grey'
path = os.getcwd() + '/Chess_Resources/'

def set_vars():
    square_clicked = (0, 0)
    old_click = (0,0) 
    bttnclr_turn = 0
    onclick = 1
    turn = 0