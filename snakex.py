#!/usr/bin/env python3
import pyxel
import collections
import random

SCREEN_WIDTH = 31
SCREEN_HEIGHT = 31
COLOR_MAX = 15
RED = 8
RIGHT, LEFT, UP, DOWN = (1,0), (-1,0), (0,-1), (0,1)
UP_RIGHT, UP_LEFT, DOWN_RIGHT, DOWN_LEFT = (1,-1), (-1,-1), (1,1), (-1,1)

class Snake:
    def __init__(self, initial_x, initial_y):
        self.color = random.randint(1, COLOR_MAX) # exclude black
        self.body = collections.deque()
        self.body_set = set()
        self.body.append((initial_x, initial_y))
        self.body_set.add((initial_x, initial_y))
        self.direction = RIGHT
        self.is_alive = True
        self.need_grow = 0
        self.is_grow_turn = True
    
    def update_body(self):
        if not self.is_alive:
            return

        old_head = self.body[0]
        new_head = (old_head[0] + self.direction[0], old_head[1] + self.direction[1])

        # print("new head is" + str(new_head))
        # print("body set is " + str(self.body_set))
        # print("body is " + str(self.body))

        if new_head in self.body_set:
            self.is_alive = False
            pyxel.play(0, [6,5,4,3,2,1,0], loop=False)
            return

        self.body.appendleft(new_head)
        self.body_set.add(new_head)
        if self.need_grow == 0 or not self.is_grow_turn:
            old_tail = self.body.pop()
            self.body_set.remove(old_tail)
        else:
            self.need_grow -= 1

        if new_head[0] < 0 or new_head[0] >= SCREEN_WIDTH or new_head[1] < 0 or new_head[1] >= SCREEN_HEIGHT:
            self.is_alive = False
            pyxel.play(0, [6,5,4,3,2,1,0], loop=False)
            return
        
        self.is_grow_turn = not self.is_grow_turn
    
    def body_collide(self, x, y):
        return True if (x,y) in self.body_set else False

class Apple:
    def __init__(self):
        self.x, self.y, self.color = 0, 0, 0
        self.spawn()
    
    def spawn(self):
        self.x = random.randint(0, SCREEN_WIDTH-1)
        self.y = random.randint(0, SCREEN_HEIGHT-1)
        self.color = random.randint(1, COLOR_MAX) # exclude black
    
    def coordinate(self):
        return (self.x, self.y)

class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT)
        pyxel.load('my_resource.pyxel')
        self.snake = Snake(SCREEN_WIDTH//2,SCREEN_HEIGHT//2)
        self.apple = Apple()
        # random apple until it is not inside snake
        while self.snake.body_collide(*self.apple.coordinate()) or self.apple.color == self.snake.color:
            self.apple.spawn()
        self.apples_ate = 0
        pyxel.run(self.update, self.draw)
    
    def restart(self):
        pyxel.stop()  # stop death music
        self.snake = Snake(SCREEN_WIDTH//2,SCREEN_HEIGHT//2)
        self.apple = Apple()
        # random apple until it is not inside snake
        while self.snake.body_collide(*self.apple.coordinate()) or self.apple.color == self.snake.color:
            self.apple.spawn()
        self.apples_ate = 0
    
    def update_direction_or_speed_up(self, new_direction):
        current_direction = self.snake.direction
        # if given direction is the opposite of current direction, the given direction is ignored
        if current_direction[0] + new_direction[0] == 0 and current_direction[1] + new_direction[1] == 0:
            return
        # same thing, handling the odd case where different direction keys were pressed twice within 10 frames
        if len(self.snake.body) > 1:
            head_x, head_y = self.snake.body[0]
            neck_x, neck_y = self.snake.body[1]
            practical_current_direction = ( head_x-neck_x, head_y-neck_y)
            if practical_current_direction[0] + new_direction[0] == 0 and practical_current_direction[1] + new_direction[1] == 0:
                return

        if current_direction == new_direction:
            self.snake.update_body()
        else:
            self.snake.direction = new_direction

    def update(self):
        # check apple hit
        if self.snake.body_collide(*self.apple.coordinate()):
            self.snake.need_grow = self.apple.color
            self.apples_ate += 1
            pyxel.play(0, min(self.apples_ate-1, 20), loop=False)
        
            # random apple until it is not inside snake
            while self.snake.body_collide(*self.apple.coordinate()) or self.apple.color == self.snake.color:
                self.apple.spawn()

        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
        elif pyxel.btnp(pyxel.KEY_G):
            self.restart()
            return
        elif pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.KEY_D):
            self.update_direction_or_speed_up(RIGHT)
        elif pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.KEY_A):
            self.update_direction_or_speed_up(LEFT)
        elif pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_W):
            self.update_direction_or_speed_up(UP)
        elif pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_S) or pyxel.btnp(pyxel.KEY_X):
            self.update_direction_or_speed_up(DOWN)
        elif pyxel.btnp(pyxel.KEY_Q):
            self.update_direction_or_speed_up(UP_LEFT)
        elif pyxel.btnp(pyxel.KEY_E):
            self.update_direction_or_speed_up(UP_RIGHT)
        elif pyxel.btnp(pyxel.KEY_Z):
            self.update_direction_or_speed_up(DOWN_LEFT)
        elif pyxel.btnp(pyxel.KEY_C):
            self.update_direction_or_speed_up(DOWN_RIGHT)
        
        # snake moves every 9 frames but speeding up until every 2 frames
        if pyxel.frame_count % max(2, 9 - self.apples_ate) != 0:
            return
        
        # update snake body, move the last parts to the front
        self.snake.update_body()

    def draw(self):
        pyxel.cls(0)
        
        if self.snake.is_alive:
            pyxel.rect(*self.apple.coordinate(), *self.apple.coordinate(), self.apple.color)
            for body_part in self.snake.body:
                pyxel.rect(*body_part, *body_part, self.snake.color)
        else:
            pyxel.text(SCREEN_WIDTH//5,SCREEN_HEIGHT//4, "SCORE:", RED)
            pyxel.text(SCREEN_WIDTH//2,SCREEN_HEIGHT - SCREEN_HEIGHT//2, str(self.apples_ate), RED)

App()
