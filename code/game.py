import pygame
import random
import json

from code.const import COLOR_WHITE, MENU_SELECTION, SCREEN_HEIGHT, SCREEN_WIDTH
from code.menu import Menu

pygame.init()
pygame.mixer.init()


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class Game:
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        self.screen = screen
        self.spritesheet = pygame.image.load('./asset/player.png') # loading player sprite sheet
        self.load_sprite_data()
        self.frame_selection = self.get_frame_selection()
        self.player_frames = self.load_frames()
        self.player_rect = self.player_frames['down'][0].get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.player_speed = 4
        self.animation_speed = 3
        self.frame_counter = 0
        self.player_index = 0
        self.player_direction = 'down'
        pygame.mixer.music.load('./asset/LevelTheme.wav')
        pygame.mixer.music.play(-1)
        self.clock = pygame.time.Clock()
        self.score = 0
        self.stage = 1
        self.item_images = self.load_item_images()
        self.backgrounds = self.load_backgrounds()
        self.font = pygame.font.SysFont('System', 40)

    def load_sprite_data(self): # loading sprite sheet json file
        with open('./asset/player.json') as f:
            self.sprite_data = json.load(f)

    def get_frame_selection(self): # distributing sprite frames
        return {
            'down': ['frame_0', 'frame_1', 'frame_2', 'frame_3'],
            'left': ['frame_4', 'frame_5', 'frame_6', 'frame_7'],
            'up': ['frame_8', 'frame_9', 'frame_10', 'frame_11'],
            'right': ['frame_12', 'frame_13', 'frame_14', 'frame_15']
        }

    def load_item_images(self): # loading the flowers
        return {
            'item1': (pygame.image.load('./asset/flower1.png'), 1, 0.8),
            'item2': (pygame.image.load('./asset/flower2.png'), -3, 0.5),
            'item3': (pygame.image.load('./asset/flower3.png'), 2, 0.3),
            'item4': (pygame.image.load('./asset/flower4.png'), 5, 0.1),
        }

    def load_backgrounds(self): # loading background for level1 and level2
        return {
            1: pygame.image.load('./asset/LevelBG.png'),
            2: pygame.image.load('./asset/LevelBG2.png')
        }

    def load_frames(self): # loading the sprite sheet frames
        frames = {}
        for direction, frame_names in self.frame_selection.items():
            frames[direction] = []
            for frame_name in frame_names:
                frame_info = self.sprite_data['frames'][frame_name + '.png']['frame']
                frame = self.spritesheet.subsurface(
                    pygame.Rect(frame_info['x'], frame_info['y'], frame_info['w'], frame_info['h']))
                frames[direction].append(frame)
        return frames

    def generate_item(self): # random generator for the flowers
        key, (image, points, frequency) = \
        random.choices(list(self.item_images.items()), weights=[i[2] for i in self.item_images.values()])[0]
        rect = pygame.Rect(random.randint(0, SCREEN_WIDTH - 50), random.randint(0, SCREEN_HEIGHT - 50), 50, 50)
        spawn_time = pygame.time.get_ticks()
        return {'image': image, 'points': points, 'rect': rect, 'spawn_time': spawn_time}

    def handle_player_movement(self, keys): # player keyboard movements as in up, down, left and right keys
        moving = False
        if keys[pygame.K_LEFT] and self.player_rect.left > 0:
            self.player_rect.x -= self.player_speed
            moving = True
            self.player_direction = 'left'
        if keys[pygame.K_RIGHT] and self.player_rect.right < SCREEN_WIDTH:
            self.player_rect.x += self.player_speed
            moving = True
            self.player_direction = 'right'
        if keys[pygame.K_UP] and self.player_rect.top > 0:
            self.player_rect.y -= self.player_speed
            moving = True
            self.player_direction = 'up'
        if keys[pygame.K_DOWN] and self.player_rect.bottom < SCREEN_HEIGHT:
            self.player_rect.y += self.player_speed
            moving = True
            self.player_direction = 'down'
        return moving

    def update_player_frame(self, moving): # sprite sheet animation
        if moving:
            self.frame_counter += 1
            if self.frame_counter >= self.animation_speed:
                self.frame_counter = 0
                self.player_index = (self.player_index + 1) % 4
        else:
            self.player_index = 0

    def draw_score(self): # set the score on the screen
        text = self.font.render(f'SCORE: {self.score}', True, COLOR_WHITE)
        self.screen.blit(text, (10, 10))

    def show_message(self, message):# for the text that appears on the screen between levels and at the end
        text = self.font.render(message, True, COLOR_WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(2000)

    def load_game(self):
        self.reset_game()
        running = True
        items = [self.generate_item() for _ in range(5)]
        item_lifetime = 6000 # set the lifetime span of the flowers for 6 seconds

        while running:
            self.screen.blit(self.backgrounds[self.stage], (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            moving = self.handle_player_movement(keys)
            self.update_player_frame(moving)

            for item in items[:]: # colliding with the flowers
                if self.player_rect.inflate(-20, -20).colliderect(item['rect']):
                    self.score = max(0, self.score + item['points'])
                    items.remove(item)
                    items.append(self.generate_item())
                elif pygame.time.get_ticks() - item['spawn_time'] > item_lifetime:
                    items.remove(item)
                    items.append(self.generate_item())

            self.screen.blit(self.player_frames[self.player_direction][self.player_index], self.player_rect)
            for item in items:
                self.screen.blit(item['image'], item['rect'])

            self.draw_score()
            pygame.display.flip()
            self.clock.tick(60)

            if self.score >= 30: # score points
                if self.stage == 1:
                    self.stage = 2
                    self.score = 0
                    self.show_message('LEVEL 2') # message between level1 and level2
                else:
                    self.show_message('TO BE CONTINUED...') # message at the end of level 2 before going back to menu
                    running = False

    def quit_game(self):
        pygame.quit()
        quit()

    def run(self): # menu
        while True:
            menu = Menu(self.screen)
            menu_return = menu.run()
            if menu_return == MENU_SELECTION[0]:
                self.reset_game()
                self.load_game()
            elif menu_return == MENU_SELECTION[1]:
                self.quit_game()
