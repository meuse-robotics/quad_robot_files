import network

from machine import Pin
import uasyncio as asyncio

import robot
import html

pico_led = Pin('LED', machine.Pin.OUT)

ssid = 'your-SSID'
password = 'your-PASSWORD'
#IP_ADDRESS = '192.168.0.100'
wlan = network.WLAN(network.STA_IF)

async def connect_to_wifi():
    #wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.config(pm = 0xa11140)
    wlan.connect(ssid, password)
    print("Connecting to Wi-Fi...")
    while not wlan.isconnected():
        await asyncio.sleep(1)
    #wlan_status = wlan.ifconfig()
    #wlan.ifconfig((IP_ADDRESS, wlan_status[1], wlan_status[2], wlan_status[3]))
    #wlan_status = wlan.ifconfig()
    print("Connected to Wi-Fi!")
    print("IP Address:", wlan.ifconfig()[0])

async def serve_client(reader, writer):
    print("Client connected")
    request_line = await reader.readline()
    print("Request:", request_line)
    # We are not interested in HTTP request headers, skip them
    while await reader.readline() != b"\r\n":
        pass

    request = str(request_line)
    try:
        request = request.split()[1]
    except IndexError:
        pass
    
    if request == '/lighton?':
        pico_led.on()
    elif request =='/lightoff?':
        pico_led.off()
    elif request == '/stop?':
        robot.set_action('STOP')
    elif request == '/fwrd?':
        robot.set_action('FWRD')
    elif request == '/bwrd?':
        robot.set_action('BWRD')
    elif request == '/ltrn?':
        robot.set_action('LTRN')
    elif request == '/rtrn?':
        robot.set_action('RTRN')
    elif request == '/left?':
        robot.set_action('LEFT')
    elif request == '/rght?':
        robot.set_action('RGHT')
         
    response = html.html
    writer.write('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    writer.write(response)

    await writer.drain()
    await writer.wait_closed()
    print("Client disconnected")

async def main():
    print('Connecting to Network...')
    await connect_to_wifi()

    print('Setting up webserver...')
    asyncio.create_task(asyncio.start_server(serve_client, "0.0.0.0", 80))
    
    while True:
        robot.drive()
        await asyncio.sleep(0.03)
                
try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()
