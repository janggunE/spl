import RPi.GPIO as GPIO
import time
import pygame

GPIO.setmode(GPIO.BCM) #BCM으로 GPIO설정

servo_pin = 11  #GPIO 출력 번호, 바꿀 수 있음
GPIO.setup(servo_pin,GPIO.OUT) #GPIO 출력 핀 설정

pwm = GPIO.PWM(servo_pin,50) #주파수 50헤르츠인 PWM 개체 생성
pwm.start(0) #듀티 사이클 0인 PWM 신호 시작하는 함수
#여기에 서보모터 초기 각도를 90도로 지정하고 싶다..
def set_duty_cycle(duty_cycle):
    pwm.ChangeDutyCycle(duty_cycle) #듀티사이클 바꿔서 입력해주는 함수

pygame.init()
pygame.joystick.init() #조이스틱 모듈 초기화하는 함수

joystick = pygame.joystick.Joystick(0) #첫번째 조이스틱 객체 생성하는 함수
                                       # 숫자는 매개변수

while True:
    pygame.event.pump() #밀려 있는 이벤트 처리
    x_axis = joystick.get_axis(0) #0을 x축으로 설정
    y_axis = joystick.get_axis(1) #1을 y축으로 설정

    duty_cycle = ((y_axis + 1)/2)*100 #100분율로 듀티사이클 설정

    set_duty_cycle(duty_cycle) #듀티사이클 변경 후 입력

    time.sleep(0.02) #서보모터에 처리할 시간 주기
