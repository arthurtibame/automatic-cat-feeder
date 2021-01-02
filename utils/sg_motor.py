import RPi.GPIO as GPIO
import time


class SG_Motor(object):
    def __init__(self, control_pin=18, pwm_freq=50, step=90) -> None:
        self.pwm_freq=pwm_freq
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(control_pin, GPIO.OUT) 
        self.pwm = GPIO.PWM(control_pin, pwm_freq)
        self.pwm.start(0)
        print("init to 0")
 
    def __angle_to_duty_cycle(self, angle=0):
        duty_cycle = (0.05 * self.pwm_freq) + (0.19 * self.pwm_freq * angle / 180)
        return duty_cycle

    def start(self):
        #self.pwm.ChangeDutyCycle(self.__angle_to_duty_cycle(0))
        time.sleep(1)
        self.pwm.ChangeDutyCycle(self.__angle_to_duty_cycle(0))

    def stop(self):        
        self.pwm.ChangeDutyCycle(self.__angle_to_duty_cycle(180))        
        #time.sleep(2)
        #self.pwm.ChangeDutyCycle(self.__angle_to_duty_cycle(180))        
        #self.pwm.stop()
        #GPIO.cleanup()

