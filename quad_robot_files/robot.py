from machine import Pin, PWM, Timer
import time

# ******************
# ***** Action *****
# ******************
Action_type=['STOP','FWRD','BWRD','LTRN','RTRN','LEFT','RGHT']

SV_FREQ = 50.0     # サーボ信号周波数
MAX_DUTY = 65025.0 # 周期内の分割数
MIN_SV_PULSE = 0.6  # 最小パルス幅　0°
MAX_SV_PULSE = 2.4  # 最大パルス幅 180°

correction = [4,0, 0,0,8,-8, 8,-8,0,-8, -12,0]
servo = []
temp_angle = [90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90]
step = [
[90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 3],
[90,100,110, 90, 90, 90, 90, 90, 90, 90, 80, 70, 3],
[90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 8],
[90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 3],
[90, 90, 90, 90, 80, 70, 90,100,110, 90, 90, 90, 3],
[90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 8]
]
fwrd = [
[90,105, 70, 90, 86, 95, 90, 94, 85, 90, 75,110, 3],
[90,100,110, 90, 82,100, 90, 98, 80, 90, 80, 70, 3],
[90, 90, 90, 90, 78,105, 90,102, 75, 90, 90, 90, 8],
[90, 94, 85, 90, 75,110, 90,105, 70, 90, 86, 95, 3],
[90, 98, 80, 90, 80, 70, 90,100,110, 90, 82,100, 3],
[90,102, 75, 90, 90, 90, 90, 90, 90, 90, 78,105, 8]
]
bwrd = [
[90,102, 75, 90, 90, 90, 90, 90, 90, 90, 78,105, 3],
[90, 98, 80, 90, 80, 70, 90,100,110, 90, 82,100, 3],
[90, 94, 85, 90, 75,110, 90,105, 70, 90, 86, 95, 8],
[90, 90, 90, 90, 78,105, 90,102, 75, 90, 90, 90, 3],
[90,100,110, 90, 82,100, 90, 98, 80, 90, 80, 70, 3],
[90,105, 70, 90, 86, 95, 90, 94, 85, 90, 75,110, 8]
]
ltrn = [
[90-10, 90, 90, 90+ 5, 90, 90, 90+ 5, 90, 90, 90-10, 90, 90, 3],
[90+10,100,110, 90+ 0, 90, 90, 90+ 0, 90, 90, 90+10, 80, 70, 3],
[90+10, 90, 90, 90- 5, 90, 90, 90- 5, 90, 90, 90+10, 90, 90, 8],
[90+ 5, 90, 90, 90-10, 90, 90, 90-10, 90, 90, 90+ 5, 90, 90, 3],
[90+ 0, 90, 90, 90+10, 80, 70, 90+10,100,110, 90+ 0, 90, 90, 3],
[90- 5, 90, 90, 90+10, 90, 90, 90+10, 90, 90, 90- 5, 90, 90, 8]
]
rtrn = [
[90+10, 90, 90, 90- 5, 90, 90, 90- 5, 90, 90, 90+10, 90, 90, 3],
[90-10,100,110, 90- 0, 90, 90, 90- 0, 90, 90, 90-10, 80, 70, 3],
[90-10, 90, 90, 90+ 5, 90, 90, 90+ 5, 90, 90, 90-10, 90, 90, 8],
[90- 5, 90, 90, 90+10, 90, 90, 90+10, 90, 90, 90- 5, 90, 90, 3],
[90- 0, 90, 90, 90-10, 80, 70, 90-10,100,110, 90- 0, 90, 90, 3],
[90+ 5, 90, 90, 90-10, 90, 90, 90-10, 90, 90, 90+ 5, 90, 90, 8]
]
left = [
[90-10, 90, 90, 90+ 5, 90, 90, 90- 5, 90, 90, 90+10, 90, 90, 3],
[90+10,100,110, 90+ 0, 90, 90, 90- 0, 90, 90, 90-10, 80, 70, 3],
[90+10, 90, 90, 90- 5, 90, 90, 90+ 5, 90, 90, 90-10, 90, 90, 8],
[90+ 5, 90, 90, 90-10, 90, 90, 90+10, 90, 90, 90- 5, 90, 90, 3],
[90+ 0, 90, 90, 90+10, 80, 70, 90-10,100,110, 90- 0, 90, 90, 3],
[90- 5, 90, 90, 90+10, 90, 90, 90-10, 90, 90, 90+ 5, 90, 90, 8]
]
rght = [
[90+10, 90, 90, 90- 5, 90, 90, 90+ 5, 90, 90, 90-10, 90, 90, 3],
[90-10,100,110, 90- 0, 90, 90, 90+ 0, 90, 90, 90+10, 80, 70, 3],
[90-10, 90, 90, 90+ 5, 90, 90, 90- 5, 90, 90, 90+10, 90, 90, 8],
[90- 5, 90, 90, 90+10, 90, 90, 90-10, 90, 90, 90+ 5, 90, 90, 3],
[90- 0, 90, 90, 90-10, 80, 70, 90+10,100,110, 90+ 0, 90, 90, 3],
[90+ 5, 90, 90, 90-10, 90, 90, 90+10, 90, 90, 90- 5, 90, 90, 8]
]

div_counter = 0
key_frame = 0
next_key_frame = 1
rows = 0
action = []
action_mode = 'STOP'

# パルス幅を計算する関数
def get_pulse_width(angle):
    pulse_ms = MIN_SV_PULSE + (MAX_SV_PULSE - MIN_SV_PULSE) * angle / 180.0
    x = (int)(MAX_DUTY * (pulse_ms * SV_FREQ /1000.0))
    return x

# 全てのサーボを順番に駆動
for i in range(12):
    servo.append(PWM(Pin(11 - i)))
    servo[i].freq(50)
    servo[i].duty_u16(get_pulse_width(90 + correction[i]))

# ******************
# ***** LED *****
# ******************
led = Pin(25, Pin.OUT)
led.value(0)

# ******************
# *** SET ACTION ***
# ******************
def set_action(mode):
    global action_mode
    global action
    global rows
    global div_counter
    global key_frame
    global next_key_frame
    
    if mode == 'STOP':
        action_mode = mode
    elif mode == 'FWRD':
        action_mode = mode
        action.clear()
        action = fwrd.copy()
        rows = len(fwrd)
    elif mode == 'BWRD':
        action_mode = mode
        action.clear()
        action = bwrd.copy()
        rows = len(bwrd)
    elif mode == 'LTRN':
        action_mode = mode
        action.clear()
        action = ltrn.copy()
        rows = len(ltrn)
    elif mode == 'RTRN':
        action_mode = mode
        action.clear()
        action = rtrn.copy()
        rows = len(rtrn)
    elif mode == 'LEFT':
        action_mode = mode
        action.clear()
        action = left.copy()
        rows = len(left)
    elif mode == 'RGHT':
        action_mode = mode
        action.clear()
        action = rght.copy()
        rows = len(rght)

    div_counter = 0
    key_frame = 0
    next_key_frame = 1

# ******************
# ****** DRIVE *****
# ******************
def drive():
    global action_mode
    global div_counter
    global key_frame
    global next_key_frame

    if action_mode != 'STOP':
        # キーフレームを更新
        div_counter += 1
        if div_counter >= action[key_frame][12]:
            div_counter = 0
            key_frame = next_key_frame
            next_key_frame += 1
            if next_key_frame > rows-1:
                next_key_frame = 0

        # 角度計算
        for i in range(12):
            temp_angle[i] = action[key_frame][i] + \
                     (action[next_key_frame][i] - action[key_frame][i]) \
                    * div_counter / action[key_frame][12]
    else:
        for i in range(12):
            temp_angle[i] = 90
    # サーボ駆動
    for i in range(12):
        servo[i].duty_u16(get_pulse_width(int(temp_angle[i]) + correction[i]))
