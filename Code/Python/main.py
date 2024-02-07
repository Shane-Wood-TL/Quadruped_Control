import PySimpleGUI as sg
import serial
import threading
import queue

lastValue = 0

def serial_thread(com_port, window, values_queue):
    def read_serial(s, window):
        while True:
            try:
                # Read from the serial port
                res = s.readline().decode().strip()
                global lastValue
                if(res == lastValue):
                    print((res))
                    res = lastValue
                # Update the GUI in a thread-safe way
                window.write_event_value('-UPDATE_SERIAL-', res)
                
            except Exception as e:
                #print(f'Error reading from serial: {e}')
                break

    try:
        s = serial.Serial(com_port, 9600, timeout=1)
        
        # Start a separate thread to continuously read serial input
        serial_thread = threading.Thread(target=read_serial, args=(s, window))
        serial_thread.daemon = True  # Set the thread as daemon to allow it to exit when the main thread exits
        serial_thread.start()
        
        while True:
            # Check if there are values to send
            if not values_queue.empty():
                values_to_send = values_queue.get()
                # Convert values to bytes and send them over serial
                s.write(values_to_send.encode())
                s.write(b"\n")  # Write newline character after sending values
                
    except Exception as e:
        #print(f'Error in serial thread: {e}')
        pass

sg.theme('DarkBlue1')

# Define sub-layouts
header_layout = [
    [sg.Text('Robot Controller')],
]

leg_layout = [
    [sg.Text('', size=(6, 1)), sg.Text('Aleg', size=(6, 1)), sg.Text('Bleg', size=(6, 1)), sg.Text('Cleg', size=(6, 1)), sg.Text('Dleg', size=(6, 1))],
    [sg.Text('xH', size=(6, 1)), sg.InputText('1', size=(6, 1), key="xHa"), sg.InputText('1', size=(6, 1), key="xHb"), sg.InputText('1', size=(6, 1), key="xHc"), sg.InputText('1', size=(6, 1), key="xHd")],
    [sg.Text('xLR', size=(6, 1)), sg.InputText('1', size=(6, 1), key="xLRa"), sg.InputText('1', size=(6, 1), key="xLRb"), sg.InputText('1', size=(6, 1), key="xLRc"), sg.InputText('1', size=(6, 1), key="xLRd")],
    [sg.Text('xFB', size=(6, 1)), sg.InputText('1', size=(6, 1), key="xFBa"), sg.InputText('1', size=(6, 1), key="xFBb"), sg.InputText('1', size=(6, 1), key="xFBc"), sg.InputText('1', size=(6, 1), key="xFBd")],
    [sg.Button('Send Values')],
]

mode_layout = [
    [sg.Checkbox('PID')],
    [sg.Checkbox('Gyro')],
    [sg.Checkbox('Set Motor Offsets')],
]

connection_layout = [
    [sg.Text('Connection')],
    [sg.Text('COM Port:', size=(10, 1)), sg.InputText(size=(10, 1), key='-COM_PORT-')],
    [sg.Text('TELNET Port:', size=(10, 1)), sg.InputText(size=(10, 1), key='-TELNET_PORT-')],
    [sg.Button('Connect')],
]

# Combine sub-layouts into a larger layout using sg.Column
layout = [
    [sg.Column(header_layout, element_justification='c')],
    [sg.Column(leg_layout, size=(400, 150), key='-LEG_LAYOUT-'), sg.Column(mode_layout, element_justification='c')],
    [sg.Column(connection_layout, element_justification='c')],
]

# Create the Window
window = sg.Window('Robot Control', layout)

values_queue = queue.Queue()

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    elif event == 'Connect':
        com_port = values['-COM_PORT-']
        # Start the serial communication thread with the dynamically entered COM port
        serial_thread_instance = threading.Thread(target=serial_thread, args=(com_port, window, values_queue), daemon=True)
        serial_thread_instance.start()
    
    elif event == 'Send Values':
        try:
            # Get values from the input fields and convert them to floats
            xH_values = [float(values[f'xH{i}']) for i in ['a', 'b', 'c', 'd']]
            xLR_values = [float(values[f'xLR{i}']) for i in ['a', 'b', 'c', 'd']]
            xFB_values = [float(values[f'xFB{i}']) for i in ['a', 'b', 'c', 'd']]

            # Construct the values_to_send string
            values_to_send = ','.join(map(str, xH_values))
            values_to_send += ',' + ','.join(map(str, xLR_values))
            values_to_send += ',' + ','.join(map(str, xFB_values))

            # Put the values_to_send in the queue
            values_queue.put(values_to_send)
        except ValueError:
            # Handle the case where conversion to float fails (e.g., non-numeric input)
            #print("Error: Input must be numeric")
            pass

window.close()