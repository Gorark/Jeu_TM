import FreeSimpleGUI as sg
from time import sleep
sg.theme('Dark Grey 13')
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import random
import time
import string
from random import *

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
Good luck!\n"""

def password_game():
    pygame.init()
    # Configuration de la fenêtre
    largeur, hauteur = 800, 600
    fenetre = pygame.display.set_mode((largeur, hauteur))
    pygame.display.set_caption("Hacking Game")

    # Couleurs
    BLANC = (255, 255, 255)
    NOIR = (0, 0, 0)
    ROUGE = (255, 0, 0)
    VERT = (0, 255, 0)
    BLEU = (0, 0, 255)
    GRIS = (200, 200, 200)

    # Police de caractères
    police = pygame.font.SysFont('Arial', 36)
    police_titre = pygame.font.SysFont('Arial', 24, bold=True)

    # Génération d'un mot de passe aléatoire
    def generer_mot_de_passe(longueur=6):
        caracteres = string.ascii_letters + string.digits
        return ''.join(random.choice(caracteres) for _ in range(longueur))

    # Fonction de la barre de progression
    def progress_bar():
        for i in range(101):
            fenetre.fill(NOIR)
            largeur_barre = int(i * 2)
            pygame.draw.rect(fenetre, BLEU, (150, 250, largeur_barre, 50))
            texte = police.render(f"Revealing password: {i}%", True, BLANC)
            fenetre.blit(texte, (400 - texte.get_width() // 2, 320))
            pygame.display.flip()
            pygame.time.delay(30)

    # Fonction du bouton Password Breaker
    def password_breaker_button():
        progress_bar()
        return f"The password is: {mot_de_passe}"

    # Fonction pour afficher un écran de fin
    def afficher_ecran_fin(message_final):
        fenetre.fill(NOIR)
        texte_final = police_titre.render(message_final, True, VERT if "Granted" in message_final else ROUGE)
        fenetre.blit(texte_final, (largeur // 2 - texte_final.get_width() // 2, hauteur // 2 - texte_final.get_height() // 2))
        pygame.display.flip()
        pygame.time.delay(3000)

    mot_de_passe = generer_mot_de_passe()
    attempt = ""
    message = ""
    attempt_count = 0
    max_attempts = 3
    horloge = pygame.time.Clock()
    win = 0  # 0: Perdu, 1: Gagné

    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = event.pos
                if 600 <= x <= 780 and 500 <= y <= 580:
                    message = password_breaker_button()
            elif event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_RETURN:
                    if attempt == mot_de_passe:
                        message = "Access Granted. You Win!"
                        win = 1
                        game_over = True
                    else:
                        message = "Access Denied"
                        attempt_count += 1
                        if attempt_count >= max_attempts:
                            message = f"Access Denied. You Lost. The password was: {mot_de_passe}"
                            win = 0
                            game_over = True
                        attempt = ""
                elif event.key == pygame.K_BACKSPACE:
                    attempt = attempt[:-1]
                else:
                    attempt += event.unicode

        fenetre.fill(NOIR)
        text_attempt = police.render(f"Attempt: {attempt}", True, BLANC)
        text_message = police.render(message, True, ROUGE if message.startswith("Access Denied") else VERT)
        text_attempts_left = police.render(f"Attempts left: {max_attempts - attempt_count}", True, BLANC)
        title = police_titre.render("Password Breaker", True, VERT)

        fenetre.blit(text_attempt, (20, 20))
        fenetre.blit(text_attempts_left, (20, 60))
        if message:
            fenetre.blit(text_message, (20, 100))
        pygame.draw.rect(fenetre, BLANC, (600, 500, 180, 80))
        pygame.draw.rect(fenetre, NOIR, (605, 505, 170, 70))
        title_rect = title.get_rect(center=(605 + 85, 505 + 35))
        fenetre.blit(title, title_rect)

        pygame.display.flip()
        horloge.tick(30)

        if game_over:
            afficher_ecran_fin(message)
            running = False

    pygame.quit()
    return win






def layout1():
    rawtools=[]
    money=0
    mission1won=0
    tools = list(set(rawtools))
    Pswexists = "Password Cracker"  in rawtools
    Decexists = "Decrypter" in rawtools
    Fireexists = "Firewall Bypass"  in rawtools
    IPexists = "IP Probe"  in rawtools
    def MissionHacking():
        if Pswexists!=True:
            if sg.popup_yes_no(f"Watch out, you don't have the Password Breaker, the mission could me harder do you still want to continue?",no_titlebar=True)=="No":
                sg.WIN_CLOSED==None
                
        listeentreprises=["Sigma's Entreprises","Acme Corporation", "InGen", "Monsters, Inc.", "Gringotts", "Umbrella Corporation", "Hooli", "Massive Dynamic", "Wonka Candy Company", "The Krusty Krab", "Dunder Mifflin",]
        randomselection=listeentreprises[randint(0,10)]#il y a 11 termes et 0 est le premier
        if sg.popup_yes_no(f"You have selected the mail from {randomselection}.\nThe speech is as follows:\nInfiltrate a competitor's computer system and sabotage their files.\nHack into a computer and delete key files.\nLocate and destroy crucial data on a main system.\nRequired Tools: Password Cracker\nReward: 1500.-\nDo you want to choose this mission?",no_titlebar=True)=="Yes":
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

    marketdata = ["Password Cracker","Cracks Passwords",1000], ["Decrypter","Decrypt files with equal or lower encryption than the version, by clicking on them. ",5000], ["Firewall Bypass","Bypass the firewall",2500], ["IP Probe","Probe the ip",10000]
    
    tab_layout1 = [[sg.Text("Choose your Mission:")],[sg.Listbox(["Mission 1"],size=(300, 50),enable_events=True,key='LIST')]]
    tab_layout2 = [[sg.Button('Team Management'),]]
    tab_layout3 = [[sg.Text("Buy your favourites tools")],[sg.Table(values=marketdata, headings=["Tools", "Details", "Price"],enable_events=True,hide_vertical_scroll=True,auto_size_columns=True,max_col_width=70,enable_click_events=True,justification='l',select_mode=sg.TABLE_SELECT_MODE_BROWSE,key='Market')]]
    tab_layout4 = [[sg.Text(f"Tools Owned: {tools}",key="-TOOLS-", font=("Calibri", 24))]]
    layout = [[sg.Titlebar("CyberOps Entreprises")],[sg.Text(f"Money Counter: {money}",key="pippo", font=("Calibri", 24))], [sg.Button("Free money")] ]
    #layout.append([sg.Graph(background_color='gray', graph_bottom_left=(0,0), graph_top_right=(2500, 1250), canvas_size=(2500, 1250),key="fond")])
    #rectangle = window['fond'].DrawRectangle((10,10), (1250,1240), fill_color='gray', line_color='black'  )
    layout.append([sg.TabGroup([[sg.Tab("Mission", tab_layout1), sg.Tab("Team", tab_layout2),sg.Tab("Market", tab_layout3),sg.Tab("User", tab_layout4)]])])
    

    window = sg.Window('Generated Layouts', layout, finalize=True)  
    #sg.Popup("Welcome to CyberOps Entreprises.",no_titlebar=True,font="Default 20")
    #sleep(0.2)
    #sg.Popup("You are probably confused we're going to show you around don't worry\n\nFirst head to the [Missions] tab and press the [Mission 1] button for a little check",no_titlebar=True,font="Default 20")
    event, values = window.read()
    
    #print(event, values)
    while True:                             # Event Loop
        event, values = window.read()       # type: str, dict
        print(event,values)
        
        if event=="Free money":
            money+=300
            window['pippo'].update(f"Money Counter:{money}")

            print(money)
        if event in (sg.WIN_CLOSED, '-EXIT-'):         # If the user exits
            break
        if event == 'Market':
            selected_row_index = values['Market'][0]  # Get the index of the selected row +verif documentation
            selected_tool = marketdata[selected_row_index][0]  # Get the data of the selected row and the first column
            selected_price = marketdata[selected_row_index][-1]
            if selected_price > money:
                sg.popup("You don't have enough money to buy that.",no_titlebar=True)
            if selected_price <= money:
                if sg.popup_yes_no(f"Do you want to buy the {selected_tool}  for {selected_price}.-?",no_titlebar=True)=="Yes":
                        money-=selected_price
                        rawtools.append(selected_tool)
                        tools = list(set(rawtools))
                        window['-TOOLS-'].update(f"Tools Owned: {tools}")
                        window['pippo'].update(f"Money Counter:{money}")
                        
                        if Pswexists==True:
                           sg.popup("You successfully bought the Password Cracker",no_titlebar=True)
                        if Decexists==True:
                           sg.popup("You successfully bought the Decrypter",no_titlebar=True)
                        if Fireexists==True:
                           sg.popup("You successfully bought the Firewall Bypass",no_titlebar=True)
                        if IPexists==True:
                           sg.popup("You successfully bought the IP Probe",no_titlebar=True)
                else:
                    sg.WIN_CLOSED==None
         
    
                
        if event == 'LIST' and len(values['LIST']):
            if "Mission 1" in values['LIST']:
                while mission1won != 1:
                    if sg.popup_yes_no("You have selected Mission 1.\nFrom: Your Sensei\nWe need to check that you are a reasonable guy and not a dumbass.\nReward: 1000.-\nDo you want to choose this mission?",no_titlebar=True)=="Yes":
                        if sg.popup_yes_no("You chose this mission, now answer the question to complete it.\nThis is the question:\nIf you enter a stranger's pc do you know the password?",no_titlebar=True)=="Yes":
                            sg.popup("You lost, it is protected you need a tool to know it",no_titlebar=True)
                            sg.WIN_CLOSED==None
                        else:
                            sg.popup("Few... we were right,you are a trustable person.The money will be transfered in your account.",no_titlebar=True)
                            money+=1000
                            window['pippo'].update(f"Money Counter:{money}")
                            mission1won=1
                            window.extend_layout(window['LIST'], [([sg.Listbox(("Sigma's Entreprises", "Mission 3", "Mission 4", "Mission 5"),size=(300, 50),enable_events=True,key='Mission list')])])
                            event, values = window.read()
                            window['LIST'].update(values["LIST"])
                            sg.WIN_CLOSED==None
                            sg.popup("Now let's go try your first true mission.\nHead to  [Sigma's Entreprises]",no_titlebar=True,font="Default 20")                        
                    else:
                        sg.popup("Why are you here then duh.",no_titlebar=True)
                        event, values = window.read()
                        window['LIST'].update(values["LIST"])
                    
            if "Sigma's Entreprises" in values['Mission list']:
                if sg.popup_yes_no("You have selected the mail from Sigma's Entreprises.\nThe speech is as follows:\nInfiltrate a competitor's computer system and sabotage their files.\nHack into a computer and delete key files.\nLocate and destroy crucial data on a main system.\nRequired Tools: Password Cracker\nReward: 1500.-\nDo you want to choose this mission?",no_titlebar=True)=="Yes":
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
            if "Mission 3" in values["Mission list"]:
                MissionHacking()
    window.close()
layout1()