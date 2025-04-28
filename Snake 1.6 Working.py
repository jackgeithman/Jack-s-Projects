import pygame
import random

# Initiate pygame!
pygame.init() 

#Display 
display_width, display_height = 1200, 900
window_width, window_height = 800, 600
offset_x, offset_y = 200, 150
window = pygame.display.set_mode((display_width, display_height))

# Color 
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
black = (0, 0, 0)
color = white

# Block and Line Widths
line_width = 10
block_width = 20

#Wall
wall= []
wall_top = pygame.Rect(offset_x, offset_y, window_width, line_width)
wall_right = pygame.Rect(display_width - offset_x, offset_y, line_width, window_height)
wall_bottom = pygame.Rect(offset_x, display_height - offset_y, window_width + line_width, line_width)
wall_left = pygame.Rect(offset_x, offset_y, line_width, window_height)
wall.append(wall_top)
wall.append(wall_right)
wall.append(wall_bottom)
wall.append(wall_left)

#Clock
clock = pygame.time.Clock()

#Fonts
score_font = pygame.font.Font(None, 50) # None is defualt font, 50 = size.
lost_font = pygame.font.Font(None, 100) 

# Functions

def start ():
    global movement, snake_position, score_txt, lost_txt, lost, running, apple, snake_segments, score
    
    snake_segments = [pygame.Rect(((window_width // 2) + block_width + offset_x), 
                           ((window_height // 2) + block_width + offset_y), 
                           block_width, block_width)]

    apple = pygame.Rect((random.randint(block_width + offset_x, (display_width - block_width - offset_x)),
                      random.randint(block_width + offset_y, (display_height - block_width - offset_y)), 
                      block_width, block_width))
    
    #Variables
    movement = "stop"
    snake_position = 0 
    score = 0
    score_txt = score_font.render(f"Score: {score}", True, white)
    lost_txt = lost_font.render("You have lost :(", True, red)
    lost = False
    running = True




def check_collisions():
    if snake_segments[0].colliderect(apple):
        move_apple()
        set_score()
        add_segment()
    for w in wall:
         if apple.colliderect(w):
            move_apple()
    for w in wall:
        for i in range (len(snake_segments)):
            if snake_segments[i].colliderect(w):
                lose()

def set_score():
    global score
    score += 1
    global score_txt
    score_txt = score_font.render(f"Score: {score}", True, white)

def move_apple():
    global apple
    apple = pygame.Rect(
        random.randint((block_width + offset_x), (display_width - block_width - offset_x)), 
        random.randint((block_width + offset_y), (display_height - block_width - offset_y)), 
        block_width, block_width)

def add_segment():
        global snake_segments
        new_segment = pygame.Rect(snake_segments[-1].x, snake_segments[-1].y, block_width, block_width)
        snake_segments.append(new_segment)
                    
def snake_movement(event):
        global apple
        global movement
        global running
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                movement = "left"
            if event.key == pygame.K_RIGHT:
                movement = "right"
            if event.key == pygame.K_UP:
                movement = "up"
            if event.key == pygame.K_DOWN:
                movement = "down"
            

def controller(event):
    global apple
    global movement
    global running
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_b:
                movement = "stop"
        if event.key == pygame.K_a:
                move_apple()
        if event.key == pygame.K_q:
                running = False
        if event.key == pygame.K_r:
                start()

def move_snake():
     global snake_segments
     global snake_position
     global movement
     global running
     for i in range(len(snake_segments) - 1, 0, -1): 
          snake_segments[i].x = snake_segments[i-1].x
          snake_segments[i].y = snake_segments[i-1].y
     if movement == "left":
        snake_segments[0].x += -20
     if movement == "right":
        snake_segments[0].x += 20
     if movement == "up":
        snake_segments[0].y += -20
     if movement == "down":
        snake_segments[0].y += 20

def lose():
     global lost
     lost = True
     window.blit(lost_txt, (400, 30))


def draw():

    def draw_frame():
        for i in range(4):
            pygame.draw.rect(window, white, wall[i])
        
    def draw_apple():
        pygame.draw.rect(window, red, apple)

    def draw_score():
        window.blit(score_txt, (50, 50)) # Make sure you set x,y position as a tuple for blit f()

    def draw_snake():
        for segment in snake_segments:
            pygame.draw.rect(window, green, (segment))

    draw_apple()
    draw_frame()
    draw_snake()
    draw_score()

##################################### 
start()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        snake_movement(event) 
        controller(event)
    if lost == False:
        window.fill(black)
        check_collisions()
        move_snake()
        draw()
        pygame.display.update() #Upddates display with updated information.
        clock.tick(20) #Holds function for 1/200th of a second.
    if lost == True:
        pygame.display.update()
        clock.tick(20) #Holds function for 1/200th of a second.


pygame.quit()
