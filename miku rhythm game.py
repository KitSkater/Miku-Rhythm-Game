import pygame
import time
import os

# Setup
pygame.init()
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Miku Rhythm Game 💙")

# Fonts
font = pygame.font.SysFont("Arial", 30)
big_font = pygame.font.SysFont("Arial", 48)

# Colors
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
PINK = (255, 105, 180)
BLACK = (0, 0, 0)
GREY = (100, 100, 100)

# Key mapping
keys = ['left', 'up', 'down', 'right']
key_map = {
    'left': pygame.K_LEFT,
    'up': pygame.K_UP,
    'down': pygame.K_DOWN,
    'right': pygame.K_RIGHT
}
positions = {
    'left': 200,
    'up': 300,
    'down': 400,
    'right': 500
}

# Target height
target_y = HEIGHT - 100

# Note object
class Note:
    def __init__(self, direction, time_to_hit):
        self.direction = direction
        self.x = positions[direction]
        self.y = -50
        self.time_to_hit = time_to_hit
        self.hit = False

    def update(self, dt):
        self.y += 300 * dt

    def draw(self):
        pygame.draw.rect(win, CYAN, (self.x - 25, self.y - 25, 50, 50))

# Load beatmap
def load_beatmap(file_path):
    notes = []
    with open(file_path, 'r') as f:
        for line in f:
            if line.strip() == '':
                continue
            t, d = line.strip().split()
            notes.append(Note(d, float(t)))
    return notes

# Draw targets
def draw_targets():
    for dir in keys:
        x = positions[dir]
        pygame.draw.rect(win, PINK, (x - 25, target_y - 25, 50, 50), 3)

# Game variables
notes = load_beatmap("beatmap.txt")
score = 0
combo = 0
hits = []
note_index = 0
start_time = None
miku = pygame.image.load("assets/miku.png")

# Load and play song
pygame.mixer.music.load("assets/song.mp3")
pygame.mixer.music.play()

clock = pygame.time.Clock()
running = True

while running:
    dt = clock.tick(60) / 1000.0
    win.fill(BLACK)

    if start_time is None:
        start_time = time.time()

    current_time = time.time() - start_time
    draw_targets()

    # Spawn notes
    while note_index < len(notes) and notes[note_index].time_to_hit <= current_time + 1:
        note_index += 1

    for note in notes:
        note.update(dt)
        if not note.hit:
            note.draw()

    # Draw Miku
    win.blit(pygame.transform.scale(miku, (200, 200)), (WIDTH - 220, HEIGHT - 220))

    # Input check
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            for note in notes:
                if not note.hit and abs(note.time_to_hit - current_time) <= 0.3:
                    if event.key == key_map[note.direction]:
                        time_diff = abs(note.time_to_hit - current_time)
                        note.hit = True
                        if time_diff <= 0.1:
                            hits.append(("Perfect", time.time()))
                            score += 100
                            combo += 1
                        else:
                            hits.append(("Good", time.time()))
                            score += 50
                            combo += 1
                        break
            else:
                hits.append(("Miss", time.time()))
                combo = 0

    # Draw score
    win.blit(font.render(f"Score: {score}", True, WHITE), (20, 20))
    win.blit(font.render(f"Combo: {combo}", True, WHITE), (20, 60))

    # Show recent hit text
    hits = [h for h in hits if time.time() - h[1] < 1.0]
    for i, (label, _) in enumerate(hits[-3:]):
        color = WHITE if label == "Perfect" else CYAN if label == "Good" else GREY
        text = big_font.render(label, True, color)
        win.blit(text, (WIDTH // 2 - 60, 100 + i * 40))

    pygame.display.update()

pygame.quit()
