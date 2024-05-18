import pygame, sys
from CODE.player import Player

# Init all frameworks, basic func and assign values
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((360, 640))

player = Player(50, 449)
rect_time_background = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)

player.image_load(['DATA/images/player/not_run', 'DATA/images/player/jump/jump1', 'DATA/images/player/jump/jump2'], 2**2)
player.collision_rects()

# Sounds
sound_3 = pygame.mixer.Sound('DATA/sounds/game_over.ogg')
sound_4 = pygame.mixer.Sound('DATA/sounds/restart.ogg')
sound_bool = False


def reset_parameters():
    player.x = 50
    player.y = 449
    player.x_old = 0
    player.map_list = []
    player.map_delete_rects = []
    player.map_delete_rects_time = []
    player.elements_in_delete_rect_list = 0
    player.replace_level_count = 0
    player.level_count = 1
    player.level_second_time = 3
    player.movement_bool = False
    player.movement_count = 100
    player.image_list_index = 0
    player.image_index = 0
    player.amount_counter = 0
    player.animate_bool = True
    player.gravity_count = 0
    player.gravity_bool = True
    player.screen_fill_default = [200, 100, 200]
    player.screen_fill = player.screen_fill_default.copy()
    player.rect_time_opacity_default = 0
    player.rect_time_opacity = 0
    player.rect_time_opacity_bool = False
    player.map_min_rect_y = []
    player.map_min_rect_x = []


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Player funcs
    player.move(screen, 150, player.gravity_bool)
    player.map_generation(player.movement_count, screen)
    player.collision_handler()
    player.animate([50, 4], screen)
    player.flip_anchor_point(screen, screen.get_width() - (screen.get_width() - 50), screen.get_width() - 50)
    player.gravity()
    player.camera_shake(10, 449)

    # White background
    player.background_feel(10)
    player.rect_time_background(3)

    # Output on display
    screen.fill(player.screen_fill)
    rect_time_background.fill((255, 255, 255, player.rect_time_opacity))
    screen.blit(rect_time_background, (0, 0))

    # Texts
    screen.blit(player.text_objects(str(player.level_count), 'DATA/fonts/Decrypted.ttf', 50, 'white'), (screen.get_width() // 2, screen.get_height() // 10))

    # Particles
    player.particle.particle1(screen, 1, (player.x + (player.image_lists[player.image_list_index][player.image_index].get_width() // 2)),
                              player.y + (player.image_lists[player.image_list_index][player.image_index].get_height() // 1.5),
                              10, [6, 10], 5, 2, [230, 230, 230])
    player.particle.particle1(screen, 2, player.particle_1_x + 45,
                              player.particle_1_y,
                              10, [7, 11], 10, 2, [50, 50, 50])

    # Get menu
    if sum(player.i) < -1700:
        restart_text = player.text_objects('Press Spacebar to Restart', 'DATA/fonts/Decrypted.ttf', 40, 'black')
        screen.blit(restart_text,
                    ((screen.get_width() // 2) - (restart_text.get_width() // 2), screen.get_height() // 2))
        player.particle.particle1(screen, 3, player.x,
                                  player.y,
                                  10, [7, 11], 10, 2, [50, 50, 50])
        if player.particle.bool[2]:
            sound_3.play()

        player.particle.bool[2] = False
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            if not player.particle.bool[2]:
                sound_4.play()
            reset_parameters()
    else:
        player.particle.bool[2] = True
        screen.blit(player.image_lists[player.image_list_index][player.image_index], (player.x, player.y))
        [pygame.draw.rect(screen, (0, 200, 100), i) for i in player.map_list]

    pygame.display.update()
    clock.tick(60)

# this version contains bugs with map generation and sound is not available during a collision between a player and a block at the same jump location
# and there are also shortcomings in the player’s positioning and animation
# that's not all because there are unnecessary libraries here that need to be removed and also imported only used functions
# I would also restructure the code a little and make it more compact and readable
# but I won’t do all this because I’m lazy