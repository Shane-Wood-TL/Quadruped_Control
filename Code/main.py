import PySimpleGUI as sg
import serial

sg.theme('DarkBlue1') 

# Define sub-layouts
header_layout = [
    [sg.Text('Robot Controller')],
]

leg_layout = [
    [sg.Text('', size=(6, 1)), sg.Text('Aleg', size=(6, 1)), sg.Text('Bleg', size=(6, 1)), sg.Text('Cleg', size=(6, 1)), sg.Text('Dleg', size=(6, 1))],
    [sg.Text('xH', size=(6, 1)), sg.InputText(size=(6, 1)), sg.InputText(size=(6, 1)), sg.InputText(size=(6, 1)), sg.InputText(size=(6, 1))],
    [sg.Text('xLR', size=(6, 1)), sg.InputText(size=(6, 1)), sg.InputText(size=(6, 1)), sg.InputText(size=(6, 1)), sg.InputText(size=(6, 1))],
    [sg.Text('xFB', size=(6, 1)), sg.InputText(size=(6, 1)), sg.InputText(size=(6, 1)), sg.InputText(size=(6, 1)), sg.InputText(size=(6, 1))],
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

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    elif event == 'Connect':
        com_port = values['-COM_PORT-']
        telnet_port = values['-TELNET_PORT-']
        # Add code to handle connection with the specified COM and/or TELNET port
        print(f'Connecting to COM Port: {com_port}, TELNET Port: {telnet_port}')
        s = serial.Serial(com_port)
        res = s.read()
        print(res)

window.close()
