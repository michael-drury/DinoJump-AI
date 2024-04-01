import unittest
import dino_ai.assets as assets

# TODO: Should be able to remove settings
import dino_ai.settings as settings


class TestDino(unittest.TestCase):

    def setUp(self):
        self.dino = assets.Dino()

    #### Init ####
    def test_init_success(self):
        self.assertIsInstance(
            self.dino,
            assets.Dino,
            "Failed to initialise dino instance",
        )

    def test_init_no_elevation(self):
        self.assertEqual(self.dino.get_elevation(), 0)

    #### Jump ####
    def test_jump_success(self):
        try:
            self.dino.jump()
        except:
            self.fail("Jump raised assertion")

    def test_jump_invalid_type_arg(self):
        with self.assertRaises(TypeError):
            self.dino.jump(True)

    def test_jump_elevation_above_ground(self):
        self.dino.jump()
        self.dino.update()

        self.assertGreater(self.dino.get_elevation(), 0)

    def test_jump_dino_stops_at_floor_after_jump(self):
        # TODO: Calculate number of cycles using variables passed through to set up dino

        self.dino.jump()
        self.dino.update()

        num_cycles = 0
        while self.dino.get_elevation() > 0:
            self.dino.update()

            num_cycles += 1
            self.assertTrue(num_cycles < 100)

    # TODO: Pass in images to Dino on init for easier testing of what is jumping and what is running?
    # TODO: Is it bad practice to use private functions for testing?
    # TODO: The tests should be concerened without outward behaviour, not internal config, hence the argument
    # for not using internal functions - we shouldn't care about the internal workings!
    # This makes tests more brittle
    # Can lead to failing tests, even if the actual public API is behaving correctly
    # Focus on behaviour instead!

    # TODO: Set animation frame rate here so it's clear that the image won't animate??
    def test_jump_dino_image_changes_on_jump(self):

        run_img = self.dino.get_image()
        self.dino.jump()
        self.dino.update()
        jump_img = self.dino.get_image()
        self.assertNotEqual(run_img, jump_img)

    def test_xxxx_image_changes_if_duck_when_jumping(self):
        return

    def test_xxxx_image_changes_if_stop_ducking_when_jumping(self):
        return

    def test_duck_dino_jumps_if_duck_pressed_at_same_time(self):

        self.dino.jump()
        self.dino.duck()
        self.dino.update()

        self.assertTrue(self.dino.get_elevation() > 0)

    # TODO: Make sure jump has same test coverage as duck

    #### Duck ####
    def test_duck_success(self):
        try:
            self.dino.duck()
        except:
            self.fail("Duck raised assertion")

    def test_duck_invalid_type_arg(self):
        with self.assertRaises(TypeError):
            self.dino.duck(True)

    # TODO: This is an integration test or diving into the details of how the module works. Don't use this
    def test_duck_img_set(self):
        self.dino.duck()
        self.dino.update()
        # TODO: How can we check that this is the dino ducking image?
        self.dino.get_image()

    # def test_duck_stops_ducking_if_duck_not_called(self):
    # TODO: Check to see that the image used isn't the ducking image

    def test_duck_dino_image_changes_on_duck(self):
        run_img = self.dino.get_image()
        self.dino.duck()
        self.dino.update()
        duck_img = self.dino.get_image()

        self.assertNotEqual(run_img, duck_img)

    def test_duck_dino_image_changes_on_duck_release(self):
        self.dino.duck()
        self.dino.update()
        duck_img = self.dino.get_image()
        self.dino.update()
        run_img = self.dino.get_image()

        self.assertNotEqual(duck_img, run_img)

    def test_duck_dino_shorter_on_duck(self):
        run_height = self.dino.get_image().get_height()
        self.dino.duck()
        self.dino.update()
        duck_height = self.dino.get_image().get_height()

        self.assertGreater(run_height, duck_height)

    def test_duck_dino_returns_to_normal_height_on_duck_release(self):
        self.dino.duck()
        self.dino.update()
        duck_height = self.dino.get_image().get_height()
        self.dino.update()
        run_height = self.dino.get_image().get_height()

        self.assertGreater(run_height, duck_height)

    def test_duck_dino_jump_time_shorter_if_ducking(self):
        # NOTE: Ducking should increase gravity and result in a shorter jump

        self.dino.jump()
        self.dino.update()
        jump_frames_no_duck = 1
        while self.dino.get_elevation() > 0:
            self.dino.update()
            jump_frames_no_duck += 1

        self.dino.jump()
        self.dino.duck()
        self.dino.update()
        jump_frames_duck = 1
        while self.dino.get_elevation() > 0:
            self.dino.update()
            jump_frames_duck += 1

        self.assertGreater(jump_frames_no_duck, jump_frames_duck)

    #### Update ####
    def test_update_success(self):
        try:
            self.dino.update()
        except:
            self.fail("Update raised assertion")

    def test_update_jump_continues_on_hold(self):
        return

    def test_update_new_jump_if_still_held_on_floor_contact(self):
        return

    # TODO: Organise how/ where these tests are located. Seems like theres much crossover between tests

    #### Get img ####
    # TODO: Should this go first, before get_image has been tested?
    def test_get_image_success_no_input(self):
        try:
            self.dino.get_image()
        except:
            self.fail("Get image raised assertion")

    def test_get_image_success_duck(self):
        self.dino.duck()
        try:
            self.dino.get_image()
        except:
            self.fail("Get image raised an assertion after ducking")


    def test_get_image_success_jump(self):
        self.dino.jump()
        try:    
            self.dino.get_image()
        except:
            self.fail("Get image raised an assertion after jumping")


    def test_get_image_animates_on_no_input(self):
        start_img = self.dino.get_image()
        
        num_frames = 0
        while(self.dino.get_image() == start_img):
            self.dino.update()
            
            num_frames += 1
            # TODO: Have number of animation frames as an arg for dino class so this can be properly tested!
            self.assertTrue(num_frames < 100)

    def test_get_image_animates_on_duck(self):
        
        # TODO: Check elsewhere that .duck is used everytime .update is where necessary!
        self.dino.duck()
        self.dino.update()  
        start_img = self.dino.get_image()
        
        num_frames = 0
        while(self.dino.get_image() == start_img):
            self.dino.duck()
            self.dino.update()
            
            num_frames += 1
            # TODO: Have number of animation frames as an arg for dino class so this can be properly tested!
            self.assertTrue(num_frames < 100)
            
        
    def test_get_image_no_animate_while_jump(self):
        self.dino.jump()
        self.dino.update()  
        start_img = self.dino.get_image()

        while(self.dino.get_elevation() > 0):
            self.assertEqual(start_img, self.dino.get_image())
            self.dino.update()

    def test_get_image_no_animate_while_jump_and_duck(self):
        self.dino.jump()
        self.dino.duck()
        self.dino.update()  
        start_img = self.dino.get_image()

        while(self.dino.get_elevation() > 0):
            self.assertEqual(start_img, self.dino.get_image())
            self.dino.duck()
            self.dino.update()

    #### Get pos x ####
    def test_get_pos_x_success(self):
        try:    
            self.dino.get_img_pos_x()
        except:
            self.fail("Get image raised an assertion after jumping")
            
    def test_get_pos_x_valid_on_init(self):
        # TODO: Check x position is equal to an input when dino class init
        return

    #### Get pos y ####
    def test_get_pos_y_success(self):
        try:    
            self.dino.get_img_pos_y()
        except:
            self.fail("Get image raised an assertion after jumping")

    def test_get_pos_y_valid_on_init(self):
        # TODO: Check y position is equal to an input when dino class init
        # TODO; Use get_height from image and get_pos_y to determine if this is equal to starting input
        return