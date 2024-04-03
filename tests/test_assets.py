import unittest
import math
import dino_ai.assets as assets

POS_X_START = 0
POS_Y_START = 0
FPS = 60
FRAMES_PER_IMAGE_ANIMATE = 10
GRAVITY_NORMAL = -10
GRAVITY_DUCKING = -15
JUMP_INITIAL_VELOCITY = 15

# TODO: Can have these here as defaults to use that are valid. Refactor?
# TODO: Use same strat for dino
VALID_START_X = 0
VALID_MIN_Y = 0
VALID_MAX_Y = 100
VALID_MIN_RAD = 1
VALID_MAX_RAD = 4
VALID_FLOOR_Y = 10


# TODO: Need to consider that a pixel is effectively counting as a meter here?
# Have some kind of scaling tool?
class TestDino(unittest.TestCase):

    # TODO: Remove setup and move to individual test cases so it's clear what arguments are adjusted for that specific test case
    def setUp(self):
        self.dino = assets.Dino(
            POS_X_START,
            POS_Y_START,
            fps=FPS,
            frames_per_img_animate=FRAMES_PER_IMAGE_ANIMATE,
            gravity_normal=GRAVITY_NORMAL,
            gravity_ducking=GRAVITY_DUCKING,
            jump_initial_velocity=JUMP_INITIAL_VELOCITY,
        )

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

    def test_jump_visible_on_default_settings(self):
        self.dino.jump()
        self.dino.update()

        num_frames = 0
        while self.dino.get_elevation() > 0:
            self.dino.update()
            num_frames += 1

        self.assertTrue(num_frames > 2)

    def test_jump_elevation_above_ground(self):
        self.dino.jump()
        self.dino.update()

        self.assertGreater(self.dino.get_elevation(), 0)

    def test_jump_dino_stops_at_floor_after_jump(self):
        jump_time = (2 * JUMP_INITIAL_VELOCITY) / -GRAVITY_NORMAL
        jump_frames = math.ceil(FPS * jump_time)

        self.dino.jump()

        for _frame in range(0, jump_frames):
            self.dino.update()

        self.assertTrue(self.dino.get_elevation() == 0)

    def test_jump_dino_image_changes_on_jump(self):
        run_img = self.dino.get_image()
        self.dino.jump()
        self.dino.update()
        jump_img = self.dino.get_image()
        self.assertNotEqual(run_img, jump_img)

    def test_jump_image_changes_if_duck_when_jumping(self):
        self.dino.jump()
        self.dino.update()
        jump_img = self.dino.get_image()
        self.dino.duck()
        self.dino.update()
        jump_duck_img = self.dino.get_image()

        self.assertNotEqual(jump_img, jump_duck_img)

    def test_jump_image_changes_if_stop_ducking_when_jumping(self):
        self.dino.jump()
        self.dino.duck()
        self.dino.update()
        jump_duck_img = self.dino.get_image()
        self.dino.update()
        jump_img = self.dino.get_image()

        self.assertNotEqual(jump_img, jump_duck_img)

    def test_jump_dino_jumps_if_duck_pressed_at_same_time(self):
        self.dino.jump()
        self.dino.duck()
        self.dino.update()

        self.assertTrue(self.dino.get_elevation() > 0)

    def test_update_no_jump_reset_on_jump_hold(self):
        self.dino.jump()
        self.dino.update()

        elevation_1 = self.dino.get_elevation()

        self.dino.jump()
        self.dino.update()

        elevation_2 = self.dino.get_elevation()

        self.assertGreater(elevation_2, elevation_1)

    def test_update_new_jump_if_still_held_on_floor_contact(self):
        self.dino.jump()
        self.dino.update()

        while self.dino.get_elevation() > 0:
            self.dino.jump()
            self.dino.update()

        self.dino.jump()
        self.dino.update()
        self.assertTrue(self.dino.get_elevation() > 0)

    #### Duck ####
    def test_duck_success(self):
        try:
            self.dino.duck()
        except:
            self.fail("Duck raised assertion")

    def test_duck_invalid_type_arg(self):
        with self.assertRaises(TypeError):
            self.dino.duck(True)

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
            self.dino.duck()
            self.dino.update()
            jump_frames_duck += 1

        self.assertGreater(jump_frames_no_duck, jump_frames_duck)

    #### Update ####
    def test_update_success(self):
        try:
            self.dino.update()
        except:
            self.fail("Update raised assertion")

    def test_update_animate_after_exact_frame_num(self):
        # TODO: Do this
        return

    #### Get img ####
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

    def test_get_image_animates_on_run(self):
        dino = assets.Dino(0, 0, fps=1, frames_per_img_animate=1)
        start_img = dino.get_image()
        dino.update()
        end_img = dino.get_image()

        self.assertNotEqual(start_img, end_img)

    def test_get_image_animates_on_duck(self):
        dino = assets.Dino(0, 0, fps=1, frames_per_img_animate=1)

        dino.duck()
        dino.update()
        start_img = dino.get_image()
        dino.duck()
        dino.update()
        end_img = dino.get_image()

        self.assertNotEqual(start_img, end_img)

    def test_get_image_no_animate_while_jump(self):
        dino = assets.Dino(0, 0, fps=1, frames_per_img_animate=1)

        dino.jump()
        dino.update()
        start_img = dino.get_image()
        dino.jump()
        dino.update()
        end_img = dino.get_image()

        self.assertEqual(start_img, end_img)

    def test_get_image_no_animate_while_jump_and_duck(self):
        dino = assets.Dino(0, 0, fps=1, frames_per_img_animate=1)

        dino.jump()
        dino.duck()
        dino.update()
        start_img = dino.get_image()
        dino.duck()
        dino.update()
        end_img = dino.get_image()

        self.assertEqual(start_img, end_img)

    #### Get pos x ####
    def test_get_pos_x_success(self):
        try:
            self.dino.get_image_pos_x()
        except:
            self.fail("Get image raised an assertion after jumping")

    def test_get_pos_x_valid_on_init(self):
        self.assertEqual(POS_X_START, self.dino.get_image_pos_x())

    #### Get pos y ####
    def test_get_pos_y_success(self):
        try:
            self.dino.get_image_pos_y()
        except:
            self.fail("Get image raised an assertion after jumping")

    def test_get_pos_y_valid_on_init(self):
        start_y = self.dino.get_image_pos_y() + self.dino.get_image().get_height()
        self.assertTrue(start_y == POS_Y_START)


class TestBird(unittest.TestCase):

    def test_invalid_fps_type(self):
        with self.assertRaises(TypeError):
            assets.Bird(VALID_START_X, VALID_MIN_Y, VALID_MAX_Y, fps="100")

    def test_invalid_start_x_type(self):
        with self.assertRaises(TypeError):
            assets.Bird("1", VALID_MIN_Y, VALID_MAX_Y)

    def test_invalid_frames_per_image_type(self):
        with self.assertRaises(TypeError):
            assets.Bird(
                VALID_START_X, VALID_MIN_Y, VALID_MAX_Y, frames_per_img_animate="1"
            )

    def test_invalid_min_y_type(self):
        with self.assertRaises(TypeError):
            assets.Bird(VALID_START_X, "1", VALID_MAX_Y)

    def test_invalid_max_y_type(self):
        with self.assertRaises(TypeError):
            assets.Bird(VALID_START_X, VALID_MIN_Y, "1")

    def test_max_less_than_min(self):
        with self.assertRaises(ValueError):
            assets.Bird(VALID_START_X, 2, 1)

    def test_invalid_game_speed(self):
        with self.assertRaises(TypeError):
            assets.Bird(VALID_START_X, VALID_MIN_Y, VALID_MAX_Y, game_speed="1")

    def test_object_create_success(self):
        self.assertIsInstance(
            assets.Bird(VALID_START_X, VALID_MIN_Y, VALID_MAX_Y),
            assets.Bird,
            "Failed to initialise bird instance",
        )

    def test_get_image_pos_y_within_bounds(self):
        min_y = 50
        max_y = 97
        for bird in range(0, 100):
            bird = assets.Bird(VALID_START_X, min_y, max_y)
            self.assertGreaterEqual(max_y, bird.get_image_pos_y())
            self.assertLessEqual(min_y, bird.get_image_pos_y())

    def test_image_position_randomly_changes_within_range(self):
        min_y = 50
        max_y = 97
        bird = assets.Bird(VALID_START_X, min_y, max_y)
        bird_y = bird.get_image_pos_y()

        for bird in range(0, 100):
            bird = assets.Bird(0, min_y, max_y)
            if bird.get_image_pos_y() != bird_y:
                return

        self.assertTrue(0, "No variance in bird y position detected")

    def test_animates_on_update(self):
        bird = assets.Bird(
            VALID_START_X, VALID_MIN_Y, VALID_MAX_Y, frames_per_img_animate=1
        )
        start_image = bird.get_image()
        bird.update()
        next_frame_image = bird.get_image()

        self.assertNotEqual(start_image, next_frame_image)

    def test_moves_expected_distance_on_update(self):
        game_speed = 10
        frame_rate = 10
        bird = assets.Bird(VALID_START_X, 0, 10, game_speed, frame_rate)
        bird.update()
        distance_traveled = VALID_START_X - bird.get_image_pos_x()
        expected_distanced_traveled = game_speed / frame_rate

        self.assertEqual(distance_traveled, expected_distanced_traveled)

    def test_double_game_speed_equals_double_distance_traveled(self):
        game_speed = 10
        frame_rate = 10
        bird = assets.Bird(VALID_START_X, 0, 10, game_speed, frame_rate)
        bird.update()
        bird_pos_1 = bird.get_image_pos_x()
        distance_traveled_1 = VALID_START_X - bird_pos_1
        bird.set_game_speed(game_speed * 2)
        bird.update()
        distance_traveled_2 = bird_pos_1 - bird.get_image_pos_x()
        self.assertEqual(distance_traveled_1 * 2, distance_traveled_2)


class TestDirt(unittest.TestCase):

    def test_invalid_fps_type(self):
        with self.assertRaises(TypeError):
            assets.Dirt(VALID_START_X, VALID_MIN_Y, VALID_MAX_Y, fps="100")

    def test_invalid_start_x_type(self):
        with self.assertRaises(TypeError):
            assets.Dirt("1", VALID_MIN_Y, VALID_MAX_Y)

    def test_invalid_frames_per_image_type(self):
        with self.assertRaises(TypeError):
            assets.Dirt(
                VALID_START_X, VALID_MIN_Y, VALID_MAX_Y, frames_per_img_animate="1"
            )

    def test_invalid_min_y_type(self):
        with self.assertRaises(TypeError):
            assets.Dirt(VALID_START_X, "1", VALID_MAX_Y)

    def test_invalid_max_y_type(self):
        with self.assertRaises(TypeError):
            assets.Dirt(VALID_START_X, VALID_MIN_Y, "1")

    def test_max_less_than_min(self):
        with self.assertRaises(ValueError):
            assets.Dirt(VALID_START_X, 2, 1)

    def test_invalid_game_speed(self):
        with self.assertRaises(TypeError):
            assets.Dirt(VALID_START_X, VALID_MIN_Y, VALID_MAX_Y, game_speed="1")

    def test_object_create_success(self):
        self.assertIsInstance(
            assets.Dirt(VALID_START_X, VALID_MIN_Y, VALID_MAX_Y),
            assets.Dirt,
            "Failed to initialise dirt instance",
        )

    def test_image_position_randomly_changes_within_range(self):
        min_y = 50
        max_y = 97
        dirt = assets.Dirt(VALID_START_X, min_y, max_y)
        dirt_y = dirt.get_image_pos_y()

        for dirt in range(0, 100):
            dirt = assets.Dirt(VALID_START_X, min_y, max_y)
            if dirt.get_image_pos_y() != dirt_y:
                return

        self.assertTrue(0, "No variance in dirt y position detected")

    def test_size_randomly_changes(self):
        dirt = assets.Dirt(VALID_START_X, VALID_MIN_Y, VALID_MAX_Y)
        dirt_rad = dirt.get_radius()

        for dirt in range(0, 100):
            dirt = assets.Dirt(VALID_START_X, VALID_MIN_Y, VALID_MAX_Y)
            if dirt.get_radius() != dirt_rad:
                return

        self.assertTrue(0, "No variance in dirt radius detected")

    def test_dirt_radius_within_bounds(self):
        min_rad = 2
        max_rad = 5
        for dirt in range(0, 100):
            dirt = assets.Dirt(
                VALID_START_X,
                VALID_MIN_Y,
                VALID_MAX_Y,
                min_rad=min_rad,
                max_rad=max_rad,
            )
            rad = dirt.get_radius()
            self.assertGreaterEqual(rad, min_rad)
            self.assertLessEqual(rad, max_rad)

    def test_moves_expected_distance_on_update(self):
        game_speed = 10
        frame_rate = 10
        dirt = assets.Dirt(
            VALID_START_X,
            VALID_MIN_Y,
            VALID_MAX_Y,
            game_speed=game_speed,
            fps=frame_rate,
        )
        dirt.update()
        distance_traveled = VALID_START_X - dirt.get_image_pos_x()
        expected_distanced_traveled = game_speed / frame_rate

        self.assertEqual(distance_traveled, expected_distanced_traveled)

    def test_double_game_speed_equals_double_distance_traveled(self):
        game_speed = 10
        frame_rate = 10
        dirt = assets.Dirt(
            VALID_START_X, VALID_MIN_Y, VALID_MAX_Y, game_speed, frame_rate
        )
        dirt.update()
        dirt_pos_1 = dirt.get_image_pos_x()
        distance_traveled_1 = VALID_START_X - dirt_pos_1
        dirt.set_game_speed(game_speed * 2)
        dirt.update()
        distance_traveled_2 = dirt_pos_1 - dirt.get_image_pos_x()

        self.assertEqual(distance_traveled_1 * 2, distance_traveled_2)

    def test_get_dirt_image_raises_error(self):
        dirt = assets.Dirt(VALID_START_X, VALID_MIN_Y, VALID_MAX_Y)
        with self.assertRaises(NotImplementedError):
            dirt.get_image()


class TestCactus(unittest.TestCase):

    def test_error_on_invalid_cacuts_size(self):
        with self.assertRaises(ValueError):
            assets.Cactus(VALID_START_X, VALID_FLOOR_Y, cactus_size=4)

    def test_invalid_cactus_size_type(self):
        with self.assertRaises(TypeError):
            assets.Cactus(VALID_START_X, VALID_FLOOR_Y, cactus_size="4")

    def test_invalid_fps_type(self):
        with self.assertRaises(TypeError):
            assets.Cactus(VALID_START_X, VALID_FLOOR_Y, fps="100")

    def test_invalid_start_x_type(self):
        with self.assertRaises(TypeError):
            assets.Cactus("1", VALID_FLOOR_Y)

    def test_invalid_frames_per_image_type(self):
        with self.assertRaises(TypeError):
            assets.Cactus(VALID_START_X, VALID_FLOOR_Y, frames_per_img_animate="1")

    def test_floor_y_type(self):
        with self.assertRaises(TypeError):
            assets.Cactus(VALID_START_X, "1")

    def test_invalid_game_speed(self):
        with self.assertRaises(TypeError):
            assets.Cactus(VALID_START_X, VALID_FLOOR_Y, game_speed="1")

    def test_object_create_success(self):
        self.assertIsInstance(
            assets.Cactus(VALID_START_X, VALID_FLOOR_Y),
            assets.Cactus,
            "Failed to initialise bird instance",
        )

    def test_setting_different_cactus_size_gives_different_image(self):
        cactus_img_0 = assets.Cactus(
            VALID_START_X, VALID_FLOOR_Y, cactus_size=0
        ).get_image()
        cactus_img_1 = assets.Cactus(
            VALID_START_X, VALID_FLOOR_Y, cactus_size=1
        ).get_image()

        self.assertNotEqual(cactus_img_0, cactus_img_1)

    def test_moves_expected_distance_on_update(self):
        game_speed = 10
        frame_rate = 10
        cactus = assets.Cactus(VALID_START_X, VALID_FLOOR_Y, game_speed, frame_rate)
        cactus.update()
        distance_traveled = VALID_START_X - cactus.get_image_pos_x()
        expected_distanced_traveled = game_speed / frame_rate

        self.assertEqual(distance_traveled, expected_distanced_traveled)

    def test_double_game_speed_equals_double_distance_traveled(self):
        game_speed = 10
        frame_rate = 10
        cactus = assets.Cactus(VALID_START_X, VALID_FLOOR_Y, game_speed, frame_rate)
        cactus.update()
        cactus_pos_1 = cactus.get_image_pos_x()
        distance_traveled_1 = VALID_START_X - cactus_pos_1
        cactus.set_game_speed(game_speed * 2)
        cactus.update()
        distance_traveled_2 = cactus_pos_1 - cactus.get_image_pos_x()
        self.assertEqual(distance_traveled_1 * 2, distance_traveled_2)

    def test_pos_y_as_expected(self):
        cactus = assets.Cactus(VALID_START_X, VALID_FLOOR_Y)
        self.assertEqual(
            VALID_FLOOR_Y - cactus.get_image().get_height(), cactus.get_image_pos_y()
        )
