import unittest
import time
import src.game as game
import tests.test_common as test_common

VALID_NUM_DINOS = 3
VALID_WIN_WIDTH = 1200
VALID_WIN_HEIGHT = 400
VALID_START_SPEED = 100
VALID_FRAME_RATE = 60


class TestGame(unittest.TestCase):

    def setUp(self):
        test_common.block_display_render()
        self.game = game.Game(
            VALID_NUM_DINOS,
            VALID_WIN_WIDTH,
            VALID_WIN_HEIGHT,
            start_speed=VALID_START_SPEED,
            frame_rate=VALID_FRAME_RATE,
        )

    #### Init ####
    def test_init_success(self):
        self.assertIsInstance(
            self.game, game.Game, "Failed to initialize Game instance."
        )

    def test_init_invalid_num_dino_arg_type(self):
        with self.assertRaises(TypeError):
            game.Game("", VALID_WIN_WIDTH, VALID_WIN_HEIGHT)

    def test_init_invalid_width_arg_type(self):
        with self.assertRaises(TypeError):
            game.Game(VALID_NUM_DINOS, "", VALID_WIN_HEIGHT)

    def test_init_invalid_height_arg_type(self):
        with self.assertRaises(TypeError):
            game.Game(VALID_NUM_DINOS, VALID_WIN_WIDTH, "")

    def test_init_invalid_speed_arg_type(self):
        with self.assertRaises(TypeError):
            game.Game(
                VALID_NUM_DINOS, VALID_WIN_WIDTH, VALID_WIN_HEIGHT, start_speed=""
            )

    def test_init_invalid_fps_arg_type(self):
        with self.assertRaises(TypeError):
            game.Game(VALID_NUM_DINOS, VALID_WIN_WIDTH, VALID_WIN_HEIGHT, frame_rate="")

    def test_init_no_arg(self):
        with self.assertRaises(TypeError):
            game.Game()

    def test_init_no_dinos(self):
        with self.assertRaises(ValueError):
            game.Game(0, VALID_WIN_WIDTH, VALID_WIN_HEIGHT)

    # #### Restrict Game Loop Speed ####
    def test_restrict_game_loop_speed_success(self):
        try:
            self.game.restrict_game_loop_speed()
        except:
            self.fail("Restrict game loop speed raised assertion")

    def test_restrict_game_loop_causes_pause(self):
        start_time = time.time()
        self.game.restrict_game_loop_speed()
        end_time = time.time()

        duration = end_time - start_time
        expected_delay = 1 / VALID_FRAME_RATE

        self.assertAlmostEqual(duration, expected_delay, delta=0.05)

    #### Increment Dino Speed ####
    def test_increment_game_speed(self):
        try:
            self.game.increment_game_speed()
        except:
            self.fail("Increment dino speed raised assertion")

        self.assertGreater(self.game.get_game_speed(), VALID_START_SPEED)

    def test_increment_game_speed_faster_incomming_objet(self):
        obj_dist_1 = self.game.get_next_obstacle_info(0).distance
        self.game.update_environment()
        obj_dist_2 = self.game.get_next_obstacle_info(0).distance
        for _ in range(100):
            self.game.increment_game_speed()
        self.game.update_environment()
        obj_dist_3 = self.game.get_next_obstacle_info(0).distance

        dist_trav_1 = obj_dist_1 - obj_dist_2
        dist_trav_2 = obj_dist_2 - obj_dist_3
        self.assertGreater(dist_trav_2, dist_trav_1)

    #### Window Closed ####
    def test_window_close_open_success(self):
        try:
            self.game.window_closed()
        except:
            self.fail("Window close raised assertion")

    def test_window_close_detect_open(self):
        self.assertFalse(self.game.window_closed())

    #### Quit Game ####
    def test_quit_game(self):
        try:
            self.game.quit_game()
        except:
            self.fail("Quit game raised assertion")

    #### Get Dino Elevation ####
    def test_get_dino_elevation_invalid_type(self):
        with self.assertRaises(TypeError):
            self.game.get_dino_elevation("")

    def test_get_dino_elevation_success(self):
        try:
            self.game.get_dino_elevation(0)
        except:
            self.fail("Get dino elevation raised assertion")

    def test_get_dino_elevation_returns_correct_value(self):
        self.assertEqual(self.game.get_dino_elevation(0), 0)

    def test_get_dino_elevation_dino_out_of_range(self):
        with self.assertRaises(IndexError):
            self.game.get_dino_elevation(VALID_NUM_DINOS + 1)

    #### Get Dino Speed ####
    def test_get_dino_speed_success(self):
        try:
            self.game.get_game_speed()
        except:
            self.fail("Get dino speed raised assertion")

    #### Increment Score ####
    def test_get_dino_speed_success(self):
        try:
            self.game.increment_score()
        except:
            self.fail("Increment score raised assertion")

    #### Get Next Obstacle Info ####
    def test_get_next_obstacle_success(self):
        try:
            self.game.get_next_obstacle_info(0)
        except:
            self.fail("Increment score raised assertion")

    def test_get_next_obstacle_invalid_id_index_error(self):
        with self.assertRaises(IndexError):
            self.game.get_next_obstacle_info(VALID_NUM_DINOS)

    def test_get_next_osbstacle_wrong_type_arg(self):
        with self.assertRaises(TypeError):
            self.game.get_next_obstacle_info("")

    def test_get_next_obstacle_never_below_floor(self):

        for _ in range(100):

            game_instance = game.Game(
                VALID_NUM_DINOS, VALID_WIN_WIDTH, VALID_WIN_HEIGHT
            )
            next_object = game_instance.get_next_obstacle_info(0)

            self.assertGreaterEqual(next_object.elevation, 0)

    def test_get_next_obstacle_expected_output(self):
        try:
            obst = self.game.get_next_obstacle_info(0)
            dist = obst.distance
            elev = obst.elevation
            height = obst.height
            cac = obst.is_cactus
            width = obst.width
        except:
            self.fail("Unable to access expected output")

    def test_get_next_obstacle_differnent_obstacles(self):
        game_instance = game.Game(
            VALID_NUM_DINOS, VALID_WIN_WIDTH, VALID_WIN_HEIGHT, start_speed=300
        )
        is_cactus = game_instance.get_next_obstacle_info(0).is_cactus
        for _ in range(1000):
            game_instance.update_environment()
            if is_cactus is not game_instance.get_next_obstacle_info(0).is_cactus:
                return

        self.assertTrue(0, "Obstacles all of same type")

    #### Update Environment ####
    def test_update_environment_success(self):
        try:
            self.game.update_environment()
        except:
            self.fail("Update environment raised assertion")

    def test_update_environment_moves_obstacles(self):

        distance_start = self.game.get_next_obstacle_info(0).distance
        self.game.update_environment()
        distance_end = self.game.get_next_obstacle_info(0).distance

        self.assertLess(distance_end, distance_start)

    def test_update_environment_new_obstacles_generated(self):

        game_instance = game.Game(
            VALID_NUM_DINOS, VALID_WIN_WIDTH, VALID_WIN_HEIGHT, start_speed=50
        )
        num_obstacles = 0
        prev_dist = VALID_WIN_WIDTH * 2
        for _ in range(1000):
            game_instance.update_environment()
            cur_dist = game_instance.get_next_obstacle_info(0).distance
            if cur_dist > prev_dist:
                num_obstacles += 1
                prev_dist = VALID_WIN_WIDTH * 2

            prev_dist = cur_dist
            if num_obstacles >= 10:
                return

        self.assertTrue(0, "Less than 10 obstacles seen in 1000 high-speed iterations")

    #### Update Dino ####
    def test_dino_update_success(self):
        return

    #### Dino Jump ####
    def test_dino_jump_success(self):
        try:
            self.game.dino_jump(0)
        except:
            self.fail("Dino jump raised an assertion")

    def test_dino_jump_invalid_index(self):
        with self.assertRaises(IndexError):
            self.game.dino_jump(VALID_NUM_DINOS)

    def test_dino_jump_invalid_type(self):
        with self.assertRaises(TypeError):
            self.game.dino_jump("")

    def test_dino_jump_results_in_increased_dino_elevation(self):
        DINO_ID = 0
        self.game.dino_jump(DINO_ID)
        self.game.update_dino(DINO_ID)
        self.assertGreater(self.game.get_dino_elevation(DINO_ID), 0)

    def test_dino_jump_no_jump_from_other_dinos(self):
        DINO_ID = 0
        self.game.dino_jump(DINO_ID)
        self.game.update_dino(DINO_ID)
        self.assertEqual(self.game.get_dino_elevation(DINO_ID + 1), 0)

    #### Dino Duck ####
    def test_dino_duck_success(self):
        try:
            self.game.dino_duck(0)
        except:
            self.fail("Dino duck raised an assertion")

    def test_dino_duck_invalid_index(self):
        with self.assertRaises(IndexError):
            self.game.dino_duck(VALID_NUM_DINOS)

    def test_dino_duck_invalid_type(self):
        with self.assertRaises(TypeError):
            self.game.dino_duck("")

    #### Dino Object Collision ####
    def test_dino_collision_success(self):
        try:
            self.game.dino_object_collision(0)
        except:
            self.fail("Collision detection raised an assertion")

    def test_dino_object_collision_invalid_type(self):
        with self.assertRaises(TypeError):
            self.game.dino_object_collision("")

    def test_dino_object_collision_invalid_index(self):
        with self.assertRaises(IndexError):
            self.game.dino_object_collision(VALID_NUM_DINOS)

    def test_dino_collision_no_collision_on_init(self):
        self.assertFalse(self.game.dino_object_collision(0))

    def test_dino_collision_detected_on_game_update(self):
        ITERATIONS = 10000
        DINO_ID = 0
        for _ in range(0, ITERATIONS):
            self.game.update_environment()
            if self.game.dino_object_collision(DINO_ID):
                return

        self.assertTrue(0, "No collision within " + str(ITERATIONS) + " iterations")

    #### Draw Game ####
    def test_draw_game_success(self):
        try:
            self.game.draw_game()
        except:
            self.fail("Draw game raised assertion")

    def tearDown(self):
        self.game.quit_game()


if __name__ == "__main__":
    unittest.main()
