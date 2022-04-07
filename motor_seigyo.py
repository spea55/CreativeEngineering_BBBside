
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import serial
import os
import time
from collections import deque

import serial_test as st

pin_pwm = ["P9_14", "P9_22"]
pin_gpio = [['P8_26', 'P9_12'], ['P8_18', 'P8_16']]
PIN_ONPA = ['P8_12', 'P8_14']

def main():
    q_data = deque()
    count = 0
    num = 0
    flag = True
    
    conn = st.recv_data()
    init_gpio()
    while True:
        # direction = int(input('dir:'))
        # duty = int(input('duty:'))
        # length=int(input('len:'))
        if len(q_data) == 0:
            q_data, num = conn.get_data()
            if num  == '':
                continue

        else:
            # if flag:
            #     flag_txt = '0' + os.linesep
            #     port.write(flag_txt.encode('ascii'))
            #     port.flush() 
            #     flag = False
            
            data = q_data.popleft()
            direction = data[0]
            duty = data[1]
            length = data[2]
            print(direction,length,duty)
            
            if direction < 0:
                run_motor(0, 0)
                break
            elif direction == 10:
                C=int(input("コース"))
                rute(C)
            else:
                
                length=length*300
                sensor(length, direction, duty)

    PWM.stop(pin_pwm[0])
    PWM.stop(pin_pwm[1])
    PWM.cleanup()

def rute(C):
    if C==1:
        atk_rute_1()
    elif C==2:
        atk_rute_2()
    elif C==3:
        atk_rute_3()
        
def init_gpio():
    GPIO.setup(pin_gpio[0][0], GPIO.OUT)
    GPIO.setup(pin_gpio[0][1], GPIO.OUT)
    GPIO.setup(pin_gpio[1][0], GPIO.OUT)
    GPIO.setup(pin_gpio[1][1], GPIO.OUT)

    PWM.start(pin_pwm[0], 50, 2000000)
    PWM.start(pin_pwm[1], 50, 2000000)
    
def atk_rute_1():
    #すべての5点回収からのゴール
    #sensor(マス,方向,duty)
    run_motor(3,75)
    time.sleep(10)
    run_motor(0,0)
    
    sensor(1,1,75)
    sensor(1,4,75)
    sensor(1,3,75)
    sensor(1,1,75)
    
    run_motor(4,75)
    time.sleep(10)
    run_motor(0,0)
    
    sensor(1,2,75)
    sensor(1,3,75)
    sensor(1,4,75)
    sensor(2,1,75)
    sensor(1,3,75)
    sensor(1,1,75)
    sensor(1,3,75)
    sensor(2,4,75)

    sensor(1,1,75)
    run_motor(3,75)
    time.sleep(5)
    run_motor(0,0)

def atk_rute_2():
    #[1,5]回収からのゴール
    sensor(2,3,75)
    sensor(1,1,75)
    sensor(1,3,75)
    sensor(1,1,75)
    sensor(3,4,75)
    sensor(1,2,75)
    sensor(1,3,75)
    sensor(1,4,75)
    sensor(1,1,75)
    sensor(2,3,75)
    sensor(1,1,75)
    sensor(3,3,75)
    sensor(1,1,75)
    sensor(2,4,75)
    sensor(1,1,75)
    sensor(2,3,75)    

def atk_rute_3():
    #[0.0]-[0.3]を通らないようにルート
    sensor(5,3,75)
    sensor(1,1,75)
    sensor(1,4,75)
    sensor(1,3,75)
    sensor(1,1,75)
    run_motor(4,75)
    time.sleep(4)
    run_motor(0,0)
    while True:
        wall=distance_wall(1)
        if wall<=30:
            run_motor(0,0)
            break
        run_motor(4,75)
        time.sleep(0.05)
        run_motor(0,0)
    sensor(1,2,75)
    sensor(1,3,75)
    sensor(1,4,75)
    sensor(2,1,75)
    sensor(1,3,75)
    sensor(1,1,75)
    sensor(1,3,75)
    sensor(2,4,75)
    sensor(1,2,75)
    sensor(1,4,75)
    sensor(1,2,75)
    sensor(2,3,75)
    sensor(1,1,75)
    sensor(3,3,75)
    sensor(1,1,75)
    sensor(2,4,75)
    sensor(1,1,75)
    sensor(2,3,75)


def run_motor(direction, duty):
    if direction == 1: # up
        print('direction up')
        print('duty', duty)
        PWM.set_duty_cycle(pin_pwm[0], duty)
        GPIO.output(pin_gpio[0][0], GPIO.HIGH)
        GPIO.output(pin_gpio[0][1], GPIO.LOW)
    elif direction == 2: #down
        print('direction down')
        print('duty', duty)
        PWM.set_duty_cycle(pin_pwm[0], duty)
        GPIO.output(pin_gpio[0][0], GPIO.LOW)
        GPIO.output(pin_gpio[0][1], GPIO.HIGH)
    elif direction == 3: #right
        print('direction right')
        print('duty', duty)
        PWM.set_duty_cycle(pin_pwm[1], duty)
        GPIO.output(pin_gpio[1][0], GPIO.HIGH)
        GPIO.output(pin_gpio[1][1], GPIO.LOW)
    elif direction == 4: #left
        print('direction left')
        print('duty', duty)
        PWM.set_duty_cycle(pin_pwm[1], duty)
        GPIO.output(pin_gpio[1][0], GPIO.LOW)
        GPIO.output(pin_gpio[1][1], GPIO.HIGH)
    elif direction <= 0: #stop
        print('stop')
        PWM.set_duty_cycle(pin_pwm[0], duty)
        PWM.set_duty_cycle(pin_pwm[1], duty)
        GPIO.output(pin_gpio[0][0], GPIO.LOW)
        GPIO.output(pin_gpio[0][1], GPIO.LOW)
        GPIO.output(pin_gpio[1][0], GPIO.LOW)
        GPIO.output(pin_gpio[1][1], GPIO.LOW)


def distance_wall(n):
    distance_wall = 0

    while True:
        a=distance_onpa(n)
        if a<4000:
            distance_wall=a
            break
        else:
            run_motor(0,0)

    return distance_wall
    
def distance_onpa(n):
    start=0
    end=0
    GPIO.setup(PIN_ONPA[n], GPIO.OUT)
    GPIO.output(PIN_ONPA[n],GPIO.LOW)
    time.sleep(0.000002)
    GPIO.output(PIN_ONPA[n],GPIO.HIGH)
    time.sleep(0.0000005)
    GPIO.output(PIN_ONPA[n],GPIO.LOW)
    GPIO.setup(PIN_ONPA[n],GPIO.IN)
    while GPIO.input(PIN_ONPA[n])==0:
        start=time.time_ns()
    while GPIO.input(PIN_ONPA[n])==1:
        end=time.time_ns()
    difference_time = end-start
    distanceWall = difference_time * 0.172 / 1000
    print('距離', distanceWall)
    return distanceWall

def sensor(length, direction, duty):
    n=0
    if direction == 1 or direction == 2:
        n=0
    elif direction == 3 or direction == 4:
        n=1
    distanceWall_origin = 0
    distanceWall_now = 0
    distance_move = 0
    distance_hold = 0
    length=length*300
    flag=0

    distanceWall_origin = distance_wall(n)
    distance_last = distanceWall_origin
    run_motor(direction, duty)
    

    while True:
        #距離を測定
        distanceWall_now = distance_wall(n)
        
        #一回前の測定との差が300以下でmoveを更新
        if abs(distanceWall_now-distanceWall_origin)<300:
            #else入ったとき、いままでの移動量を更新
            if flag==1:
                distance_hold+=distance_move
                flag=0
            run_motor(direction,duty)

            #moveを更新
            distance_move=abs(distanceWall_now-distance_last)

            #現在位置を更新
            distanceWall_origin=distanceWall_now

            print('移動',distance_move+distance_hold)
        #おかしい値の場合、基準距離を変更
        else:
            run_motor(0,0)
            #elseに入ったことを保存
            flag=1

            #現在位置、基準位置を保存
            distanceWall_origin=distanceWall_now
            distance_last=distanceWall_now

            #正しい値が出るまで一度停止
            
            time.sleep(0.5)
            continue
        
        #今までの移動量(hold)+今の基準位置での移動量(move)の総移動量で判定
        if  length-(distance_move+distance_hold) <= 20:
            run_motor(0, 0)
            break
            
        elif length-(distance_move+distance_hold) <= 100:
            run_motor(direction, 50)
            time.sleep(0.05)
            run_motor(0,0)
            
        # elif length-(distance_move+distance_hold) < -10:
        #     length=abs(length-(distance_move+distance_hold))
        #     if direction == 1:
        #         direction=2
        #     elif direction == 2:
        #         direction=1
        #     elif direction == 3:
        #         direction=4
        #     elif direction == 4:
        #         direction==3
        #     sensor(length, direction, duty)
            
        

if __name__ == '__main__':
    main()
