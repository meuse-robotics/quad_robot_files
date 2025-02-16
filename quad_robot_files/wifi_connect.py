import network
import time

# Set the Wi-Fi SSID and password
SSID = "your-SSID"
PASSWORD = "your-PASSWORD"

# Function to connect to Wi-Fi
def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)  # STA_IF is Station mode
    wlan.active(True)  # Enable Wi-Fi
    wlan.config(pm = 0xa11140)  # Turn off Wi-Fi power saving
    wlan.connect(SSID, PASSWORD)  # Connect to the Wi-Fi network

    print("Connecting to Wi-Fi...")
    while not wlan.isconnected():  # Wait until connected
        print(".", end="")
        time.sleep(1)

    print("\nConnected!")
    print("IP Address:", wlan.ifconfig()[0])  # Display the IP address

# Main process
connect_to_wifi()
