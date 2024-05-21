import pygame
from network import Network
from player import Player

# initialize pygame and other related stuff
pygame.init()

# set up our window and the clock
width = 500
height = 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")
clock = pygame.time.Clock()

# set up player and network
net = Network()
p = net.getP()
player = Player(p["x"], p["y"], p["ID"])
p["active"] = player.is_active

# our list that will contain other players
other_players = {}

# our game loop
run = True
while run:
    # make our clock run and screen white
    clock.tick(60)
    screen.fill((255, 255, 255))

    # get other players
    player_data = {"ID":player.ID, "x":player.rect.x, "y":player.rect.y, "active":player.is_active}
    recv_player_data = net.send(player_data)
    for key, value in recv_player_data.items():
        if key != player.ID:
            if key not in other_players:
                if value["active"]:
                    other_players[key] = Player(value["x"], value["y"], value["ID"])
            else:
                # update the values
                if value["active"]:
                    other_players[key].rect.x = value["x"]
                    other_players[key].rect.y = value["y"]

    # Remove disconnected players from other_players
    disconnected_players = [key for key in other_players.keys() if key not in recv_player_data]
    for key in disconnected_players:
        del other_players[key]

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            # remove player
            player_data = {"ID": player.ID, "x": player.x, "y": player.y,
                           "active": False}
            player.kill()
            # send final info to server
            recv_player_data = net.send(player_data)
            recv_player_data = net.send(player_data["ID"])

    # draw and update other players
    for p in other_players.values():
        p.draw(screen)
        p.update()

    # update our own player
    player.update()
    player.draw(screen)

    # update screen
    pygame.display.flip()

# quit
pygame.quit()
