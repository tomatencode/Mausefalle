from kivy.app import App
from kivy.properties import Clock
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Ellipse, Triangle, Rectangle
from kivy.properties import StringProperty
from mausefallenauto import solve_ivp, find_Fa, find_phi, rr, u, m
from mausefallenauto import rr
from mausefallenauto import m
from mausefallenauto import u
from mausefallenauto import max_sim_length

class MainWidget(RelativeLayout):

    size_car = 27
    time_running = 0
    track_start = .1
    track_length = .8
    car_x = 0

    arrow_speed_length = 0

    arrow_acceleration_length = 0


    sim_speed = 1

    sim_play = False
    sulution = solve_ivp(max_sim_length)
    car_x_label = StringProperty("x: 0")
    car_v_label = StringProperty("v: 0")
    car_t_label = StringProperty("t: 0")


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.innit_car()
        self.innit_speed_arrow()
        self.innit_acceleration_arrow()
    
        Clock.schedule_interval(self.update,1.0/60.0)

    def innit_car(self):
        with self.canvas:
            Color(1,1,1)
            self.car = Ellipse(size = (self.size_car,self.size_car))

    def innit_speed_arrow(self):
        with self.canvas:
            Color(0,0.6,0)
            self.speed_arrow_base = Rectangle()
            self.speed_arrow_tip = Triangle()
        
    def innit_acceleration_arrow(self):
        with self.canvas:
            Color(0,0,0.6)
            self.acceleration_arrow_base = Rectangle()
            self.acceleration_arrow_tip = Triangle()
    
    def start_stop(self,obj):
        if obj.state == "down":
            self.sim_play = True
            obj.text = "stop"
        if obj.state == "normal":
            self.sim_play = False
            obj.text = "start"

    def restart(self):
        self.time_running = 0
    
    def speed_change(self,obj):
        self.sim_speed = obj.value

    def draw_triangle(self,extra_y,length):
        arrow_pos_x = self.car_x+self.size_car*0.5
        arrow_y = self.size_car*0.5
        arrow_base_pos = arrow_pos_x,arrow_y-self.height/300+extra_y
        arrow_base_size = length,self.height/150
        point1 = (arrow_pos_x+length,arrow_y-self.height/75+extra_y)
        point2 = (arrow_pos_x+length,arrow_y+self.height/75+extra_y)
        point3 = (arrow_pos_x+length+self.width/60,arrow_y+extra_y)
        return (arrow_base_pos,arrow_base_size,(*point1, *point2, *point3))

    def update_speed_arrow(self):
        self.arrow_speed_length = (self.speed*10)*self.sim_speed
        base_pos,base_size,points = self.draw_triangle(self.size_car*-0.3,self.arrow_speed_length)
        self.speed_arrow_base.pos = base_pos
        self.speed_arrow_base.size = base_size
        self.speed_arrow_tip.points = [*points]
    
    def update_acceleration_arrow(self):
        self.arrow_acceleration_length = (find_Fa(rr,u,find_phi(self.distance,rr,u))*10)/m
        base_pos,base_size,points = self.draw_triangle(self.size_car*0.3,self.arrow_acceleration_length)
        self.acceleration_arrow_base.pos = base_pos
        self.acceleration_arrow_base.size = base_size
        self.acceleration_arrow_tip.points = [*points]

    def update_car(self):
        self.size_car = self.width/30
        self.car.size = (self.size_car,self.size_car)
        self.max_distance = self.sulution.sol(max_sim_length)[1]
        self.distance_percent = self.distance / self.max_distance
        self.car_x = (self.track_start*self.width) + (self.track_length*self.width) * self.distance_percent

    def update_lables(self):

        self.car_x_label = "x: " + str(round(self.distance,1)) + "m"
        self.car_v_label = "v: " + str(round(self.speed,1)) + "m/s"
        self.car_t_label = "t: " + str(round(self.time_running,1)) + "s"
    
    def update(self,dt):

        dt = min(dt,1/50)

        if self.sim_play:
            self.time_running += dt*self.sim_speed
        
        self.distance = self.sulution.sol(self.time_running)[1]
        self.speed = self.sulution.sol(self.time_running)[0]

        self.update_car()
        self.update_speed_arrow()
        self.update_acceleration_arrow()
        self.update_lables()

        self.car.pos = (self.car_x,0)

class AutoAnimationApp(App):
    def build(self):
        self.load_kv("AutoAnimation.kv")

AutoAnimationApp().run()