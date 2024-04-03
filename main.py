"""
Genetic algorithm NEAT plays a version of the dinosaur jump game from google.

The game has been written in Python, and created using the Pygame module.
NOTE: Pygame module uses top left coordinate as origin (0, 0)

Author: Michael Drury
"""

import os
import dino_ai.neural_net as neural_net

if __name__ == "__main__":

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config/config-feedforward.txt")

    neural_net.run(config_path)
