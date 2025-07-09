import pygame
from game import Game

def main():
    pygame.init()
    window = pygame.display.set_mode((500, 600))
    pygame.display.set_caption("2048")
    clock = pygame.time.Clock()
    game = Game(window)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                game.process_event(event)  

        game.update()
        game.draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()