# Grandmaster Level Chess AI (in progress)

This is a chess AI and chess game built using python. 

I'm trying use a similar AI design as Alpha Go built by Google Deepmind.

This AI combines probabilistic tree search with a convolutional neural net.

The trained convolutional net will be used as an evaluation function to narrow down the search space of the tree search.  After the search space has been narrowed down, the optimal move will be determined using the minimax algorithm


Please use virtual machine to run this:

```
brew install python3
virtualenv -p /usr/local/bin/python3 venv 
virtualenv venv
source venv/bin/activate
pip install ipython notebook
```

You can find more details in my blog:
luweilikesdata.blogspot.com




### Explanation of the tree generator:

The tree generator component of the chess AI generates the possible future board positions based on the possible moves that the pieces can make.  At any given position, there are on average 20 possible moves that can be made in chess.

![alt tag](http://www.andreykurenkov.com/writing/images/2016-4-15-a-brief-history-of-game-ai/2-evalfunc.png)

The above illustrates a chess tree.  Possible moves are generated from the current position to create hypothetical future states. 

## Explanation of the evaluation function

I would say that this is the intuitive component of the chess AI.  Given an 8x8 chess position, the evaluation function with determine between a move is good or not by assigning it a numerical score.   A negative score means that black is winning, a positive score means that white is winning.
Image result for brains
This component of the AI is the most important because it is the one that can be optimized.


## Explanation of the minimax algorithm:

The minimax algorithm essentially tries to find the optimal move from a tree of moves.   Starting from the leaves of the tree, you want to backwards calculate back to the optimal move by alternating between min() and max() (hence the name, minimax). 

When it is your turn, you want to optimize for your outcome, therefore you want to calculate the max() position score. 

When it is your opponents turn, he wants to minimize your outcome, therefore it calculates the min() position score.

![alt tag](https://www3.ntu.edu.sg/home/ehchua/programming/java/images/GameTTT_minimax.png)


The guide below explains minimax very well:
http://web.cs.ucla.edu/~rosen/161/notes/minimax.html

