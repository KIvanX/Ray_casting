import numpy
import math
from numba import njit


@njit(fastmath=True, cache=True)
def get_rays(x, y, ang, num_ray, delta_ang, card):
    n = len(card)
    m = len(card[0])
    a, ind = ang-delta_ang, 0
    lengs = numpy.zeros((num_ray+1, ))
    while a < ang+delta_ang:
        go = 1
        rad_a = math.radians(a)

        zn_v = math.cos(rad_a) / abs(math.cos(rad_a)) if a != 90 else 1
        px_v = x + (50 - x % 50)
        py_v = y - math.tan(rad_a) * (50 - x % 50) if a != 90 else 1

        zn_g = math.sin(rad_a) / abs(math.sin(rad_a)) if a != 0 else 1
        px_g = x + 1 / math.tan(rad_a) * (y % 50) if a != 0 else 1
        py_g = y - y % 50

        k = 0
        resv = (0, 0)
        resg = (0, 0)
        while go:
            k += 1
            if k == 10000:
                go = 0

            if not resv[0] and not (k == 1 and zn_v < 0):
                j, i = int((px_v + zn_v*3) / 50), int(py_v / 50)
                if not(0 <= i < n and 0 <= j < m) or card[i][j]:
                    resv = (px_v, py_v)

            if not resg[0] and not (k == 1 and zn_g < 0):
                j, i = int(px_g / 50), int((py_g - zn_g*3) / 50)
                if not(0 <= i < n and 0 <= j < m) or card[i][j]:
                    resg = (px_g, py_g)

            if resv[0] and resg[0]:
                go = 0
                if (x - resv[0]) ** 2 + (y - resv[1]) ** 2 < (x - resg[0]) ** 2 + (y - resg[1]) ** 2:
                    lengs[ind] = ((x - resv[0]) ** 2 + (y - resv[1]) ** 2)**0.5
                else:
                    lengs[ind] = ((x - resg[0]) ** 2 + (y - resg[1]) ** 2)**0.5

            px_v += 50 * zn_v
            py_v -= math.tan(rad_a) * 50 * zn_v
            px_g += 1 / (math.tan(rad_a) if a != 0 else 0.0001) * 50 * zn_g
            py_g -= 50 * zn_g

        a += delta_ang*2 / num_ray
        ind += 1
    return lengs[::-1]
