class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0
        self.delimeter = 10

    def apply(self, obj):
        obj.rect.x += self.dx // self.delimeter
        obj.rect.y += self.dy // self.delimeter

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)
    