import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pygame

from matplotlib.animation import FuncAnimation
from time import time

fig = plt.figure()

#TIME Parameter
interval1= 20 #단위 ms

Time_bound= 20 #초 단위


ax = plt.axes(xlim=(-20, 150), ylim=(-10, 10)) #수정, 예찬천재
plt.grid(True, axis='x')
ax.set_facecolor('black') #배경화면

#ps4
pygame.init()

joysticks = []
for i in range(pygame.joystick.get_count()):
    joysticks.append(pygame.joystick.Joystick(i))
for joystick in joysticks:
    joystick.init()



#실시간 확인용 파라미터
time_text = ax.text(0.7, 0.95, '', transform=ax.transAxes)
Velocity_text = ax.text(0.7, 0.90, '', transform=ax.transAxes)
AC_text = ax.text(0.7, 0.85, '', transform=ax.transAxes)
dx_text = ax.text(0.7, 0.80, '', transform=ax.transAxes)
#진행시간을 저장하는 배열
def duration_optimization(dur):
    sum_dur = np.zeros(dur.shape[0]+1)
    sum_dur[0]=0
    for i in range(dur.shape[0]):
        sum_dur[i+1]= dur[i] + sum_dur[i]
    return sum_dur

# Velocity
def Velocity(T,k):
    V= ac[k]*(T-do[k])*3.6 + start_V[k]
    return V

# initialization function: plot the background of each frame
def init():
    line.set_data([], [])
    point.set_data([], [])
    point_x.set_data([], [])
    return line,point, point_x

# animation function.  This is called sequentially
def update(i):
    global start_time,K,ds,yt,dyt, xt
    for event in pygame.event.get():
        if event.type == pygame.JOYAXISMOTION:
            if event.axis == 0:
                dyt=event.value*0.2
    con_time= ds*(time() - start_time) #프로그램 진행 시간

    ytt=yt[-1] + dyt*ds
    if ytt<0: ytt=0
    yt.append(ytt)

    if con_time-do[K] >= dur[K]:
        K=K+1
    V=Velocity(con_time,K)

    dy = yt[-1] - V

    time_text.set_text(f'Time = {con_time:0.1f} s ({ds}X)')
    Velocity_text.set_text(f'V = {V :.1f}Km/h')
    AC_text.set_text(f'AC = {ac[K]:.1f}m/s')
    dx_text.set_text(f'dy = {dy :.1f}')
   #여기가 경고 해주는 부분 (지우면 노랑색 없어짐)
   # if abs(dy)>10 : ax.set_facecolor('yellow')
    #else : ax.set_facecolor('black')

    xt = np.append(xt,con_time)

    point.set_data(yt,con_time)
    point_x.set_data(yt,con_time)#포인터는 실시간으로 변해야 함 쌓이면 안됨
    line.set_data(yt,xt)


    #ax = plt.axes(xlim=(-20, 150), ylim=(y_bot,y_top))  #시간축 update
    ax.set_ylim(con_time-Time_bound/2,con_time+Time_bound/2)
    #plt.ylim(y_bot,y_top)
    plt.draw()

    return time_text, Velocity_text, AC_text,dx_text, line, point, point_x


#Database 호출
df = pd.read_csv('https://raw.githubusercontent.com/dabo248/nedc/master/csv/nedc.csv')
ac = df['acceleration'] #accerlation 호출
dur =df['duration'] #duration 호출
Vt=[0]
Vt.extend(df['end_velocity'])
do=duration_optimization(dur) #해당 행에서의 end Time을 저장

frames1 = do[-1]*10**3/interval1 #600
print(frames1)
dyt=0
yt=[0]
y=[0]
start_V =df['start_velocity']
start_time=time()
K=0 #구간을 지정함
ds = 10 #시간 배속을 결정하는 상수

xt= [0]

#plt.gca().axes.yaxis.set_visible(False)


Vt1 = np.array(Vt) + 10 #실제 차대동력계 시험에서 떨어진 간격 알아내서 하면 좋을 듯
Vt2 = np.array(Vt) - 10

plt.plot(Vt, do, color = (135/255, 206/255, 235/255), linewidth = 3) #하늘색 중간 라인 색깔
plt.plot(Vt1, do, 'r', linewidth = 3)
plt.plot(Vt2, do, 'r', linewidth = 3)

line, = ax.plot([],[], 'w-', linewidth = 2)
point, = ax.plot([],[],'ro',markersize = 10, fillstyle = 'none')
point_x, = ax.plot([],[],'rx', markersize = 7) #포인트를 나중에 배치해서 안겹치게

time_text.set_color('white')
Velocity_text.set_color('white')
AC_text.set_color('white')
dx_text.set_color('white')

ax.tick_params(axis='x', top = True, bottom = False, labeltop = True, labelbottom = False)

ani = FuncAnimation(fig=fig, func=update, frames=int(frames1),
                    init_func=init, interval=interval1, blit=False)
plt.show()