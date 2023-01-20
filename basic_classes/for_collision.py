import pygame
from values.sprite_groups import invisible_objects_group


# в этот класс кидаем rect.x и rect.y первоначального расположения спрайта и его размеры
# класс выдаст 4 прямоугольника, которые будут находится со всех сторон спрайта
# после эти прямоугольники используем для коллизии с миром
class CollisionsEdges:
    IMAGE = pygame.image.load("data/crutch_for_edge_of_collision.png")

    def __init__(self, pos: (int, int), height, wight):
        self.pos = pos
        self.height = height
        self.wight = wight
        self.indent_from_sprite = 1
        self.indent_from_corner = 3

    def creating_top_edge(self):
        top_edge = pygame.sprite.Sprite(invisible_objects_group)
        top_edge.rect = pygame.Rect(self.pos[0] + self.indent_from_corner,
                                    self.pos[1] - self.indent_from_sprite,
                                    self.wight - self.indent_from_corner * 2, 1)

        return top_edge

    def creating_left_edge(self):
        left_edge = pygame.sprite.Sprite(invisible_objects_group)
        left_edge.rect = pygame.Rect(self.pos[0] - self.indent_from_sprite,
                                     self.pos[1] + self.indent_from_corner,
                                     1, self.height - self.indent_from_corner * 2)
        return left_edge

    def creating_bottom_edge(self):
        bottom_edge = pygame.sprite.Sprite(invisible_objects_group)
        bottom_edge.rect = pygame.Rect(self.pos[0] + self.indent_from_corner,
                                       self.pos[1] + self.indent_from_sprite + self.height,
                                       self.wight - self.indent_from_corner * 2, 1)
        return bottom_edge

    def creating_right_edge(self):
        right_edge = pygame.sprite.Sprite(invisible_objects_group)
        right_edge.rect = pygame.Rect(self.pos[0] + self.indent_from_sprite + self.wight,
                                      self.pos[1] + self.indent_from_corner,
                                      1, self.height - self.indent_from_corner * 2)
        return right_edge

    def creating_all_edges(self):
        all_edges = {"top": self.creating_top_edge(),
                     "left": self.creating_left_edge(),
                     "bottom": self.creating_bottom_edge(),
                     "right": self.creating_right_edge()}
        return all_edges
