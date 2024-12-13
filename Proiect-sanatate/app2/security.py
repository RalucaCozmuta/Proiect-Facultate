import pygame
import sys
from pygame.locals import *
import hashlib

# Inițializare Pygame
pygame.init()

# Dimensiunile ferestrei
WIDTH, HEIGHT = 500, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Autentificare și Înregistrare")

# Culori
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Fonturi
font = pygame.font.SysFont("Arial", 24)

# Starea aplicației
current_state = "login"  # Poate fi "login", "register" sau "dashboard"

# Baza de date simplificată (în memoria RAM)
users_db = {}

# Funcție pentru desenarea unui text pe ecran
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Funcție pentru criptarea parolelor
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Funcție pentru verificarea autentificării
def authenticate(username, password):
    if username in users_db:
        return users_db[username] == hash_password(password)
    return False

# Funcție pentru a adăuga un utilizator în "baza de date"
def register_user(username, password):
    if username not in users_db:
        users_db[username] = hash_password(password)
        return True
    return False

# Funcția pentru afișarea ecranului de autentificare
def login_screen():
    global current_state
    screen.fill(WHITE)
    draw_text("Autentificare", font, BLACK, screen, 200, 50)

    username_input = ""
    password_input = ""
    username_active = False
    password_active = False
    input_box_color = BLACK

    while current_state == "login":
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # Gestionează clicurile pe input
            if event.type == MOUSEBUTTONDOWN:
                if username_rect.collidepoint(event.pos):
                    username_active = True
                    password_active = False
                elif password_rect.collidepoint(event.pos):
                    password_active = True
                    username_active = False
                else:
                    username_active = False
                    password_active = False

            # Gestionarea tastelor apăsate
            if event.type == KEYDOWN:
                if username_active:
                    if event.key == K_RETURN:
                        # Efectuează autentificarea
                        if authenticate(username_input, password_input):
                            current_state = "dashboard"
                        else:
                            draw_text("Autentificare eșuată", font, RED, screen, 200, 300)
                            pygame.display.update()
                            pygame.time.wait(1000)
                        username_input = ""
                    elif event.key == K_BACKSPACE:
                        username_input = username_input[:-1]
                    else:
                        username_input += event.unicode

                elif password_active:
                    if event.key == K_RETURN:
                        if authenticate(username_input, password_input):
                            current_state = "dashboard"
                        else:
                            draw_text("Autentificare eșuată", font, RED, screen, 200, 300)
                            pygame.display.update()
                            pygame.time.wait(1000)
                        password_input = ""
                    elif event.key == K_BACKSPACE:
                        password_input = password_input[:-1]
                    else:
                        password_input += event.unicode

        # Desenează inputuri
        username_rect = pygame.draw.rect(screen, input_box_color, (150, 120, 200, 32))
        password_rect = pygame.draw.rect(screen, input_box_color, (150, 180, 200, 32))

        draw_text(f"Utilizator: {username_input}", font, BLACK, screen, 150, 100)
        draw_text(f"Parola: {password_input}", font, BLACK, screen, 150, 160)

        pygame.display.update()

# Funcția pentru ecranul de înregistrare
def register_screen():
    global current_state
    screen.fill(WHITE)
    draw_text("Înregistrare", font, BLACK, screen, 200, 50)

    username_input = ""
    password_input = ""
    username_active = False
    password_active = False
    input_box_color = BLACK

    while current_state == "register":
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                if username_rect.collidepoint(event.pos):
                    username_active = True
                    password_active = False
                elif password_rect.collidepoint(event.pos):
                    password_active = True
                    username_active = False
                else:
                    username_active = False
                    password_active = False

            if event.type == KEYDOWN:
                if username_active:
                    if event.key == K_RETURN:
                        if register_user(username_input, password_input):
                            current_state = "login"
                        else:
                            draw_text("Utilizator deja existent!", font, RED, screen, 200, 300)
                            pygame.display.update()
                            pygame.time.wait(1000)
                        username_input = ""
                    elif event.key == K_BACKSPACE:
                        username_input = username_input[:-1]
                    else:
                        username_input += event.unicode

                elif password_active:
                    if event.key == K_RETURN:
                        if register_user(username_input, password_input):
                            current_state = "login"
                        else:
                            draw_text("Utilizator deja existent!", font, RED, screen, 200, 300)
                            pygame.display.update()
                            pygame.time.wait(1000)
                        password_input = ""
                    elif event.key == K_BACKSPACE:
                        password_input = password_input[:-1]
                    else:
                        password_input += event.unicode

        # Desenează inputuri
        username_rect = pygame.draw.rect(screen, input_box_color, (150, 120, 200, 32))
        password_rect = pygame.draw.rect(screen, input_box_color, (150, 180, 200, 32))

        draw_text(f"Utilizator: {username_input}", font, BLACK, screen, 150, 100)
        draw_text(f"Parola: {password_input}", font, BLACK, screen, 150, 160)

        pygame.display.update()

# Funcția pentru ecranul de dashboard
def dashboard_screen():
    global current_state
    screen.fill(WHITE)
    draw_text("Bine ai venit în dashboard!", font, BLACK, screen, 150, 100)

    while current_state == "dashboard":
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Desenează butonul de delogare
        logout_button = pygame.draw.rect(screen, BLUE, (150, 200, 200, 50))
        draw_text("Delogare", font, WHITE, screen, 200, 210)

        if logout_button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            current_state = "login"

        pygame.display.update()

# Loop principal
while True:
    if current_state == "login":
        login_screen()
    elif current_state == "register":
        register_screen()
    elif current_state == "dashboard":
        dashboard_screen()
