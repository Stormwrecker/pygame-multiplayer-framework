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

# in case of server-setup failure
def clean_up_fail(msg=None, net=None):
    if msg is not None:
        print("Failed to connect to server:", msg)
    else:
        print("Failed to connect to server")
    player = Player(100, 100, 0)
    server_working = False
    if net is not None:
        net.client.close()
    return player, server_working

# set up player and network
server_working = False
try:
    net = Network()
    p = net.getP()
    if type(p) == dict:
        player = Player(p["x"], p["y"], p["ID"])
        p["active"] = player.is_active
        fake_id = p["ID"] + 1
        pygame.display.set_caption(f"Player {fake_id}")
        print(f"Connected: You are Player {fake_id}")
        server_working = True
    else:
        player, server_working = clean_up_fail(p, net)
except:
    player, server_working = clean_up_fail(p)

# our list that will contain other players
other_players = {}

# our game loop
run = True
while run:
    # make our clock run and screen white
    clock.tick(60)
    screen.fill((100, 100, 150))

    # get other players
    player_data = {"ID":player.ID, "x":player.rect.x, "y":player.rect.y, "active":player.is_active}
    if server_working:
        recv_player_data = net.trade(player_data)
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
            if server_working:
                # send final info to server
                recv_player_data = net.trade(player_data)
                recv_player_data = net.trade(player_data["ID"])
                net.client.close()

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
