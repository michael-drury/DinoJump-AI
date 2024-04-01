

GAME_TITLE = "Dino AI"

# TODO: ADD UNITS!

#### Window Size ####
WIN_WIDTH = 1200 # PX??
WIN_HEIGHT = 400 # PX??

#### Game Speed ####
FRAME_RATE = 60 # FPS
FRAMES_PER_IMAGE_ANIMATE = (
    FRAME_RATE / 10
)  

#### Environment ####
ENV_FLOOR_HEIGHT = 350 # PX? Which coordinate system?
ENV_NUM_DIRT_PIECES = 20 # PX?

#### Dino Sprites ####

# TODO: Don't use velocity/ speed interchangeably 
DINO_JUMP_VELOCITY = 100
DINO_INITIAL_SPEED = 8
DINO_SPEED_INCREMENT = 0.03
