from serial import Serial
from serial.tools import list_ports
from serial.tools.miniterm import Miniterm
from piku.core import config


def default():
    return list_ports.comports()[0].device

def serial_command(args):
    port = 115200
    device = config.get('system', 'serial') or default()

    # print help text
    print(r'================================================================================')
    print(f'Connecting to serial device ${device} on port ${port}...')
    print(r'  * ctrl-x: close terminal')
    print(r'  * ctrl-c: enter python repl on device')
    print(r'  * ctrl-d: exit python repl on device and reload')
    print(r'================================================================================')

    # connect to serial
    serial_instance = Serial(device, port)

    # start terminal
    miniterm = Miniterm(serial_instance, echo=False, eol='crlf')
    miniterm.exit_character = chr(0x18)  # GS/CTRL+])
    miniterm.menu_character = chr(0x14)  # Menu: CTRL+T
    miniterm.raw = False
    miniterm.set_rx_encoding('UTF-8')
    miniterm.set_tx_encoding('UTF-8')
    miniterm.start()

    # wait for terminal exit
    try:
        miniterm.join(True)
    except KeyboardInterrupt:
        pass
    miniterm.join()
    miniterm.close()
