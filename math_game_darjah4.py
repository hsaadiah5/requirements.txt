import pygame
import random
import math
import wave
import struct
import os

pygame.init()

# =========================
# SETTING PAPARAN
# =========================
WIDTH, HEIGHT = 1000, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Math Adventure Darjah 4")

WHITE = (255, 255, 255)
PURPLE = (120, 70, 180)
LIGHT_PURPLE = (220, 200, 255)
PINK = (255, 170, 210)
BLUE = (90, 180, 255)
GREEN = (80, 200, 120)
RED = (240, 90, 90)
YELLOW = (255, 220, 90)
DARK = (40, 40, 70)

font_big = pygame.font.SysFont("comicsansms", 48, bold=True)
font_mid = pygame.font.SysFont("comicsansms", 34, bold=True)
font_small = pygame.font.SysFont("comicsansms", 24)

clock = pygame.time.Clock()

# =========================
# BUAT SOUND SENDIRI
# =========================
def create_sound(filename, freq=440, duration=0.2):
    if os.path.exists(filename):
        return

    sample_rate = 44100
    amplitude = 16000
    frames = int(duration * sample_rate)

    with wave.open(filename, "w") as wav_file:
        wav_file.setparams((1, 2, sample_rate, frames, "NONE", "not compressed"))

        for i in range(frames):
            value = int(amplitude * math.sin(2 * math.pi * freq * i / sample_rate))
            wav_file.writeframes(struct.pack("<h", value))

create_sound("correct.wav", 700, 0.18)
create_sound("wrong.wav", 180, 0.25)

correct_sound = pygame.mixer.Sound("correct.wav")
wrong_sound = pygame.mixer.Sound("wrong.wav")

# =========================
# FUNGSI SOALAN
# =========================
def generate_question():
    operasi = random.choice(["+", "-", "×", "÷"])

    if operasi == "+":
        a = random.randint(20, 999)
        b = random.randint(10, 999)
        answer = a + b

    elif operasi == "-":
        a = random.randint(100, 999)
        b = random.randint(10, a)
        answer = a - b

    elif operasi == "×":
        a = random.randint(2, 12)
        b = random.randint(2, 12)
        answer = a * b

    else:
        b = random.randint(2, 12)
        answer = random.randint(2, 12)
        a = b * answer

    question = f"{a} {operasi} {b} = ?"

    choices = [answer]
    while len(choices) < 4:
        wrong = answer + random.randint(-20, 20)
        if wrong != answer and wrong > 0 and wrong not in choices:
            choices.append(wrong)

    random.shuffle(choices)
    return question, answer, choices

# =========================
# BUTANG
# =========================
def draw_button(text, x, y, w, h, color):
    pygame.draw.rect(screen, color, (x, y, w, h), border_radius=20)
    pygame.draw.rect(screen, WHITE, (x, y, w, h), 4, border_radius=20)

    label = font_mid.render(str(text), True, DARK)
    rect = label.get_rect(center=(x + w // 2, y + h // 2))
    screen.blit(label, rect)

    return pygame.Rect(x, y, w, h)

# =========================
# KARAKTER RINGKAS
# =========================
def draw_character(x, y, happy=True):
    pygame.draw.circle(screen, YELLOW, (x, y), 55)
    pygame.draw.circle(screen, DARK, (x - 20, y - 15), 6)
    pygame.draw.circle(screen, DARK, (x + 20, y - 15), 6)

    if happy:
        pygame.draw.arc(screen, DARK, (x - 25, y - 5, 50, 35), 0, math.pi, 4)
    else:
        pygame.draw.arc(screen, DARK, (x - 25, y + 10, 50, 35), math.pi, 2 * math.pi, 4)

    pygame.draw.circle(screen, PINK, (x - 35, y + 5), 10)
    pygame.draw.circle(screen, PINK, (x + 35, y + 5), 10)

# =========================
# BACKGROUND INFOGRAFIK
# =========================
def draw_background():
    screen.fill(LIGHT_PURPLE)

    pygame.draw.circle(screen, PINK, (80, 90), 60)
    pygame.draw.circle(screen, BLUE, (900, 100), 75)
    pygame.draw.circle(screen, YELLOW, (850, 560), 65)
    pygame.draw.circle(screen, GREEN, (120, 540), 70)

    for i in range(0, WIDTH, 80):
        pygame.draw.line(screen, WHITE, (i, 0), (i + 40, HEIGHT), 1)

# =========================
# GAME VARIABLE
# =========================
question, answer, choices = generate_question()
score = 0
total = 0
feedback = ""
happy = True

running = True

# =========================
# LOOP UTAMA
# =========================
while running:
    draw_background()

    title = font_big.render("Math Adventure Darjah 4", True, PURPLE)
    screen.blit(title, (230, 30))

    score_text = font_small.render(f"Markah: {score} / {total}", True, DARK)
    screen.blit(score_text, (40, 30))

    draw_character(150, 220, happy)

    box = pygame.Rect(300, 140, 580, 150)
    pygame.draw.rect(screen, WHITE, box, border_radius=25)
    pygame.draw.rect(screen, PURPLE, box, 5, border_radius=25)

    q_text = font_big.render(question, True, DARK)
    q_rect = q_text.get_rect(center=box.center)
    screen.blit(q_text, q_rect)

    buttons = []
    positions = [
        (300, 350),
        (590, 350),
        (300, 480),
        (590, 480)
    ]

    colors = [BLUE, GREEN, PINK, YELLOW]

    for i, choice in enumerate(choices):
        rect = draw_button(choice, positions[i][0], positions[i][1], 240, 90, colors[i])
        buttons.append((rect, choice))

    if feedback:
        fb_color = GREEN if feedback == "Betul!" else RED
        fb_text = font_mid.render(feedback, True, fb_color)
        fb_rect = fb_text.get_rect(center=(WIDTH // 2, 610))
        screen.blit(fb_text, fb_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            for rect, choice in buttons:
                if rect.collidepoint(mouse_pos):
                    total += 1

                    if choice == answer:
                        score += 1
                        feedback = "Betul!"
                        happy = True
                        correct_sound.play()
                    else:
                        feedback = f"Salah! Jawapan: {answer}"
                        happy = False
                        wrong_sound.play()

                    question, answer, choices = generate_question()

    pygame.display.update()
    clock.tick(60)

pygame.quit()