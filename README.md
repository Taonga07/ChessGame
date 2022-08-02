# ChessGame - Master
[![Pylint](https://github.com/Taonga07/ChessGame/actions/workflows/pylint.yml/badge.svg)](https://github.com/Taonga07/ChessGame/actions/workflows/pylint.yml)
[![Pytest](https://github.com/Taonga07/ChessGame/actions/workflows/pytest.yml/badge.svg)](https://github.com/Taonga07/ChessGame/actions/workflows/pytest.yml)
[![Run on Repl.it](https://repl.it/badge/github/Taonga07/ChessGame)](https://repl.it/github/Taonga07/ChessGame)
![open issues](https://img.shields.io/github/issues-raw/Taonga07/ChessGame)
![closed issues](https://img.shields.io/github/issues-closed-raw/Taonga07/ChessGame)
![open pull requets](https://img.shields.io/github/issues-pr/taonga07/ChessGame)
![closed pullrequests](https://img.shields.io/github/issues-pr-closed-raw/taonga07/ChessGame)
![activity](https://img.shields.io/github/commit-activity/y/taonga07/ChessGame)

![image](https://i.ibb.co/DK14y3k/Screenshot-from-2021-09-23-19-17-35.png)

This is a two player game; playing against computer is not an option yet but could be.

A Guide is being written so you can make this project yourself but as the game is not yet finished neither is it.
Here is the link if you have acess to it https://docs.google.com/document/d/1YOnf6xDqEIGD04JVzfhgvXFyDlK1BxJagbxBN3dT_7Q/edit

Currently the this branch holds the best code. so will be updated so all the errors and imperfections are dealt with in other branches.
The Rules are being developed at the moment. Curently I am working on [Check and Checkmate](https://github.com/Taonga07/ChessGame/tree/Check).

A list of jobs for this game can be found here.

- [x] all pieces rules
- [ ] pawn exchange
- [x] highlight possible moves
- [x] all pieces on board
- [x] all pieces can move
- [x] tests
- [ ] check / checkmate
- [ ] ompasount

notes 
```
sudo snap install pypy3
sudo snap install pypy3-pip
/usr/local/bin/pypy3 -m ensurepip
/usr/local/bin/pypy3 -m pip install --upgrade pip

#all tests
pypy3 -m pip install pytest requests
pypy3 -m pytest

#profile test_perm.py to and use snakeviz gui to see where spending most of the time
pypy3 -m pip install cProfile snakeviz
cd tests
pypy3 -m cProfile -o test_perm.prof test_perm.py
snakeviz test_perm.prof


##working branch

git checkout 0eecccf
```
