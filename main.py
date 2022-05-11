import pickle
import numpy
import pygame
import math
from rays import get_rays

with open('map.pkl', 'rb') as f:
    card = pickle.load(f)

W, H = 1200, 600
n, m, A = len(card), len(card[0]), H // len(card)
pygame.init()
window = pygame.display.set_mode((W, H))
font = pygame.font.SysFont('Arial', 30, bold=True)
clock = pygame.time.Clock()

fon_sky = pygame.image.load('textures/sky3.jpg').convert()
fon_grass = pygame.image.load('textures/grass.png').convert()
fon_wall = pygame.image.load('textures/simple_fon.jpg').convert()

game, x, y, ang, offset_sky = 1, A * 2, A * 2, 315, 0
while game:
    clock.tick()
    pygame.display.set_caption("Ray casting 3D    FPS: " + str(int(clock.get_fps())))
    pygame.draw.rect(window, (30, 100, 30), (0, H // 2, W, H // 2))
    offset_sky = ang * 1200 / 360
    window.blit(fon_sky, (offset_sky, 0))
    window.blit(fon_sky, (offset_sky - 1200, 0))

    num_ray, delta_ang = 600, 45
    rays = get_rays(x, y, ang, A, num_ray, delta_ang, numpy.array(card))[1:]
    # rays = [(200, 10, 10, 0)] * num_ray

    walls_list, draw_num = [], 0
    w = W / num_ray
    for i, (l, xl, yl, side) in enumerate(rays):
        h = 20000 / l if 20000 / l < 1200 else 1200
        offset = xl % A if side else yl % A
        cropped = fon_wall.subsurface((min(offset * (600 / A), 600-w), 0, w, 600))
        cropped = pygame.transform.scale(cropped, (w, h))
        window.blit(cropped, (i * w, H / 2 - h / 2))

    pygame.draw.rect(window, (50, 120, 50), (10, 10, W // 4, H // 4))
    for i in range(n):
        for j in range(m):
            if card[i][j]:
                pygame.draw.rect(window, (150, 150, 150), (10 + int(j * A / 4.0), 10 + int(i * A / 4), A / 4, A / 4))
    pygame.draw.circle(window, (200, 200, 0), (10 + x // 4, 10 + y // 4), 3)
    c1 = 10 + x / 4 + math.cos(math.radians(ang)) * 6, 10 + y / 4 - math.sin(math.radians(ang)) * 5
    c2 = 10 + x / 4 + math.cos(math.radians(ang + 90)) * 2, 10 + y / 4 - math.sin(math.radians(ang + 90)) * 2
    c3 = 10 + x / 4 + math.cos(math.radians(ang - 90)) * 2, 10 + y / 4 - math.sin(math.radians(ang - 90)) * 2
    pygame.draw.polygon(window, (200, 200, 0), (c1, c2, c3))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = 0

        if event.type == pygame.MOUSEBUTTONDOWN:
            xmap, ymap = pygame.mouse.get_pos()
            if 10 <= xmap <= W // 4 + 10 and 10 <= ymap <= H // 4 + 10:
                card[(ymap - 10) // (A // 4)][(xmap - 10) // (A // 4)] = not card[(ymap - 10) // (A // 4)][
                    (xmap - 10) // (A // 4)]
                with open('map.pkl', 'wb') as f:
                    pickle.dump(card, f)

    xp, yp, but = x, y, pygame.key.get_pressed()
    if but[pygame.K_UP]:
        x += math.cos(math.radians(ang))
        y -= math.sin(math.radians(ang))
    if but[pygame.K_DOWN]:
        x -= math.cos(math.radians(ang))
        y += math.sin(math.radians(ang))
    if but[pygame.K_LEFT]:
        ang = (ang + 1.5) % 360
    if but[pygame.K_RIGHT]:
        ang = (ang - 1.5) % 360

    if card[int(y / A)][int(xp / A)]:
        y = yp
    elif card[int(yp / A)][int(x / A)]:
        x = xp
    if card[int(y / A)][int(x / A)]:
        x, y = xp, yp
