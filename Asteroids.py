import simplegui
import random
import math

def main():
    new_game = Asteroids()

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, 
                                        animated = False, animated_dim = None):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated
        self.animated_dim = animated_dim

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated
    
    def get_animated_dim(self):
        return self.animated_dim

class Ship:
    def __init__(self, pos, vel, angle, image, info, BOARD_WIDTH, BOARD_HEIGHT):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.FRICTION = 0.009
        self.BOARD_WIDTH = BOARD_WIDTH
        self.BOARD_HEIGHT = BOARD_HEIGHT
        self.MISSILE_SPEED = 7
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.timer = None
        self.time_passed = 0.0
        self.ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
        self.missile_info = ImageInfo([5, 5], [10, 10], 3, 40)
        self.missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")
        self.missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
        self.missile_sound.set_volume(.7)


    def angle_to_vector(self, ang):
        return [math.cos(ang), math.sin(ang)]

    def dist(self, p,q):
        return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

    def radian_to_degree(self, angle):
        return angle * math.pi / 180.0

    def draw(self,canvas):
        angle = self.radian_to_degree(self.angle)
        if not self.thrust:
            canvas.draw_image(self.image, self.image_center, self.image_size, 
                                           self.pos, self.image_size, angle)
        else:
            center = (self.image_center[0] + self.image_size[0], 
                                                           self.image_center[1])
            canvas.draw_image(self.image, center, self.image_size, self.pos, 
                                self.image_size, angle)
     
    def update_angle(self):
        self.angle += self.angle_vel
        
    def vel_direction_shift(self, is_thrusting, acc_fraction):
        # acc_fraction must be a float between 0 and 1. These values will control
        # how fast or how slow the ship accelerates when the thrust is on
        angle = self.radian_to_degree(self.angle)
        if is_thrusting:
            acc = self.angle_to_vector(angle)
            self.vel[0] += acc_fraction * acc[0]
            self.vel[1] += acc_fraction * acc[1]
    
    def include_friction(self):
        self.vel[0] *= (1 - self.FRICTION)
        self.vel[1] *= (1 - self.FRICTION)
    
    def update_and_wrap_pos(self):
        self.pos[0] = (self.pos[0] + self.vel[0]) % self.BOARD_WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % self.BOARD_HEIGHT
    
    def update_ship_movement(self):
        self.update_angle()
        self.vel_direction_shift(self.thrust, 0.15)
        self.include_friction()
        self.update_and_wrap_pos()
        
    def rotate_ship_cw(self):
        self.angle_vel += 1
                
    def rotate_ship_counter_cw(self):
        self.angle_vel -= 1
            
    def timer_handler(self):
        self.time_passed += 1
   
    def start_timer(self):
        # timer calls on self.timer_handler every 1000 milliseconds
        self.timer = simplegui.create_timer(1000, self.timer_handler)
        self.timer.start()
 
    def reset_timer(self):
        self.timer.stop()
        self.time_passed = 0.0

    def play_thrust_sound(self):
        if self.time_passed > 20:
            self.ship_thrust_sound.rewind()
        self.ship_thrust_sound.play()
    
    def reset_thrust_sound(self):
        self.ship_thrust_sound.pause()
        self.ship_thrust_sound.rewind()
        self.reset_timer()
        
    def activate_thrust(self):
        self.start_timer()
        self.thrust = True
        self.play_thrust_sound()
        
    def deactivate_thrust(self):
        self.thrust = False
        self.reset_thrust_sound()
    
    def missile_launch_vel(self):
        angle = self.radian_to_degree(self.angle)
        forward = self.angle_to_vector(angle)
        return [self.vel[0] + self.MISSILE_SPEED * forward[0], 
                                self.vel[1] + self.MISSILE_SPEED * forward[1]]
    
    def missile_launch_pos(self):
        angle = self.radian_to_degree(self.angle)
        forward = self.angle_to_vector(angle)
        pos_x = self.pos[0] + (self.image_size[1] / 2) * forward[0]
        pos_y = self.pos[1] + (self.image_size[1] / 2) * forward[1]
        return [pos_x, pos_y]
    
    def generate_missile(self):
        return Sprite(self.missile_launch_pos(), self.missile_launch_vel(), 0, 
                0, self.missile_image, self.missile_info, self.BOARD_WIDTH, 
                self.BOARD_HEIGHT, self.missile_sound)
        
    def get_pos(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def get_vel(self):
        return self.vel

class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, BOARD_WIDTH, 
                                                    BOARD_HEIGHT, sound = None):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.BOARD_WIDTH = BOARD_WIDTH
        self.BOARD_HEIGHT = BOARD_HEIGHT
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.animated_dim = info.get_animated_dim()
        self.age = 0
        self.time = 0
        if sound:
            sound.rewind()
            sound.play()

    def angle_to_vector(self, ang):
        return [math.cos(ang), math.sin(ang)]

    def dist(self, p,q):
        return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)
    
    def radian_to_degree(self, angle):
        return angle * math.pi / 180.0

    def animated_idx(self):
        return [self.time % self.animated_dim, 0]

    def animated_center(self):
        idx = self.animated_idx()
        return [self.image_center[0] + idx[0] * self.image_size[0],
                               self.image_center[1] + idx[1] * self.image_size[1]]
    
    def draw(self, canvas):
        angle = self.radian_to_degree(self.angle)
        if not self.animated:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, 
                                           self.image_size, angle)
        else:
            canvas.draw_image(self.image, self.animated_center(), self.image_size, 
                              self.pos, self.image_size, angle)
            self.time += 1
        
    def increment_sprite_age(self):
        self.age += 1
    
    def sprite_is_aged(self):
        if self.age > self.lifespan:
            return True
        else:
            return False
    
    def update_angle(self):
        self.angle += self.angle_vel
    
    def update_and_wrap_pos(self):
        self.pos[0] = (self.pos[0] + self.vel[0]) % self.BOARD_WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % self.BOARD_HEIGHT
    
    def update_sprite_movement(self):
        self.increment_sprite_age()
        self.update_angle()
        self.update_and_wrap_pos()
        
    def collide(self, other_object):
        distance = self.dist(self.pos, other_object.pos)
        sum_rad = self.radius + other_object.radius
        if distance <= sum_rad:
            return True
        else:
            return False
   
    def get_lifespan(self):
        return self.lifespan
        
    def set_pos(self, new_pos):
        ''' 
        pos represents the x, y coordinates of the Sprite's position
        in vector form. pos should be of type list.
        
        Updates Sprite's position to inputted pos.
        '''
        self.pos = new_pos
    
    def set_angle_vel(self, new_ang_vel):
        ''' 
        angle_vel represents the angular velocity of the ship in radians.
        
        Updates Sprite's angular velocity to inputted angle_vel.
        '''
        self.angle_vel = new_ang_vel
        
    def set_vel(self, new_vel):
        ''' 
        vel represents the x, y coordinates of the Sprite's velocity
        in vector form. vel should be of type list.
        
        Updates Sprite's velocity to inputted vel.
        '''
        self.vel = new_vel
        
    def set_sound(self, new_sound):
        self.sound = new_sound
        self.sound.rewind()
        self.sound.play()

    def get_pos(self):
        return self.pos
    
    def get_vel(self):
        return self.vel
    
    def get_angle(self):
        return self.angle
    
    def get_angle_vel(self):
        return self.angle_vel

class Asteroids:
    def __init__(self, rock_group = None, missile_group = None):
        self.started = False
        self.lives = 5
        self.score = 0
        self.time = 0
        self.WIDTH = 800
        self.HEIGHT = 600
        self.MAX_ROCKS = 12
        self.timer = None
        self.explosion_group = set([])
        if not missile_group:
            self.missile_group = set([])
        else:
            self.missile_group = missile_group
        if not rock_group:
            self.rock_group = set([])
        else:
            self.rock_group = rock_group
        
        self.frame = simplegui.create_frame("Asteroids", self.WIDTH, self.HEIGHT)
        self.timer = simplegui.create_timer(1000.0, self.rock_spawner)
        
        self.frame.set_draw_handler(self.draw)
        self.frame.set_keyup_handler(self.keyuphandler)
        self.frame.set_keydown_handler(self.keydownhandler)
        self.frame.set_mouseclick_handler(self.mouseclick)
        self.frame.start()
        self.timer.start()  
        
        # ship image
        self.ship_info = ImageInfo([45, 45], [90, 90], 35)
        self.ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")
        
        self.my_ship = Ship([self.WIDTH / 2, self.HEIGHT / 2], [0, 0], 0, self.ship_image, self.ship_info, self.WIDTH, self.HEIGHT)

        # debris image
        self.debris_info = ImageInfo([320, 240], [640, 480])
        self.debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")
        
        # nebula images - nebula_brown.png, nebula_blue.png
        self.nebula_info = ImageInfo([400, 300], [800, 600])
        self.nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")
        
        # splash image
        self.splash_info = ImageInfo([200, 150], [400, 300])
        self.splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

        # asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
        self.asteroid_info = ImageInfo([45, 45], [90, 90], 40)
        self.asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")
        
        # animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
        self.explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True, 23)
        self.explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")
        
        # sound assets purchased from sounddogs.com, please do not redistribute
        self.soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
        self.explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

        self.play_background_music()

        self.key_inputs_down = {"left": self.my_ship.rotate_ship_counter_cw,
                                "right": self.my_ship.rotate_ship_cw,
                                "up": self.my_ship.activate_thrust,
                                "space": self.shoot_missile}

        self.key_inputs_up = {"left": self.my_ship.rotate_ship_cw,
                              "right": self.my_ship.rotate_ship_counter_cw,
                              "up": self.my_ship.deactivate_thrust}

    def angle_to_vector(self, ang):
        return [math.cos(ang), math.sin(ang)]

    def dist(self, p,q):
        return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

    def draw_start_prompt_splash(self, canvas):
        canvas.draw_image(self.splash_image, self.splash_info.get_center(),
                        self.splash_info.get_size(),
                        [self.WIDTH / 2, self.HEIGHT / 2],
                        self.splash_info.get_size())

    def play_background_music(self):
        self.soundtrack.play()
        
    def stop_background_music(self):
        self.soundtrack.pause()
        self.soundtrack.rewind()
        
    def game_start_prompts(self, canvas):
        if not self.started:
            self.draw_start_prompt_splash(canvas)
        
    def increment_time(self):
        self.time += 1
        
    def wait_time(self):
        return (self.time / 4) % self.WIDTH
    
    def draw_debris(self, canvas, wait_time):
        center = self.debris_info.get_center()
        size = self.debris_info.get_size()
        pos = [self.wait_time() - self.WIDTH / 2, self.HEIGHT / 2]
        canvas.draw_image(self.debris_image, center, size, 
             pos,(self.WIDTH, self.HEIGHT))
        canvas.draw_image(self.debris_image, center, size, 
            (self.wait_time() + self.WIDTH / 2, self.HEIGHT / 2), 
            (self.WIDTH, self.HEIGHT))
    
    def draw_nebula(self, canvas):
        canvas.draw_image(self.nebula_image, self.nebula_info.get_center(), 
            self.nebula_info.get_size(), [self.WIDTH / 2, self.HEIGHT / 2], 
            [self.WIDTH, self.HEIGHT])
     
    def draw_lives_count(self, canvas):
        canvas.draw_text("Lives: " + str(self.lives), 
            [self.WIDTH / 20, self.HEIGHT / 12], 24, "White") 
        
    def draw_score(self, canvas):
        canvas.draw_text("Score: " + str(self.score), 
            [6 * self.WIDTH / 7, self.HEIGHT / 12], 24, "White")
        
    def draw_background_objects(self, canvas, wait_time):
        self.draw_debris(canvas, self.wait_time)
        self.draw_nebula(canvas)
    
    def draw_game_metrics(self, canvas):
        self.draw_lives_count(canvas)
        self.draw_score(canvas)
        
    def draw_updated_ship(self, canvas):
        self.my_ship.draw(canvas)
        self.my_ship.update_ship_movement()
    
    def collide_group(self, group, other_object):
        size_init = len(group)
        for obj in set(group):
            if obj.collide(other_object):
                group.remove(obj)
                explosion = Sprite(obj.get_pos(), obj.get_vel(), 
                                obj.get_angle(), obj.get_angle_vel(), 
                                self.explosion_image, self.explosion_info, 
                                self.WIDTH, self.HEIGHT, self.explosion_sound)
                self.explosion_group.add(explosion)
        if len(group) == size_init:
            return 0
        else:
            return size_init - len(group)
    
    def group_collide_group(self, group1, group2):
        num_collisions = 0
        for obj in set(group1):
            collide = self.collide_group(group2, obj)
            if collide > 0:
                group1.discard(obj)
            num_collisions += collide
        return num_collisions

    def rand_rock_vel(self):
        return [random.randrange(-100, 100) / 100.0, 
                random.randrange(-100, 100) / 100.0]
    
    def rand_rock_pos(self):
        return [random.randrange(0, self.WIDTH), 
                random.randrange(0, self.HEIGHT)] 
    
    def rand_rock_angle_vel(self):
        return random.randrange(-35, 35) / 10.0
    
    def rock_vel_factor(self):
        factor = self.score / 12
        if factor > 3:
            factor = 3
        return factor
        
    def incr_rock_vel_with_score(self):
        fac = self.rock_vel_factor()
        vel_range_dict = {'low': [-10 - 2 * fac, 10 - 2 * fac], 
                          'high': [-10 + 2 * fac, 10 + 2 * fac]}
        rock_vel = []
        while len(rock_vel) < 2:
            vel_range = vel_range_dict[random.choice(vel_range_dict.keys())]
            rock_vel.append(random.randrange(vel_range[0], 
                                                vel_range[1]) / 10.0)
        return rock_vel
        
    def overlaps_ship(self, pos, radius):
        ship_pos = self.my_ship.get_pos()
        ship_rad = self.my_ship.get_radius()
        if self.dist(ship_pos, pos) < (ship_rad + 4 * radius):
            return True
        else:
            return False
    
    def gen_nonoverlap_pos_to_ship(self, sprite_info):
        pos = self.rand_rock_pos()
        while self.overlaps_ship(pos, sprite_info.get_radius()):
            pos = self.rand_rock_pos()
        return pos
    
    def rock_spawner(self):
        if self.started:
            if len(self.rock_group) <= self.MAX_ROCKS:
                pos = self.gen_nonoverlap_pos_to_ship(self.asteroid_info)
                vel = self.incr_rock_vel_with_score()
                a_rock = Sprite(pos, vel, 0, self.rand_rock_angle_vel(), 
                                self.asteroid_image, self.asteroid_info,
                                self.WIDTH, self.HEIGHT)
                self.rock_group.add(a_rock)
    
    def shoot_missile(self):
        new_missile = self.my_ship.generate_missile()
        self.missile_group.add(new_missile)

    def remove_aged_sprites(self, sprite_group):
        for sprite in set(sprite_group):
            if sprite.sprite_is_aged():
                sprite_group.remove(sprite)
        
    def process_sprite_group(self, canvas, sprite_group):
        self.remove_aged_sprites(sprite_group)
        for sprite in sprite_group:
            sprite.draw(canvas)
            sprite.update_sprite_movement()
        
    def keyuphandler(self, key):
        for (key_type, func) in self.key_inputs_up.items():
            if key == simplegui.KEY_MAP[key_type]:
                func()
    
    def keydownhandler(self, key):
        for (key_type, func) in self.key_inputs_down.items():
            if key == simplegui.KEY_MAP[key_type]:
                func()
                
    def gen_bound(self):
        gui_center = [self.WIDTH / 2, self.HEIGHT / 2]
        splash_size = self.splash_info.get_size()
        return {'low_x': gui_center[0] - splash_size[0] / 2, 
                'hi_x': gui_center[0] + splash_size[0] / 2, 
                'low_y': gui_center[1] - splash_size[1] / 2, 
                'hi_y': gui_center[1] + splash_size[1] / 2}

    def mouseclick(self, pos):
        bounds_dict = self.gen_bound()
        in_width = bounds_dict['low_x'] < pos[0] < bounds_dict['hi_x'] 
        in_height = bounds_dict['low_y'] < pos[1] < bounds_dict['hi_y']
        if (not self.started) and in_width and in_height:
            self.started = True

    def draw(self, canvas):
        self.increment_time()
        self.draw_background_objects(canvas, self.wait_time())
        self.draw_game_metrics(canvas)
        self.draw_updated_ship(canvas)
        self.rock_spawner()
        
        if self.lives < 1:
            self.started = False
            self.rock_group = set([])
            self.game_start_prompts(canvas)
            self.play_background_music()
            self.lives = 3
            self.score = 0
        elif not self.started:
            self.game_start_prompts(canvas)
            self.play_background_music()
        else:
            self.stop_background_music()
            self.process_sprite_group(canvas, self.explosion_group)
            self.process_sprite_group(canvas, self.missile_group)
            self.process_sprite_group(canvas, self.rock_group)
            num_collisions = self.collide_group(self.rock_group, self.my_ship)
            self.lives -= num_collisions
            num_missile_hits = self.group_collide_group(self.missile_group, 
                                                            self.rock_group)
            self.score += num_missile_hits

main()