from source import game

class ObjectManager:
    def __init__(self):
        self.objects = set()
        self.to_remove = set()
        self.player = None

    def register(self, object):
        self.objects.add(object)

    def register_player(self, object):
        self.player = object
        self.register(object)

    def unregister(self, object):
        # print("Request to remove object: " + str(object))
        self.to_remove.add(object)

    def unregister_player(self, object):
        self.player = None
        self.unregister(object)

    def process_removals(self):
        for obj in self.to_remove:
            # print("Removing object: " + str(obj))
            obj.delete()
            self.objects.remove(obj)
        self.to_remove = set()

    def update_all(self):
        for obj in self.objects:
            obj.update()
        self.process_removals()

    def draw_all(self):
        for obj in self.objects:
            obj.draw()

    def get_object_from_shape(self, shape):
        for obj in self.objects:
            if hasattr(obj, 'shape') and obj.shape == shape:
                return obj

    def get_player(self):
        return self.player
