import pygame
from pygame.locals import *

import pymunk

from source.utilities import *

class Bomber:
    def __init__(self, event_manager):
        width = 20
        height = 30
        vertices = [
            (-(width/2), -(height/2)),
            ( 0,  (height/2)),
            ( (width/2), -(height/2))
        ]
        radius = 5

        mass = 5
        moment = pymunk.moment_for_poly(mass, vertices, radius=radius)
        self.body = pymunk.Body(mass, moment)
        self.body.position = (400, 300)

        self.shape = pymunk.Poly(self.body, vertices, radius=radius)

        # Object constants
        self.turn_torque = 3000
        self.engine_thrust = 1000
        self.braking_force = 1500
        self.reverse_thrust = 800
        self.ang_vel_limit = 10

        # State variables
        self.turning_left = False
        self.turning_right = False
        self.thrusting = False
        self.braking = False

        # Register callback functors
        event_manager.register_keydown(K_LEFT, self.cb_left_turn_on)
        event_manager.register_keydown(K_RIGHT, self.cb_right_turn_on)
        event_manager.register_keydown(K_UP, self.cb_thrust_forwards_on)
        event_manager.register_keydown(K_DOWN, self.cb_thrust_backwards_on)

        event_manager.register_keyup(K_LEFT, self.cb_left_turn_off)
        event_manager.register_keyup(K_RIGHT, self.cb_right_turn_off)
        event_manager.register_keyup(K_UP, self.cb_thrust_forwards_off)
        event_manager.register_keyup(K_DOWN, self.cb_thrust_backwards_off)

    def cb_left_turn_on(self, event):
        self.turning_left = True
    def cb_right_turn_on(self, event):
        self.turning_right = True
    def cb_thrust_forwards_on(self, event):
        self.thrusting = True
    def cb_thrust_backwards_on(self, event):
        self.braking = True

    def cb_left_turn_off(self, event):
        self.turning_left = False
    def cb_right_turn_off(self, event):
        self.turning_right = False
    def cb_thrust_forwards_off(self, event):
        self.thrusting = False
    def cb_thrust_backwards_off(self, event):
        self.braking = False

    def update(self, space):
        Utils.wrap_body(space, self.body)

        # print(str(self.body.angular_velocity))
        if self.turning_left and not self.turning_right and self.body.angular_velocity < self.ang_vel_limit:
            self.body.torque = self.turn_torque
        elif self.turning_right and not self.turning_left and self.body.angular_velocity > -self.ang_vel_limit:
            self.body.torque = -self.turn_torque
        elif self.body.angular_velocity > 0.1:
            self.body.torque = -self.turn_torque
        elif self.body.angular_velocity < -0.1:
            self.body.torque = self.turn_torque
        else:
            self.body.angular_velocity = 0
            self.body.torque = 0

        # forward_vel = self.body.velocity.rotated(-self.body.angle).y
        if self.thrusting:
            force = (0, self.engine_thrust)
            point = (0, 0)
            self.body.apply_force_at_local_point(force, point)
        elif self.braking:# and forward_vel > 1:
            # force = (0, -self.braking_force)
            force = (0, -self.reverse_thrust)
            point = (0, 0)
            self.body.apply_force_at_local_point(force, point)
        # print(str(self.body.torque))

    def draw(self, screen):
        width, height = Utils.get_screen_size()
        # print (str(self.body.position))
        position = int(self.body.position.x), \
            height - int(self.body.position.y)
        # pygame.draw.circle(screen, (0, 0, 255), position, int(self.radius), 2)

# def draw_bomber(screen, bomber):
    # p = int(bomber.body.position.x), 600 - int(bomber.body.position.y)
    # pygame.draw.circle(screen, (0, 0, 255), p, int(bomber.radius), 2)
