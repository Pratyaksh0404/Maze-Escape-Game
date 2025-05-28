import pygame
import random
import sys
import math

# Initialize pygame
pygame.init()

# Constants
MAZE_WIDTH = 15
MAZE_HEIGHT = 15
FPS = 60
TIME_LIMIT = 60  # seconds
TOP_BAR_HEIGHT = 40  # reserved space for timer and key info

# Colors
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

# Setup screen
window = pygame.display.set_mode((800, 640), pygame.RESIZABLE)
pygame.display.set_caption("Maze Escape")
clock = pygame.time.Clock()

# Load images
player_img = pygame.image.load("player.png")
key_img = pygame.image.load("key.png")
door_locked_img = pygame.image.load("door_locked.png")
door_open_img = pygame.image.load("door_open.png")
wall_texture = pygame.image.load("wall_texture.png")

# Time boost item (drawn programmatically)
time_boost_img = pygame.Surface((40, 40), pygame.SRCALPHA)
pygame.draw.circle(time_boost_img, (0, 200, 255), (20, 20), 13)

def scale_images(tile_size):
    global player_img, key_img, door_locked_img, door_open_img, wall_texture
    player_img = pygame.transform.scale(player_img, (tile_size, tile_size))
    key_img = pygame.transform.scale(key_img, (tile_size, tile_size))
    door_locked_img = pygame.transform.scale(door_locked_img, (tile_size, tile_size))
    door_open_img = pygame.transform.scale(door_open_img, (tile_size, tile_size))
    wall_texture = pygame.transform.scale(wall_texture, (tile_size, tile_size))

def rotate_player_image(direction):
    if direction == 'LEFT':
        return pygame.transform.flip(player_img, True, False)
    return player_img

def generate_maze(width, height):
    maze = [[1 for _ in range(width)] for _ in range(height)]
    directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]

    def is_valid(nx, ny):
        return 0 <= nx < height and 0 <= ny < width

    def carve(x, y):
        maze[x][y] = 0
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            between_x, between_y = x + dx // 2, y + dy // 2
            if is_valid(nx, ny) and maze[nx][ny] == 1:
                maze[between_x][between_y] = 0
                carve(nx, ny)

    carve(0, 0)
    return maze

def get_random_tile(maze, min_dist, avoid_list):
    while True:
        y, x = random.randint(0, MAZE_HEIGHT-1), random.randint(0, MAZE_WIDTH-1)
        if maze[y][x] == 0 and all(abs(x - ax) + abs(y - ay) >= min_dist for ay, ax in avoid_list):
            return (y, x)

class Player:
    def __init__(self, x, y, tile_size):
        self.tile_size = tile_size
        self.grid_x = x
        self.grid_y = y
        self.x = x * tile_size
        self.y = y * tile_size
        self.target_x = self.x
        self.target_y = self.y
        self.speed = 4
        self.facing = 'RIGHT'
        self.has_key = False
        self.moving = False
        self.x_offset = 0
        self.y_offset = 0

    def update(self, keys, maze):
        if not self.moving:
            if keys[pygame.K_w] and self.can_move(0, -1, maze):
                self.grid_y -= 1
                self.target_y -= self.tile_size
                self.moving = True
            elif keys[pygame.K_s] and self.can_move(0, 1, maze):
                self.grid_y += 1
                self.target_y += self.tile_size
                self.moving = True
            elif keys[pygame.K_a] and self.can_move(-1, 0, maze):
                self.grid_x -= 1
                self.target_x -= self.tile_size
                self.moving = True
                self.facing = 'LEFT'
            elif keys[pygame.K_d] and self.can_move(1, 0, maze):
                self.grid_x += 1
                self.target_x += self.tile_size
                self.moving = True
                self.facing = 'RIGHT'

        if self.moving:
            if self.x < self.target_x: self.x += self.speed
            elif self.x > self.target_x: self.x -= self.speed
            if self.y < self.target_y: self.y += self.speed
            elif self.y > self.target_y: self.y -= self.speed

            if self.x == self.target_x and self.y == self.target_y:
                self.moving = False

    def can_move(self, dx, dy, maze):
        new_x = self.grid_x + dx
        new_y = self.grid_y + dy
        if 0 <= new_x < MAZE_WIDTH and 0 <= new_y < MAZE_HEIGHT:
            return maze[new_y][new_x] == 0
        return False

    def draw(self, surface):
        surface.blit(rotate_player_image(self.facing), (self.x + self.x_offset, self.y + self.y_offset))

def draw_button(text, x, y, width, height, bg_color=GRAY, text_color=WHITE):
    font = pygame.font.SysFont(None, 36)
    pygame.draw.rect(window, bg_color, (x, y, width, height))
    txt = font.render(text, True, text_color)
    window.blit(txt, (x + (width - txt.get_width()) // 2, y + (height - txt.get_height()) // 2))
    return pygame.Rect(x, y, width, height)

def show_menu():
    while True:
        window.fill((200, 200, 255))
        width, height = window.get_size()

        title_font = pygame.font.SysFont("comicsansms", 72)
        title_text = title_font.render("MAZE ESCAPE", True, (0, 50, 150))
        window.blit(title_text, ((width - title_text.get_width()) // 2, 60))

        btn_width, btn_height = 200, 60
        play_x = (width - btn_width) // 2
        exit_x = (width - btn_width) // 2

        play_btn = draw_button("Play Game", play_x, 180, btn_width, btn_height, bg_color=(0, 120, 215))
        exit_btn = draw_button("Exit", exit_x, 280, btn_width, btn_height, bg_color=(200, 50, 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_btn.collidepoint(event.pos):
                    return
                elif exit_btn.collidepoint(event.pos):
                    pygame.quit(); sys.exit()

def show_end_screen():
    while True:
        window.fill((200, 200, 255))  # Same bg color
        width, height = window.get_size()

        font = pygame.font.SysFont("comicsansms", 48)
        text = font.render("Maze Escaped!", True, (0, 150, 50))
        window.blit(text, ((width - text.get_width()) // 2, 80))

        btn_width, btn_height = 200, 60
        play_again_x = (width - btn_width) // 2
        menu_x = (width - btn_width) // 2

        restart_btn = draw_button("Play Again", play_again_x, 180, btn_width, btn_height, bg_color=(0, 120, 215))
        menu_btn = draw_button("Main Menu", menu_x, 280, btn_width, btn_height, bg_color=(200, 50, 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_btn.collidepoint(event.pos):
                    return "restart"
                elif menu_btn.collidepoint(event.pos):
                    return "menu"


def astar_pathfinding(maze, start, goal):
    from queue import PriorityQueue
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: abs(start[0] - goal[0]) + abs(start[1] - goal[1])}

    while not open_set.empty():
        _, current = open_set.get()
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for dx, dy in dirs:
            neighbor = (current[0] + dy, current[1] + dx)
            if 0 <= neighbor[0] < MAZE_HEIGHT and 0 <= neighbor[1] < MAZE_WIDTH:
                if maze[neighbor[0]][neighbor[1]] != 1:
                    tentative = g_score[current] + 1
                    if neighbor not in g_score or tentative < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative
                        f_score[neighbor] = tentative + abs(neighbor[0] - goal[0]) + abs(neighbor[1] - goal[1])
                        open_set.put((f_score[neighbor], neighbor))
    return []

def draw_arrow_path(surface, path, tile_size, x_offset, y_offset):
    arrow_color = (30, 144, 255)  # Dodger blue
    for i in range(len(path) - 1):
        y1, x1 = path[i]
        y2, x2 = path[i+1]
        start_pos = (x_offset + x1 * tile_size + tile_size // 2,
                     y_offset + y1 * tile_size + tile_size // 2)
        end_pos = (x_offset + x2 * tile_size + tile_size // 2,
                   y_offset + y2 * tile_size + tile_size // 2)
        pygame.draw.line(surface, arrow_color, start_pos, end_pos, 4)

        # Draw arrowhead
        dx, dy = end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]
        angle = math.atan2(dy, dx)
        arrow_len = 10
        arrow_angle = math.pi / 6
        left = (end_pos[0] - arrow_len * math.cos(angle - arrow_angle),
                end_pos[1] - arrow_len * math.sin(angle - arrow_angle))
        right = (end_pos[0] - arrow_len * math.cos(angle + arrow_angle),
                 end_pos[1] - arrow_len * math.sin(angle + arrow_angle))
        pygame.draw.polygon(surface, arrow_color, [end_pos, left, right])

def show_ideal_path(window, maze, keys, doors, tile_size, x_offset, y_offset):
    full_path = []
    current = (0, 0)
    for key in keys:
        full_path += astar_pathfinding(maze, current, key['pos'])[:-1]
        current = key['pos']
    full_path += astar_pathfinding(maze, current, doors[-1]['pos'])

    draw_arrow_path(window, full_path, tile_size, x_offset, y_offset)
    label_font = pygame.font.SysFont(None, 32)
    label_text = label_font.render("Correct Path", True, (0, 0, 0))
    window.blit(label_text, (400, 10))
    pygame.display.flip()
    pygame.time.wait(3000)

def times_up_screen():
    while True:
        window.fill((255, 230, 230))
        width, height = window.get_size()

        font = pygame.font.SysFont("comicsansms", 48)
        text = font.render("Time's Up!", True, (200, 0, 0))
        window.blit(text, ((width - text.get_width()) // 2, 80))

        btn_width, btn_height = 200, 60
        restart_btn = draw_button("Play Again", (width - btn_width) // 2, 180, btn_width, btn_height, bg_color=(0, 120, 215))
        menu_btn = draw_button("Main Menu", (width - btn_width) // 2, 280, btn_width, btn_height, bg_color=(200, 50, 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_btn.collidepoint(event.pos):
                    return "restart"
                elif menu_btn.collidepoint(event.pos):
                    return "menu"

def game_loop():
    global window
    keys_list, doors, fake_doors = [], [], []

    maze = generate_maze(MAZE_WIDTH, MAZE_HEIGHT)
    width, height = window.get_size()
    tile_size = min((width // MAZE_WIDTH), (height - TOP_BAR_HEIGHT) // MAZE_HEIGHT)
    x_offset = (width - (tile_size * MAZE_WIDTH)) // 2
    y_offset = ((height - TOP_BAR_HEIGHT) - (tile_size * MAZE_HEIGHT)) // 2 + TOP_BAR_HEIGHT
    scale_images(tile_size)
    player = Player(0, 0, tile_size)
    player.x_offset = x_offset
    player.y_offset = y_offset

    avoid_list = [(0, 0)]
    for i in range(3):
        k_pos = get_random_tile(maze, 6, avoid_list)
        d_pos = get_random_tile(maze, 5, avoid_list + [k_pos])
        keys_list.append({'pos': k_pos, 'collected': False})
        doors.append({'pos': d_pos, 'unlocked': False})
        avoid_list.extend([k_pos, d_pos])

    for _ in range(3):
        fake = get_random_tile(maze, 4, avoid_list)
        fake_doors.append({'pos': fake, 'visible': True})
        avoid_list.append(fake)

    boosts = [get_random_tile(maze, 6, avoid_list) for _ in range(2)]
    used_boosts = set()

    font = pygame.font.SysFont(None, 30)
    start_ticks = pygame.time.get_ticks()
    game_won = False
    collected_keys = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                window = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                width, height = event.w, event.h
                tile_size = min((width // MAZE_WIDTH), (height - TOP_BAR_HEIGHT) // MAZE_HEIGHT)
                x_offset = (width - (tile_size * MAZE_WIDTH)) // 2
                y_offset = ((height - TOP_BAR_HEIGHT) - (tile_size * MAZE_HEIGHT)) // 2 + TOP_BAR_HEIGHT
                scale_images(tile_size)
                player.tile_size = tile_size
                player.x = player.grid_x * tile_size
                player.y = player.grid_y * tile_size
                player.target_x = player.x
                player.target_y = player.y
                player.x_offset = x_offset
                player.y_offset = y_offset

        dt = clock.tick(FPS)
        seconds = TIME_LIMIT - (pygame.time.get_ticks() - start_ticks) // 1000
        window.fill(WHITE)

        pressed = pygame.key.get_pressed()
        if not game_won and seconds > 0:
            player.update(pressed, maze)

        # Draw maze and game elements...
        pygame.draw.rect(window, BLACK, (x_offset-2, y_offset-2, tile_size * MAZE_WIDTH + 4, tile_size * MAZE_HEIGHT + 4), 4)
        for row in range(MAZE_HEIGHT):
            for col in range(MAZE_WIDTH):
                if maze[row][col] == 1:
                    rect = pygame.Rect(x_offset + col * tile_size, y_offset + row * tile_size, tile_size, tile_size)
                    window.blit(wall_texture, rect)

        for i, boost in enumerate(boosts):
            if i not in used_boosts:
                window.blit(pygame.transform.scale(time_boost_img, (tile_size, tile_size)),
                            (x_offset + boost[1]*tile_size, y_offset + boost[0]*tile_size))
                if (player.grid_y, player.grid_x) == boost:
                    used_boosts.add(i)
                    start_ticks += 10000

        for i, k in enumerate(keys_list):
            if not k['collected']:
                window.blit(key_img, (x_offset + k['pos'][1]*tile_size, y_offset + k['pos'][0]*tile_size))
                if (player.grid_y, player.grid_x) == k['pos']:
                    k['collected'] = True
                    collected_keys += 1

        for i, d in enumerate(doors):
            if collected_keys > i:
                d['unlocked'] = True
            img = door_open_img if d['unlocked'] else door_locked_img
            window.blit(img, (x_offset + d['pos'][1]*tile_size, y_offset + d['pos'][0]*tile_size))
            if d['unlocked'] and (player.grid_y, player.grid_x) == d['pos'] and i == len(doors)-1:
                game_won = True

        for f in fake_doors:
            if f['visible']:
                window.blit(door_locked_img, (x_offset + f['pos'][1]*tile_size, y_offset + f['pos'][0]*tile_size))
                if (player.grid_y, player.grid_x) == f['pos']:
                    f['visible'] = False

        player.draw(window)

        pygame.draw.rect(window, WHITE, (0, 0, window.get_width(), TOP_BAR_HEIGHT))
        timer_text = font.render(f"Time Left: {max(seconds, 0)}s", True, RED if seconds <= 10 else BLACK)
        keys_text = font.render(f"Keys: {collected_keys}/{len(keys_list)}", True, BLACK)
        window.blit(timer_text, (10, 10))
        window.blit(keys_text, (200, 10))

        pygame.display.flip()

        if game_won:
            pygame.time.delay(500)
            show_ideal_path(window, maze, keys_list, doors, tile_size, x_offset, y_offset)
            pygame.time.delay(3000)
            result = show_end_screen()
            if result == "restart":
                game_loop()
            else:
                show_menu()
                game_loop()

        elif seconds <= 0:
            show_ideal_path(window, maze, keys_list, doors, tile_size, x_offset, y_offset)
            pygame.time.delay(3000)
            result = times_up_screen()
            if result == "restart":
                game_loop()
            else:
                show_menu()
                game_loop()

# Run the game
show_menu()
game_loop()
