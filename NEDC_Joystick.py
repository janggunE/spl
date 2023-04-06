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
line1, = plt.plot([], [],color='red')
line2, = plt.plot([], [],color='red')
line_main, = plt.plot([], [])
dot, = plt.plot([], [], 'r')
plt.grid(True, axis='x')
#ax.set_facecolor('black') #배경화면

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
    line1.set_data([], [])
    line2.set_data([], [])
    line_main.set_data([],[])
    time_text.set_text('')
    Velocity_text.set_text('')
    return line1, line2,line_main, time_text,Velocity_text,AC_text

# animation function.  This is called sequentially
def update(i):
    global x,y,start_time,K,ds, y_bot, y_top,yt,dyt, xt
    for event in pygame.event.get():
        if event.type == pygame.JOYAXISMOTION:
            if event.axis == 0:
                dyt=event.value*0.2
    con_time= ds*(time() - start_time) #프로그램 진행 시간

    ytt=yt[-1] + dyt*ds
    if ytt<0: ytt=0
    yt.append(ytt)

    if con_time+10-do[K] >= dur[K]:
        K=K+1
    V=Velocity(con_time+10,K)
    y.append(V)
    y1=np.array(y)+10
    y2=np.array(y)-10

    dx_array=abs(np.array(x)-con_time)
    dx_indexarray=np.where(dx_array==min(dx_array))
    dx_index=dx_indexarray[0][0]

    dy = yt[-1] - y[dx_index]

    time_text.set_text(f'Time = {con_time:0.1f} s ({ds}X)')
    Velocity_text.set_text(f'{V = :.1f}Km/h')
    AC_text.set_text(f'AC = {ac[K]:.1f}m/s')
    dx_text.set_text(f'{dy = :.1f}')

    if abs(dy)>10 : ax.set_facecolor('yellow')
    else : ax.set_facecolor('white')



    x = np.append(x,con_time+10)
    xt = np.append(xt,con_time)

    line1.set_data(y1, x)
    line2.set_data(y2, x)
    line_main.set_data(y, x)
    dot.set_data(yt,xt)

    #ax = plt.axes(xlim=(-20, 150), ylim=(y_bot,y_top))  #시간축 update
    ax.set_ylim(con_time-Time_bound/2,con_time+Time_bound/2)
    #plt.ylim(y_bot,y_top)
    plt.draw()

    return line1, line2,line_main,  time_text, Velocity_text, AC_text,dx_text,dot


#Database 호출
df = pd.read_csv('https://raw.githubusercontent.com/dabo248/nedc/master/csv/nedc.csv')
ac = df['acceleration'] #accerlation 호출
dur =df['duration'] #duration 호출
do=duration_optimization(dur) #해당 행에서의 end Time을 저장

frames1 = do[-1]*10**3/interval1 #600
print(frames1)
dyt=0
yt=[0]
start_V =df['start_velocity']
start_time=time()
K=0 #구간을 지정함
ds = 1 #시간 배속을 결정하는 상수

x= np.linspace(0,10,300)
xt= [0]
y=[0 for i in range(300)]

#plt.gca().axes.yaxis.set_visible(False)


ani = FuncAnimation(fig=fig, func=update, frames=int(frames1),
                    init_func=init, interval=interval1, blit=False)
plt.show()