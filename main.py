import pickle
import numpy
import pygame
import math
from rays import get_rays

with open('map.pkl', 'rb') as f:
    card = pickle.load(f)

n, m = len(card)*50, len(card[0])*50

pygame.init()
window = pygame.display.set_mode((m, n))
pygame.display.set_caption("Ray casting 2D")
font = pygame.font.SysFont('Arial', 30, bold=True)
clock = pygame.time.Clock()

pers = pygame.Surface((30, 30))
pers.fill('#888888')
pygame.draw.rect(pers, '#333333', (0, 0, 30, 30), border_radius=8)
pygame.draw.rect(pers, '#AA1111', (25, 14, 5, 3))
rect = pers.get_rect()

game, x, y, ang = 1, 55, 55, -45
while game:
    clock.tick(80)
    window.fill('#888888')
    text_fps = font.render(str(int(clock.get_fps())), False, (200, 0, 0))

    new_image = pygame.transform.rotate(pers, ang)
    rect = new_image.get_rect(center=rect.center)
    window.blit(new_image, (x + rect.x, y + rect.y))

    for i in range(len(card)):
        for j in range(len(card[i])):
            if card[i][j]:
                pygame.draw.rect(window, (0, 0, 0), (j * 50, i * 50, 50, 50))

    window.blit(text_fps, (10, 5))

    x_sk = x + 15 + math.cos(math.radians(ang)) * 15
    y_sk = y + 15 - math.sin(math.radians(ang)) * 15

    num_ray, delta_ang = 500, 60
    lengs = get_rays(x_sk, y_sk, ang, num_ray, delta_ang, numpy.array(card))

    for i, l in enumerate(lengs[::-1]):
        a = (ang - delta_ang) + delta_ang*2 / num_ray * i
        pygame.draw.line(window, (250, 0, 0), (x_sk, y_sk), (x_sk + math.cos(math.radians(a)) * l,
                                                             y_sk - math.sin(math.radians(a)) * l))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = 0

    xp, yp, angp, but = x, y, ang, pygame.key.get_pressed()
    if but[pygame.K_UP]:
        x += math.cos(math.radians(ang)) * 3
        y -= math.sin(math.radians(ang)) * 3
    if but[pygame.K_DOWN]:
        x -= math.cos(math.radians(ang)) * 3
        y += math.sin(math.radians(ang)) * 3
    if but[pygame.K_LEFT]:
        ang = (ang + 3) % 360
    if but[pygame.K_RIGHT]:
        ang = (ang - 3) % 360

    for i in range(8):
        leng = 15 if (ang + i * 45) % 90 == 0 else 18
        xp1 = int(xp + 15) + leng * math.cos(math.radians(ang + i * 45))
        yp1 = int(yp + 15) - leng * math.sin(math.radians(ang + i * 45))
        x1 = int(x + 15) + leng * math.cos(math.radians(ang + i * 45))
        y1 = int(y + 15) - leng * math.sin(math.radians(ang + i * 45))
        if card[int(yp1 / 50)][int(x1 / 50)]:
            x = xp
        if card[int(y1 / 50)][int(xp1 / 50)]:
            y = yp
        if card[int(y1 / 50)][int(x1 / 50)] and ang != angp:
            z = [(1, 1), (1, 1), (1, 0), (-1, 0), (-1, 0), (-1, -1), (0, -1), (1, 1)]
            x -= math.cos(math.radians(ang)) * 3 * z[i][0]
            y += math.sin(math.radians(ang)) * 3 * z[i][1]
