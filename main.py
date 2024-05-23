import FreeSimpleGUI as sg
from time import sleep
sg.theme('Dark Grey 13')
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import random
import time

# Fonction principale du jeu de hacking
def hacking_game():
    # Initialiser Pygame
    pygame.init()

    # Dimensions de l'écran
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Hacking's Game")

    # Couleurs
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    BLUE = (0, 0, 255)
    SBLUE = (0, 0, 155)

    # Police de caractères
    font = pygame.font.Font(None, 36)

    # Classe pour le joueur
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.Surface((50, 50))
            self.image.fill(GREEN)
            self.rect = self.image.get_rect()
            self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
            self.speed_x = 0
            self.speed_y = 0
            self.hacking = False
            self.hack_progress = 0
            self.hack_fail = False
            self.hack_fail_time = 0
        
        def update(self):
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH
            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.bottom > SCREEN_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT

            if self.hacking:
                self.image.fill(SBLUE)
                self.hack_progress += 1
                if self.hack_progress >= 100:
                    self.hack()
            else:
                self.image.fill(GREEN)
            
            if self.hack_fail and pygame.time.get_ticks() - self.hack_fail_time > 1000:
                self.hack_fail = False

        def hack(self):
            global score, win
            for target in targets:
                if self.rect.colliderect(target.rect):
                    if random.random() < 0.9:  # 90% de chance de succès
                        score += 1
                        if score >= 10:  # Condition de victoire
                            win = True
                    else:
                        score -= 1
                        if score < 0:
                            score = 0
                        self.hack_fail = True
                        self.hack_fail_time = pygame.time.get_ticks()
                    targets.remove(target)
                    all_sprites.remove(target)
                    add_new_target()
                    break
            self.hacking = False
            self.hack_progress = 0

    # Classe pour les cibles de hacking
    class Target(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            self.image = pygame.Surface((50, 50))
            self.image.fill(RED)
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)

    def add_new_target():
        x = random.randint(0, SCREEN_WIDTH - 50)
        y = random.randint(0, SCREEN_HEIGHT // 2)
        target = Target(x, y)
        all_sprites.add(target)
        targets.add(target)

    # Initialisation du joueur et des cibles
    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    targets = pygame.sprite.Group()
    for i in range(5):
        add_new_target()

    # Variables de jeu
    global score, win, game_result
    score = 0
    win = False
    game_result = 0  # Initialiser à 0
    running = True
    clock = pygame.time.Clock()
    start_time = time.time()  # Début du timer
    time_limit = 60  # Limite de temps en secondes

    # Boucle principale du jeu
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player.speed_x = -5
                elif event.key == pygame.K_d:
                    player.speed_x = 5
                elif event.key == pygame.K_w:
                    player.speed_y = -5
                elif event.key == pygame.K_s:
                    player.speed_y = 5
                elif event.key == pygame.K_SPACE:
                    player.hacking = True
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_a, pygame.K_d):
                    player.speed_x = 0
                elif event.key in (pygame.K_w, pygame.K_s):
                    player.speed_y = 0

        # Mise à jour des sprites
        all_sprites.update()

        # Vérifier le timer
        elapsed_time = time.time() - start_time
        if elapsed_time > time_limit:
            running = False
            game_result = 0  # Le joueur a perdu
            break

        # Dessin à l'écran
        SCREEN.fill(BLACK)
        all_sprites.draw(SCREEN)

        # Affichage du score
        score_text = font.render(f"Score: {score}", True, WHITE)
        SCREEN.blit(score_text, (10, 10))

        # Affichage du timer
        timer_text = font.render(f"Temps: {int(time_limit - elapsed_time)}s", True, WHITE)
        SCREEN.blit(timer_text, (SCREEN_WIDTH - 150, 10))

        # Affichage de la barre de progression du hacking
        if player.hacking:
            pygame.draw.rect(SCREEN, BLUE, (player.rect.x, player.rect.y - 10, player.hack_progress, 5))

        # Affichage du message d'échec de hacking
        if player.hack_fail:
            fail_text = font.render("Hacking failed !", True, RED)
            SCREEN.blit(fail_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))

        # Condition de victoire
        if win:
            game_result = 1  # Le joueur a gagné
            win_text = font.render("You Won !", True, WHITE)
            SCREEN.blit(win_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False

        pygame.display.flip()
        clock.tick(60)

    # Affichage du message de défaite si le temps est écoulé
    if not win:
        lose_text = font.render("Time elapsed ! You lost.", True, RED)
        SCREEN.blit(lose_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(3000)

    pygame.quit()
    return game_result
Hack_Rules = """Game Controls and Rules\n
Controls:\n
- Move Up: W\n
- Move Down: S\n
- Move Left: A\n
- Move Right: D\n
- Start Hacking: SPACE\n
\n
Rules:\n
1. Objective: Hack 10 targets within 1 minute.\n
2. Hacking:\n
   - Move close to a red target.\n
   - Press SPACE to start hacking (player turns blue, progress bar appears).\n
   - If successful (90% chance), the target disappears and a new one spawns. If it fails, your score decreases.\n
3. Win Condition: Reach a score of 10 within the time limit.\n
4. Lose Condition:\n
   - If time runs out before reaching 10, you lose.\n
   - Failed hack shows "Hacking Failed!" message.\n
   - Timer at top right shows remaining time. If time runs out, "Time's up! You lost." message is displayed.\n
\n
Good luck!\n"""

tools=[]




def layout1():
    money=0
    tab_layout1 = [[sg.Text("Choose your Mission:"),sg.Listbox(["Mission 1"],size=(300, 50),enable_events=True,key='LIST')]]
    tab_layout2 = [[sg.Button('Team Management'),]]
    layout = [[sg.Text(f"Money Counter: {money}",key="pippo", font=("Calibri", 24))], [sg.Button("Free money")] ]
    #layout.append([sg.Graph(background_color='gray', graph_bottom_left=(0,0), graph_top_right=(2500, 1250), canvas_size=(2500, 1250),key="fond")])
    #rectangle = window['fond'].DrawRectangle((10,10), (1250,1240), fill_color='gray', line_color='black'  )
    layout.append([sg.TabGroup([[sg.Tab("Mission", tab_layout1), sg.Tab("Team", tab_layout2)]])])
    

    window = sg.Window('Generated Layouts', layout, finalize=True)  
    #sg.Popup("Welcome to CyberOps Entreprises.",no_titlebar=True,font="Default 20")
    #sleep(0.2)
    #sg.Popup("You are probably confused we're going to show you around don't worry\n\nFirst head to the [Missions] tab and press the [Mission 1] button for a little check",no_titlebar=True,font="Default 20")
    event, values = window.read()
    
    #print(event, values)
    while True:                             # Event Loop
        event, values = window.read()       # type: str, dict
        #print(event)
        if event=="Free money":
            money+=300
            window['pippo'].update(f"Money Counter:{money}")

            print(money)
        if event in (sg.WIN_CLOSED, '-EXIT-'):         # If the user exits
            break
        if event == 'LIST' and len(values['LIST']):
            if "Mission 1" in values['LIST']:
                if sg.popup_yes_no("You have selected Mission 1.\nFrom: Your Sensei\nWe need to check that you are a reasonable guy and not a dumbass.\nReward: 1000.-\nDo you want to choose this mission?",no_titlebar=True)=="Yes":
                    if sg.popup_yes_no("You chose this mission, now answer the question to complete it.\nThis is the question:\nIf you enter a stranger's pc do you know the password?",no_titlebar=True)=="Yes":
                        sg.popup("You lost, it is protected you need a tool to know it",no_titlebar=True)
                        sg.WIN_CLOSED==None
                    else:
                        sg.popup("Few... we were right,you are a trustable person.The money will be transfered in your account.",no_titlebar=True)
                        money+=1000
                        tools.append("Password Cracker")
                        window['pippo'].update(f"Money Counter:{money}")
                        window.extend_layout(window['LIST'], [([sg.Listbox(("Sigma", "Mission 3", "Mission 4", "Mission 5"),size=(300, 50),enable_events=True,key='LIST')])])
                        sg.WIN_CLOSED==None
                        sg.popup("Now let's go try your first true mission.\nHead to  [Sigma]",no_titlebar=True,font="Default 20")

                else:
                    sg.popup("Why are you here then duh.",no_titlebar=True)
                    sg.WIN_CLOSED==None
            if "Sigma" in values['LIST']:
                if sg.popup_yes_no("You have selected Sigma.\nThe speech is as follows:\nInfiltrate a competitor's computer system and sabotage their files.\nHack into a computer and delete key files.\nLocate and destroy crucial data on a main system.\nRequired Tools: Password Cracker, Surveillance Bypass\nReward: 1500.-\nDo you want to choose this mission?",no_titlebar=True)=="Yes":
                    sg.popup(f"{Hack_Rules}",no_titlebar=True)
                    result = hacking_game()
                    if result==1:
                        sg.popup("GG You won",no_titlebar=True)
                        money+=1500
                        window['pippo'].update(f"Money Counter:{money}")
                    if result==0:
                        sg.popup("You lost",no_titlebar=True)
                        sg.WIN_CLOSED==None

                else:
                    
                    sg.WIN_CLOSED==None
    window.close()
layout1()