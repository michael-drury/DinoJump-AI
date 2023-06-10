# DinoJump-AI

The genetic algorithm [NEAT](https://neat-python.readthedocs.io/en/latest/index.html) (NeuroEvolution of Augmenting Topologies) has been implemented to find an optimal neural network, capable of playing a dinosaur jumping game to a high level.
The game is based on that found within the Google Chrome browser. To access the Google game, internet connection must be disabled.

Once an optimal neural network has been found, an *svg* file will be exported showing a  visualisation of the connections and weights of this network.

### Gameplay
The goal of the game is for the dinosaur character to avoid oncoming obstacles by either jumping over them, or ducking to avoid them. The speed at which the character runs increases as the players score increments. The game is over when the character comes into contact with an object.

### Neural Network
The NEAT algorithm initially creates a several randomised neural networks, from a series of specified game inputs and actions to be taken. The game inputs in this instance, consist of parameters such as the distance of the closest oncoming object. An example of an action, would be to jump over an object.
It then determines the success of each of these networks by assessing the scores achieved. Following this, subsequent networks are produced that a mutated versions of the must successful networks from the previous generation.

### Language

 - Python  3.7

## Running Program

### Run in-browser

Click the button below to run the program in Gitpod.


[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/michael-drury/Dinojump-AI)

### Run locally

1. Clone the repository into a local directory by running `git clone https://github.com/michael-drury/DinoJump-AI`

2. Install necessary libraries by running `pip3 install -r requirements.txt`
- numpy
- pygame
- neat-python
- graphviz
- matplotlib

3. Run the repository by running `python3 main.py`

## Contributors

- [Michael Drury](https://github.com/michael-drury): Main project
- [Code Reclaimers](https://github.com/CodeReclaimers): `visualise.py`

## Inspiration

- [Tech with Tim](https://www.youtube.com/channel/UC4JX40jDee_tINbkjycV4Sg)
- [Code Bullet](https://www.youtube.com/channel/UC0e3QhIYukixgh5VVpKHH9Q)