import unittest
import time
import dino_ai.game as game
import tests.test_common as test_common

VALID_NUM_DINOS = 3
VALID_WIN_WIDTH = 1200
VALID_WIN_HEIGHT = 400
VALID_START_SPEED = 8
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
            game.Game(
                VALID_NUM_DINOS, VALID_WIN_WIDTH, VALID_WIN_HEIGHT, frame_rate=""
            )

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
        expected_delay = 1/VALID_FRAME_RATE
        
        self.assertAlmostEqual(duration, expected_delay, delta=0.05)

    # #### Increment Dino Speed ####
    def test_increment_game_speed(self):
        try:
            self.game.increment_game_speed()
        except:
            self.fail("Increment dino speed raised assertion")

        self.assertGreater(self.game.get_game_speed(), VALID_START_SPEED)

    # #### Window Closed ####
    def test_window_close_open_success(self):
        try:
            self.game.window_closed()
        except:
            self.fail("Window close raised assertion")

    def test_window_close_detect_open(self):
        self.assertFalse(self.game.window_closed())
        
    # TODO: Simulate window open

    # #### Quit Game ####
    def test_quit_game(self):
        try:
            self.game.quit_game()
        except:
            self.fail("Quit game raised assertion")

    # #### Get Dino Elevation ####
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
            
    def test_get_next_osbstacle_wrong_type_arg(self):
        with self.assertRaises(TypeError):
            self.game.get_next_obstacle_info("")
        
    # TODO: Check obstacle output params

    #### Update Environment ####
    
    #### Dino Jump ####
    
    #### Dino Duck ####
    
    #### Update Dino Position ####
    
    #### Dino Object Collision ####
    
    #### Draw Game ####


    def tearDown(self):
        self.game.quit_game()


if __name__ == "__main__":
    unittest.main()
