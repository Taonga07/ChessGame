cd /home/taonga07/Documents/DigiLocal/Chess2030/ChessGame/
autopep8 --in-place --aggressive --aggressive Headless.py
autopep8 --in-place --aggressive --aggressive Pieces.py
autopep8 --in-place --aggressive --aggressive Gui.py
black /home/taonga07/Documents/DigiLocal/Chess2030
shopt -s globstar  # for Bash
pylint /home/taonga07/Documents/DigiLocal/Chess2030/ChessGame/
