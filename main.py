import FreeSimpleGUI as sg
from time import sleep
sg.theme('Dark Grey 11')
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" #copié depuis internet
import pygame
import time
import string
import datetime
from random import *

# CONSTANTS

EMPLOYEE_TIMEOUT_SECONDS=120

# Fonction principale du jeu de hacking
def hacking_game():#créé avec IA(ChatGpt3.5), je l'ai guidée dans le developpement, la première requête était celle-ci"Code me a game that take the mechanic of hacking and reminds of hacking with a hacking driven graphics, the game should have a 90% win ratio"
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
                    if random() < 0.9:  # 90% de chance de succès
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
        x = randint(0, SCREEN_WIDTH - 50)
        y = randint(0, SCREEN_HEIGHT // 2)
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
    time_limit = 45  # Limite de temps en secondes

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
# le texte de règles ci dessous a été créé avec IA, j'ai demandé à la suite de la conversation plus haut:"Fait moi une explication des touches et des règles du jeu en anglais"
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

def password_game(): #créé avec IA,(ChatGpt3.5) avec cette commande"Create a hackign game in which you have to crack a password, make it a callable function le jeu doit être dans une fenêtre et avoir un gui plaisant, le mots de passe doit  être aléatoire mais trouvable grâce à une certain logique de laprt de l'utilisateur" 
    global Pswexists #la suite de l'integration du jeu a été faite par moi
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
        return ''.join(choice(caracteres) for _ in range(longueur))

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

    # Fonction du bouton Password Cracker
    def password_Cracker_button():
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
                if Pswexists and 600 <= x <= 780 and 500 <= y <= 580:
                    message = password_Cracker_button()
            elif event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_RETURN:
                    if attempt == mot_de_passe:
                        message = "Access Granted."
                        win = 1
                        game_over = True
                    else:
                        message = "Access Denied"
                        attempt_count += 1
                        if attempt_count >= max_attempts:
                            message = f"Access Denied. You Lost." # The password was: {mot_de_passe}
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
        title = police_titre.render("Password Cracker", True, VERT)

        fenetre.blit(text_attempt, (20, 20))
        fenetre.blit(text_attempts_left, (20, 60))
        if message:
            fenetre.blit(text_message, (20, 100))
        if Pswexists:
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







rawtools=[]
money=1000
mission1won=0
tools = list(set(rawtools))
pswcount=0
employees_owned = []
removed_employees = []
employed_employees ={}
tuple_employed_employees=[f'{key} {value}' for key, value in employed_employees.items()]
dictionnary_free_employees = {}
tuple_free_employees=[f'{key} {value}' for key, value in dictionnary_free_employees.items()]
list_free_employees= [f'{key} {value}' for key, value in dictionnary_free_employees.items()]
employees_owned_string = [ str(emp) for emp in employees_owned ]
removed_employees_string = [ str(emp) for emp in removed_employees]
tools=["Password Cracker","Decrypter","Firewall Bypass","Log Eraser"] 
Pswexists = "Password Cracker" in rawtools
Decexists = "Decrypter" in rawtools
Fireexists = "Firewall Bypass" in rawtools
IPexists = "Log Eraser" in rawtools
class Mission:
    def __init__(self, name):
        self.name = name
        self.dangerosity = randint(1,3)
        self.nb_employees = randint(1, min(4, len(tools)))
        self.missiontype=randint(0, 1)
        self.toolsrequired=randomtoolsnumber(self.nb_employees)
class Employee:
    def __init__(self, name, tool,  braveness):
        self.name = name
        self.tool = tool
        self.braveness = braveness
        self.last_used = None

    def __str__(self):
        return f"{self.name},{self.tool},Braveness Level:{self.braveness}"

    def use(self):
        self.last_used = datetime.datetime.now()
        available_employee = self.last_used + datetime.timedelta(seconds=EMPLOYEE_TIMEOUT_SECONDS)
        sg.popup(f"Unavailable employee {self.name} until {available_employee}",no_titlebar=True)

    def is_available(self):
        if self.last_used == None:
            return True
        
        if datetime.datetime.now() - self.last_used >= datetime.timedelta(seconds=EMPLOYEE_TIMEOUT_SECONDS):
            return True
        else:
            return False




def MissionNames():
    listeentreprises=["Acme Corporation", "InGen", "Monsters, Inc.", "Gringotts", "Umbrella Corporation", "Hooli", "Massive Dynamic", "Wonka Candy Company", "The Krusty Krab", "Dunder Mifflin", "Cyberdyne Systems", "Wayne Enterprises", "Stark Industries", "Oscorp", "LexCorp", "Tyrell Corporation", "Nakatomi Trading Corporation", "Omni Consumer Products (OCP)", "Blue Sun Corporation", "Vehement Capital Partners", "Globex Corporation", "Soylent Corp", "Initech", "Callister Inc", "Cheers", "Ollivander's Wand Shop", "Gekko and Co.", "The Dharma Initiative", "Wally World", "The Leftorium", "McDowell’s", "Bada Bing", "Vitameatavegamin", "Bushwood Country Club", "Consumer Recreation Services", "The Max", "Mel’s Diner", "Paper Street Soap Company", "The Foundation", "The Peach Pit", "Merrick BioTech", "The Reef", "Macmillan Toys", "Blue Moon Detective Agency", "Stay Puft Corporation", "Silver Shamrock", "El Banco Corrupto", "Victoria’s Circuit", "Madam Malkin’s Robes for All Occasions", "Arcade Flower Shop", "Atlantic American Airlines", "KACL", "Flingers"]
    randomselection=listeentreprises[randint(0,len(listeentreprises)-1)]
    return randomselection        


def MissionChooser(n):
    Missiontypes = [1, 2]
    n = randint(0, 1)
    if n == 0:
        Missionchoosen = MissionHacking()
    elif n == 1:
        Missionchoosen = MissionPassword()
    return Missionchoosen
def Missionadder():
    missions.clear()
    for i in range(5):
        mission_name = MissionNames()
        mission = Mission(mission_name)
        missions.append(mission)
    event, values = window.read()
    window['Mission list'].update(values=[mission.name for mission in missions])
def yes_no_popup_listbox(title, message, options,message2, default_values=None):
    if default_values is None:
        default_values = []
    layout = [
        [sg.Text(message)],
        [sg.Listbox(options, default_values=default_values, key='LIST', 
                    select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, size=(50, 6))],
        [sg.Text(message2)],
        [sg.Button('Yes'), sg.Button('No')]
    ]

    window = sg.Window(title, layout, modal=True, enable_close_attempted_event=True)
    
    while True:
        event, values = window.read()
        
        if event in (sg.WINDOW_CLOSED, sg.WINDOW_CLOSE_ATTEMPTED_EVENT):
            result = ('Close', [])
            break
        elif event in ('Yes', 'No'):
            result = (event, values['LIST'])
            break
    window.close()
    return result
def randomnamegenerator():
    first_names = ['John', 'Emma', 'Michael', 'Sophia', 'William', 'Olivia', 'James', 'Ava', 'Robert', 'Isabella', 
                'David', 'Mia', 'Joseph', 'Charlotte', 'Daniel', 'Amelia', 'Thomas', 'Harper', 'Christopher', 'Evelyn']

    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez', 
                'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin']

    random_first_name = choice(first_names)
    random_last_name = choice(last_names)

    rdmname = f"{random_first_name} {random_last_name}"
    return rdmname
def randombravenessgenerator():
    braveness=[3,2,1] 
    random_braveness = choice(braveness)

    return random_braveness
def randomtoolgenerator():
    tools=["Password Cracker","Decrypter","Firewall Bypass","Log Eraser"] 
    random_tools = choice(tools)
    return random_tools 
def randomtoolsnumber(chosennbemployees):
        selected_tools = sample(tools, chosennbemployees)
        return selected_tools 

def employeesgenerator():
    bravenessnew=randombravenessgenerator()
    employees_price=10000+(bravenessnew*2500)
    return randomnamegenerator(),randomtoolgenerator(),bravenessnew,employees_price

def get_emp_object_by_string(emp_string):
    for emp in employees_owned:
        if str(emp) == emp_string:
            return emp
def get_mis_object_by_string(mis_string):
    for mis in missions:
        if mis.toolsrequired == mis_string:
            return mis
        

def reussitemission():
    global selected_options
    total_braveness = 0
    
    
    for emp_string in selected_options:
        
        emp = get_emp_object_by_string(emp_string)
        total_braveness += emp.braveness

    print("total braveness", total_braveness)
    txreussite=((((0.6*len(selected_options))/chosennbemployees))*100+((len(selected_options)*chosendangerosity)-(total_braveness))*5)
    if randint(1,100) < txreussite:
        resultat="Win"
    else:
        resultat="Lose"
    print("tx",txreussite)
    print("len:",len(selected_options))
    return resultat
def dangerositygenerator():
    dangerosity=randint(1,3)
    return dangerosity
def nbremployeesgenerator():
    nbremployees=randint(1,3)
    return nbremployees
dangerosity = dangerositygenerator()
nb_employees = nbremployeesgenerator()


marketdata = (["Password Cracker","Cracks Passwords",1000], ["Decrypter","Decrypt files by clicking on them. ",5000], ["Firewall Bypass","Bypass the firewall",2500], ["Log Eraser","Erase the logs",10000])   
Teamshop=[*employeesgenerator()],[*employeesgenerator()],[*employeesgenerator()]
missions=[]
tab_layout1 = [[sg.Text("Choose your Mission:")],[sg.Listbox(values=[mission.name for mission in missions],size=(300, 50),enable_events=True,key="Mission list")]]
tab_layout2 = [[sg.Text(f"Here are all your employees :",key="TEAM", font=("Calibri", 24))],[sg.Table(values=tuple_free_employees, headings=["Name", "Skills","Level of Braveness"],enable_events=True,hide_vertical_scroll=True,auto_size_columns=True,max_col_width=70,enable_click_events=True,justification='l',select_mode=sg.TABLE_SELECT_MODE_BROWSE,key='freeemployees')]]
tab_layout3 = [[sg.Text("Buy your favourites tools")],[sg.Table(values=marketdata, headings=["Tools", "Details", "Price"],enable_events=True,hide_vertical_scroll=True,auto_size_columns=True,max_col_width=70,enable_click_events=True,justification='l',select_mode=sg.TABLE_SELECT_MODE_BROWSE,key='Market')],[sg.Text("Buy Workers for your Entreprise!")],[sg.Table(values=Teamshop, headings=["Name", "Skills","Level of Braveness", "Price"],enable_events=True,hide_vertical_scroll=True,auto_size_columns=True,max_col_width=70,enable_click_events=True,justification='l',select_mode=sg.TABLE_SELECT_MODE_BROWSE,key='WORKERSHOP')]] #besoin d'une tuple pas d'une liste
tab_layout4 = [[sg.Text(f"Tools Owned: {tools}",key="-TOOLS-", font=("Calibri", 24))]]
layout = [[sg.Titlebar("CyberOps Entreprises")],[sg.Text(f"Money Counter: {money}",key="pippo", font=("Calibri", 24))]]
layout.append([sg.TabGroup([[sg.Tab("Mission", tab_layout1), sg.Tab("Team", tab_layout2),sg.Tab("Market", tab_layout3),sg.Tab("User", tab_layout4)]]), [sg.Button("Free money")] ])
window = sg.Window('CyberOps Entreprises', layout, finalize=True) 
Missionadder()
selected_indices = window["Mission list"].get_indexes()
if selected_indices:
    chosenmission = selected_indices[0]

def MissionHacking():
    global money
    global selected_options
    global list_free_employees
    global chosenmissionnumber,chosenmission,chosendangerosity,chosennbemployees,employees_owned_string
    Pswexists = "Password Cracker" in rawtools
    result=150 #pour éviter de faire bugger le result on le defini avec une valeur au pif
    selected_indices = window["Mission list"].get_indexes()
    pswtext=["recover access to a critical server after the password was lost", "investigate potential insider threats by accessing encrypted files", "retrieve data from a locked device for a legal case", "test the security of their systems against potential breaches", "access an employee's account after they left the company without sharing credentials", "bypass forgotten passwords on essential software", "ensure compliance with cybersecurity regulations by testing password strength", "recover encrypted data after a ransomware attack", "access backup systems when primary credentials fail", "audit and improve password policies by identifying weak points."]
    randompswtext=pswtext[randint(0,len(pswtext)-1)]
    chosenpswtext=randompswtext

    if selected_indices:
        chosenmissionnumber = selected_indices[0] 
        chosenmission=selected_mission.name
        chosendangerosity=selected_mission.dangerosity
        chosennbemployees=selected_mission.nb_employees
        chosentoolsrequired=selected_mission.toolsrequired
        chosentools_string = ",".join(chosentoolsrequired)
        moneyreward=int(2000*chosennbemployees*chosendangerosity*0.3)
        employees_owned_available = []
        for employee_owned_elem in employees_owned:
            if employee_owned_elem.is_available():
                employees_owned_available.append(employee_owned_elem)
        employees_owned_string = [ str(emp) for emp in employees_owned_available]
        result, selected_options = yes_no_popup_listbox(#besoin d'une liste pas d'un tuple
                'Mission Mail',
                f"You have selected the mail from {chosenmission}\nThe speech is as follows:\n{chosenpswtext}\nRequired Tools: {chosentools_string}\n{chosennbemployees} or more employees required\n Danger Level {chosendangerosity}\n Reward: {moneyreward}.-\n Here you can select the employees you want to send",
                employees_owned_string,
                "Do you want to choose this mission?"
            )
        if result == 'Yes':
            if selected_options:
                if len(selected_options) >= chosennbemployees and len(selected_options)!=0:
                    chosentoolsrequired_temp = chosentoolsrequired
                    for tool in chosentoolsrequired:
                        for emp_str in selected_options:
                            if get_emp_object_by_string(emp_str).tool in chosentoolsrequired_temp:
                                chosentoolsrequired_temp.remove(get_emp_object_by_string(emp_str).tool)
                    if len(chosentoolsrequired_temp) == 0:
                        print("we have all tools")
                        sg.popup(f'You Selected those employees and they have the required tools: {", ".join(selected_options)}',no_titlebar=True)
                        resultat=reussitemission()
                    sg.popup(f'You Selected those employees and they have the required tools: {", ".join(selected_options)}',no_titlebar=True)
                    resultat=reussitemission()
                    if resultat=="Win":
                        money+=moneyreward
                        window['pippo'].update(f"Money Counter:{money}")
                        sg.popup(f'You completed the mission with success\n The employees you sent will be unavailable for 2 minutes, you will receive a pop-up when they are back',no_titlebar=True)
                        Missionadder()
                    if resultat=="Lose":
                        sg.popup(f'You failed the mission\n The employees you sent will be unavailable for 2 minutes,',no_titlebar=True)
                        money-=moneyreward*2
                        window['pippo'].update(f"Money Counter:{money}")
                        Missionadder()
                    for emp_str in selected_options:
                        get_emp_object_by_string(emp_str).use()
                    else:
                        sg.popup("You miss these tools:", ",".join(chosentoolsrequired_temp))
                        sg.WIN_CLOSED==None

                if len(selected_options) < chosennbemployees:
                    sg.popup("You did not select enough employees")
                    sg.WIN_CLOSED==None
            else:
                sg.popup('You are going to complete the mission alone because you selected no employees',no_titlebar=True)
                sg.popup("Now you will start the hacking those are the rules ",no_titlebar=True)
                sg.popup(f"{Hack_Rules}",no_titlebar=True)
                result = hacking_game()
                if result==1:
                    sg.popup("You completed the mission with success.\nTake your money reward.",no_titlebar=True)
                    money+=moneyreward
                    window['pippo'].update(f"Money Counter:{money}")
                    Missionadder()
                if result==0:
                    sg.popup("You failed the mission",no_titlebar=True)
                    money-=moneyreward*2
                    window['pippo'].update(f"Money Counter:{money}")
                    sg.WIN_CLOSED==None
                    Missionadder()
        elif result == 'No':
            sg.WIN_CLOSED==None
def MissionPassword():
    global money
    global selected_options
    global list_free_employees
    global chosenmissionnumber,chosenmission,chosendangerosity,chosennbemployees,employees_owned_string
    Pswexists = "Password Cracker" in rawtools
    result=150 #pour éviter de faire bugger le result on le defini avec une valeur au pif
    selected_indices = window["Mission list"].get_indexes()
    pswtext=["recover access to a critical server after the password was lost", "investigate potential insider threats by accessing encrypted files", "retrieve data from a locked device for a legal case", "test the security of their systems against potential breaches", "access an employee's account after they left the company without sharing credentials", "bypass forgotten passwords on essential software", "ensure compliance with cybersecurity regulations by testing password strength", "recover encrypted data after a ransomware attack", "access backup systems when primary credentials fail", "audit and improve password policies by identifying weak points."]
    randompswtext=pswtext[randint(0,len(pswtext)-1)]
    chosenpswtext=randompswtext

    if selected_indices:
        chosenmissionnumber = selected_indices[0] 
        chosenmission=selected_mission.name
        chosendangerosity=selected_mission.dangerosity
        chosennbemployees=selected_mission.nb_employees
        chosentoolsrequired=selected_mission.toolsrequired
        chosentools_string = ",".join(chosentoolsrequired)
        moneyreward=int(2000*chosennbemployees*chosendangerosity*0.3)
        pswrequired=["Password Cracker"]
        employees_owned_available = []
        for employee_owned_elem in employees_owned:
            if employee_owned_elem.is_available():
                employees_owned_available.append(employee_owned_elem)
        employees_owned_string = [ str(emp) for emp in employees_owned_available]
        result, selected_options = yes_no_popup_listbox(#besoin d'une liste pas d'un tuple
                'Mission Mail',
                f"You have selected the mail from {chosenmission}\nThe speech is as follows:\n{chosenpswtext}\nRequired Tools: {pswrequired}\n{chosennbemployees} or more employees required\n Danger Level {chosendangerosity}\n Reward: {moneyreward}.-\n Here you can select the employees you want to send",
                employees_owned_string,
                "Do you want to choose this mission?"
            )
        if result == 'Yes':
            if selected_options:
                if len(selected_options) >= chosennbemployees and len(selected_options)!=0:
                    chosentoolsrequired_temp = chosentoolsrequired
                    for tool in pswrequired:
                        for emp_str in selected_options:
                            if get_emp_object_by_string(emp_str).tool in pswrequired:
                                pswrequired.remove(get_emp_object_by_string(emp_str).tool)
                    if len(pswrequired) == 0:
                        print("we have all tools")
                    else:
                        sg.popup("You miss these tools:", ",".join(pswrequired))
                        sg.WIN_CLOSED==None

                    sg.popup(f'You Selected those employees and they have the required tools: {", ".join(selected_options)}',no_titlebar=True)
                    resultat=reussitemission()
                    if resultat=="Win":
                        money+=moneyreward
                        window['pippo'].update(f"Money Counter:{money}")
                        sg.popup(f'You completed the mission with success\n The employees you sent will be unavailable for 2 minutes, you will receive a pop-up when they are back',no_titlebar=True)
                        Missionadder()
                    if resultat=="Lose":
                        sg.popup(f'You failed the mission\n The employees you sent will be unavailable for 2 minutes,',no_titlebar=True)
                        money-=moneyreward*2
                        window['pippo'].update(f"Money Counter:{money}")
                        Missionadder()
                    for emp_str in selected_options:
                        get_emp_object_by_string(emp_str).use()

                if len(selected_options) < chosennbemployees:
                    sg.popup("You did not select enough employees")
                    sg.WIN_CLOSED==None
            else:
                sg.popup('You are going to complete the mission alone because you selected no employees',no_titlebar=True)
                if Pswexists==True: 
                    result = password_game()
                    if result==1:
                        sg.popup("You completed the mission with success",no_titlebar=True)
                        money+=moneyreward
                        
                        window['pippo'].update(f"Money Counter:{money}")
                        Missionadder()
                    if result==0:
                        sg.popup("You failed the mission",no_titlebar=True)
                        money-=moneyreward*2
                        window['pippo'].update(f"Money Counter:{money}")
                        sg.WIN_CLOSED==None
                        Missionadder()
                    else:               
                        sg.WIN_CLOSED==None 
                if Pswexists!=True:
                            if sg.popup_yes_no(f"Watch out, you don't have the Password Cracker, the mission could be harder do you still want to continue?",no_titlebar=True)=="No":
                                sg.WIN_CLOSED==None
                            else:
                                result = password_game()
                                if result==1:
                                    sg.popup("You completed the mission with success",no_titlebar=True)
                                    money+=moneyreward
                                    
                                    window['pippo'].update(f"Money Counter:{money}")
                                    Missionadder()
                                if result==0:
                                    sg.popup("You failed the mission",no_titlebar=True)
                                    money-=moneyreward*2
                                    window['pippo'].update(f"Money Counter:{money}")
                                    sg.WIN_CLOSED==None
                                    Missionadder()
                                else:             
                                    sg.WIN_CLOSED==None  
                               
                        
        elif result == 'No':
            sg.WIN_CLOSED==None
sg.Popup("Welcome to CyberOps Entreprises.",no_titlebar=True,font="Default 20")

sleep(0.2)
sg.Popup("You are probably confused we're going to show you around don't worry\n\nFirst head to the [Market] to buy your first tool",no_titlebar=True,font="Default 20")
event, values = window.read()

while True:                             
    event, values = window.read()       
    #print(event,values)
    Pswexists = "Password Cracker" in rawtools
    Decexists = "Decrypter" in rawtools
    Fireexists = "Firewall Bypass" in rawtools
    IPexists = "Log Eraser" in rawtools
    if event=="Free money":
        money+=30000
        window['pippo'].update(f"Money Counter:{money}")

        print(money)
    if event in (sg.WIN_CLOSED, '-EXIT-'):         
        break
    if event == 'Market':
        selected_row_index = values['Market'][0]  # Donne l' index de la ligne séléctionnée
        selected_tool = marketdata[selected_row_index][0]  # Donne les données de la ligne et de la première colonne selectionnées 
        selected_price = marketdata[selected_row_index][-1]
        if selected_tool in rawtools:
            sg.popup("You already bought that tool.",no_titlebar=True)
        else:
            if selected_price > money:
                sg.popup("You don't have enough money to buy that.",no_titlebar=True)
            if selected_price <= money:
                if sg.popup_yes_no(f"Do you want to buy the {selected_tool}  for {selected_price}.-?",no_titlebar=True)=="Yes":
                        money-=selected_price
                        rawtools.append(selected_tool)
                        tools = list(set(rawtools))
                        window['-TOOLS-'].update(f"Tools Owned: {tools}")
                        window['pippo'].update(f"Money Counter:{money}")
                        Pswexists = "Password Cracker" in rawtools
                        
                        sg.popup(f"You successfully bought the {selected_tool}",no_titlebar=True)
                        if Pswexists==True and pswcount==0:
                            sg.popup("The tools are a way of completing mission, if you do not own the tools required in the mission mail you won't be able to complete it\nNow let's go try your first true mission with this tool.\n Head to [Missions] and choose one that requires the Password Cracker only",no_titlebar=True,font="Default 20")
                            pswcount+=1
                        
                sg.WIN_CLOSED==None
    if event == "WORKERSHOP":
        if len(values["WORKERSHOP"]) == 0:#évite un index out of range
            sleep(0.5)
        else:
            selected_row_index = values["WORKERSHOP"][0]  
            selected_worker = Teamshop[selected_row_index][0] 
            selected_skill = Teamshop[selected_row_index][1]
            selected_braveness = Teamshop[selected_row_index][2]
            selected_price = Teamshop[selected_row_index][-1]
            if selected_worker in employees_owned:
                sg.popup("Easter EGG",no_titlebar=True)
            else:
                if selected_price > money:
                    sg.popup("You don't have enough money to recruit him.",no_titlebar=True)
                if selected_price <= money:
                    if sg.popup_yes_no(f"Do you want to recruit {selected_worker}  for {selected_price}.-?",no_titlebar=True)=="Yes":
                            money-=selected_price
                            name=selected_worker
                            tool=selected_skill 
                            braveness=selected_braveness  
                            employee = Employee(name, tool,braveness)
                            employees_owned.append(employee)
                            tuple_free_employees=tuple_free_employees+([[selected_worker,selected_skill,selected_braveness]])
                            employees_owned_string = [ str(emp) for emp in employees_owned ]
                            print(tuple_free_employees) 
                            window['freeemployees'].update(tuple_free_employees)
                            Teamshop=()
                            Teamshop=([*employeesgenerator(),10000],[*employeesgenerator(),10000],[*employeesgenerator(),10000])
                            window['WORKERSHOP'].update(Teamshop)
                            window['pippo'].update(f"Money Counter:{money}")
                            sg.popup(f"You successfully recruited {selected_worker}",no_titlebar=True)
                            if len(employees_owned)==1:
                                sg.popup(f"You successfully recruited your first employee!\nYou can use them to complete missions, as you might have noticed they have different tools and Braveness levels.\nKeep that in mind when you are sending them into a mission and watch out for the required number of employees too!",no_titlebar=True,font="Default 20")       
                    sg.WIN_CLOSED==None
        

            
    if event == 'Mission list' and len(values['Mission list']):
        selected_mission_name = values['Mission list'][0]
        for mission in missions:
            if mission.name == selected_mission_name:
                selected_mission = mission
                break
        
        MissionChooser(mission.missiontype)
window.close()
