import numpy as np
import matplotlib.pyplot as plt

xi = [0, 0.4, 0.8, 1.2, 1.6]
yi = [-2.2026, -0.19315, 0.79464, 1.5624, 2.2306]
x = 8


def find_h(xi):
    hi = []
    for i in range(len(xi) - 1):
        hi.append(xi[i + 1] - xi[i])
    return hi


def find_d(yi):
    values_array = []
    for i in range(3):
        values_array.append(((yi[i + 2] - yi[i + 1]) / 0.4) - ((yi[i + 1] - yi[i]) / 0.4))
    return np.array(values_array)


def system_solution(a, b):
    q_part = np.linalg.solve(a, b)
    qi = [0.0]
    for i in range(len(q_part)):
        qi.append(q_part[i])
    qi.append(0.0)
    return qi


def spline_interpolation(x, xi, yi):
    hi = find_h(xi)
    a = [
        [(hi[1] * 2) / 3, hi[2] / 6, 0],
        [hi[1] / 6, (hi[2] * 2) / 3, hi[3] / 6],
        [hi[2] / 6, 0, (hi[3] * 2) / 3]
    ]
    b = find_d(yi)
    qi = system_solution(a, b)

    if x <= xi[-1]:
        for i in range(4):
            if xi[i] <= x <= xi[i + 1]:
                return qi[i] * ((xi[i + 1] - x) ** 3) / (6 * hi[i]) \
                    + qi[i + 1] * ((x - xi[i]) ** 3) / (6 * hi[i]) \
                    + (yi[i] / hi[i] - qi[i] * hi[i] / 6) * (xi[i + 1] - x) \
                    + (yi[i + 1] / hi[i] - qi[i + 1] * hi[i] / 6) * (x - xi[i])
    else:
        i = 4
        h = xi[-1] - xi[-2]
        return qi[i] * ((xi[-1] - x) ** 3) / (6 * h) \
            + qi[i - 1] * ((x - xi[-2]) ** 3) / (6 * h) \
            + (yi[i] / h - qi[i] * h / 6) * (xi[-1] - x) \
            + (yi[i - 1] / h - qi[i - 1] * h / 6) * (x - xi[-2])


def plot():
    plt.grid(True)
    plt.xlabel("$X$")
    plt.ylabel("$S(x)$")

    x1 = np.linspace(xi[0], xi[-1], 100)
    y1 = [spline_interpolation(i, xi, yi) for i in x1]

    plt.plot(x1, y1, color='#000', label='Spline')
    plt.scatter(xi, yi, c='coral')

    plt.show()
    plt.close()


print("Розрахунок сплайна за допомогою інтерполяції: ", spline_interpolation(x, xi, yi))
plot()
