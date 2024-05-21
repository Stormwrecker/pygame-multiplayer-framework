import pygame

# image dictionary
image_dict = {}
color_list = ["Pink", "Blue", "Green", "Yellow", "Beige"]
for i, v in enumerate(color_list):
    image_dict[i] = pygame.image.load(f"images/alien{v}.png")

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, ID):
        pygame.sprite.Sprite.__init__(self)
        # set up variables
        self.ID = ID
        self.origin = (x, y)
        # image and rect
        self.image = image_dict[self.ID].convert_alpha()
        self.image.set_colorkey("#FFAEC9")
        self.rect = self.image.get_rect()
        self.rect.topleft = self.origin
        # other variables
        self.speed = 5
        self.is_active = True
        self.frame_index = 0
        self.x = x
        self.y = y

    def update(self):
        # get keys
        keys = pygame.key.get_pressed()

        # key presses
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed

        # update position
        self.rect.topleft = [self.x, self.y]

    def draw(self, win):
        # draw image
        win.blit(self.image, self.rect)
