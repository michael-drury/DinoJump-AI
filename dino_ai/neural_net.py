import neat
import dino_ai.graph as graph
import dino_ai.game as game
import dino_ai.render as render

WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 400

generation = 0


def calculate_output_neuron(net, inputNeurons):
    return net.activate(
        (
            inputNeurons[0],
            inputNeurons[1],
            inputNeurons[2],
            inputNeurons[3],
            inputNeurons[4],
            inputNeurons[5],
            inputNeurons[6],
        )
    )


def is_above_trigger_threshold(neuron):
    return neuron > 0.5


def generate_neural_network(genome, config):
    return neat.nn.FeedForwardNetwork.create(genome, config)


def fitness_function(population, config):

    global generation
    generation += 1

    dinoAI = game.Game(len(population), WINDOW_WIDTH, WINDOW_HEIGHT)

    nets: list[neat.nn.FeedForwardNetwork] = []
    genomes = []
    dinoAliveIndex = list(range(0, len(population)))

    for genome_id, genome in population:
        nets.append(generate_neural_network(genome, config))
        genome.fitness = 0
        genomes.append(genome)

    while len(dinoAliveIndex) > 0:

        dinoAI.restrict_game_loop_speed()
        dinoAI.increment_game_speed()
        dinoAI.update_environment()

        # if dinoAI.window_closed:
        #     print("### Window closed ###")
        #     dinoAI.quit_game()

        for dinoId in dinoAliveIndex:
            dinoAI.update_dino(dinoId)
            genomes[dinoId].fitness += 0.1

            nextObstacle = dinoAI.get_next_obstacle_info(dinoId)
            dinoElevation = dinoAI.get_dino_elevation(dinoId)
            dinoSpeed = dinoAI.get_game_speed()

            inputNerons = [
                nextObstacle.distance,
                nextObstacle.height,
                nextObstacle.width,
                nextObstacle.elevation,
                dinoSpeed,
                dinoElevation,
                nextObstacle.distance,
            ]

            outputNeurons = calculate_output_neuron(nets[dinoId], inputNerons)
            if is_above_trigger_threshold(outputNeurons[0]):
                dinoAI.dino_jump(dinoId)
            if is_above_trigger_threshold(outputNeurons[1]):
                dinoAI.dino_duck(dinoId)

            if dinoAI.dino_object_collision(dinoId):
                genomes[dinoId].fitness -= 1
                dinoAliveIndex.remove(dinoId)

        dinoAI.increment_score()
        dinoAI.draw_game()
        dinoAI.get_renderer().display_generation(generation)
        dinoAI.get_renderer().update_display()


def loadConfigFile(configFile):
    return neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        configFile,
    )


def set_genome_statistics_reporter(population):
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)


def plotNetwork(config, winner):

    node_names = {
        -1: "obst_dist",
        -2: "obst_height",
        -3: "obst_width",
        -4: "obst_y",
        -5: "dino_speed",
        -6: "dino.y",
        -7: "is_cactus",
        0: "Jump",
        1: "Duck",
    }
    graph.draw_net(config, winner, True, node_names)
    print("\nBest genome:\n{!s}".format(winner))


def evolve_generations(population, num_generations):
    return population.run(fitness_function, num_generations)


def run(configFile):

    config = loadConfigFile(configFile)
    population = neat.Population(config)
    set_genome_statistics_reporter(population)

    winner = evolve_generations(population, 100)

    plotNetwork(config, winner)
