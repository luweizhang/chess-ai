# Grandmaster Level Chess AI

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
