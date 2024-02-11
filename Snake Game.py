import pygame, sys, time, random


class Difficulty:
    """
    Қиындық параметрлері
    Оңай      ->  10
    Орташа    ->  25
    Қиын      ->  40
    Өте қиын  ->  60
    """
    def __init__(self, level) -> None:
        self.level = level

class WindowParameters():  # Ойын терезесінің (экранынің) параметрлері
    def __init__(self, frame_size_x, frame_size_y) -> None:
        self.frame_size_x = frame_size_x  # Терезе ені
        self.frame_size_y = frame_size_y  # Терезе биіктігі

# Ойынды инициализациялау, қателердің бар-жоғын тексеру
check_errors = pygame.init()
# pygame.init() мысал шығаруы -> (6, 0)
# tuple-дағы екінші сан - қателердің саны
if check_errors[1] > 0:
    print(f'[!] Ойынды инициализациалау кезінде {check_errors[1]} қате табылды, тоқтату...')
    sys.exit(-1)
else:
    print('[+] Ойын сәтті инициализацияланды')


pygame.display.set_caption('Жылан')  # Ойын терезесін инициализациялау


window_parameters = WindowParameters(720, 480)
game_window = pygame.display.set_mode((window_parameters.frame_size_x, window_parameters.frame_size_y))


#  Түс объекттері. Color класстың конструкторына берілетін 3 сан - қызыл, жасыл, көк (RGB color model) түстерінің кодтары. Осылайша түстерді анықтай аламыз.
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)


fps_controller = pygame.time.Clock()  # FPS - 1 секундтағы кадрлар сандарының контроллері


class Game():
    snake_pos = [100, 50]  # Жылан басының координаталары
    snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]  # Жылан координаталары

    # Жылан тамағының координаталары
    food_pos = [random.randrange(1, (window_parameters.frame_size_x//10)) * 10, random.randrange(1, (window_parameters.frame_size_y//10)) * 10]
    food_spawn = True  # Тағамның координаталары өзгерді ме

    direction = 'ОҢ'
    change_to = direction

    score = 0


    # Ойын Аяқталды
    @staticmethod
    def game_over():
        my_font = pygame.font.SysFont('times new roman', 90)  # шрифт
        game_over_surface = my_font.render('Ойын Аяқталды', True, red)  # ойын аяқталу экранынің беті
        game_over_rect = game_over_surface.get_rect()  # ойын аяқталу төртбұрышы
        game_over_rect.midtop = (window_parameters.frame_size_x/2, window_parameters.frame_size_y/4)  # өлшемін анықтау
        game_window.fill(black)  # түсін анықтау
        game_window.blit(game_over_surface, game_over_rect)
        Game.show_score(0, red, 'ұпай', 20)
        pygame.display.flip()
        time.sleep(3)
        pygame.quit()
        sys.exit()


    # Ұпай санын көрсету
    @staticmethod
    def show_score(choice, color, font, size):
        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render('Ұпай саны : ' + str(game.score), True, color)
        score_rect = score_surface.get_rect()
        if choice == 1:
            score_rect.midtop = (window_parameters.frame_size_x/10, 15)
        else:
            score_rect.midtop = (window_parameters.frame_size_x/2, window_parameters.frame_size_y/1.25)
        game_window.blit(score_surface, score_rect)

game = Game()
difficulty = Difficulty(10)

# Негізгі логика
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Перне басылған сайын
        elif event.type == pygame.KEYDOWN:
            # W -> Жоғары; S -> Төмен; A -> Сол; D -> Оң
            if event.key == pygame.K_UP or event.key == ord('w'):
                game.change_to = 'ЖОҒАРЫ'
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                game.change_to = 'ТӨМЕН'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                game.change_to = 'СОЛ'
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                game.change_to = 'ОҢ'
            # Esc -> Ойыннан шығу
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    # Жыланның бірден қарама-қарсы бағытта қозғала алмайтыды
    if game.change_to == 'ЖОҒАРЫ' and game.direction != 'ТӨМЕН':
        game.direction = 'ЖОҒАРЫ'
    if game.change_to == 'ТӨМЕН' and game.direction != 'ЖОҒАРЫ':
        game.direction = 'ТӨМЕН'
    if game.change_to == 'СОЛ' and game.direction != 'ОҢ':
        game.direction = 'СОЛ'
    if game.change_to == 'ОҢ' and game.direction != 'СОЛ':
        game.direction = 'ОҢ'

    # Жыланды жылжыту
    if game.direction == 'ЖОҒАРЫ':
        game.snake_pos[1] -= 10
    if game.direction == 'ТӨМЕН':
        game.snake_pos[1] += 10
    if game.direction == 'СОЛ':
        game.snake_pos[0] -= 10
    if game.direction == 'ОҢ':
        game.snake_pos[0] += 10

    # Жылан денесінің өсу механизмі
    game.snake_body.insert(0, list(game.snake_pos))
    if game.snake_pos[0] == game.food_pos[0] and game.snake_pos[1] == game.food_pos[1]:
        game.score += 1
        game.food_spawn = False
    else:
        game.snake_body.pop()

    # Экранда жаңа тағамның пайда болуы
    if not game.food_spawn:
        game.food_pos = [random.randrange(1, (window_parameters.frame_size_x//10)) * 10, random.randrange(1, (window_parameters.frame_size_y//10)) * 10]
    game.food_spawn = True

    game_window.fill(black)
    for pos in game.snake_body:
        # Жылан денесі
        # .draw.rect(ойын_беті, түс, xy-координаталары)
        # xy-координаталары -> .Rect(x, y, x_өлшемі, y_өлшемі)
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

    # Жылан тағамы
    pygame.draw.rect(game_window, white, pygame.Rect(game.food_pos[0], game.food_pos[1], 10, 10))

    # Ойынның аяқталу шарттары
    # Шектен шығу
    if game.snake_pos[0] < 0 or game.snake_pos[0] > window_parameters.frame_size_x-10:
        game.game_over()
    if game.snake_pos[1] < 0 or game.snake_pos[1] > window_parameters.frame_size_y-10:
        game.game_over()
    # Жыланның денесіне қол тигізу
    for block in game.snake_body[1:]:
        if game.snake_pos[0] == block[0] and game.snake_pos[1] == block[1]:
            game.game_over()

    game.show_score(1, white, 'consolas', 20)
    # Ойын экранын жаңарту
    pygame.display.update()
    # Жаңарту жылдамдығы
    fps_controller.tick(difficulty.level)