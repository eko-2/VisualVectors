import pygame
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 900
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Force Vector Calculator")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Fonts
font = pygame.font.Font(None, 32)

def draw_text(text, x, y):
    surface = font.render(text, True, BLACK)
    screen.blit(surface, (x, y))

def calculate_resultant(horizontal, vertical):
    resultant = math.sqrt(horizontal**2 + vertical**2)
    angle = math.degrees(math.atan2(vertical, horizontal))
    return resultant, angle

def create_vector_plot(horizontal, vertical):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.quiver(0, 0, horizontal, vertical, angles='xy', scale_units='xy', scale=1, color='r')
    ax.quiver(0, 0, horizontal, 0, angles='xy', scale_units='xy', scale=1, color='b')
    ax.quiver(0, 0, 0, vertical, angles='xy', scale_units='xy', scale=1, color='g')
    
    max_force = max(abs(horizontal), abs(vertical), 1)
    ax.set_xlim(-max_force, max_force)
    ax.set_ylim(-max_force, max_force)
    ax.set_aspect('equal')
    ax.grid(True)
    ax.set_title("Force Vectors")
    ax.set_xlabel("Horizontal Force")
    ax.set_ylabel("Vertical Force")
    
    # Convert Matplotlib figure to Pygame surface
    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    size = canvas.get_width_height()
    plt.close(fig)
    return pygame.image.fromstring(raw_data, size, "RGB")

# Input boxes
horizontal_input = pygame.Rect(200, 50, 140, 32)
vertical_input = pygame.Rect(200, 100, 140, 32)
horizontal_force = ""
vertical_force = ""
active_input = None

# Main loop
running = True
graph_surface = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if horizontal_input.collidepoint(event.pos):
                active_input = horizontal_input
            elif vertical_input.collidepoint(event.pos):
                active_input = vertical_input
            else:
                active_input = None
        if event.type == pygame.KEYDOWN:
            if active_input:
                if event.key == pygame.K_RETURN:
                    active_input = None
                elif event.key == pygame.K_BACKSPACE:
                    if active_input == horizontal_input:
                        horizontal_force = horizontal_force[:-1]
                    else:
                        vertical_force = vertical_force[:-1]
                else:
                    if active_input == horizontal_input:
                        horizontal_force += event.unicode
                    else:
                        vertical_force += event.unicode

    screen.fill(WHITE)

    # Draw input boxes
    pygame.draw.rect(screen, RED if active_input == horizontal_input else BLACK, horizontal_input, 2)
    pygame.draw.rect(screen, RED if active_input == vertical_input else BLACK, vertical_input, 2)

    # Render text
    draw_text("Horizontal Force:", 20, 50)
    draw_text("Vertical Force:", 20, 100)
    draw_text(horizontal_force, 210, 50)
    draw_text(vertical_force, 210, 100)

    # Calculate and display resultant force
    try:
        h_force = float(horizontal_force) if horizontal_force else 0
        v_force = float(vertical_force) if vertical_force else 0
        resultant, angle = calculate_resultant(h_force, v_force)
        draw_text(f"Resultant Force: {resultant:.2f}", 20, 150)
        draw_text(f"Angle: {angle:.2f} degrees", 20, 200)

        # Create and display the graph
        graph_surface = create_vector_plot(h_force, v_force)
        screen.blit(graph_surface, (200, 250))

    except ValueError:
        draw_text("Please enter valid numbers", 20, 150)

    pygame.display.flip()

pygame.quit()
