import pygame, os

pygame.init()


class Entity:

    def image_load(self, image_folders, size):
        self.image_lists = []

        for image_folder in image_folders:
            image_list = []
            image_list_name = os.listdir(image_folder)

            for image_name in image_list_name:
                image = pygame.image.load(image_folder + '/' + image_name)
                image_transform = pygame.transform.scale(image, (image.get_width() * size, image.get_height() * size))
                image_transform_flip = pygame.transform.flip(image_transform, True, False)
                image_list.append(image_transform), image_list.append(image_transform_flip)

            self.image_lists.append(image_list)

    def collision_rects(self):
        self.collision_rect_lists = []

        for list in self.image_lists:
            collision_rect_list = []

            for image in list:
                collision_rect_list.append(image.get_rect())
            self.collision_rect_lists.append(collision_rect_list)

    def text_objects(self, text, font, size, color):
        font_1 = pygame.font.Font(font, size)
        text = font_1.render(text, False, pygame.Color(color))
        return text
