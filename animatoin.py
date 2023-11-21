from kivy.app import App
from kivy.properties import Clock
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Ellipse, Triangle, Rectangle
from kivy.properties import StringProperty
from mausefallenauto import solve_ivp
from mausefallenauto import rr
from mausefallenauto import m
from mausefallenauto import u
from mausefallenauto import max_sim_length

class MainWidget(RelativeLayout):

    größe_car = 20
    time_running = 0
    sim_play = False
    sulution = solve_ivp(max_sim_length)
    car_x_label = StringProperty("x: 0")
    car_v_label = StringProperty("v: 0")


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.innit_car()
    
        Clock.schedule_interval(self.update,1.0/60.0)

    def innit_car(self):
        with self.canvas:
            Color(1,1,1)
            self.car = Ellipse(size = (self.größe_car,self.größe_car))
    
    def start_stop(self,obj):
        if obj.state == "down":
            self.sim_play = True
            obj.text = "stop"
        if obj.state == "normal":
            self.sim_play = False
            obj.text = "start"

    def update(self,dt):

        dt = min(dt,1/50)

        if self.sim_play:
            self.time_running += dt

        self.speed = self.sulution.sol(self.time_running)[0]

        self.distance = self.sulution.sol(self.time_running)[1]
        self.max_distance = self.sulution.sol(max_sim_length)[1]

        self.car_x = (self.distance / self.max_distance) * (self.width - self.größe_car)

        self.car_x_label = "x: " + str(round(self.distance,2)) + "m"
        self.car_v_label = "v: " + str(round(self.speed,2)) + "m/s"

        self.car.pos = (self.car_x,0)

class AutoAnimationApp(App):
    def build(self):
        self.load_kv("AutoAnimation.kv")

AutoAnimationApp().run()