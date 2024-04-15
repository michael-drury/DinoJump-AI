import os
import src.neural_net as neural_net

if __name__ == "__main__":

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config/config-feedforward.txt")

    neural_net.run(config_path)
