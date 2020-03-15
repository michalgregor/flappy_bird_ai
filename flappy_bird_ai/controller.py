import time
from . import PLAYER_SHAPE, PIPE_SHAPE

class BaseController:
    def __init__(self, action_delay=200):
        self.action_delay = action_delay / 1000   
        self.last_action_time = -action_delay

    def choose_action(self, *args):
        """
        Arguments: determined by preproc.
        Returns: A boolean value that expressed whether to flap or not.
        """
        raise NotImplementedError()        

    def preproc(self, bird, upperPipes, lowerPipes):
        """
        Preprocesses the input into:
            velocity: The vertical component of the bird's velocity.
            dist_horiz: The horizontal distance between the center of the gap
                        and the center of the bird.
            dist_verti: The vertical distance between the center of the gap
                        and the center of the bird.
        """
        playerw, playerh = PLAYER_SHAPE
        player_centerx = bird.playerx + playerw / 2
        player_centery = bird.playery + playerh / 2
        pipeW, pipeH = PIPE_SHAPE

        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            assert(uPipe['x'] == lPipe['x'])

            if bird.playerx > uPipe['x'] + pipeW:
                continue

            pipe_centerx = uPipe['x'] + pipeW / 2
            pipe_gap = lPipe['y'] - uPipe['y'] - pipeH
            pipe_centery = uPipe['y'] + pipeH + pipe_gap / 2

            break

        velocity = bird.playerVelY
        dist_horiz = pipe_centerx - player_centerx
        dist_verti = pipe_centery - player_centery

        return velocity, dist_horiz, dist_verti

    def __call__(self, bird, upperPipes, lowerPipes):
        playerFlapped = False

        if time.time() - self.last_action_time >= self.action_delay:
            args = self.preproc(bird, upperPipes, lowerPipes)            
            playerFlapped = self.choose_action(*args)
            self.last_action_time = time.time()

        return playerFlapped

class RandomController(BaseController):
    def preproc(self, *args):
        return []

    def choose_action(self, *args):
        return random.randint(0, 1)

