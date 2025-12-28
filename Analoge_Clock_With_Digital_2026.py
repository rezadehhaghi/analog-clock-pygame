import pygame
import math
import time

# -------------------- INIT --------------------
pygame.init()
SCREEN = pygame.display.set_mode((300, 300))
pygame.display.set_caption("Analog + Digital Clock")
CLOCK = pygame.time.Clock()

# -------------------- COLORS --------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 128)
RED = (255, 0, 0)

# -------------------- FONT --------------------
font = pygame.font.Font('Seven Segment.ttf', 36)

# -------------------- COLON TIMER --------------------
COLON_INTERVAL = 500
last_colon_toggle = pygame.time.get_ticks()
show_colon = True

# -------------------- FUNCTIONS --------------------
def sin_cos(deg):
    rad = math.radians(deg)
    return math.sin(rad), math.cos(rad)

def draw_hand(angle, length, width, color):
    s, c = sin_cos(angle)
    x = 150 + length * s
    y = 150 - length * c
    pygame.draw.line(SCREEN, color, (150, 150), (x, y), width)

# -------------------- MAIN LOOP --------------------
running = True
while running:
    CLOCK.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # -------------------- TIME --------------------
    t = time.localtime()
    hour = t.tm_hour % 12
    minute = t.tm_min
    second = t.tm_sec

    # -------------------- CLEAR SCREEN --------------------
    SCREEN.fill(BLACK)

    # -------------------- CLOCK FACE --------------------
    pygame.draw.circle(SCREEN, YELLOW, (150, 150), 150)
    pygame.draw.circle(SCREEN, YELLOW, (150, 150), 135)

    # minute marks
    for i in range(60):
        angle = i * 6
        s, c = sin_cos(angle)
        x1 = 150 + 130 * s
        y1 = 150 - 130 * c
        x2 = 150 + 145 * s
        y2 = 150 - 145 * c
        pygame.draw.line(SCREEN, BLACK, (x1, y1), (x2, y2), 1)

    # hour marks
    for i in range(12):
        angle = i * 30
        s, c = sin_cos(angle)
        x1 = 150 + 120 * s
        y1 = 150 - 120 * c
        x2 = 150 + 145 * s
        y2 = 150 - 145 * c
        pygame.draw.line(SCREEN, BLACK, (x1, y1), (x2, y2), 4)

    # -------------------- HANDS --------------------
    second_angle = second * 6
    minute_angle = minute * 6 + second * 0.1
    hour_angle = hour * 30 + minute * 0.5

    draw_hand(hour_angle, 70, 5, BLACK)
    draw_hand(minute_angle, 100, 3, BLACK)
    draw_hand(second_angle, 120, 2, RED)

    # -------------------- DIGITAL CLOCK --------------------
    now = pygame.time.get_ticks()
    if now - last_colon_toggle >= COLON_INTERVAL:
        show_colon = not show_colon
        last_colon_toggle = now

    hh = f"{t.tm_hour:02}"
    mm = f"{minute:02}"

    # clear digital area
    pygame.draw.rect(SCREEN, WHITE, (100, 200, 100, 40))

    y = 220
    x_h = 125
    x_c = 150
    x_m = 175

    SCREEN.blit(font.render(hh, True, BLUE),
                font.render(hh, True, BLUE).get_rect(center=(x_h, y)))

    SCREEN.blit(font.render(mm, True, BLUE),
                font.render(mm, True, BLUE).get_rect(center=(x_m, y)))

    if show_colon:
        SCREEN.blit(font.render(":", True, BLUE),
                    font.render(":", True, BLUE).get_rect(center=(x_c, y)))

    # -------------------- UPDATE --------------------
    pygame.display.flip()

pygame.quit()
