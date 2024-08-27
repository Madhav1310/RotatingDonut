import numpy as np
import curses
import time

# Constants for the donut shape
R1 = 10  # Radius of the circle that forms the donut's tube
R2 = 2  # Distance from the center of the donut to the center of the tube

# Projection constants
K1_CONSTANT = 150  # Scaling factor for projecting 3D coordinates onto the 2D screen
K2_CONSTANT = 5    # Influences the perspective projection (depth effect)

# Rotation increments
INCREMENT_A = 0.07  # Increment for angle A for each frame (horizontal rotation speed)
INCREMENT_B = 0.03  # Increment for angle B for each frame (vertical rotation speed)

# Step values for generating angles in the donut animation
# Step size for the outer loop generating theta angles
THETA_STEP = 0.1  # Smaller values increase the detail and smoothness of the donut's outer curvature

# Smaller values increase the detail and smoothness of the donut's tube surface
PHI_STEP = 0.05  # Step size for the inner loop generating phi angles


def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    max_y, max_x = stdscr.getmaxyx()
    max_x = max_x - max_x % 2  # Ensure max_x is even

    A, B = 0.0, 0.0

    while True:
        stdscr.clear()  # Clear the screen
        output = np.zeros((max_y, max_x), dtype='int32')

        K1 = K1_CONSTANT * (max_x / 80)
        K2 = K2_CONSTANT

        for j in np.arange(0, 6.28, THETA_STEP):
            ct, st = np.cos(j), np.sin(j)
            for i in np.arange(0, 6.28, PHI_STEP):
                sp, cp = np.sin(i), np.cos(i)
                h = ct + 2
                D = 1 / (sp * h * np.sin(A) + st * np.cos(A) + 5)
                t = sp * h * np.cos(A) - st * np.sin(A)

                x = int((max_x / 2) + 30 * D * (cp * h * np.cos(B) - t * np.sin(B)))
                y = int((max_y / 2) - 15 * D * (cp * h * np.sin(B) + t * np.cos(B)))
                o = int(8 * ((st * np.sin(A) - sp * ct * np.cos(A)) * np.cos(B) - sp * ct * np.sin(A) - st * np.cos(A) - cp * ct * np.sin(B)))
                if 0 <= y < max_y and 0 <= x < max_x:
                    if output[y, x] < D:
                        output[y, x] = D
                        try:
                            stdscr.addch(y, x, ".,-~:;=!*#$@"[o if o > 0 else 0])
                        except curses.error:
                            pass

        stdscr.refresh()  # Refresh the screen
        #time.sleep(0.05)  # Frame delay

        A += INCREMENT_A
        B += INCREMENT_B
        #time.sleep(0.025)  # Decreased sleep for a smoother, faster animation

curses.wrapper(main)