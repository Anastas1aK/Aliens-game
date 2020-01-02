import pygame
import random

pygame.init()

display_width = 800
display_height = 600

display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Igra')


class Alians:
    def __init__(self, alien_x, alien_y, alien_width, alien_height, alien_img ):
        self.alien_x = alien_x
        self.alien_y = alien_y
        self.alien_width = alien_width
        self.alien_height = alien_height
        self.alien_img = alien_img

    def generate(self):
        self.alien_y = random.randrange(-600, -200)
        self.alien_x = random.randint(0, 747)

    def go(self):
        if self.alien_y <= display_height:
            display.blit(alien_img, (self.alien_x, self.alien_y))
            if scores <= 200:
                self.alien_y += 10
            elif 200 < scores <= 400:
                self.alien_y += 15
            elif 400 < scores <= 700:
                self.alien_y += 20
            elif 700 < scores <= 900:
                self.alien_y += 16
            elif 700 < scores <= 1400:
                self.alien_y += 12


    def pos(self):
        if self.alien_y <= display_height:
            return 0
        else:
            return 1

    def check_dmg(self, bullet):
        if self.alien_x <= bullet.x <= self.alien_x + self.alien_width:
            if self.alien_y <= bullet.y <= self.alien_y + self.alien_height:
                return 1
        else:
            return 0



class Alians2:
    def __init__(self, alien_x2, alien_y2, alien_width2, alien_height2, alien_img2 ):
        self.alien_x2 = alien_x2
        self.alien_y2 = alien_y2
        self.alien_width2 = alien_width2
        self.alien_height2 = alien_height2
        self.alien_img2 = alien_img2
        self.cooldown_al2 = 0
        self.path_x = self.alien_x2 + self.alien_width2 // 2
        self.path_y = self.alien_y2 + self.alien_height2

    def generate2(self):
        self.alien_y2 = random.randrange(-600, -200)
        self.alien_x2 = random.randint(0, 747)

    def go2(self):
        if self.alien_y2 <= display_height:
            display.blit(alien_img2, (self.alien_x2, self.alien_y2))
            if 700 < scores <= 1200:
                self.alien_y2 += 7

    def pos2(self):
        if self.alien_y2 <= display_height:
            return 0
        else:
            return 1

    def check_dmg2(self, bullet):
        if self.alien_x2 <= bullet.x <= self.alien_x2 + self.alien_width2:
            if self.alien_y2 <= bullet.y <= self.alien_y2 + self.alien_height2:
                return 1
        else:
            return 0

   # def shoot(self):
    #    if not self.cooldown_al2:
     #       new_bullet = Bullet(self.path_x, self.path_y)
      #      self.all_bullets.append(new_bullet)
       #     self.cooldown_al2 = 200
       # else:
        #    self.cooldown_al2 -= 1

        #for bullet in self.all_bullets:
         #   if 60 <= bullet.y <= display_height + 5:
          #      self.path_y += 10
           # elif:
            #    self.all_bullets.remove(bullet)


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 25

    def move(self):
        self.y -= self.speed
        if self.y >= 0:
            display.blit(bullet_img, (self.x, self.y))
            return True
        else:
            return False


player_width = 50
player_height = 60
cord_x = display_width // 2 - 25
cord_y = 540
player_speed = 5

alien_width = 50
alien_height = 53
alien_x = random.randint(0, 747)
alien_y = -alien_height

scores = 0

player_img = pygame.image.load('hero1.png')
alien_img = pygame.image.load('al1.png')
bullet_img = pygame.image.load('bullet.jpg')
alien_img2 = pygame.image.load('al_2.png')

clock = pygame.time.Clock()

circlerect = pygame.rect.Rect((cord_x, cord_y, player_width, player_height))


def run_game():

    game = True
    cooldown = 0

    aliens_arr = []
    aliens_arr2 = []
    create_alien_arr(aliens_arr)
    create_alien_arr2(aliens_arr2)

    all_btn_bullets = []

    while game:
        pygame.time.delay(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        display.fill((100, 149, 237))
        count_scores()
        if scores <= 60:
            draw_alien(all_btn_bullets, scores)
        elif 60 < scores <= 200:
            draw_alien(all_btn_bullets, scores)
            draw_array(aliens_arr)
        elif 200 < scores <= 700:
            draw_alien(all_btn_bullets, scores)
            draw_array(aliens_arr)
        elif 700 < scores <= 1400:
            draw_array(aliens_arr)
            draw_array2(aliens_arr2)

        print_text('Scores: ' + str(scores), 600, 10)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and circlerect.x > 10:
            circlerect.x -= 20
        if keys[pygame.K_RIGHT] and circlerect.x < 740:
            circlerect.x += 20
        if keys[pygame.K_ESCAPE]:
            pause()

        if not cooldown:
            if keys[pygame.K_SPACE]:
                all_btn_bullets.append(Bullet(circlerect.x + player_width / 2 - 4, circlerect.y + 15))
                cooldown = 50
        else:
            print_text('Cooldown time: ' + str(cooldown // 10), 482, 40)
            cooldown -= 5

        if scores == 1000:
            aliens_arr.append(Alians(alien_x, alien_y, alien_width, alien_height, alien_img))
        if scores == 1100:
            aliens_arr.append(Alians(alien_x, alien_y, alien_width, alien_height, alien_img))
        if scores == 1200:
            aliens_arr.append(Alians(alien_x, alien_y, alien_width, alien_height, alien_img))

        for bullet in all_btn_bullets:
            if not bullet.move():
                all_btn_bullets.remove(bullet)

        display.blit(player_img, circlerect)
        if alien_collision(alien_x, alien_y, circlerect.x, circlerect.y):
            game = False
        if alien_collision1(aliens_arr):
            game = False
        if alien_collision2(aliens_arr2):
            game = False

        check_alien_dmg(all_btn_bullets, aliens_arr)
        check_alien_dmg2(all_btn_bullets, aliens_arr2)

        pygame.display.update()
        clock.tick(60)
    return game_over()


def draw_alien(bullets, score):
    global alien_x, alien_y, alien_width, alien_height, alien_img
    if alien_y == -50:
        alien_x = random.randint(0, 747)
    else:
        alien_x = alien_x
    if alien_y <= display_height:
        display.blit(alien_img, (alien_x, alien_y))
        if score <= 200:
            alien_y += 10
        elif 200 < score <= 400:
            alien_y += 15
        elif 400 < score <= 700:
            alien_y += 20
    else:
        alien_y = -50
    for bullet in bullets:
        if alien_x <= bullet.x <= alien_x + alien_width:
            if alien_y + alien_height >= bullet.y >= alien_y:
                alien_y = -50
                alien_x = random.randint(0, 747)
                bullets.remove(bullet)
    if score >= 700:
        alien_x = - 70


def print_text(message, x, y, font_color = (0, 0, 0), font_type = 'PingPong.ttf', font_size = 30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    display.blit(text, (x, y))


def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        print_text('Paused. Press enter to continue', 160, 300)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            paused = False
        pygame.display.update()
        clock.tick(15)


def create_alien_arr(array):
    array.append(Alians(random.randint(0, 747), -200, 50, 53, alien_img))
    array.append(Alians(random.randint(0, 747), -600, 50, 53, alien_img))
    array.append(Alians(random.randint(0, 747), -450, 50, 53, alien_img))


def create_alien_arr2(array2):
    array2.append(Alians2(random.randint(0, 747), -300, 26, 39, alien_img2))
    array2.append(Alians2(random.randint(0, 747), -500, 26, 39, alien_img2))
    array2.append(Alians2(random.randint(0, 747), -450, 26, 39, alien_img2))


def draw_array(array):
    for Aliens in array:
        p = Aliens.pos()
        if p == 0:
            Aliens.go()
        if p == 1:
            Aliens.generate()


def draw_array2(array_al2):
    for Aliens in array_al2:
        p = Aliens.pos2()
        if p == 0:
            Aliens.go2()
        if p == 1:
            Aliens.generate2()


def game_over():
    stopped = True
    while stopped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        print_text('Game over. Press Esc to exit', 200, 300)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            return False
        pygame.display.update()
        clock.tick(15)


def count_scores():
    global scores
    if alien_y != -30:
        scores += 1
    else:
        scores = scores
    pygame.display.update()
    return scores


def alien_collision(al_x, al_y, player_x, player_y):

    if al_y + 42 > player_y:
        if al_x - 50 <= player_x <= player_x <= al_x + 50:
            display.fill((255, 255, 255))
            print_text('Scores: ' + str(scores), 350, 350)
            return True
    return False


def alien_collision1(barriers):
    for barrier in barriers:
        if barrier.alien_y + 42 > circlerect.y:
            if barrier.alien_x - 50 <= circlerect.x <= barrier.alien_x + 50:
                display.fill((255, 255, 255))
                print_text('Scores: ' + str(scores), 350, 350)
                return True
    return False


def alien_collision2(barriers2):
    for barrier2 in barriers2:
        if barrier2.alien_y2 + 42 > circlerect.y:
            if barrier2.alien_x2 - 50 <= circlerect.x <= barrier2.alien_x2 + 50:
                display.fill((255, 255, 255))
                print_text('Scores: ' + str(scores), 350, 350)
                return True
    return False


def check_alien_dmg(bullets, aliens):
    for alien in aliens:
        for bullet in bullets:
            p = alien.check_dmg(bullet)
            if p == 1:
                alien.generate()
                bullets.remove(bullet)


def check_alien_dmg2(bullets, aliens2):
    for alien2 in aliens2:
        for bullet in bullets:
            p = alien2.check_dmg2(bullet)
            if p == 1:
                alien2.generate2()
                bullets.remove(bullet)


while run_game():
    pass
pygame.quit()
quit()