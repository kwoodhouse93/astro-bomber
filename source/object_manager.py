class ObjectManager:
    def __init__(self, screen, space):
        self.objects = set()
        self.screen = screen
        self.space = space
        self.to_remove = set()

    def register(self, object):
        self.objects.add(object)

    def unregister(self, object):
        self.to_remove.add(object)

    def process_removals(self):
        for obj in self.to_remove:
            self.objects.remove(obj)
        self.to_remove = set()

    def update_all(self):
        # print(self.objects)
        for obj in self.objects:
            obj.update(self.space)
        self.process_removals()

    def draw_all(self):
        for obj in self.objects:
            obj.draw(self.screen)

    def get_object_from_shape(self, shape):
        for obj in self.objects:
            if hasattr(obj, 'shape') and obj.shape == shape:
                return obj
