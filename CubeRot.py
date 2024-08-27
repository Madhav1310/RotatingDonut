import os
import math
from time import sleep

# Create a matrix for the screen
def make_screen(w, h, char):
    return [[char] * w for _ in range(h)]

# Clear the screen
def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

# Print the screen
def print_screen(screen):
    clear()
    print('\n'.join(''.join(row) for row in screen))

# Draw a line on the screen
def draw_line(screen, p1, p2, char, color):
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    steps = max(abs(dx), abs(dy))
    dx, dy = dx / steps, dy / steps
    x, y = p1[0], p1[1]

    for _ in range(int(steps) + 1):
        screen[int(y)][int(x)] = '\033[0;' + str(color + 30) + ';40m' + char + '\033[0;0m'
        x, y = x + dx, y + dy

# Define characters and get terminal size
empty_char = ' '
fill_char = 'o'
size = os.get_terminal_size()
width, height = size.columns, size.lines

# Main function to create the animation
def animate(t):
    screen = make_screen(width, height, empty_char)
    center = [int(width / 2), int(height / 2)]
    radius = 10
    skew = 2.5
    depth = 10

    points = [
        [math.cos(t) * radius + center[0], math.sin(t) * radius / skew + depth / 2 + center[1]],
        [math.cos(t + math.pi/2) * radius + center[0], math.sin(t + math.pi/2) * radius / skew + depth / 2 + center[1]],
        [math.cos(t + math.pi) * radius + center[0], math.sin(t + math.pi) * radius / skew + depth / 2 + center[1]],
        [math.cos(t + 3*math.pi/2) * radius + center[0], math.sin(t + 3*math.pi/2) * radius / skew + depth / 2 + center[1]]
    ]
    points += [[p[0], p[1] - depth] for p in points]

    # Draw each edge of the cube
    for i in range(4):
        draw_line(screen, points[i], points[(i + 1) % 4], fill_char, i)
        draw_line(screen, points[i], points[i + 4], fill_char, i)
        draw_line(screen, points[i + 4], points[(i + 1) % 4 + 4], fill_char, i)

    sleep(0.15)
    print_screen(screen)
    animate(t + 0.1)

# Start the animation
animate(0)