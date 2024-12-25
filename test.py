import pygame
import card_constructor
import card_data

pygame.init()

# Set up the display surface (the screen)
screen = pygame.display.set_mode((800, 600))  # A surface to render on

card = card_constructor.create_card(1057, card_data.card_info[1057])

running = True
while running:
    screen.fill((0, 0, 0))  # Fill the screen with a black background

    # Draw the card
    card.draw_sprite(screen)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            card.start_drag(event.pos)  # Start dragging when the mouse button is pressed
        
        if event.type == pygame.MOUSEMOTION:
            if card.dragging:
                card.drag(event.pos)  # Update the card's position during the drag
        
        if event.type == pygame.MOUSEBUTTONUP:
            card.stop_drag()  # Snap the card back to its original position when the mouse button is released

    card.update()

    pygame.display.flip()  # Update the display

pygame.quit()