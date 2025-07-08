import pygame
from game import Game

def main():
    pygame.init()
    okno = pygame.display.set_mode((500, 600))
    pygame.display.set_caption("2048")
    zegar = pygame.time.Clock()
    gra = Game(okno)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                gra.przetworz_zdarzenie(event)

        gra.aktualizuj()
        gra.rysuj()
        pygame.display.flip()
        zegar.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()