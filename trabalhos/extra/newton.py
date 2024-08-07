import matplotlib.pyplot as plt
import numpy as np
import sympy

from matplotlib.widgets import Slider

print('Digite a função f(x, y):')
f = sympy.sympify(input())

print('Digite a função g(x, y):')
g = sympy.sympify(input())

print('Digite o chute inicial (x0, y0):')
x0, y0 = map(float, input().split())

print('Digite o início, o fim e a quantidade de pontos para os eixos:')
axis_start, axis_end, axis_points = map(float, input().split())

fx = sympy.diff(f, 'x')
fy = sympy.diff(f, 'y')

gx = sympy.diff(g, 'x')
gy = sympy.diff(g, 'y')

print(f'f(x, y) = {f}')
print(f'g(x, y) = {g}')
print(f'x0 = {x0}, y0 = {y0}')
print()
print(f'fx = {fx}, fy = {fy}')
print(f'gx = {gx}, gy = {gy}')

jacobian = sympy.Matrix([[fx, fy], [gx, gy]])
values = sympy.Matrix([f, g])

delta = jacobian.inv() * (-values)

f_lambda = sympy.lambdify(('x', 'y'), f, 'numpy')
g_lambda = sympy.lambdify(('x', 'y'), g, 'numpy')

plt.style.use('bmh')

figure, ax = plt.subplots(1, 1, figsize=(10, 8))
figure.subplots_adjust(bottom=0.2)
ax.axes.set_aspect('equal')

ax.spines['left'].set_position('zero')
ax.spines['bottom'].set_position('zero')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')

ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

x_space = np.linspace(axis_start, axis_end, int(axis_points))
y_space = np.linspace(axis_start, axis_end, int(axis_points))

x_mesh, y_mesh = np.meshgrid(x_space, y_space)

ax.contour(x_mesh, y_mesh, f_lambda(x_mesh, y_mesh), levels=[0], colors='g')
ax.contour(x_mesh, y_mesh, g_lambda(x_mesh, y_mesh), levels=[0], colors='b')

previous_points, = ax.plot([], [], 'yo')
current_points, = ax.plot(x0, y0, 'ro')

def update(_):
    x = x0
    y = y0

    x_data = []
    y_data = []

    for _ in range(iteration.val):
        x_data.append(x)
        y_data.append(y)

        x += float(delta[0].subs({'x': x, 'y': y}))
        y += float(delta[1].subs({'x': x, 'y': y}))
        
    previous_points.set_data(x_data, y_data)
    current_points.set_data([x], [y])

    figure.canvas.draw_idle()

axes_iteration = figure.add_axes([0.2, 0.1, 0.6, 0.03])

iteration = Slider(axes_iteration, 'Iteration', 0, 20, valinit=0, valstep=1)
iteration.on_changed(update)

plt.show()