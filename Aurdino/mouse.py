import serial
import pyautogui
from pynput.mouse import Controller,Button
pyautogui.FAILSAFE = False
# Replace with your Bluetooth device's COM port
port = 'COM5'  # On Wi ndows
# port = '/dev/rfcomm0'  # On Linux
joystick_x_min = 0
joystick_x_max = 1023
joystick_y_min = 0
joystick_y_max = 1023
screen_width, screen_height = pyautogui.size()
sensitivity = 100
threshold = 50
# Configure the serial connection
ser = serial.Serial(port, 9600)  # Change the baud rate to match your HC-05 configuration
mouse = Controller()
X_OFFSET = 0.0
Y_OFFSET = 0.0
Z_THRESHOLD = 0.0  # Adjust this threshold based on your application
SENSITIVITY = 10.0
esc= False
try:
    while True:
        print("lll")
        data = ser.readline().decode('utf-8').strip()
        if True:
            print(data)
            values = data.split()
            if len(values) >= 2:
                x_value = int(values[0])
                y_value = int(values[1])
                b1 = int(values[2])
                b2 = int(values[3])
                b3 = int(values[4])
                b4=int(values[5])
                b5=int(values[6])
                b6 =int(values[7])
                b7= int(values[8])
                b8 = int(values[9])

                # ax, ay, az, gx, gy, gz = int(values[5]),int(values[6]),int(values[7]),int(values[8]),int(values[9]),int(values[10])
                # # Adjust the following lines to map sensor data to mouse movement
                # dx = gx / 1000  # Adjust the scaling factor
                # dy = gy / 1000  # Adjust the scaling factor
                # pyautogui.moveRel(dx, dy)

                # Define a sensitivity factor to control mouse movement
                              # Adjust this value to control sensitivity (0.5 is an example)

                # Map joystick values to mouse cursor movement with sensitivity adjustment
                x_position = int(
                    ((x_value - joystick_x_min) / (joystick_x_max - joystick_x_min) * screen_width) * sensitivity)
                y_position = int(
                    ((y_value - joystick_y_min) / (joystick_y_max - joystick_y_min) * screen_height) * sensitivity)
                x_joystick = x_value
                y_joystick = y_value

                if abs(x_joystick - 510) > threshold:
                    if x_joystick > 510:
                        pyautogui.press('right')
                    else:
                        pyautogui.press('left')

                if abs(y_joystick - 513) > threshold:
                    if y_joystick > 513:
                        pyautogui.press('down')
                    else:
                        pyautogui.press('up')
                # Move the mouse cursor
                # pyautogui.moveTo(x_position, y_position)
                # mouse.position = (x_position, y_position)
                if b1==1:
                    if esc==False:
                        pyautogui.press('f5')
                        esc=True
                    else:
                        pyautogui.press('esc')
                        esc = False


                if b2 == 1:
                    mouse.click(Button.right, 1)
                if b3 == 1:
                    mouse.click(Button.left, 1)
                if b4 == 1:
                    pyautogui.press('enter')
                if b5 == 1:
                    pyautogui.press('tab')
                if b6 == 1:
                    pyautogui.hotkey('win', 'd')
                if b7== 1:
                    pyautogui.hotkey('ctrl', 'tab')
                if b8 == 1:
                    pyautogui.hotkey('win', 'tab')

        print(data)
except KeyboardInterrupt:
    ser.close()
except pyautogui.FailSafeException:
    # Handle fail-safe exception (e.g., exit the script)
    print("PyAutoGUI fail-safe triggered. Exiting script.")
except Exception as e:
    # Handle other exceptions
    print(f"An error occurred: {e}")
finally:
    # Close the serial connection
    ser.close()
# Close the serial connection when done
