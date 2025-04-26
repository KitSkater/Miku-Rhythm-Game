import pygame
import base64
import io
import sys

# Initialize Pygame
pygame.init()

# 🎤 Window setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Miku Rhythm Game 🎵")

# 🎨 Base64-encoded Miku image
miku_image_base64 = b"""
iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABHUlEQVRYR+2XsQ2AIBBE3/f+lzvC
xMtJXUT0db8BlvOB0AhOkHn84xhMIlSu2Ce279NUAKZ7NNKmAAmJoYZrKAv1IW7bgBWURcwrGtoF
4VaAdSEVQGECtxN6kNnTx0rr2LWSUJD2Oa2s8Whk2fZPXT5bHXYuQELn8xCziUKOwTVlf5gGWDaz
YOaWWuJz1AcBjvTV+6hKNxkaRrHPoqS0KnGoYhxuUwMvlOxKH46fv1Vb6au0qg6quNJ/qn7DZkj5
HgAAAABJRU5ErkJggg==
"""

# 🖼️ Decode and load Miku image
miku_image_data = base64.b64decode(miku_image_base64)
miku_image_file = io.BytesIO(miku_image_data)
miku = pygame.image.load(miku_image_file)

# 🎵 Load the music file
try:
    pygame.mixer.music.load("song.mp3")  # Song must be in the same folder
except:
    print("⚠️ Couldn't find 'song.mp3'! Put your song in the same folder!")
    sys.exit()

# Play the song
pygame.mixer.music.play(-1)  # Loop forever

# 🎯 Main game loop
clock = pygame.time.Clock()
running = True
while running:
    screen.fill((255, 255, 255))  # White background

    # Draw Miku in the bottom-right corner
    screen.blit(miku, (WIDTH - miku.get_width() - 10, HEIGHT - miku.get_height() - 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()


