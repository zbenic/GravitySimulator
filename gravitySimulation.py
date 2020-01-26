import numpy
import pygame

SIM_WINDOW_WIDTH = 800  # pixels
SIM_WINDOW_HEIGHT = 600  # pixels
MAX_OBJECT_DIAMETER = 100  # pixels
MAX_NUM_OF_OBJECTS = 10

def init_objects():
    random_float_array = numpy.random.uniform(75.5, 125.5, size=(2, 2))
    for i in range(0, MAX_NUM_OF_OBJECTS):



def draw_objects(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(simDisplay, color, [thingx, thingy, thingw, thingh])


def main():
    pygame.init()

    simDisplay = pygame.display.set_mode((SIM_WINDOW_WIDTH, SIM_WINDOW_HEIGHT))
    pygame.display.set_caption('Gravity Simulation')

    clock = pygame.time.Clock()

    crashed = False
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True

            print(event)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    quit()

    #######
    def things(thingx, thingy, thingw, thingh, color):
        pygame.draw.rect(simDisplay, color, [thingx, thingy, thingw, thingh])
    #######


if __name__ == '__main__':
    main()
