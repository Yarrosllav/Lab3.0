import numpy as np
import matplotlib.pyplot as plt

x = [0, 0.4, 0.8, 1.2, 1.6]
y = [-2.2026, -0.19315, 0.79464, 1.5624, 2.2306]
xi = 8
hi = np.diff(x)

def find_d(yi):
    result = []
    for i in range(len(yi) - 2):
        result.append(((yi[i + 2] - yi[i + 1]) / hi[i + 1]) - ((yi[i + 1] - yi[i]) / hi[i]))
    return np.array(result)

def find_q(a, b):
    q_arr = np.linalg.solve(a, b)
    qi = [0.0]
    for i in range(len(q_arr)):
        qi.append(q_arr[i])
    qi.append(0.0)
    return qi

def spline(x, xi, yi):
    n = len(xi)
    a = np.zeros((n - 2, n - 2))
    b = find_d(yi)

    for i in range(n - 2):
        if i == 0:
            a[i, i] = (hi[i] ** 2) / 3
            a[i, i + 1] = hi[i] / 6
        elif i == n - 3:
            a[i, i - 1] = hi[i] / 6
            a[i, i] = (hi[i] ** 2) / 3
        else:
            a[i, i - 1] = hi[i] / 6
            a[i, i] = (hi[i] ** 2) / 3 + (hi[i + 1] ** 2) / 3
            a[i, i + 1] = hi[i + 1] / 6

    qi = find_q(a, b)

    for i in range(len(xi) - 1):
        if xi[i] <= x <= xi[i + 1]:
            return qi[i] * ((xi[i + 1] - x)**3) / (6 * hi[i]) \
                   + qi[i + 1] * ((x - xi[i])**3) / (6 * hi[i]) \
                   + (yi[i] / hi[i] - qi[i] * hi[i] / 6) * (xi[i + 1] - x) \
                   + (yi[i + 1] / hi[i] - qi[i + 1] * hi[i] / 6) * (x - xi[i])

    return yi[-1]

def plot():
    plt.grid(True)
    plt.xlabel("$X$")
    plt.ylabel("$F(x)$")
    x1 = np.linspace(x[0], x[-1], 100)
    y1 = [spline(i, x, y) for i in x1]
    plt.plot(x, y)
    plt.plot(x1, y1)
    plt.title("Cubic spline")
    plt.scatter(x, y, color='red')
    plt.show()
    plt.close()

print(f"Розрахунок сплайну в точці X* = {xi}: ", spline(xi, x, y))
plot()
