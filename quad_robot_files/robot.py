from machine import Pin, PWM, Timer
import time
import motion_data

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
led = Pin('LED', Pin.OUT)
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
        action = motion_data.fwrd.copy()
        rows = len(motion_data.fwrd)
    elif mode == 'BWRD':
        action_mode = mode
        action.clear()
        action = motion_data.bwrd.copy()
        rows = len(motion_data.bwrd)
    elif mode == 'LTRN':
        action_mode = mode
        action.clear()
        action = motion_data.ltrn.copy()
        rows = len(motion_data.ltrn)
    elif mode == 'RTRN':
        action_mode = mode
        action.clear()
        action = motion_data.rtrn.copy()
        rows = len(motion_data.rtrn)
    elif mode == 'LEFT':
        action_mode = mode
        action.clear()
        action = motion_data.left.copy()
        rows = len(motion_data.left)
    elif mode == 'RGHT':
        action_mode = mode
        action.clear()
        action = motion_data.rght.copy()
        rows = len(motion_data.rght)

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
