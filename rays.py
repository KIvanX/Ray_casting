import numpy
import math
from numba import njit


@njit(fastmath=True, cache=True)
def get_rays(x, y, angle, a, num_ray, radius_ang, card):
    delta_ang = radius_ang*2 / num_ray
    rays = numpy.zeros((num_ray+1, 4))
    for ind in range(num_ray):
        rad_a = math.radians(angle - radius_ang + delta_ang * ind)
        sin_a = math.sin(rad_a) if math.sin(rad_a) != 0 else 0.001
        cos_a = math.cos(rad_a) if math.cos(rad_a) != 0 else 0.001
        tan_a = sin_a / cos_a

        zn_v = cos_a / abs(cos_a)
        px_v = x + (a - x % a)
        py_v = y - tan_a * (a - x % a)

        zn_g = sin_a / abs(sin_a)
        px_g = x + 1 / tan_a * (y % a)
        py_g = y - y % a

        first = True
        resv = (0, 0)
        resg = (0, 0)
        while True:
            if not resv[0] and not (first and zn_v < 0):
                j, i = int((px_v + zn_v*3) / a), int(py_v / a)
                if not(0 <= i < len(card) and 0 <= j < len(card[0])) or card[i][j]:
                    resv = (px_v, py_v)

            if not resg[0] and not (first and zn_g < 0):
                j, i = int(px_g / a), int((py_g - zn_g*3) / a)
                if not(0 <= i < len(card) and 0 <= j < len(card[0])) or card[i][j]:
                    resg = (px_g, py_g)

            if resv[0] and resg[0]:
                if (x - resv[0]) ** 2 + (y - resv[1]) ** 2 < (x - resg[0]) ** 2 + (y - resg[1]) ** 2:
                    rays[ind] = [math.sqrt((x - resv[0]) ** 2 + (y - resv[1]) ** 2), resv[0], resv[1], 0]
                else:
                    rays[ind] = [math.sqrt((x - resg[0]) ** 2 + (y - resg[1]) ** 2), resg[0], resg[1], 1]
                rays[ind][0] *= math.cos(math.radians(radius_ang - delta_ang * ind))
                break

            px_v += a * zn_v
            py_v -= tan_a * a * zn_v
            px_g += 1 / tan_a * a * zn_g
            py_g -= a * zn_g
            first = False

    return rays[::-1]
