import serial
import serial.tools.list_ports


class MotionSerial:
    def __init__(self):
        self.baudrate =  11520
        self.ser = self.__connect_to_first_port()

    def __find_ports(self):
        ports = serial.tools.list_ports.comports()
        port_list = [port.device for port in ports]
        return port_list

    def __connect_to_first_port(self):
        ports = self.__find_ports()
        if not ports:
            return None

        first_port = ports[0]
        print(f"Connecting to the first available port: {first_port}")

        try:
            ser = serial.Serial(first_port, self.baudrate, timeout=1)
            
            return ser
        except serial.SerialException as e:
            print(f"Error: {e}")
            return None

    def send(self, message:str):
        if self.ser == None:
            print('not connected')
            return
        
        self.ser.write(f'{message}\n'.encode())
        print(f"Message sent: {message}")
        response = self.ser.readline().decode("utf-8").strip()
        print(f"Response received: {response}")