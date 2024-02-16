import pygame
from network import Network
from player import Player

pygame.init()

width = 500
height = 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

other_players = []
net = Network()
p = net.getP()
p.is_active = True

clock = pygame.time.Clock()
run = True
while run:
    clock.tick(60)
    screen.fill((255, 255, 255))

    other_players = net.send(p)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            p.is_active = False
            p.x, p.y = p.origin
            other_players = net.send(p)
            other_players = net.send(p.ID)

    p.move()
    p.draw(screen)
    if other_players is not None:
        for i in other_players:
            i.draw(screen)
    pygame.display.flip()

pygame.quit()
