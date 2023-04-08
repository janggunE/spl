import pygame

import RPi.GPIO as GPIO
import time

servo_pin = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

pwm = GPIO.PWM(servo_pin, 50)

pwm.start(0.0)

pygame.init()

pygame.joystick.init()

joystick = pygame.joystick.Joystick(0)
joystick.init()
K=0

while True:
    for event in pygame.event.get():
        if event.type == pygame.JOYAXISMOTION:
            if event.axis ==0:
                value = joystick.get_axis(0)
                
                angle=(value+1)/2*180.0

                if angle==0:
                    K=K+1
                    if K<=10:
                        pwm.ChangeDutyCycle(angle / 18 + 2)
                elif:
                    K=0
                    pwm.ChangeDutyCycle(angle / 18 + 2)
                
        elif event.type == pygame.JOYBUTTONDOWN:
            if event.button == 9:
                pwm.ChangeDutyCycle(0.0)
                exit()