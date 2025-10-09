import pygame

class GameUI:
    def __init__(self,):
        pygame.init()
        self.WIDTH, self.HEIGHT = 600, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Caro")
        self.clock = pygame.time.Clock()

        self.state = "menu"
        self.game = None