import pygame
import math


class Player():
    def __init__(self, x, y, d, foodposx, foodposy, col):
        self.position = [x, y]
        self.body = [[100, 50]]
        self.direction = "stop"
        self.vel = 10
        self.life_status = "alive"
        self.id = d
        self.foodx = foodposx
        self.foody = foodposy
        self.eatenfood = False
        self.playerkilled=-1
        self.color=col

    def draw(self, win):
        for pos in self.body:
            pygame.draw.rect(win, self.color, (pos[0], pos[1], 10, 10))
        pygame.draw.rect(win, (225, 0, 0), (self.foodx, self.foody, 10, 10))

    def changedir(self, dir):
        if self.direction != "left" and dir == "right":
            self.direction = dir
        if self.direction != "right" and dir == "left":
            self.direction = dir
        if self.direction != "up" and dir == "down":
            self.direction = dir
        if self.direction != "down" and dir == "up":
            self.direction = dir

    def gameover(self):
        self.life_status = "dead"

    def keymove(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gameover()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.changedir("up")
                elif event.key == pygame.K_DOWN:
                    self.changedir("down")
                elif event.key == pygame.K_RIGHT:
                    self.changedir("right")
                elif event.key == pygame.K_LEFT:
                    self.changedir("left")

    def move(self):
        if self.direction == "right":
            self.position[0] += 10
        elif self.direction == "left":
            self.position[0] -= 10
        elif self.direction == "up":
            self.position[1] -= 10
        elif self.direction == "down":
            self.position[1] += 10
        self.update()

    def snakecollision(self, p2):
        for player in p2:
            if player.life_status == "alive":
                for part in player.body[1:]:
                    if math.hypot(self.position[0] - part[0], self.position[1] - part[1]) < 10:
                        self.playerkilled = player.id
                if math.hypot(self.position[0] - player.position[0], self.position[1] - player.position[1]) < 10:
                    self.life_status = "dead"
                    self.playerkilled = player.id

    def update(self):
        self.body.insert(0, list(self.position))
        if math.hypot(self.position[0] - self.foodx, self.position[1] - self.foody) < 10:
            self.eatenfood = True
        else:
            self.body.pop()

    def check_collision(self):
        if self.position[0] > 490 or self.position[0] < 0:
            return True
        elif self.position[1] > 490 or self.position[1] < 0:
            return True
        for bodypart in self.body[3:]:
            if self.position == bodypart:
                return True
        return 0

