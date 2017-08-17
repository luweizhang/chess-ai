import load
import pickle
import theano
import theano.tensor as T
import math
import chess, chess.pgn
import heapq
import time
import re
import string
import numpy
import sunfish
import pickle
import random
import traceback

def get_model_from_pickle(fn):
    f = open(fn)
    Ws, bs = pickle.load(f)
    
    Ws_s, bs_s = load.get_parameters(Ws=Ws, bs=bs)
    x, p = load.get_model(Ws_s, bs_s)
    
    predict = theano.function(
        inputs=[x],
        outputs=p)

    return predict
    
#func = get_model_from_pickle('model.pickle')
