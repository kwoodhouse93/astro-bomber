import pygame

class Utils:
    @staticmethod
    def get_screen_size():
        return pygame.display.get_surface().get_size()

    @staticmethod
    def wrap_body(space, body):
        width, height = Utils.get_screen_size()
        new_x = body.position.x
        new_y = body.position.y
        change_pos = False

        if body.position.x < 0:
            new_x = body.position.x + width
            change_pos = True
        elif body.position.x > width:
            new_x = body.position.x - width
            change_pos = True
        if body.position.y < 0:
            new_y = body.position.y + height
            change_pos = True
        elif body.position.y > height:
            new_y = body.position.y - height
            change_pos = True

        if change_pos:
            body.position = (new_x, new_y)
            space.reindex_shapes_for_body(body)
