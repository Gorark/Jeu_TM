import pygame
import random
import string

def password_game():
    global pswexists
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
                if Pswexists and 600 <= x <= 780 and 500 <= y <= 580:
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

# Exécutez le jeu
resultat = password_game()
print("Résultat du jeu:", "Gagné" if resultat == 1 else "Perdu")
