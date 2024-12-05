import pygame, random, json
from worm import *
from player import *

WORM_SEGMENTS = 20

COIN_SIZE = 20

HIGHSCORES_FILEPATH = 'highscores.json'

pygame.init()

monitor_info = pygame.display.Info()
SCREEN_WIDTH = monitor_info.current_w
SCREEN_HEIGHT = monitor_info.current_h

name = input('enter your name: ')

# pygame setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Dodge the Worms!")
clock = pygame.time.Clock()
running = True


def check_collision(player: Player, worm: Worm) -> bool:
    '''
    returns true if the player collided with the worm
    '''
    if abs(player.pos[0] - worm.head[0]) < WORM_RADIUS + PLAYER_SIZE / 2 and abs(player.pos[1] - worm.head[1]) < WORM_RADIUS + PLAYER_SIZE / 2:
        return True
    
    for segment in worm.tail_segments:
        if abs(player.pos[0] - segment[0]) < WORM_RADIUS / 2 + PLAYER_SIZE / 2 and abs(player.pos[1] - segment[1]) < WORM_RADIUS / 2 + PLAYER_SIZE / 2:
            return True

    return False


def increase_difficulty(worms: list[Worm]):
    for worm in worms:
        worm.max_speed += 0.5
        worm.turn_limit *= 1.01
    worms.append(Worm(WORM_SEGMENTS, 0, 0, pygame.Color(110, 110, 200), MAX_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT))


def create_coin(coins):
    left_bound = int(SCREEN_WIDTH / 16)
    right_bound = int(15 * SCREEN_WIDTH / 16)
    upper_bound= int(SCREEN_HEIGHT / 16)
    lower_bound = int(15 * SCREEN_HEIGHT / 16)
    coins.append(pygame.Rect(random.randint(left_bound, right_bound), random.randint(upper_bound, lower_bound), COIN_SIZE, COIN_SIZE))


def create_blue_coin(coins):
    left_bound = int(SCREEN_WIDTH / 16)
    right_bound = int(15 * SCREEN_WIDTH / 16)
    upper_bound= int(SCREEN_HEIGHT / 16)
    lower_bound = int(15 * SCREEN_HEIGHT / 16)
    coins.append(pygame.Rect(random.randint(left_bound, right_bound), random.randint(upper_bound, lower_bound), 2 * COIN_SIZE / 3, 2 * COIN_SIZE / 3))


def display_end_screen():
    end_background = pygame.Rect(SCREEN_WIDTH / 4, SCREEN_HEIGHT / 4, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    pygame.draw.rect(screen, pygame.Color(255, 20, 125), end_background)
    end_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
    end_textpos = end_text.get_rect(centerx=screen.get_width() / 2, y=end_background.top + 10)
    screen.blit(end_text, end_textpos)
    line_y_pos = end_background.top + 74
    place = 1
    for name_score in highscores_list[:10]:
        name = name_score[0]
        their_score = name_score[1]
        name_text = small_font.render(f'{place}. {name}', True, (255, 255, 255))
        name_textpos = name_text.get_rect(centerx=SCREEN_WIDTH / 2 - SCREEN_WIDTH / 8, y=line_y_pos)
        screen.blit(name_text, name_textpos)
        score_text = small_font.render(str(their_score), True, (255, 255, 255))
        score_textpos = score_text.get_rect(centerx=SCREEN_WIDTH / 2 + SCREEN_WIDTH / 8, y=line_y_pos)
        screen.blit(score_text, score_textpos)
        line_y_pos += 32
        place += 1


worms = []

coins = []
blue_coins = []

player = Player(SCREEN_WIDTH, SCREEN_HEIGHT)

second_counter = 60

score = 0
seconds = 0

font = pygame.font.Font(None, 64)
small_font = pygame.font.Font(None, 32)

alive = True

pygame.mouse.set_visible(False)

try:
    with open(HIGHSCORES_FILEPATH, mode='r', encoding='utf-8') as highscores_file:
        highscores_dict = json.load(highscores_file)
        highscores_list = [(name, highscores_dict[name]) for name in highscores_dict.keys()]
        highscores_list.sort(reverse=True, key=lambda x:x[1])
except FileNotFoundError:
    highscores_dict = {}
    highscores_list = []

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if alive:
        if second_counter == 0:
            seconds += 1
            if seconds > 0 and seconds % 10 == 0:
                increase_difficulty(worms)
                create_blue_coin(blue_coins)
            else:
                create_coin(coins)
            second_counter = 60
        else:
            second_counter -= 1

        # fill the screen with a color to wipe away anything from last frame
        screen.fill(pygame.Color(0, 0, 0))

        for worm in worms:
            if check_collision(player, worm):
                alive = False
                if name in highscores_dict and score <= highscores_dict[name]:
                    break
                highscores_dict[name] = score
                highscores_list = [(name, highscores_dict[name]) for name in highscores_dict.keys()]
                highscores_list.sort(reverse=True, key=lambda x:x[1])
                

        # RENDER YOUR GAME HERE
        for worm in worms:
            worm.draw(screen)
            worm.change_state(player)
        player.draw(screen)

        for coin in coins:
            pygame.draw.circle(screen, pygame.Color(255, 200, 0), (coin.left + coin.width / 2, coin.top + coin.width / 2), coin.width / 2)
            if player.rect.colliderect(coin):
                coins.remove(coin)
                score += 1

        for coin in blue_coins:
            pygame.draw.circle(screen, pygame.Color(50, 50, 255), (coin.left + coin.width / 2, coin.top + coin.width / 2), coin.width / 2)
            if player.rect.colliderect(coin):
                blue_coins.remove(coin)
                score += 5

        text = font.render(f"{score}", True, (255, 255, 255))
        textpos = text.get_rect(centerx=screen.get_width() / 2, y=10)
        screen.blit(text, textpos)

        # flip() the display to put your work on screen
        pygame.display.flip()

        player.move()

        for worm in worms:
            worm.move_head(player.pos[0], player.pos[1])
            worm.move_tail_segments()
    else:
        display_end_screen()
        pygame.display.flip()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r] or keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
            alive = True
            worms = []
            coins = []
            blue_coins = []
            player = Player(SCREEN_WIDTH, SCREEN_HEIGHT)
            second_counter = 60
            score = 0
            seconds = 0
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            running = False

    clock.tick(60)  # limits FPS to 60

with open(HIGHSCORES_FILEPATH, mode='w', encoding='utf-8') as save_file:
    save_file.truncate(0)
    save_file.seek(0)
    save_file.write(json.dumps(highscores_dict))

pygame.quit()