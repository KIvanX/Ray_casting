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
font = pygame.font.SysFont('Arial', 30, bold=True)
clock = pygame.time.Clock()

game, x, y, ang = 1, 55, 55, -45
while game:
    clock.tick()
    pygame.display.set_caption("Ray casting 3D    FPS: " + str(int(clock.get_fps())))
    window.fill((50, 50, 100))
    pygame.draw.rect(window, (30, 80, 30), (0, n/2, m, n/2))

    x_sk = x + 15 + math.cos(math.radians(ang)) * 15
    y_sk = y + 15 - math.sin(math.radians(ang)) * 15

    num_ray, delta_ang = 1000, 60
    lengs = get_rays(x_sk, y_sk, ang, num_ray, delta_ang, numpy.array(card))[1:]
    w = m / num_ray
    for i, l in enumerate(lengs):
        a = (ang - delta_ang) + delta_ang * 2 / num_ray * i
        h = 25000 / (l * math.cos(math.radians(ang - a)))
        cl = 130 - h**0.15 * 50
        color = (130 - cl, 140 - cl, 150 - cl)
        pygame.draw.rect(window, color, (int(i*w), n/2-h/2, int(w)+1, h))

        if 0 < i < num_ray-1:
            prv = 25000 / (lengs[i-1] * math.cos(math.radians(ang - (a - delta_ang*2 / num_ray))))
            nxt = 25000 / (lengs[i+1] * math.cos(math.radians(ang - (a + delta_ang*2 / num_ray))))
            if prv + nxt > h*2+1 or prv + nxt < h*2-1:
                pygame.draw.line(window,
                                 (color[0] - 30, color[1] - 30, color[2] - 30),
                                 (int(i*w + w/2), n/2-h/2), (int(i*w + w/2), n/2+h/2))

    pygame.draw.rect(window, (50, 120, 50), (10, 10, m/5, n/5))
    for i in range(len(card)):
        for j in range(len(card[i])):
            if card[i][j]:
                pygame.draw.rect(window, (150, 150, 150), (10 + j * 10, 10 + i * 10, 10, 10))
    pygame.draw.circle(window, (200, 200, 0), (10 + x / 5, 10 + y / 5), 3)
    c1 = 10 + x / 5 + math.cos(math.radians(ang)) * 6, 10 + y / 5 - math.sin(math.radians(ang)) * 5
    c2 = 10 + x / 5 + math.cos(math.radians(ang+90)) * 2, 10 + y / 5 - math.sin(math.radians(ang+90)) * 2
    c3 = 10 + x / 5 + math.cos(math.radians(ang-90)) * 2, 10 + y / 5 - math.sin(math.radians(ang-90)) * 2
    pygame.draw.polygon(window, (200, 200, 0), (c1, c2, c3))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = 0

        if event.type == pygame.MOUSEBUTTONDOWN:
            xmap, ymap = pygame.mouse.get_pos()
            if 10 <= xmap <= m/5 and 10 <= ymap <= n/5:
                card[(ymap-10) // 10][(xmap-10) // 10] = not card[(ymap-10) // 10][(xmap-10) // 10]
                with open('map.pkl', 'wb') as f:
                    pickle.dump(card, f)

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
