This code is adapted from a series that TechWithTim made, but I made it expandable and can have up to any number of clients. So far, this framework has proved to be pretty indestructible and is pretty much fool-proof. It runs on the TCP protocol using socket and _thread (I tried UDP, but it's proven unreliable for me, and everyone online also discourages the use of UDP). Hopefully, it's generic enough to implement it in whatever Pygame project you have.

To run:
Simply run server.py in your IDE then open up command prompts (or terminals) in the same directory and type in this command: 'python client.py' and hit enter.

To change max amount of players:
You can change max amount of players by simply modifying the MAX_PLAYERS variable in server.py and modifying the section of code in player.py just above the Player class.

Below is a preview of 5 clients interacting with each other:

![image](https://github.com/Stormwrecker/pygame-multiplayer-framework/assets/109243857/c5070339-9132-49b8-9356-62c9464ee821)

Cool, right?

Dependencies:
Pygame 2
