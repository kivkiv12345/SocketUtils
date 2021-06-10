"""
This module allows the user to send arbitrary data to the specified destination.
Accepts a variety of different command line arguments.
"""

import socket, argparse

parser = argparse.ArgumentParser(description='Sends arbitrary data to the specified destination.')

# DEFAULT VALUES <THESE MAY BE EDITED TO YOUR HEART'S CONTENT>
PORT_DEFAULT:           int     = 9355
DESTINATION_DEFAULT:    str     = socket.gethostname()
ENCODE_DEFAULT:         str     = 'utf-8'

parser.add_argument('-p', '--port', type=int, metavar='', default=PORT_DEFAULT,
                    help=f"Which port to send to, defaults to {PORT_DEFAULT}")
parser.add_argument('-d', '--destination', type=str, metavar='', default=DESTINATION_DEFAULT,
                    help=f"The IP address of destination. Defaults to {DESTINATION_DEFAULT}")
parser.add_argument('-m', '--message', type=str, metavar='', required=True,  # TODO Kevin: It should be possible to pipe the message from a file (see: sys.stdin).
                    help='Message to send to the specified destination')
parser.add_argument('-e', '--encode', type=lambda value: None if value.lower() in {'none', ''} else value, default=ENCODE_DEFAULT, metavar='',
                    help=f"Determines how the message should be encoded. Defaults to '{ENCODE_DEFAULT}'. May be disabled with: '-e none'")

args = parser.parse_args()

try:
    # This provides PyCharm with autocomplete suggestions.
    # It does, however, raise an unexceptable SyntaxError when running python < 3.
    args.port: int
    args.destination: str
    args.message: str
    args.encode: str
except SyntaxError:
    pass  # In such situation, it's necessary to remove this code.


def main():
    # TODO Kevin: Check out socket.sendfile()
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        _message = (args.message.encode(args.encode) if args.encode else args.message)
        client_socket.sendto(_message, (socket.gethostname(), args.port))


if __name__ == '__main__':
    main()
