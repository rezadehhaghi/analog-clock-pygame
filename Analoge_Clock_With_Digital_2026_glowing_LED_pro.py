import pygame
import math
import time

# -------------------- INIT --------------------
pygame.init()
SCREEN = pygame.display.set_mode((300, 300))
pygame.display.set_caption("Bauhaus Industrial Clock")
CLOCK = pygame.time.Clock()

# -------------------- COLORS (YOUR CHOICES) --------------------
BG     = (25, 25, 25)     # matte dark gray
FACE   = (230, 230, 230)  # neutral white
HANDS  = (0, 0, 0)        # pure black
SECOND = (180, 40, 40)    # restrained red
DIGIT  = (100, 100, 100) # soft gray
GLOW   = (120, 120, 120) # subtle glow

# -------------------- FONT --------------------
FONT_PATH = "DS-DIGI.TTF"
FONT_SIZE = 32

# -------------------- COLON BLINK --------------------
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

def draw_text(surface, text, font_path, size, color, pos):
    font = pygame.font.Font(font_path, size)
    surf = font.render(text, True, color)
    surface.blit(surf, surf.get_rect(center=pos))

# -------------------- MAIN LOOP --------------------
running = True
while running:
    CLOCK.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # -------------------- TIME (CORRECT & SMOOTH) --------------------
    t = time.localtime()
    frac = time.time() % 1

    hour   = t.tm_hour
    minute = t.tm_min
    second = t.tm_sec + frac

    # -------------------- BACKGROUND --------------------
    SCREEN.fill(BG)

    # -------------------- CLOCK FACE --------------------
    pygame.draw.circle(SCREEN, BG,   (150, 150), 130)
    pygame.draw.circle(SCREEN, FACE, (150, 150), 140)
    

    # hour marks
    for i in range(12):
        a = i * 30
        s, c = sin_cos(a)
        pygame.draw.line(
            SCREEN, HANDS,
            (150 + 115 * s, 150 - 115 * c),
            (150 + 135 * s, 150 - 135 * c),
            3
        )

    # -------------------- HAND ANGLES --------------------
    second_angle = second * 6
    minute_angle = (minute + second / 60) * 6
    hour_angle   = (hour % 12 + minute / 60 + second / 3600) * 30

    # -------------------- HANDS --------------------
    draw_hand(hour_angle,   60, 5, HANDS)
    draw_hand(minute_angle, 90, 3, HANDS)
    draw_hand(second_angle,110, 2, SECOND)

    # -------------------- DIGITAL CLOCK --------------------
    now_ms = pygame.time.get_ticks()
    if now_ms - last_colon_toggle >= COLON_INTERVAL:
        show_colon = not show_colon
        last_colon_toggle = now_ms

    hh = f"{hour:02}"
    mm = f"{minute:02}"

    # digital background (YOUR RECT)
    pygame.draw.rect(SCREEN, FACE, (110, 200, 90, 40))

    y = 220
    x_h = 130
    x_c = 150
    x_m = 175

    draw_text(SCREEN, hh, FONT_PATH, FONT_SIZE, DIGIT, (x_h, y))
    draw_text(SCREEN, mm, FONT_PATH, FONT_SIZE, DIGIT, (x_m, y))
    if show_colon:
        draw_text(SCREEN, ":", FONT_PATH, FONT_SIZE, DIGIT, (x_c, y))

    # -------------------- UPDATE --------------------
    pygame.display.flip()

pygame.quit()
