from serial import Serial
from serial.serialutil import SerialException
from serial.tools.miniterm import Miniterm
import adafruit_board_toolkit.circuitpython_serial



def default():
    ports = adafruit_board_toolkit.circuitpython_serial.repl_comports()
    if not ports:
        return None
    return ports[0].device


def serial_command(args):
    baud = 115200
    using_default = False
    port = args.serial
    if not port:
        using_default = True
        port = default()

    # print help text
    print(r'================================================================================')
    print(f'Connecting to {"DEFAULT" if using_default else "SPECIFIED"} serial device {port} using baud {baud}...')
    print(r'  * ctrl-x: close terminal')
    print(r'  * ctrl-c: enter python repl on device')
    print(r'  * ctrl-d: exit python repl on device and reload')
    print(r'================================================================================')

    # confirm that a port was configured or a default port was found
    if not port:
        print('Failed to find the specified serial port or find a default serial port to use.')
        return

    # create serial port connection
    try:
        serial = Serial(port, baud)
    except SerialException:
        if using_default:
            print(f'Failed to open the default serial port {port}')
        else:
            print(f'Failed to open the configured serial port {port}')
        return

    # start terminal
    miniterm = Miniterm(serial, echo=False, eol='crlf')
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
