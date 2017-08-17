## Deep Learning Model (Theano)

Code for training and executing a deep learning based chess evaluation function, adapted from a deep learning blog post by Erik Bern

You can download games for training from http://www.ficsgames.org/download.html

### parse_game.py:  
Parses a directory full of chess games (.pgn) and outputs as HDF5 format for training
### load.py:        
Helper functions for loading the parsed chess game data (don't need to execute this)
### train.py:       
Train the neural network using Theano and outputs a .pickle file
### use_model.py:   
load the .pickle file to be used in the game playing evaluation function
