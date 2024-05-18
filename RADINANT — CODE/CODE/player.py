import pygame, random
from time import time
from math import ceil
from CODE.entities import Entity
from CODE.particles import Particles


class Player(Entity):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x_old = 0

        self.map_list = []
        self.map_delete_rects = []
        self.map_delete_rects_time = []
        self.elements_in_delete_rect_list = 0
        self.replace_level_count = 0
        self.level_count = 1
        self.level_second_time = 3

        self.movement_bool = False
        self.movement_count = 100

        self.image_list_index = 0
        self.image_index = 0
        self.amount_counter = 0
        self.animate_bool = True

        self.gravity_count = 0
        self.gravity_bool = True

        self.screen_fill_default = [200, 100, 200]
        self.screen_fill = self.screen_fill_default.copy()
        self.rect_time_opacity_default = 0
        self.rect_time_opacity = 0
        self.rect_time_opacity_bool = False

        self.particle = Particles(3)
        self.map_min_rect_y = []
        self.map_min_rect_x = []

        self.sound_1 = pygame.mixer.Sound('DATA/sounds/level_count.ogg')
        self.sound_2 = pygame.mixer.Sound('DATA/sounds/rect_delete.ogg')

    def map_generation(self, count, screen):
        # Init one default rect
        self.map_list.append(pygame.Rect(30, 500, 90, 30)) if len(self.map_list) == 0 else None

        # Generate rects
        if count == 1:
            for i in range(1):
                self.map_list.append(pygame.Rect(30 if random.randint(0, 1) == 0 else
                                                 240, ((self.y + 52) - (3 * 150)), 90, 30))
        else:
            if len(self.map_list) == 1:
                for i in range(1, 4):
                    self.map_list.append(pygame.Rect(30 if random.randint(0, 1) == 0 else
                                                     240, ((self.y + 52) - (i * 150)), 90, 30))

        # Delete rects
        self.i = []
        for rect in self.map_list:

            self.i.append(rect.y)
            if self.i.count(rect.y) > 1:
                self.i.remove(rect.y)
                self.map_list.remove(rect)

            if self.map_list.count(rect) > 1:
                self.map_list.remove(rect)

            if rect.y >= screen.get_height():
                self.map_list.remove(rect)

        self.collision_rect_lists[self.image_list_index][self.image_index].topleft = (self.x, self.y)

    def collision_handler(self):
        replace_level_number = 20

        # Particles in collision
        if self.movement_count == 4:
            self.particle.bool[0] = True
        else:
            self.particle.bool[0] = False

        for rect in self.map_list:
            if self.collision_rect_lists[self.image_list_index][self.image_index].colliderect(rect):

                # Player collision rect
                if (self.y > (rect.y - self.image_lists[self.image_list_index][self.image_index].get_height())
                        and (self.y < rect.y)):
                    self.y = (rect.y - (self.image_lists[0][0].get_height() - 1))
                    self.gravity_bool = False

                # Level create
                if self.movement_count == 1:
                    self.replace_level_count += 1
                    self.sound_1.play()
                    self.rect_time_opacity_default = 0
                    self.rect_time_opacity_bool = False

                if self.replace_level_count >= replace_level_number:
                    self.replace_level_count = 0
                    self.level_count += 1
                    self.screen_fill = self.screen_fill_default.copy()
                    self.screen_fill_default = [random.randint(50, 150), random.randint(50, 150), random.randint(50, 150)]

                    # Get time rect
                    if self.movement_count == 1:
                        self.level_second_time = round((self.level_second_time / 1.1), 2)

                # Rect append in delete rect list
                if self.movement_count == 1:
                    self.map_delete_rects.append(rect)
                    self.map_delete_rects_time.append((time() + self.level_second_time))

                # Rect delete in delete rect list
                if rect not in self.map_list:
                    index = self.map_delete_rects.index(rect)
                    self.map_delete_rects_time.remove(self.map_delete_rects_time[index])
                    self.map_delete_rects.remove(rect)

                break
            else:
                self.gravity_bool = True

        # Rect timing delete and particles bool
        if self.particle.bool[1]:
            self.particle.bool[1] = False

        for block in self.map_list:
            self.map_min_rect_y.append(block.y)

            if block.y == max(self.map_min_rect_y):
                self.map_min_rect_x.append(block.x)

        self.particle_1_y = max(self.map_min_rect_y)
        self.particle_1_x = self.map_min_rect_x[-1]

        for timing in self.map_delete_rects_time:
            if time() >= timing:
                index = self.map_delete_rects_time.index(timing)

                if self.map_delete_rects[index] in self.map_list:
                    self.map_list.remove(self.map_delete_rects[index])
                    self.particle.bool[1] = True
                    if sum(self.i) > -1500:
                        self.sound_2.play()
                self.map_delete_rects.pop(index)
                self.map_delete_rects_time.pop(index)

        self.collision_rect_lists[self.image_list_index][self.image_index].topleft = (self.x, self.y)

    def move(self, screen, distantion_rects, colliderect_bool):
        self.keys = pygame.key.get_pressed()

        if self.movement_bool:
            if self.keys[pygame.K_LEFT] or self.keys[pygame.K_a]:
                self.y -= distantion_rects
                self.x_old = self.x
                self.x -= 220 if self.x > (screen.get_width() // 2) else 0
                self.gravity_count = self.image_index = self.amount_counter = self.movement_count = self.movement_bool = False

            elif self.keys[pygame.K_RIGHT] or self.keys[pygame.K_d]:
                self.y -= distantion_rects
                self.x_old = self.x
                self.x += 260 if self.x < (screen.get_width() // 2) else 0
                self.gravity_count = self.image_index = self.amount_counter = self.movement_count = self.movement_bool = False
        else:
            if (not ((self.keys[pygame.K_RIGHT] or self.keys[pygame.K_d]) or
                       (self.keys[pygame.K_LEFT] or self.keys[pygame.K_a]))
                  and not colliderect_bool):
                self.movement_bool = True

    def animate(self, amount, screen):
        self.amount_counter += 1

        if self.movement_count <= amount[1]:
            self.movement_count += 1

            # Get image list index
            if self.movement_count == 1 and not self.movement_bool:
                if self.x_old < (screen.get_width() / 2):
                    if self.keys[pygame.K_LEFT] or self.keys[pygame.K_a]:
                        self.image_list_index = 2 if self.x == 62 else 1
                    elif self.keys[pygame.K_RIGHT] or self.keys[pygame.K_d]:
                        self.image_list_index = 1 if self.image_list_index == 2 and self.image_index == 0 else 2
                else:
                    if self.keys[pygame.K_LEFT] or self.keys[pygame.K_a]:
                        self.image_list_index = 2
                    elif self.keys[pygame.K_RIGHT] or self.keys[pygame.K_d]:
                        self.image_list_index = 1

            if (self.movement_count - 1) == 0:
                self.image_index = 1 if self.x_old > (screen.get_width() // 2) or (self.x < (screen.get_width() // 2) and self.image_list_index == 2 and self.image_index == 0) else 0
        else:
            self.image_list_index = 0
            self.movement_count += 1 if self.movement_count < 100 else 0

        # Set process
        if self.amount_counter >= amount[self.image_list_index if self.image_list_index < 2 else 1]:
            self.amount_counter = 0
            self.image_index += 2

        if self.image_index >= len(self.image_lists[self.image_list_index]):
            self.image_index = 1 if self.x > (screen.get_width() / 2) else 0

    def flip_anchor_point(self, screen, point_1, point_2):
        # Right position
        if self.image_list_index == 2 and self.image_index % 2 == 0:
            self.x = point_2 - self.image_lists[self.image_list_index][self.image_index].get_width()

        if self.image_list_index == 0 and self.x > (screen.get_width() // 2):
            self.x_old = self.x
            self.x = point_2 - self.image_lists[self.image_list_index][self.image_index].get_width()

        if self.x > (screen.get_width() // 2) and self.x_old < (screen.get_width() // 2) and self.image_list_index == 1:
            self.x = point_2 - self.image_lists[self.image_list_index][self.image_index].get_width()

        # Left position
        if self.image_index % 2 != 0 and self.x < (screen.get_width() // 2):
            self.x = point_1

    def gravity(self):
        if self.gravity_bool:
            self.gravity_count += 0.5 if self.gravity_count < 5 else 1 if self.gravity_count <= 15 else 0
            self.gravity_amount = min(15, self.gravity_count)
            self.y += self.gravity_amount

        elif not self.gravity_bool:
            self.gravity_amount = 0

    def camera_shake(self, ratio, default_location):
        number = 0

        # Sharp increase in subtracting values and smooth decrease
        number += ((default_location - self.y) // ratio)

        self.y += number
        self.map_min_rect_y.clear()
        self.map_min_rect_x.clear()
        for block in self.map_list:
            block.y += number

        self.particle_1_y += number
        self.collision_rect_lists[self.image_list_index][self.image_index].topleft = (self.x, self.y)

    def background_feel(self, ratio):
        number = [0, 0, 0]

        for index in range(len(self.screen_fill)):
            number[index] += (self.screen_fill_default[index] - self.screen_fill[index]) // ratio

            if (self.screen_fill[index] + number[index]) <= 255 and (self.screen_fill[index] + number[index]) >= 0:
                self.screen_fill[index] += number[index]

    def rect_time_background(self, ratio):
        number = 0

        if len(self.map_delete_rects_time) > 0:
            timing = self.map_delete_rects_time[-1]

            if self.rect_time_opacity == self.rect_time_opacity_default:
                self.rect_time_opacity_bool = True

            if self.rect_time_opacity_bool:
                try:
                    number += ceil((255 - self.rect_time_opacity) / ((timing - time()) * 30))
                except ZeroDivisionError:
                    number += 0
            else:
                number -= ceil((self.rect_time_opacity_default + self.rect_time_opacity) / ((ratio // 2) if self.level_second_time < 1 else ratio))

        if (self.rect_time_opacity + number) <= 255 and (self.rect_time_opacity + number) >= 0:
            self.rect_time_opacity += number



