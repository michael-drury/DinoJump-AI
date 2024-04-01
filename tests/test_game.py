import unittest
import dino_ai.game as game
import tests.test_common as test_common

# TODO: Game class should have settings inputs as args?
import dino_ai.settings as settings


class TestGame(unittest.TestCase):

    def setUp(self):
        test_common.block_display_render()
        self.num_dinos = 3
        self.game = game.Game(self.num_dinos)

    #### Init ####
    def test_init_success(self):
        self.assertIsInstance(
            self.game, game.Game, "Failed to initialize Game instance."
        )

    def test_init_invalid_arg_type(self):
        with self.assertRaises(TypeError):
            game.Game("")

    def test_init_no_arg(self):
        with self.assertRaises(TypeError):
            game.Game()

    def test_init_no_dinos(self):
        with self.assertRaises(ValueError):
            game.Game(0)

    #### Restrict Game Loop Speed ####
    # TODO: This is only checking that method doesn't fail and wouldn't pass TDD
    # TODO: Add a timer here to check that game loop speed has been correctly restricted!
    def test_restrict_game_loop_speed_success(self):
        try:
            self.game.restrict_game_loop_speed()
        except:
            self.fail("Restrict game loop speed raised assertion")

    #### Increment Dino Speed ####
    def test_increment_dino_speed(self):
        try:
            self.game.increment_dino_speed()
        except:
            self.fail("Increment dino speed raised assertion")

        self.assertGreater(self.game.dino_speed, settings.DINO_INITIAL_SPEED)

    #### Window Closed ####
    def test_window_close_open_success(self):
        try:
            self.game.window_closed()
        except:
            self.fail("Window close raised assertion")

    def test_window_close_detect_open(self):
        self.assertFalse(self.game.window_closed())

    # TODO: Sim window close?

    #### Quit Game ####
    def test_get_dino_elevation_success(self):
        try:
            self.game.quit_game()
        except:
            self.fail("Quit game raised assertion")

    #### Get Dino Elevation ####
    def test_get_dino_elevation_success(self):
        try:
            self.game.get_dino_elevation(0)
        except:
            self.fail("Get dino elevation raised assertion")

    # def test_get_dino_elevation_returns_correct_value(self):
    #     self.assertEqual(self.game.get_dino_elevation(0), settings.ENV_FLOOR_HEIGHT)

    def tearDown(self):
        self.game.quit_game()


if __name__ == "__main__":
    unittest.main()
