import random
import pygame
import pickle

pygame.init()

class Snake:
    def __init__(self):
        lenght = 2
        cell = 30
        head_x, head_y = 300, 300

        self.size = 1
        self.body = [(head_x, head_y + i * cell) for i in range(lenght)]
        self.direction = pygame.K_DOWN
        self.grow = 0
        self.head_image = pygame.image.load('/Users/artemduritskiy/Desktop/BYTE/Python/snake/img/head.png')
        self.segment_snake_image = pygame.image.load('/Users/artemduritskiy/Desktop/BYTE/Python/snake/img/segment.png')
        self.tail_image = pygame.image.load('/Users/artemduritskiy/Desktop/BYTE/Python/snake/img/tail.png')
        self.tail_image = pygame.transform.scale(self.tail_image, (30, 30))
        self.head_image = pygame.transform.scale(self.head_image, (30, 30))
        self.segment_snake_image = pygame.transform.scale(self.segment_snake_image, (30, 30))

        self.corner_image = pygame.image.load('/Users/artemduritskiy/Desktop/BYTE/Python/snake/img/corner.png')
        self.corner_image = pygame.transform.scale(self.corner_image, (30, 30))


    def move(self):
        x, y = self.body[0]

        if self.direction == pygame.K_UP:
            y -= 30
        elif self.direction == pygame.K_DOWN:
            y += 30
        elif self.direction == pygame.K_RIGHT:
            x += 30
        elif self.direction == pygame.K_LEFT:
            x -= 30
            
        new_segment = (x, y)

        self.body = [new_segment] + self.body
        if self.grow > 0:
            self.grow -= 1
        else:
            self.body.pop()


    def draw(self, screen):
        if self.direction == pygame.K_DOWN:
            rotate_head = self.head_image
        elif self.direction == pygame.K_UP:
            rotate_head = pygame.transform.rotate(self.head_image, 180)
        elif self.direction == pygame.K_LEFT:
            rotate_head = pygame.transform.rotate(self.head_image, -90)
        elif self.direction == pygame.K_RIGHT:
            rotate_head = pygame.transform.rotate(self.head_image, 90)

        screen.blit(rotate_head, self.body[0])

        for i in range(1, len(self.body) - 1):
            prev_seg = self.body[i - 1]
            curr_seg = self.body[i]
            next_seg = self.body[i + 1]

            vec1 = (prev_seg[0] - curr_seg[0], prev_seg[1] - curr_seg[1])
            vec2 = (next_seg[0] - curr_seg[0], next_seg[1] - curr_seg[1])


            if vec1[0] == vec2[0] or vec1[1] == vec2[1]:
                if vec1[0] != 0:
                    rotated_segment = pygame.transform.rotate(self.segment_snake_image, 90)
                else:
                    rotated_segment = self.segment_snake_image

                screen.blit(rotated_segment, curr_seg)
            else:

                if (vec1 == (0, -30) and vec2 == (30, 0)) or (vec2 == (0, -30) and vec1 == (30, 0)):
                    rotated_corner = pygame.transform.rotate(self.corner_image, 0)
                elif (vec1 == (30, 0) and vec2 == (0, 30)) or (vec2 == (30, 0) and vec1 == (0, 30)):
                    rotated_corner = pygame.transform.rotate(self.corner_image, -90)
                elif (vec1 == (0, 30) and vec2 == (-30, 0)) or (vec2 == (0, 30) and vec1 == (-30, 0)):
                    rotated_corner = pygame.transform.rotate(self.corner_image, 180)
                elif (vec1 == (-30, 0) and vec2 == (0, -30)) or (vec2 == (-30, 0) and vec1 == (0, -30)):
                    rotated_corner = pygame.transform.rotate(self.corner_image, 90)
                else:
                    rotated_corner = self.segment_snake_image

                screen.blit(rotated_corner, curr_seg)

    
        if len(self.body) > 1:
            tail_description = (self.body[-2][0] - self.body[-1][0],
                                self.body[-2][1] - self.body[-1][1])
            
            if tail_description == (0, -30):
                rotate_tail = pygame.transform.rotate(self.tail_image, 180)
            elif tail_description == (0, 30):
                rotate_tail = self.tail_image
            elif tail_description == (30, 0):
                rotate_tail = pygame.transform.rotate(self.tail_image, 90)
            elif tail_description == (-30, 0):
                rotate_tail = pygame.transform.rotate(self.tail_image, -90)

            screen.blit(rotate_tail, self.body[-1])

    def change_direction(self, direction):
        if(direction == pygame.K_UP and self.direction != pygame.K_DOWN) or \
            (direction == pygame.K_DOWN and self.direction != pygame.K_UP) or \
            (direction == pygame.K_LEFT and self.direction != pygame.K_RIGHT) or \
            (direction == pygame.K_RIGHT and self.direction != pygame.K_LEFT):
            self.direction = direction

    
    def grow_snake(self, amount=1):
        self.grow += amount

    
    def check_collision(self):
        x, y = self.body[0]

        if x < 0 or x >= 600 or y < 0 or y >= 600:
            return True
        
        if len(self.body) != len(set(self.body)):
            return True
        
        return False
        
        
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.position_gold = (0, 0)
        self.food_image = pygame.image.load('/Users/artemduritskiy/Desktop/BYTE/Python/snake/img/apple.png')
        self.food_image = pygame.transform.scale(self.food_image, (40, 40))
        self.gold_food_image = pygame.image.load('/Users/artemduritskiy/Desktop/BYTE/Python/snake/img/gold_apple.png')
        self.gold_food_image = pygame.transform.scale(self.gold_food_image, (40, 40))

    def generate_food(self, snake_body):
        while True:
            position = (random.randint(0, 19) * 30, random.randint(0, 19) * 30)
            if position not in snake_body:
                return position
    
    def get_food(self, snake_body):
        self.position = self.generate_food(snake_body)
        if random.random() < 0.5:
            while True:
                pos = self.generate_food(snake_body)
                if pos != self.position:
                    self.position_gold = pos
                    break
        else:
            self.position_gold = None

    def draw(self, screen):
        screen.blit(self.food_image, self.position)
        if self.position_gold:
            screen.blit(self.gold_food_image, self.position_gold)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.food = Food()
        self.food.get_food(self.snake.body)
        self.bg = pygame.image.load('/Users/artemduritskiy/Desktop/BYTE/Python/snake/img/bg.png')
        self.score = 0
        self.running = True
        self.font = pygame.font.Font('title_font.ttf', 20)
        self.history_score = self.load_history_score()
        self.start_time = pygame.time.get_ticks()
        self.play_again = True

    def show_start_screen(self):
        snake_img = pygame.image.load('/Users/artemduritskiy/Desktop/BYTE/Python/snake/img/snake.png')
        snake_img = pygame.transform.scale(snake_img, (300, 300))

        while True:
            self.screen.fill((114, 183, 113))

            title_font = pygame.font.Font('freesansbold.ttf', 25)
            title_text_font = pygame.font.Font('title_font.ttf', 60)
            more_text_font = pygame.font.Font('title_font.ttf', 15)

            title_text = title_text_font.render('Snake game', True, (76, 112, 75))
            self.screen.blit(title_text, (130, 380))
            self.screen.blit(snake_img, (150, 20))

            start_button = pygame.Rect(90, 450, 200, 45)
            pygame.draw.rect(self.screen, (106, 158, 104), start_button, border_radius=30)
            start_text = title_font.render('Почати гру', True, (255, 255, 255))
            self.screen.blit(start_text, (start_button.x + 32, start_button.y + 11))

            quit_button = pygame.Rect(310, 450, 200, 45)
            pygame.draw.rect(self.screen, (219, 73, 73), quit_button, border_radius=30)
            quit_text = title_font.render('Вийти', True, (255, 255, 255))
            self.screen.blit(quit_text, (quit_button.x + 60, quit_button.y + 11))

            title_text = more_text_font.render('This project was created for learning Python by Durytskyi Artem in 2025', True, (76, 112, 75))
            self.screen.blit(title_text, (50, 570))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.collidepoint(event.pos):
                        self.run_game_loop()
                        return
                    elif quit_button.collidepoint(event.pos):
                        pygame.quit()
                        exit()


    def display_end_screen(self):
        width, height = 600, 600
        end_screen = pygame.display.set_mode((width, height))
        end_screen.fill((114, 183, 113))

        font = pygame.font.Font('title_font.ttf', 50)
        font_text = pygame.font.Font('title_font.ttf', 28)
        font_text_score = pygame.font.Font('title_font.ttf', 40)
        font_btn = pygame.font.Font('freesansbold.ttf', 25)

        history_score = font.render('Score history', True, (76, 112, 75))
        end_screen.blit(history_score, (150, 20))


        for i, score in enumerate(self.history_score[-5:], start=1):
            max_score = max(self.history_score) if self.history_score else 0
            history_score = font_text.render(f'Your record: {str(max_score)}', True, (76, 112, 75))
            end_screen.blit(history_score, (200, 80))

            history_score = font_text.render(f'Score:  {self.history_score[-1]}', True, (76, 112, 75))
            end_screen.blit(history_score, (240, 115))

            score_text = font_text_score.render(f'{i}. {score}', True, (255, 255, 255))
            end_screen.blit(score_text, (260, 120 + 45 * i))

        button_rect = pygame.Rect(90, 450, 200, 45)
        pygame.draw.rect(end_screen, (106, 158, 104), button_rect, border_radius=30)
        button_text = font_btn.render('Грати знову', True, (255, 255, 255))
        end_screen.blit(button_text, (button_rect.x + 27, button_rect.y + 11))

        button_rect_home = pygame.Rect(310, 450, 200, 45)
        pygame.draw.rect(end_screen, (106, 158, 104), button_rect_home, border_radius=30)
        button_text_home = font_btn.render('На головну', True, (255, 255, 255))
        end_screen.blit(button_text_home, (button_rect_home.x + 30, button_rect_home.y + 11))

        quit_button = pygame.Rect(200, 510, 200, 45)
        pygame.draw.rect(self.screen, (219, 73, 73), quit_button, border_radius=30)
        quit_text = font_btn.render('Вийти', True, (255, 255, 255))
        self.screen.blit(quit_text, (quit_button.x + 60, quit_button.y + 11))

        pygame.display.flip()

        self.wait_for_restart(button_rect, quit_button, button_rect_home)


    def wait_for_restart(self, button_rect, quit_button, button_rect_home):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        self.run_game_loop()
                        return
                    elif button_rect_home.collidepoint(event.pos):
                        self.start()                        
                    elif quit_button.collidepoint(event.pos):
                        pygame.quit()
                        exit()

                
    def save_score_history(self):
        with open('score_history.pkl', 'wb') as file:
            pickle.dump(self.history_score, file)

    
    def display_score(self):
        score_text = self.font.render(f'Score: {str(self.score)}', True, (13, 17, 23))
        self.screen.blit(score_text, (10, 10))

    def display_time(self):
        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
        time_text = self.font.render(f'Time: {elapsed_time}', True, (13, 17, 23))
        self.screen.blit(time_text, (500, 10))

    def load_history_score(self):
        try:
            with open('score_history.pkl', 'rb') as file:
                return pickle.load(file)
        except (FileNotFoundError, EOFError):
            return []
        

    def start(self):
        self.show_start_screen()
        self.run_game_loop()

    def run_game_loop(self):
        self.running = True
        self.snake = Snake()
        self.food = Food()
        self.food.get_food(self.snake.body)
        self.score = 0
        self.start_time = pygame.time.get_ticks()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.snake.change_direction(pygame.K_UP)
                    elif event.key == pygame.K_s:
                        self.snake.change_direction(pygame.K_DOWN)
                    elif event.key == pygame.K_a:
                        self.snake.change_direction(pygame.K_LEFT)
                    elif event.key == pygame.K_d:
                        self.snake.change_direction(pygame.K_RIGHT)
            
            self.snake.move()


            if self.snake.body[0] == self.food.position:
                self.score += 1
                self.food.get_food(self.snake.body)
                self.snake.grow_snake()
            elif self.food.position_gold and self.snake.body[0] == self.food.position_gold:
                self.score += 5
                self.food.get_food(self.snake.body)

                self.snake.grow_snake(5)

            if self.snake.check_collision():
                self.running = False
                self.history_score.append(self.score)
                self.save_score_history()

            
            self.screen.blit(self.bg, (0, 0))
            self.snake.draw(self.screen)
            self.food.draw(self.screen)
            self.display_score()
            self.display_time()

            pygame.display.flip()
            self.clock.tick(8)

        self.display_end_screen()

game = Game()
game.start()
pygame.quit()