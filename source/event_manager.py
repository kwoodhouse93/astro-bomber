import pygame

class EventManager:
    def __init__(self):
        self.event_map = {}
        self.keydown_map = {}
        self.keyup_map = {}

    def register(self, event_type, functor):
        if event_type in self.event_map:
            self.event_map[event_type].append(functor)
        else:
            self.event_map[event_type] = [functor]

    def register_keydown(self, key, functor):
        if key in self.keydown_map:
            self.keydown_map[key].append(functor)
        else:
            self.keydown_map[key] = [functor]

    def register_keyup(self, key, functor):
        if key in self.keyup_map:
            self.keyup_map[key].append(functor)
        else:
            self.keyup_map[key] = [functor]

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            event_type = event.type
            if event.type == pygame.locals.KEYDOWN:
                if event.key in self.keydown_map:
                    for functor in self.keydown_map[event.key]:
                        functor(event)
            if event.type == pygame.locals.KEYUP:
                if event.key in self.keyup_map:
                    for functor in self.keyup_map[event.key]:
                        functor(event)
            if event.type in self.event_map:
                for functor in self.event_map[event.type]:
                    functor(event)
