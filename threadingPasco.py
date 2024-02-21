from pasco import PASCOBLEDevice
import time
import datetime
import threading

# List of sensor names you want to connect to
desired_sensor_names = ['Load Cell 256-888>P1', 'Load Cell 217-261>P9', 'Load Cell 026-381>P9']

# Initialize a PASCOBLEDevice instance for each sensor
sensor_instances = [PASCOBLEDevice() for _ in range(len(desired_sensor_names))]

# Function to connect to a sensor by its name
def connect_to_sensor(sensor_instance, sensor_name):
    found_devices = sensor_instance.scan()

    for ble_device in found_devices:
        if ble_device.name == sensor_name:
            sensor_instance.connect(ble_device)
            print(f'Connected to sensor with name {sensor_name}')
            return True

    print(f'Sensor with name {sensor_name} not found')
    return False

# Function for collecting data from a sensor
def collect_data(sensor_instance, sensor_name):
    if connect_to_sensor(sensor_instance, sensor_name):
        for i in range(20):
            force = sensor_instance.read_data('Force')
            with open(f'{sensor_name}_data.txt', 'a') as file:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                file.write(f'{timestamp} - Force: {force}\n')
        sensor_instance.disconnect()
        print(f'Sensor {sensor_name} disconnected')

# Create threads for each sensor
threads = []

for i in range(len(desired_sensor_names)):
    thread = threading.Thread(target=collect_data, args=(sensor_instances[i], desired_sensor_names[i]))
    threads.append(thread)

# Start the threads
for thread in threads:
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()

# Sleep for a period (adjust as needed)
time.sleep(60)  # Sleep for 60 seconds before searching again
