import pygame
import random

pygame.init()

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600
LEFT_Y_BOUNDARY = -600
RIGHT_Y_BOUNDARY = -200
LEFT_X_BOUNDARY = 0
RIGHT_X_BOUNDARY = 747

PLAYER_WIDTH = 50
PLAYER_HEIGHT = 60
PLAYER_COORD_Y = 540
PLAYER_SPEED = 5
ALIEN_WIDTH = 50
ALIEN_HEIGHT = 53


alien_x = random.randint(0, 747)
alien_y = -ALIEN_HEIGHT
player_coord_x = DISPLAY_WIDTH // 2 - 25
scores = 0

player_img = pygame.image.load('hero1.png')
alien_img = pygame.image.load('al1.png')
bullet_img = pygame.image.load('bullet.jpg')
alien_img2 = pygame.image.load('al_2.png')

clock = pygame.time.Clock()

circle_rect = pygame.rect.Rect((player_coord_x, PLAYER_COORD_Y, PLAYER_WIDTH, PLAYER_HEIGHT))


display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption('Alien game')


class Aliens:
    def __init__(self, alien_x, alien_y, alien_width, alien_height, alien_img):
        self.alien_x = alien_x
        self.alien_y = alien_y
        self._alien_width = alien_width
        self._alien_height = alien_height
        self._alien_img = alien_img

    def generate(self):
        self.alien_y = random.randrange(LEFT_Y_BOUNDARY, RIGHT_Y_BOUNDARY)
        self.alien_x = random.randint(LEFT_X_BOUNDARY, RIGHT_X_BOUNDARY)

    def go(self):
        if self.alien_y <= DISPLAY_HEIGHT:
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
        if self.alien_y <= DISPLAY_HEIGHT:
            return False
        else:
            return True

    def check_dmg(self, bullet):
        if self.alien_x <= bullet.x <= self.alien_x + self._alien_width:
            if self.alien_y <= bullet.y <= self.alien_y + self._alien_height:
                return True
        else:
            return False


class Aliens2:
    def __init__(self, alien_x2, alien_y2, alien_width2, alien_height2, alien_img2):
        self.alien_x2 = alien_x2
        self.alien_y2 = alien_y2
        self._alien_width2 = alien_width2
        self._alien_height2 = alien_height2
        self._alien_img2 = alien_img2
        self.cooldown_al2 = 0
        self.path_x = self.alien_x2 + self._alien_width2 // 2
        self.path_y = self.alien_y2 + self._alien_height2

    def generate2(self):
        self.alien_y2 = random.randrange(LEFT_Y_BOUNDARY, RIGHT_Y_BOUNDARY)
        self.alien_x2 = random.randint(LEFT_X_BOUNDARY, RIGHT_X_BOUNDARY)

    def go2(self):
        if self.alien_y2 <= DISPLAY_HEIGHT:
            display.blit(alien_img2, (self.alien_x2, self.alien_y2))
            if 0 < scores <= 1400:
                self.alien_y2 += 7

    def pos2(self):
        if self.alien_y2 <= DISPLAY_HEIGHT:
            return False
        else:
            return True

    def check_dmg2(self, bullet):
        if self.alien_x2 <= bullet.x <= self.alien_x2 + self._alien_width2:
            if self.alien_y2 <= bullet.y <= self.alien_y2 + self._alien_height2:
                return True
        else:
            return False

    def shoot(self):
        if not self.cooldown_al2:
            bullet = Bullet(self.alien_x2 + 10, self.alien_y2+3)
            self.cooldown_al2 = 50
            return bullet
        else:
            self.cooldown_al2 -= 2
            return None


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

    def move_backward(self):
        self.y += self.speed
        if self.y <= DISPLAY_HEIGHT:
            display.blit(bullet_img, (self.x, self.y))
            return True
        else:
            return False


def alien_shot(alliens_array):
    bullets = []
    for alien in alliens_array:
        bullet = alien.shoot()
        if bullet is not None:
            bullets.append(bullet)

    return bullets


def check_hit(aliens_shots):
    for shot in aliens_shots:
        if circle_rect.y <= shot.y <= circle_rect.y + PLAYER_HEIGHT:
            if circle_rect.x <= shot.x <= circle_rect.x + PLAYER_WIDTH:
                return True
    return False



def run_game():
    game = True
    cooldown = 0

    aliens_arr = []
    aliens_arr2 = []
    create_alien_arr(aliens_arr)
    create_alien_arr2(aliens_arr2)

    all_btn_bullets = []
    all_alien_shots = []
    while game:
        pygame.time.delay(1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        display.fill((100, 149, 237))
        count_scores()
        if scores <= 60:
            draw_alien(all_btn_bullets, scores)
            draw_array2(aliens_arr2)

        elif 60 < scores <= 700:
            draw_alien(all_btn_bullets, scores)
            draw_array(aliens_arr)
            draw_array2(aliens_arr2)

        elif 700 < scores <= 1400:
            draw_array(aliens_arr)
            draw_array2(aliens_arr2)

        print_text('Scores: ' + str(scores), 600, 10)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and circle_rect.x > 10:
            circle_rect.x -= 20
        if keys[pygame.K_RIGHT] and circle_rect.x < 740:
            circle_rect.x += 20
        if keys[pygame.K_ESCAPE]:
            pause()

        if not cooldown:
            if keys[pygame.K_SPACE]:
                all_btn_bullets.append(Bullet(circle_rect.x + PLAYER_WIDTH / 2 - 4, circle_rect.y + 15))
                cooldown = 50
        else:
            print_text('Cooldown time: ' + str(cooldown // 10), 482, 40)
            cooldown -= 5

        if scores == 1000:
            aliens_arr.append(Aliens(alien_x, alien_y, ALIEN_WIDTH, ALIEN_HEIGHT, alien_img))
        if scores == 1100:
            aliens_arr.append(Aliens(alien_x, alien_y, ALIEN_WIDTH, ALIEN_HEIGHT, alien_img))
        if scores == 1200:
            aliens_arr.append(Aliens(alien_x, alien_y, ALIEN_WIDTH, ALIEN_HEIGHT, alien_img))

        for bullet in all_btn_bullets:
            print(bullet)
            if not bullet.move():
                all_btn_bullets.remove(bullet)

        aliens_shots = alien_shot(aliens_arr2)
        all_alien_shots += aliens_shots
        for bullet in all_alien_shots:
            # #bullet.print_bullet()
            # print(bullet)
            if not bullet.move_backward():
                all_alien_shots.remove(bullet)

        display.blit(player_img, circle_rect)
        if alien_collision(alien_x, alien_y, circle_rect.x, circle_rect.y):
            game = False
        if alien_collision1(aliens_arr):
            game = False
        if alien_collision2(aliens_arr2):
            game = False

        check_alien_dmg(all_btn_bullets, aliens_arr)
        check_alien_dmg2(all_btn_bullets, aliens_arr2)

        hit = check_hit(all_alien_shots)
        if hit:
            game = False

        pygame.display.update()
        clock.tick(60)
    return game_over()


def draw_alien(bullets, score):
    global alien_x, alien_y, ALIEN_WIDTH, ALIEN_HEIGHT, alien_img
    if alien_y == -50:
        alien_x = random.randint(0, 747)
    else:
        alien_x = alien_x
    if alien_y <= DISPLAY_HEIGHT:
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
        if alien_x <= bullet.x <= alien_x + ALIEN_WIDTH:
            if alien_y + ALIEN_HEIGHT >= bullet.y >= alien_y:
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
    array.append(Aliens(random.randint(0, 747), -200, 50, 53, alien_img))
    array.append(Aliens(random.randint(0, 747), -600, 50, 53, alien_img))
    array.append(Aliens(random.randint(0, 747), -450, 50, 53, alien_img))


def create_alien_arr2(array2):
    array2.append(Aliens2(random.randint(0, 747), -300, 26, 39, alien_img2))
    array2.append(Aliens2(random.randint(0, 747), -500, 26, 39, alien_img2))
    array2.append(Aliens2(random.randint(0, 747), -450, 26, 39, alien_img2))


def draw_array(array):
    for aliens in array:
        p = aliens.pos()
        if not p:
            aliens.go()
        if p:
            aliens.generate()


def draw_array2(array_al2):
    for aliens in array_al2:
        p = aliens.pos2()
        if not p:
            aliens.go2()
        if p:
            aliens.generate2()


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
        if barrier.alien_y + 42 > circle_rect.y:
            if barrier.alien_x - 50 <= circle_rect.x <= barrier.alien_x + 50:
                display.fill((255, 255, 255))
                print_text('Scores: ' + str(scores), 350, 350)
                return True
    return False


def alien_collision2(barriers2):
    for barrier2 in barriers2:
        if barrier2.alien_y2 + 42 > circle_rect.y:
            if barrier2.alien_x2 - 50 <= circle_rect.x <= barrier2.alien_x2 + 50:
                display.fill((255, 255, 255))
                print_text('Scores: ' + str(scores), 350, 350)
                return True
    return False


def check_alien_dmg(bullets, aliens):
    for alien in aliens:
        for bullet in bullets:
            p = alien.check_dmg(bullet)
            if p:
                alien.generate()
                bullets.remove(bullet)


def check_alien_dmg2(bullets, aliens2):
    for alien2 in aliens2:
        for bullet in bullets:
            p = alien2.check_dmg2(bullet)
            if p:
                alien2.generate2()
                bullets.remove(bullet)


def main():
    while run_game():
        pass
    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
