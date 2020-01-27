import numpy as np
import pygame
from physicalObject import TerrestrialPlanet

SIM_WINDOW_WIDTH = 800  # pixels
SIM_WINDOW_HEIGHT = 600  # pixels
MIN_OBJECT_DIAMETER = 5  # pixels
MAX_OBJECT_DIAMETER = 50  # pixels
MAX_NUM_OF_OBJECTS = 2
FPS = 60
TIMESTEP = 1. / FPS


def init_objects():
    # TODO: default class constructor and objects_array = [TerrestrialPlanet() for _ in range(MAX_NUM_OF_OBJECTS)]?
    # TODO: watch it not to introduce collisions at the init phase
    objects_array = []
    position_vec = np.c_[np.random.randint(0, SIM_WINDOW_HEIGHT, MAX_NUM_OF_OBJECTS),
                         np.random.randint(0, SIM_WINDOW_WIDTH, MAX_NUM_OF_OBJECTS)]
    diameter = np.random.randint(MIN_OBJECT_DIAMETER, MAX_OBJECT_DIAMETER, MAX_NUM_OF_OBJECTS)
    velocity_vec = np.zeros(MAX_NUM_OF_OBJECTS)
    color = np.c_[np.random.randint(0, 255, MAX_NUM_OF_OBJECTS),
                  np.random.randint(0, 255, MAX_NUM_OF_OBJECTS),
                  np.random.randint(0, 255, MAX_NUM_OF_OBJECTS)]
    for i in range(0, MAX_NUM_OF_OBJECTS):
        objects_array.append(TerrestrialPlanet(i,
                                               position_vec[i],
                                               diameter[i],
                                               velocity_vec[i],
                                               color[i],
                                               MAX_NUM_OF_OBJECTS,
                                               TIMESTEP))
    return objects_array


def draw_objects(display, celestial_objects):
    for celestial_object in celestial_objects:
        pygame.draw.circle(display, celestial_object.color, celestial_object.position_vec, celestial_object.diameter)


def main():
    pygame.init()

    simDisplay = pygame.display.set_mode((SIM_WINDOW_WIDTH, SIM_WINDOW_HEIGHT))
    pygame.display.set_caption('Gravity Simulation')

    clock = pygame.time.Clock()

    celestial_objects = init_objects()

    crashed = False
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True

            draw_objects(simDisplay, celestial_objects)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    quit()


if __name__ == '__main__':
    main()
