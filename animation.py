from kivy.app import App
from kivy.properties import Clock
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Ellipse, Triangle, Rectangle
from kivy.properties import StringProperty
from main import solve_ivp, find_Fa, find_phi, Fr, rr, u, m, friction, max_sim_length
from energiesummentest import test


class MainWidget(RelativeLayout):

    size_car = 0
    time_running = 0
    track_start = .1
    track_length = .8
    car_x = 0

    arrow_speed_length = 0
    arrow_acceleration_length = 0
    arrow_friction_length = 0


    sim_speed = 1

    sim_play = False
    solution, max_x = solve_ivp(max_sim_length,friction)
    car_a_label = StringProperty("a: 0")
    car_v_label = StringProperty("v: 0")
    car_x_label = StringProperty("x: 0")
    max_x_label = StringProperty("max distance: " + str(round(max_x,2)))
    car_t_label = StringProperty("t: 0")


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.innit_speed_arrow()
        self.innit_acceleration_arrow()
        self.innit_friction_arrow()
        self.innit_car()
    
        Clock.schedule_interval(self.update,1.0/60.0) # ruft update() 60 mal pro sekunde

    def innit_car(self):
        """
        definirt die formen des autos
        """
        with self.canvas.before:
            Color(1,1,1)
            self.car = Ellipse()
        with self.canvas:
            Color(.7,.7,.7)
            self.arrow_base_circle_1 = Ellipse()
            self.arrow_base_circle_2 = Ellipse()

    def innit_speed_arrow(self):
        """
        definirt die formen des geschwindigkeits pfeil
        """
        with self.canvas:
            Color(0,0.5,0)
            self.speed_arrow_base = Rectangle()
        with self.canvas.after:
            Color(0,0.6,0)
            self.speed_arrow_tip = Triangle()
        
    def innit_acceleration_arrow(self):
        """
        definirt die formen des beschleunigungs pfeil
        """
        with self.canvas:
            Color(0,0,0.5)
            self.acceleration_arrow_base = Rectangle()
        with self.canvas.after:
            Color(0,0,0.6)
            self.acceleration_arrow_tip = Triangle()
    
    def innit_friction_arrow(self):
        """
        definirt die formen des reibungs pfeil
        """
        with self.canvas:
            Color(0.6,0,0)
            self.friction_arrow_base = Rectangle()
        with self.canvas.after:
            Color(0.7,0,0)
            self.friction_arrow_tip = Triangle()
    
    def start_stop(self,obj):
        """
        startet und stopt die simulation
        """
        if obj.state == "down":
            self.sim_play = True
            obj.text = "stop"
        if obj.state == "normal":
            self.sim_play = False
            obj.text = "start"

    def restart(self):
        """
        starttet die simulation neu
        """
        self.time_running = 0
    
    def speed_change(self,obj):
        self.sim_speed = obj.value

    def draw_triangle(self,extra_y,length,direction):
        """
        berechnet die koordinaten der punkte eines pfeils
        """
        arrow_pos_x = self.car_x+self.size_car*0.5
        arrow_y = self.size_car*0.5
        arrow_base_pos = arrow_pos_x,arrow_y-self.size_car*0.08+extra_y
        arrow_base_size = length,self.size_car*0.16
        point1 = (arrow_pos_x+length,arrow_y-self.height/75+extra_y)
        point2 = (arrow_pos_x+length,arrow_y+self.height/75+extra_y)
        point3 = (arrow_pos_x+length+(self.width/60)*direction,arrow_y+extra_y)
        return (arrow_base_pos,arrow_base_size,(*point1, *point2, *point3))

    def update_speed_arrow(self):
        self.arrow_speed_length = self.speed*10*(self.width/800)
        base_pos,base_size,points = self.draw_triangle(self.size_car*-0.3,self.arrow_speed_length,1)
        self.speed_arrow_base.pos = base_pos
        self.speed_arrow_base.size = base_size
        self.speed_arrow_tip.points = [*points]
    
    def update_acceleration_arrow(self):
        self.arrow_acceleration_length = self.acceleration*10*(self.width/800)
        base_pos,base_size,points = self.draw_triangle(self.size_car*0.3,self.arrow_acceleration_length,1)
        self.acceleration_arrow_base.pos = base_pos
        self.acceleration_arrow_base.size = base_size
        self.acceleration_arrow_tip.points = [*points]

    def update_friction_arrow(self):
        if friction == True:
            self.arrow_friction_length = self.friction*10*(self.width/800)
        else:
            self.arrow_friction_length = 0
        base_pos,base_size,points = self.draw_triangle(self.size_car*0.3,-self.arrow_friction_length,-1)
        self.friction_arrow_base.pos = base_pos
        self.friction_arrow_base.size = base_size
        self.friction_arrow_tip.points = [*points]

    def update_car(self):
        self.size_car = self.width/20
        self.max_distance = self.solution.sol(max_sim_length)[1]
        self.distance_percent = self.distance / self.max_distance
        self.car_x = (self.track_start*self.width) + (self.track_length*self.width) * self.distance_percent
        self.car.size = (self.size_car,self.size_car)
        self.car.pos = (self.car_x,0)
        self.arrow_base_circle_1.size = (self.size_car*0.3,self.size_car*0.3)
        self.arrow_base_circle_1.pos = (self.car_x+self.size_car*0.35,self.size_car*0.05)
        self.arrow_base_circle_2.size = (self.size_car*0.3,self.size_car*0.3)
        self.arrow_base_circle_2.pos = (self.car_x+self.size_car*0.35,self.size_car*0.65)

    def update_lables(self):
        self.car_a_label = "a: " + str(round(self.acceleration-self.friction,1)) + "m/s²"
        self.car_v_label = "v: " + str(round(self.speed,1)) + "m/s"
        self.car_x_label = "x: " + str(round(self.distance,1)) + "m"
        self.car_t_label = "t: " + str(round(self.time_running,1)) + "s"
    
    def update(self,dt):
        """
        updatet alle formen
        """

        if self.sim_play:
            self.time_running += dt*self.sim_speed
        
        self.distance = self.solution.sol(self.time_running)[1]
        self.speed = self.solution.sol(self.time_running)[0]
        self.acceleration = find_Fa(rr,u,find_phi(self.distance,rr,u))/m
        self.friction = (Fr(self.speed))/m

        self.update_speed_arrow()
        self.update_acceleration_arrow()
        self.update_friction_arrow()
        self.update_lables()
        self.update_car()

class AutoAnimationApp(App):
    def build(self):
        self.load_kv("animation.kv")

AutoAnimationApp().run() # startet die app
test(True) # testet ob der energie erhaltungssatz verletzt wurde