import pygame

pygame.init()

WIDTH, HEIGHT = 1000, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Smart Traffic Signal Simulator")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (60, 60, 60)

RED = (220, 0, 0)
YELLOW = (255, 220, 0)
GREEN = (0, 220, 0)
BLUE = (0, 120, 255)

SIGNAL_CHANGE = pygame.USEREVENT + 1


class Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.color = BLUE
        self.image = pygame.Surface((100, 50), pygame.SRCALPHA)
        self.draw_car()

        self.rect = self.image.get_rect()
        self.rect.x = -100
        self.rect.y = HEIGHT // 2 + 25

        self.velocity = 5

    def draw_car(self):
        self.image.fill((0, 0, 0, 0))

        pygame.draw.rect(
            self.image,
            self.color,
            (10, 20, 80, 20)
        )

        pygame.draw.rect(
            self.image,
            self.color,
            (25, 5, 45, 18)
        )

        pygame.draw.rect(
            self.image,
            (173, 216, 230),
            (30, 8, 15, 12)
        )

        pygame.draw.rect(
            self.image,
            (173, 216, 230),
            (50, 8, 15, 12)
        )

        pygame.draw.circle(
            self.image,
            BLACK,
            (25, 40),
            8
        )

        pygame.draw.circle(
            self.image,
            BLACK,
            (75, 40),
            8
        )

    def update(self, signal_state):
        if signal_state == "GREEN":
            speed = self.velocity
        elif signal_state == "YELLOW":
            speed = self.velocity // 2
        else:
            speed = 0

        self.rect.x += speed

        if self.rect.left > WIDTH:
            pygame.event.post(
                pygame.event.Event(SIGNAL_CHANGE)
            )

    def reset(self):
        self.rect.x = -100

    def set_color(self, color):
        self.color = color
        self.draw_car()


car = Car()

cars = pygame.sprite.Group()
cars.add(car)

signal_state = "GREEN"

running = True

while running:

    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == SIGNAL_CHANGE:

            if signal_state == "GREEN":
                signal_state = "YELLOW"
                car.set_color(YELLOW)

            elif signal_state == "YELLOW":
                signal_state = "RED"
                car.set_color(RED)

            else:
                signal_state = "GREEN"
                car.set_color(BLUE)

            car.reset()

    cars.update(signal_state)

    screen.fill((135, 206, 235))

    pygame.draw.rect(
        screen,
        (50, 180, 50),
        (0, 0, WIDTH, HEIGHT // 2)
    )

    pygame.draw.rect(
        screen,
        (50, 180, 50),
        (0, HEIGHT // 2 + 100, WIDTH, HEIGHT // 2)
    )

    pygame.draw.rect(
        screen,
        GRAY,
        (0, HEIGHT // 2, WIDTH, 100)
    )

    for x in range(0, WIDTH, 60):
        pygame.draw.rect(
            screen,
            WHITE,
            (x, HEIGHT // 2 + 45, 35, 8)
        )

    pole_x = 850

    pygame.draw.rect(
        screen,
        BLACK,
        (pole_x, 110, 15, 150)
    )

    pygame.draw.rect(
        screen,
        BLACK,
        (pole_x - 12, 70, 40, 90)
    )

    pygame.draw.circle(
        screen,
        RED if signal_state == "RED" else (60, 0, 0),
        (pole_x + 8, 90),
        10
    )

    pygame.draw.circle(
        screen,
        YELLOW if signal_state == "YELLOW" else (60, 60, 0),
        (pole_x + 8, 115),
        10
    )

    pygame.draw.circle(
        screen,
        GREEN if signal_state == "GREEN" else (0, 60, 0),
        (pole_x + 8, 140),
        10
    )

    cars.draw(screen)

    pygame.display.flip()

pygame.quit()