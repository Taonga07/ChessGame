from tkinter import filedialog, messagebox
import tkinter, json, Chess, os, CP, CD

def menu(window, board):
    menubar = tkinter.Menu(window)

    filemenu = tkinter.Menu(menubar, tearoff=0)
    editmenu = tkinter.Menu(menubar, tearoff=0)
    viewmenu = tkinter.Menu(menubar, tearoff=0)
    toolmenu = tkinter.Menu(menubar, tearoff=0)
    helpmenu = tkinter.Menu(menubar, tearoff=0)

    filemenu.add_command(label="New", command=lambda: onNew(window, board, 'Test.txt'))
    filemenu.add_command(label="Open", command=lambda: onOpen(window, board))
    filemenu.add_command(label="Save", command=lambda: onSave(window, board))
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=lambda: window.destroy())

    editmenu.add_command(label="custormise pieces", command=lambda: openGuide())
    editmenu.add_command(label="custormise board", command=lambda: openGuide())
    editmenu.add_checkbutton(label='Blindfold Chess', command=lambda: openGuide())

    viewmenu.add_checkbutton(label='points', command=lambda: openGuide())
    viewmenu.add_checkbutton(label='pieces taken', command=lambda: openGuide())
    viewmenu.add_checkbutton(label='computer evaluation', command=lambda: openGuide())
    viewmenu.add_command(label="game history", command=lambda: openGuide())

    toolmenu.add_command(label="takeback", command=lambda: openGuide())
    toolmenu.add_command(label="flip board", command=lambda: openGuide())
    toolmenu.add_command(label="Request stalemate", command=lambda: openGuide())
    toolmenu.add_command(label="Resighn", command=lambda: openGuide())
    toolmenu.add_command(label="hint", command=lambda: openGuide())

    helpmenu.add_command(label="Open Guide", command=lambda: openGuide())

    menubar.add_cascade(label="File", menu=filemenu)
    menubar.add_cascade(label="Edit", menu=editmenu)
    menubar.add_cascade(label="View", menu=viewmenu)
    menubar.add_cascade(label="Tools", menu=toolmenu)
    menubar.add_cascade(label="Help", menu=helpmenu)

    window.config(menu=menubar)

def onNew(window, board, filename):
    CD.reset_game_vars(CD.game_vars)
    board = Chess.open_board(filename)
    Chess.layout_board(window, board)

def onOpen(window, board):
    CD.reset_game_vars(CD.game_vars)
    filename = filedialog.askopenfilename(initialdir=CD.save_path, title='Open file',
                        filetypes=(("main files","*txt*"),("All files","*.*")))
    CD.save_path = os.path.split(filename)[0]   # update save location
    onNew(window, board, filename)

def onSave(window, board):
    filename = filedialog.asksaveasfilename(initialdir=CD.save_path, title='Save as',
                        filetypes=(("main files","*txt*"),("All files","*.*")))
    CD.save_path = os.path.split(filename)[0]   # update save location
    Chess.save_board(filename, board)

def openGuide():
    try:
        os.system("gedit Guide.txt")
    except:
        try:
            os.system("notepad Guide.txt")
        except:
            messagebox.showerror("Error","This is not possible!")

def dump_board(board):
    ''' string list all pieces on the board '''
    lines = []
    for row in board:
        for elem in row:
            if elem != None:
                lines.append(str(elem)) # string repr for class
    return lines

OUT_VERSION='1.0'   # increment version if output format changes, this allows for backward compatibility

def open_board(filename):#
    board = [[None]*8 for _ in range(8)]
    with open(filename, 'r') as input_file:
        input_data = input_file.readlines()
    for input_line in input_data:
        input_line = input_line.strip()
        comment_index = input_line.find('#')
        if comment_index >= 0:
            # remove chars to right of comment
            comment_line = input_line[comment_index+1:].strip()
            input_line = input_line[:comment_index]
            split_arr = comment_line.split('=', 1)
            if len(split_arr) > 1:
                var_name = split_arr[0].strip()
                var_value = split_arr[1].strip()
                #print(f"DBG input comment variable: {var_name} = {var_value}")
                if var_name == 'version' and (var_value != OUT_VERSION):
                    ''' Handle old formats, e.g. file is '1.0' but app moved on to '1.2' '''
                    #print(f"TODO: input file variable {var_name} = {var_value} differs to supported {OUT_VERSION}")
        #print(f"DBG input_line: {input_line}")
        split_arr = input_line.split(' ')
        if len(split_arr) == 4:
            # ignore lines not 4 tokens
            # Piece, Colour, Row, Column to match save_board()
            (Piece, Colour, Row, Column) = split_arr
            piece = eval(f"CP.{Piece}('{Colour}', {Column}, {Row})")
            board[int(piece.row)][int(piece.column)] = piece 
    if True:
        board_dump = dump_board(board)
        board_dump = '\n\t'.join(board_dump)
        #print(f"DBG: dump board {filename}:\n\t{board_dump}")
        
    return board

def save_board(filename, board):
    with open(filename, 'w') as filehandle:
        filehandle.write(f'# version={OUT_VERSION}\n')  # file comment
        filehandle.write(f'# Piece, Colour, Row, Column\n')  # file comment
        for row_number in range(0, 8):
            for column_number in range(0,8):
                if board[row_number][column_number] != None:
                    _piece = board[row_number][column_number].piece
                    _colour = board[row_number][column_number].colour
                    # Piece, Colour, Row, Column to match split() in open_board()
                    _line = f"{_piece} {_colour} {row_number} {column_number}\n"
                    filehandle.write(_line)

def remove_grid_item(window, row_number, column_number):
    grid_slaves = window.grid_slaves(row_number, column_number)
    if len(grid_slaves) > 0:
        for g in grid_slaves:
            g.destroy()