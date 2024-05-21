This code is adapted from a series that TechWithTim made, but I made it expanable and can have up to any number of clients. So far, this framework has proved to be pretty indestructible. It runs on the TCP protocol using socket (I tried UDP, but it's proven unreliable for me, and everyone online also discourages the use of UDP). The only error you will encounter is if you try to open too many clients. Hopefully, it's generic enough to implement it in whatever Pygame project you have.

Below is a preview of 5 clients interacting with each other:

![image](https://github.com/Stormwrecker/pygame-multiplayer-framework/assets/109243857/c5070339-9132-49b8-9356-62c9464ee821)
Cool, right?

Dependencies:
Pygame 2
