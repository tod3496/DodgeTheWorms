import pygame, random, math

# worm constants
MAX_SPEED = 3
MAX_DISTANCE = 21
WORM_RADIUS = 10
TURN_LIMIT = math.pi / 100

class Worm:
    def __init__(self, length, x, y, color, speed, screen_width, screen_height) -> None:
        match random.randint(1, 4):
            case 1:
                self.head = [0, 0]
                self.heading = 0
            case 2:
                self.head = [screen_width, 0]
                self.heading = math.pi
            case 3:
                self.head = [0, screen_height]
                self.heading = 0
            case 4:
                self.head = [screen_width, screen_height]
                self.heading = math.pi
        self.tail_segments = [(self.head[0], self.head[1]) for _ in range(length)]
        self.color = color
        self.head_color = pygame.Color(255, 255, 255)
        self.max_speed = speed
        self.speed = speed
        self.turn_limit = TURN_LIMIT
        self.current_turn_limit = TURN_LIMIT
        self.attacking = 0
        self.cooldown = 60 * 5 # 3 seconds before it can attack

    def move_head(self, x, y):
        target = [x, y]
        dist_x = target[0] - self.head[0]
        dist_y = target[1] - self.head[1]
        # distance between the head and the mouse
        dist = math.sqrt(dist_x ** 2 + dist_y ** 2)

        # make sure the head doesn't move faster than MAX_SPEED
        if dist <= self.speed:
            return

        if dist_x == 0 and dist_y == 0:
            return
        
        dist = self.speed
        
        # limit the turning speed
        
        # avoid dividing by zero
        if dist_x == 0:
            if dist_y > 0:
                new_heading = math.pi / 2
            else:
                new_heading = 3 * math.pi / 2

        elif dist_y == 0:
            if dist_x > 0:
                new_heading = 0
            else:
                new_heading = math.pi
        else:
            new_heading = math.atan(dist_y/dist_x)
            if dist_x < 0:
                new_heading += math.pi
            elif dist_y < 0:
                new_heading += 2 * math.pi

        angle_to_the_left = (self.heading - new_heading) % (2 * math.pi)
        # print('new: ' + str(new_heading) + '\n' +\
        #         'old: ' + str(self.heading) + '\n' +\
        #         'angle_to_left: ' + str(angle_to_the_left) + '\n')

        if abs(self.heading - new_heading) < self.current_turn_limit or (self.heading - new_heading) % (2 * math.pi) < self.current_turn_limit:
            self.heading = new_heading
        else:
            if angle_to_the_left > math.pi: # turning left
                self.heading += self.current_turn_limit
            else: # turning right
                self.heading -= self.current_turn_limit

        # move the head
        self.head[0] += dist * math.cos(self.heading)
        self.head[1] += dist * math.sin(self.heading)

            
    def move_tail_segments(self):
        self.tail_segments[0] = move_tail(self.tail_segments[0][0], self.tail_segments[0][1], self.head[0], self.head[1])
        i = 1
        while i < len(self.tail_segments):
            self.tail_segments[i] = move_tail(self.tail_segments[i][0], self.tail_segments[i][1], self.tail_segments[i-1][0], self.tail_segments[i-1][1])
            i += 1

    
    def change_state(self, player):
        '''
        Attacking state: if the worm is heading towards the player, set turn limit to very low and speed to very high
        Cooldown state: after the attacking state, go back to normal
        '''
        if self.attacking > 0:
            self.head_color 
            self.attacking -= 1
            self.head_color = pygame.Color(255, 0, 0)
        elif self.cooldown > 0:
            self.cooldown -= 1
            self.speed = self.max_speed / 2
            self.current_turn_limit = self.turn_limit
            self.head_color = pygame.Color(0, 0, 255)
        else:
            self.speed = self.max_speed
            self.head_color = pygame.Color(255, 255, 0)
            if math.sqrt((self.head[0] - player.pos[0]) ** 2 + (self.head[1] - player.pos[1]) ** 2) < self.speed * 66:
                angle_to_target = math.atan2(player.pos[1] - self.head[1], player.pos[0] - self.head[0])
                angle_difference = (angle_to_target - self.heading + math.pi) % (2 * math.pi) - math.pi
                if abs(angle_difference) < math.pi / 24:
                    self.speed = MAX_SPEED * 3
                    self.current_turn_limit = TURN_LIMIT / 5
                    self.attacking = 60 * 1 # 1 second
                    self.cooldown = 60 # 1 second

    def draw(self, screen):
        pygame.draw.circle(screen, self.head_color, (self.head[0], self.head[1]), WORM_RADIUS)
        for tail_x, tail_y in self.tail_segments:
            pygame.draw.circle(screen, self.color, (tail_x, tail_y), WORM_RADIUS)


def move_tail(tail_x, tail_y, anchor_x, anchor_y) -> tuple[float, float]:
    dist_x = anchor_x - tail_x
    dist_y = anchor_y - tail_y
    dist = math.sqrt(dist_x ** 2 + dist_y ** 2)

    if dist <= MAX_DISTANCE:
        return tail_x, tail_y
    
    # scale the vector to max_length=
    scalar = MAX_DISTANCE / dist
    tail_x = anchor_x - dist_x * scalar
    tail_y = anchor_y - dist_y * scalar
    return tail_x, tail_y