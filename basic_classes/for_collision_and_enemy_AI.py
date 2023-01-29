import pygame
from values.sprite_groups import invisible_objects_group, all_sprites
from values.constants import HEIGHT, WIDTH


# в этот класс кидаем rect.x и rect.y первоначального расположения спрайта и его размеры
# класс выдаст 4 прямоугольника, которые будут находится со всех сторон спрайта
# после эти прямоугольники используем для коллизии с миром
class CollisionsEdges:

    def __init__(self, pos: (int, int), height, wight):
        self.pos = pos
        self.height = height
        self.wight = wight
        self.indent_from_sprite = 1
        self.indent_from_sprite_bottom = 1
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
                                       self.pos[1] + self.indent_from_sprite_bottom + self.height,
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


# создаст поле зрения врага, передавать rect.center
class FieldViewEnemy:
    def __init__(self, pos: (int, int)):
        self.pos = pos
        self.wight_vertical_field = 11
        self.height_horizontal_field = 5

    def creating_vertical_field(self):
        vertical = pygame.sprite.Sprite(invisible_objects_group)
        vertical.rect = pygame.Rect(self.pos[0] - self.wight_vertical_field // 2, self.pos[1] - HEIGHT // 2,
                                    self.wight_vertical_field, HEIGHT)
        return vertical

    def creating_left_field(self):
        left = pygame.sprite.Sprite(invisible_objects_group)
        left.rect = pygame.Rect(self.pos[0] - WIDTH // 2, self.pos[1] - self.height_horizontal_field // 2,
                                WIDTH // 2, self.height_horizontal_field)
        return left

    def creating_right_field(self):
        right = pygame.sprite.Sprite(invisible_objects_group)
        right.rect = pygame.Rect(self.pos[0], self.pos[1] - self.height_horizontal_field // 2,
                                 WIDTH // 2, self.height_horizontal_field)
        return right

    def creating_all_field(self):
        all_field = {"vertical": self.creating_vertical_field(),
                     "left": self.creating_left_field(),
                     "right": self.creating_right_field()
                     }
        return all_field


# класс который создаст два спрайта для того чтобы можно было смотреть идёт ли враг в пропасть,
# передавать rect.x и rect.y и размеры спрайта
class SearchVoid:
    def __init__(self, pos: (int, int), wight, height):
        self.x = pos[0]
        self.y = pos[1]
        self.wight = wight
        self.height = height
        self.indent_x = 5
        self.indent_y = 5

    def creating_search_engine(self):
        y = self.y + self.height + self.indent_y
        left = pygame.sprite.Sprite(invisible_objects_group)
        left.rect = pygame.Rect(self.x - self.indent_x, y, 1, 1)
        right = pygame.sprite.Sprite(invisible_objects_group)
        right.rect = pygame.Rect(self.x + self.wight + self.indent_x, y, 1, 1)
        all_search_engine = {"left": left,
                             "right": right}
        return all_search_engine


# создаёт поле атаки врага передавать rect.center
class AttackField:
    def __init__(self, pos, radius, height):
        self.x = pos[0]
        self.y = pos[1]
        self.radius = radius
        self.height = height

    def creating_field_attack(self):
        right = pygame.sprite.Sprite(invisible_objects_group)
        right.rect = pygame.Rect(self.x, self.y - self.height, self.radius, self.height)
        left = pygame.sprite.Sprite(invisible_objects_group)
        left.rect = pygame.Rect(self.x - self.radius, self.y - self.height, self.radius, self.height)
        all_field = {"right": right,
                     "left": left}
        return all_field
