import math
import numpy as np
import pygame
import sys

pygame.init()
 
width, height = 600, 400
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

angle = 0
distance = 3  # Initial distance for perspective projection

points = []


def setup():
    global points

    points.append(np.array([-0.5, -0.5, -0.5]))
    points.append(np.array([0.5, -0.5, -0.5]))
    points.append(np.array([0.5, 0.5, -0.5]))
    points.append(np.array([-0.5, 0.5, -0.5]))
    points.append(np.array([-0.5, -0.5, 0.5]))
    points.append(np.array([0.5, -0.5, 0.5]))
    points.append(np.array([0.5, 0.5, 0.5]))
    points.append(np.array([-0.5, 0.5, 0.5]))


projection_type = 'p'  # Default perspective projection


def draw():
    global angle, distance, projection_type

    screen.fill((0, 0, 0))
    #rotation
    rotationZ = np.array([
        [math.cos(angle), -math.sin(angle), 0],
        [math.sin(angle), math.cos(angle), 0],
        [0, 0, 1]
    ])

    rotationX = np.array([
        [1, 0, 0],
        [0, math.cos(angle), -math.sin(angle)],
        [0, math.sin(angle), math.cos(angle)]
    ])

    rotationY = np.array([
        [math.cos(angle), 0, math.sin(angle)],
        [0, 1, 0],
        [-math.sin(angle), 0, math.cos(angle)]
    ])

    projected = []

    for i in range(len(points)):
        rotated = np.matmul(rotationY, points[i])
        rotated = np.matmul(rotationX, rotated)
        rotated = np.matmul(rotationZ, rotated)

        if projection_type == 'p':
            z = 1 / (distance - rotated[2])
        elif projection_type == 'o':
            z = 1

        projection = np.array([
            [z, 0, 0],
            [0, z, 0]
        ])
        projected2d = np.matmul(projection, rotated)

        projected2d *= 200
        projected.append(projected2d)
    #  draw
    for i in range(len(projected)):
        pygame.draw.circle(screen, (255, 2, 255),
                           (int(projected[i][0] + width / 2), int(projected[i][1] + height / 2)), 8)
    # connect
    for i in range(4):
        connect(i, (i + 1) % 4, projected)
        connect(i + 4, ((i + 1) % 4) + 4, projected)
        connect(i, i + 4, projected)

    # Display distance and projection type at bottom left
    font = pygame.font.Font(None, 30)
    text_distance = font.render("Distance: {:.1f}".format(distance), True, (255, 255, 255))
    text_projection = font.render("Projection: {}".format("Perspective" if projection_type == 'p' else 'Orthogonal'), True, (255, 255, 255))
    screen.blit(text_distance, (10, height - 60))
    screen.blit(text_projection, (10, height - 30))

    pygame.display.flip()
    clock.tick(60)

    angle += 0.015


def connect(i, j, points):
    a = points[i]
    b = points[j]
    pygame.draw.line(screen, (255, 255, 255), (int(a[0] + width / 2), int(a[1] + height / 2)),
                     (int(b[0] + width / 2), int(b[1] + height / 2)))  # Add missing comma here


setup()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                projection_type = 'p'
            elif event.key == pygame.K_o:
                projection_type = 'o'
            elif event.key == pygame.K_KP_PLUS or event.key == pygame.K_EQUALS:
                distance = max(0.2, distance - 0.2)
            elif event.key == pygame.K_KP_MINUS or event.key == pygame.K_MINUS:
                distance += 0.2

    draw()
