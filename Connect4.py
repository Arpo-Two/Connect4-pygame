import pygame
import random
import copy

HEIGHT = 648
WIDTH = 910
DIAGONAL = (WIDTH ** 2 + HEIGHT ** 2) ** 0.5
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.font.init()
title = pygame.font.SysFont('impact', int(DIAGONAL // 10))
font = pygame.font.SysFont('impact', int(DIAGONAL // 18))
small = pygame.font.SysFont('impact', int(DIAGONAL // 30))
u_small = pygame.font.SysFont('impact', int(DIAGONAL // 50))


class Menu:
    def __init__(self, bg, color, texts, text_fonts, positions, buttons, commands, states, secondary_color):
        self.bg = bg
        self.color = color
        self.texts = texts
        self.text_fonts = text_fonts
        self.text_sizes = [self.text_fonts[x].size(self.texts[x]) for x in range(len(self.texts))]
        self.positions = positions
        self.buttons = buttons
        self.commands = commands
        self.states = states
        self.secondary_color = secondary_color
        self.keys = []

    def draw(self, window):
        for y in range(len(self.buttons)):
            if self.states[y]:
                c = self.secondary_color
            else:
                c = self.color
            pygame.draw.circle(window, c, (int(self.buttons[y][0]), int(self.buttons[y][1])),
                               int(self.buttons[y][2]))
            pygame.draw.circle(window, (0, 0, 0), (int(self.buttons[y][0]), int(self.buttons[y][1])),
                               int(self.buttons[y][2]), int(DIAGONAL // 150))

        for x in range(len(self.texts)):
            window.blit(self.text_fonts[x].render(self.texts[x], False, (0, 0, 0)),
                        (self.positions[x][0] - self.text_sizes[x][0] / 2,
                         self.positions[x][1] - self.text_sizes[x][1] / 2))


class Game:
    def __init__(self, opponent):
        self.arrow = 0
        self.turn = 0
        self.state = 9
        self.board = [[9, 9, 9, 9, 9, 9, 9],
                      [9, 9, 9, 9, 9, 9, 9],
                      [9, 9, 9, 9, 9, 9, 9],
                      [9, 9, 9, 9, 9, 9, 9],
                      [9, 9, 9, 9, 9, 9, 9],
                      [9, 9, 9, 9, 9, 9, 9]]
        self.floors = [5, 5, 5, 5, 5, 5, 5]
        self.opponent = opponent

    def move_arrow(self, direction):
        if direction == 'e':
            self.arrow += 1
        if direction == 'w':
            self.arrow -= 1
        if self.arrow > 6:
            self.arrow -= 7
        if self.arrow < 0:
            self.arrow += 7

    def play(self, move, value):
        if self.floors[move] >= 0 and self.state == 9:
            self.board[self.floors[move]][move] = value
            self.turn = (self.turn + 1) % 2
            self.floors[move] -= 1

    def check_result(self):
        d = 0
        winner = 9
        for x in range(7):
            for y in range(3):
                if self.board[y][x] == self.board[y + 1][x] == self.board[y + 2][x] == self.board[y + 3][x] != 9:
                    winner = self.board[y][x]
        for x in range(4):
            for y in range(6):
                if self.board[y][x] == self.board[y][x + 1] == self.board[y][x + 2] == self.board[y][x + 3] != 9:
                    winner = self.board[y][x]
        for x in range(4):
            for y in range(3):
                if self.board[y][x] == self.board[y + 1][x + 1] == self.board[y + 2][x + 2] == self.board[y + 3][x + 3]\
                        != 9:
                    winner = self.board[y][x]
        for x in range(4):
            for y in range(3):
                if self.board[y + 3][x] == self.board[y + 2][x + 1] == self.board[y + 1][x + 2] == self.board[y][x + 3]\
                        != 9:
                    winner = self.board[y + 3][x]
        for x in range(7):
            for y in range(6):
                if self.board[y][x] == 9:
                    d += 1
        if d == 0:
            winner = 2
        if self.state == 9:
            self.state = winner

    def new_game(self):
        self.board = [[9, 9, 9, 9, 9, 9, 9],
                      [9, 9, 9, 9, 9, 9, 9],
                      [9, 9, 9, 9, 9, 9, 9],
                      [9, 9, 9, 9, 9, 9, 9],
                      [9, 9, 9, 9, 9, 9, 9],
                      [9, 9, 9, 9, 9, 9, 9]]

        self.floors = [5, 5, 5, 5, 5, 5, 5]
        self.state = 9


class GameMenu:
    def __init__(self, opponent):
        self.game = Game(opponent)
        self.bg = (245, 255, 235)
        self.color = (255, 160, 0)
        self.opponent = opponent
        self.pcolors = [(244, 67, 54), (77, 208, 225)]
        self.texts = ['New Game', 'Go back']
        self.text_fonts = [small, small]
        self.text_sizes = [self.text_fonts[x].size(self.texts[x]) for x in range(len(self.texts))]
        self.positions = [(int(WIDTH * 0.85), int(WIDTH * 0.15)), (int(WIDTH * 0.85), int(HEIGHT - WIDTH * 0.15))]
        self.buttons = [(int(WIDTH * 0.85), int(WIDTH * 0.15), int(WIDTH * 0.1)),
                        (int(WIDTH * 0.85), int(HEIGHT - WIDTH * 0.15), int(WIDTH * 0.1))]
        self.commands = [self.game.new_game, lambda: change_main(menu)]
        self.keys = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_SPACE]
        self.command_keys = [lambda: self.game.move_arrow('w'), lambda: self.game.move_arrow('e'),
                             lambda: self.game.play(self.game.arrow, self.game.turn)]

    def draw(self, window):
            pygame.draw.line(window, (0, 0, 0),
                             (0, int(HEIGHT // 7)), (int(WIDTH * 0.7), int(HEIGHT // 7)), int(DIAGONAL // 120))
            pygame.draw.line(window, (0, 0, 0), (int(WIDTH * 0.7), 0), (int(WIDTH * 0.7), HEIGHT), int(DIAGONAL // 120))

            for x in range(7):
                pygame.draw.line(window, (0, 0, 0), (x * int(HEIGHT // 7), int(HEIGHT // 7)),
                                 (x * int(HEIGHT // 7), HEIGHT), int(DIAGONAL // 360))

            for x in range(7):
                for y in range(6):
                    if self.game.board[y][x] != 9:
                        pygame.draw.circle(window, self.pcolors[self.game.board[y][x]],
                                           (int((x + 0.5) * HEIGHT // 7), int((1 + y + 0.5) * HEIGHT // 7)),
                                           int(HEIGHT // 21))
                    pygame.draw.circle(window, (0, 0, 0), (int((x + 0.5) * HEIGHT // 7),
                                                           int((1 + y + 0.5) * HEIGHT // 7)),
                                       int(HEIGHT // 21), int(DIAGONAL // 200))

            b = int(self.game.arrow * HEIGHT / 7)
            pygame.draw.polygon(window, self.pcolors[self.game.turn], ((HEIGHT // 56 + b, HEIGHT // 56),
                                                                  (7 * HEIGHT // 56 + b, HEIGHT // 56),
                                                                  (4 * HEIGHT // 56 + b, 7 * HEIGHT // 56)))
            pygame.draw.polygon(window, (0, 0, 0), ((HEIGHT // 56 + b, HEIGHT // 56),
                                                    (7 * HEIGHT // 56 + b, HEIGHT // 56),
                                                    (4 * HEIGHT // 56 + b, 7 * HEIGHT // 56)), int(DIAGONAL // 200))

            for y in range(len(self.buttons)):
                pygame.draw.circle(window, self.color, (self.buttons[y][0], self.buttons[y][1]), self.buttons[y][2])
                pygame.draw.circle(window, (0, 0, 0),
                                   (self.buttons[y][0], self.buttons[y][1]), self.buttons[y][2], int(DIAGONAL // 150))

            for x in range(len(self.texts)):
                window.blit(self.text_fonts[x].render(self.texts[x], False, (0, 0, 0)),
                            (self.positions[x][0] - self.text_sizes[x][0] / 2,
                             self.positions[x][1] - self.text_sizes[x][1] / 2))

            if self.game.state == 0:
                c = self.pcolors[0]
            elif self.game.state == 1:
                c = self.pcolors[1]
            else:
                c = (255, 255, 255)

            pygame.draw.circle(window, c, (int(WIDTH * 0.85), int(HEIGHT / 2)), int(WIDTH / 20))
            pygame.draw.circle(window, (0, 0, 0),
                               (int(WIDTH * 0.85), int(HEIGHT / 2)), int(WIDTH / 20), int(DIAGONAL / 150))


class Ai:
    def __init__(self):
        self.depth = 2
        self.value = 1
        self.strategy = 'random'

    def get_move(self, game):
        def evaluate_position(g):
            if self.strategy == 'random':
                return random.random()
            if self.strategy == 'gandalf':
                ev = 0
                fours = []
                for x in range(7):
                    for y in range(6):
                        if y + 3 < 6:
                            fours.append([g.board[y][x], g.board[y + 1][x],
                                          g.board[y + 2][x], g.board[y + 3][x]])
                        if x + 3 < 7:
                            fours.append([g.board[y][x], g.board[y][x + 1],
                                          g.board[y][x + 2], g.board[y][x + 3]])
                        if x + 3 < 7 and y + 3 < 6:
                            fours.append([g.board[y][x], g.board[y + 1][x + 1],
                                          g.board[y + 2][x + 2], g.board[y + 3][x + 3]])
                        if x - 3 > 0 and y + 3 < 6:
                            fours.append([g.board[y][x], g.board[y + 1][x - 1],
                                          g.board[y + 2][x - 2], g.board[y + 3][x - 3]])
                w = self.value
                e = (w + 1) % 2
                for streak in fours:
                    if streak == [w, w, w, w]:
                        ev += 100
                    if streak == [e, e, e, e]:
                        ev += -100
                    if sorted(streak) == [w, w, w, 9]:
                        ev += 1
                    if sorted(streak) == [e, e, e, 9]:
                        ev -= 1
                    if sorted(streak) == [w, w, 9, 9]:
                        ev += 0.01
                    if sorted(streak) == [e, e, 9, 9]:
                        ev -= 0.01
                return ev
            if self.strategy == 'merlin':
                ev = 0
                w = self.value
                e = (w + 1) % 2
                keys = [[3, 4, 5, 7, 5, 4, 3],
                        [4, 6, 6, 8, 6, 6, 4],
                        [5, 6, 9, 13, 9, 6, 5],
                        [5, 6, 9, 13, 9, 6, 5],
                        [4, 6, 6, 8, 6, 6, 4],
                        [3, 4, 5, 7, 5, 4, 3]]
                fours = []
                for x in range(7):
                    for y in range(6):
                        if g.board[y][x] == w:
                            ev += (keys[y][x]) * 0.001
                        elif g.board[y][x] == w:
                            ev -= (keys[y][x]) * 0.001
                        if y + 3 < 6:
                            fours.append([g.board[y][x], g.board[y + 1][x],
                                          g.board[y + 2][x], g.board[y + 3][x]])
                        if x + 3 < 7:
                            fours.append([g.board[y][x], g.board[y][x + 1],
                                          g.board[y][x + 2], g.board[y][x + 3]])
                        if x + 3 < 7 and y + 3 < 6:
                            fours.append([g.board[y][x], g.board[y + 1][x + 1],
                                          g.board[y + 2][x + 2], g.board[y + 3][x + 3]])
                        if x - 3 > 0 and y + 3 < 6:
                            fours.append([g.board[y][x], g.board[y + 1][x - 1],
                                          g.board[y + 2][x - 2], g.board[y + 3][x - 3]])
                for streak in fours:
                    if streak == [w, w, w, w]:
                        ev += 100
                    if streak == [e, e, e, e]:
                        ev += -100
                    if sorted(streak) == [w, w, w, 9]:
                        ev += 1
                    if sorted(streak) == [e, e, e, 9]:
                        ev -= 1
                    if sorted(streak) == [w, w, 9, 9]:
                        ev += 0.01
                    if sorted(streak) == [e, e, 9, 9]:
                        ev -= 0.01
                return ev
            if self.strategy == 'dumbledore':
                ev = 0
                w = self.value
                e = (w + 1) % 2
                keys = [[3.0, 4.0, 5.0, 7.0, 5.0, 4.0, 3.0],
                        [4.5, 6.5, 6.5, 8.5, 6.5, 6.5, 4.5],
                        [6.0, 7.0, 10.0, 14.0, 10.0, 7.0, 6.0],
                        [6.5, 7.5, 10.5, 14.5, 10.5, 7.5, 6.5],
                        [6.0, 8.0, 8.0, 10.0, 8.0, 8.0, 6.0],
                        [5.5, 6.5, 7.5, 9.5, 7.5, 6.5, 5.5]]
                fours = []
                for x in range(7):
                    for y in range(6):
                        if g.board[y][x] == w:
                            ev += (keys[y][x]) * 0.0025
                        elif g.board[y][x] == w:
                            ev -= (keys[y][x]) * 0.0025
                        if y + 3 < 6:
                            fours.append([g.board[y][x], g.board[y + 1][x],
                                          g.board[y + 2][x], g.board[y + 3][x]])
                        if x + 3 < 7:
                            fours.append([g.board[y][x], g.board[y][x + 1],
                                          g.board[y][x + 2], g.board[y][x + 3]])
                        if x + 3 < 7 and y + 3 < 6:
                            fours.append([g.board[y][x], g.board[y + 1][x + 1],
                                          g.board[y + 2][x + 2], g.board[y + 3][x + 3]])
                        if x - 3 > 0 and y + 3 < 6:
                            fours.append([g.board[y][x], g.board[y + 1][x - 1],
                                          g.board[y + 2][x - 2], g.board[y + 3][x - 3]])
                for streak in fours:
                    if streak == [w, w, w, w]:
                        ev += 100
                    if streak == [e, e, e, e]:
                        ev += -100
                    if sorted(streak) == [w, w, w, 9]:
                        ev += 1
                    if sorted(streak) == [e, e, e, 9]:
                        ev -= 1
                    if sorted(streak) == [w, w, 9, 9]:
                        ev += 0.01
                    if sorted(streak) == [e, e, 9, 9]:
                        ev -= 0.01
                return ev

        def min_play(g, depth, alpha, beta):
            if g.check_result() == self.value:
                return float('inf')
            if g.check_result() == (self.value + 1) % 2:
                return -float('inf')
            if depth == 0:
                return evaluate_position(g)
            available_moves = [x for x in range(7) if g.floors[x] >= 0]
            best_score = float('inf')
            for move in available_moves:
                clone = copy.deepcopy(g)
                clone.play(move, (self.value + 1) % 2)
                score = max_play(clone, depth - 1, alpha, beta)
                beta = min(beta, best_score)
                if score < best_score:
                    best_score = score
                if beta <= alpha:
                    break
            return best_score

        def max_play(g, depth, alpha, beta):
            if g.check_result() == self.value:
                return float('inf')
            if g.check_result() == (self.value + 1) % 2:
                return -float('inf')
            if depth == 0:
                return evaluate_position(g)
            available_moves = [x for x in range(7) if g.floors[x] >= 0]
            best_score = -float('inf')
            for move in available_moves:
                clone = copy.deepcopy(g)
                clone.play(move, self.value)
                score = min_play(clone, depth - 1, alpha, beta)
                alpha = max(alpha, best_score)
                if score > best_score:
                    best_score = score
                if beta <= alpha:
                    break
            return best_score

        def min_max(g, depth):
            moves = [x for x in range(7) if g.floors[x] >= 0]
            best_move = random.choice(moves)
            best_score = -float('inf')
            alpha = -float('inf')
            beta = float('inf')
            for move in moves:
                clone = copy.deepcopy(g)
                clone.play(move, self.value)
                score = min_play(clone, depth, alpha, beta)
                if score > best_score:
                    best_score = score
                    best_move = move
            return best_move, best_score

        answer = min_max(game, self.depth)
        return answer[0]


ai = Ai()


def change_main(new):
    global main
    main = new


def distance(mouse_cordinates, target):
    return ((mouse_cordinates[0] - target[0]) ** 2 + (mouse_cordinates[1] - target[1]) ** 2) ** 0.5


def change_starting_player(starter):
    if starter == 'you':
        ai.value = 1
        ai_menu.states[0] = True
        ai_menu.states[1] = False
    else:
        ai.value = 0
        ai_menu.states[1] = True
        ai_menu.states[0] = False


def change_ai_depth(depth):
    ai.depth = depth
    for x in range(2, 6):
        ai_menu.states[x] = False
    if depth == 2:
        ai_menu.states[2] = True
    elif depth == 4:
        ai_menu.states[3] = True
    elif depth == 6:
        ai_menu.states[4] = True
    else:
        ai_menu.states[5] = True


def change_ai_strategy(strategy):
    ai.strategy = strategy
    change_main(a_game)


menu = Menu((50, 205, 50), (173, 255, 47), ['CONNECT 4', 'P vs P', 'P vs A.I.'], [title, font, font],
            [(WIDTH / 2, HEIGHT / 4), (WIDTH / 4, 5 * HEIGHT / 8), (3 * WIDTH / 4, 5 * HEIGHT / 8)],
            [(WIDTH // 4, 5 * HEIGHT // 8, int(DIAGONAL // 8)), (3 * WIDTH // 4, 5 * HEIGHT // 8, int(DIAGONAL // 8))],
            [lambda: change_main(p_game), lambda: change_main(ai_menu)], [False, False], (0, 0, 0))

ai_menu = Menu((212, 225, 87), (255, 64, 129), ['Starting Player: ', 'A.I. Depth: ', 'Engine: ', 'You', 'A.I.', '2',
                                                '4', '6', '8', 'Random', 'Gandalf', 'Merlin', 'Alvus'],
               [font, font, font, small, small, font, font, font, font, u_small, u_small, u_small, u_small],
               [(WIDTH // 4, HEIGHT // 8), (WIDTH // 4, 3 * HEIGHT // 8), (WIDTH // 4, 3 * HEIGHT // 4),
                (2 * WIDTH // 3, HEIGHT // 8), (5 * WIDTH // 6, HEIGHT // 8), (0.6 * WIDTH, HEIGHT * 0.375),
                (0.7 * WIDTH, HEIGHT * 0.375), (0.8 * WIDTH, HEIGHT * 0.375), (0.9 * WIDTH, HEIGHT * 0.375),
                (2 * WIDTH // 3, HEIGHT * 0.65), (5 * WIDTH // 6, HEIGHT * 0.85), (2 * WIDTH // 3, HEIGHT * 0.85),
                (5 * WIDTH // 6, HEIGHT * 0.65)],
               [(2 * WIDTH // 3, HEIGHT // 8, WIDTH // 16), (5 * WIDTH // 6, HEIGHT // 8, WIDTH // 16),
                (0.6 * WIDTH, HEIGHT * 0.375, WIDTH // 24), (0.7 * WIDTH, HEIGHT * 0.375, WIDTH // 24),
                (0.8 * WIDTH, HEIGHT * 0.375, WIDTH // 24), (0.9 * WIDTH, HEIGHT * 0.375, WIDTH // 24),
                (2 * WIDTH // 3, HEIGHT * 0.65, WIDTH // 16), (5 * WIDTH // 6, HEIGHT * 0.85, WIDTH // 16),
                (2 * WIDTH // 3, HEIGHT * 0.85, WIDTH // 16), (5 * WIDTH // 6, HEIGHT * 0.65, WIDTH // 16)],
               [lambda: change_starting_player('you'), lambda: change_starting_player('ai'), lambda: change_ai_depth(2),
                lambda: change_ai_depth(4), lambda: change_ai_depth(6), lambda: change_ai_depth(8),
                lambda: change_ai_strategy('random'), lambda: change_ai_strategy('gandalf'),
                lambda: change_ai_strategy('merlin'), lambda: change_ai_strategy('dumbledore')],
               [True, False, True, False, False, False, False, False, False, False], (0, 188, 212))
p_game = GameMenu('real')
a_game = GameMenu('ai')
main = menu
run = True
while run:
    win.fill(main.bg)
    main.draw(win)
    if main == p_game or main == a_game:
        main.game.check_result()
    if main == a_game and a_game.game.turn == ai.value:
        move = ai.get_move(a_game.game)
        a_game.game.play(move, ai.value)
        a_game.game.turn = (ai.value + 1) % 2
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            coordinates = pygame.mouse.get_pos()
            for n, button in enumerate(main.buttons):
                if distance(coordinates, button) < button[2]:
                    main.commands[n]()
        if event.type == pygame.KEYDOWN:
            for n, key in enumerate(main.keys):
                if event.key == key:
                    main.command_keys[n]()
    pygame.display.update()
pygame.quit()
