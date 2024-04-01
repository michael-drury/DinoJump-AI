import unittest
import dino_ai.render as render
import pygame
import tests.test_common as test_common

# Leaning on Pygame for error catching to reduce size of code base so don't want to mock

class TestRender(unittest.TestCase):

    def setUp(self):
        test_common.block_display_render()
        self.title = "Test Title"
        self.width = 100
        self.height = 100
        self.floor_height = 10
        self.render = self.render = render.Render(
            self.title, self.width, self.height, self.floor_height
        )

    #### Initialise #####
    def test_init_success(self):
        self.assertIsInstance(
            self.render,
            render.Render,
            "Failed to initialise render instance",
        )

    def test_init_missing_arg(self):
        with self.assertRaises(TypeError):
            render.Render()

    def test_init_negative_height(self):
        with self.assertRaises(pygame.error):
            render.Render(self.title, self.width, -1, self.floor_height)

    def test_init_negative_width(self):
        with self.assertRaises(pygame.error):
            render.Render(self.title, -1, self.height, self.floor_height)

    def test_invalid_title_type(self):
        with self.assertRaises(TypeError):
            render.Render(0, self.width, self.height, self.floor_height)

    def test_empty_title_arg(self):
        with self.assertRaises(ValueError):
            render.Render("", self.width, self.height, self.floor_height)

    #### Display Score ####
    def test_display_score_success(self):
        try:
            self.render.display_score(1)
        except:
            self.fail("Display score raised an exception")

    def test_display_score_no_arg(self):
        with self.assertRaises(TypeError):
            self.render.display_score()

    def test_display_score_invalid_type(self):
        with self.assertRaises(TypeError):
            self.render.display_score("")

    #### Display Generation ####
    def test_display_generation_success(self):
        try:
            self.render.display_generation(1)
        except:
            self.fail("Display generation raised an exception")

    def test_display_generation_no_arg(self):
        with self.assertRaises(TypeError):
            self.render.display_generation()

    def test_display_score_invalid_type(self):
        with self.assertRaises(TypeError):
            self.render.display_generation("")

    #### Display Floor ####
    def test_display_floor_success(self):
        try:
            self.render.display_floor()
        except:
            self.fail("Display floor raised an exception")

    #### Draw Img ####
    def test_draw_img_success(self):
        test_img = pygame.image.load(os.path.join("images", "dino_jump.png"))
        try:
            self.render.draw_img(test_img, 0, 0)
        except:
            self.fail("Draw image raised an exception")

    def test_draw_img_no_args(self):
        with self.assertRaises(TypeError):
            self.render.draw_img()

    def test_display_score_invalid_type(self):
        with self.assertRaises(TypeError):
            self.render.draw_img("FILE", 0, 0)

    #### Close Window ####
    def test_close_window_success(self):
        try:
            self.render.close_window()
        except:
            self.fail("Close window raised an exception")

    #### Set Background White ####
    def test_set_background_white_success(self):
        try:
            self.render.set_background_white()
        except:
            self.fail("Set background white raised an exception")

    #### Update Display ####
    def test_update_display_success(self):
        try:
            self.render.update_display()
        except:
            self.fail("Update display raised an exception")


if __name__ == "__main__":
    unittest.main()
