#!/usr/bin/python3
"""
This module pipes contents to and from a UDP socket connections.
Ex: logging received data to a text file.
Accepts a variety of different command line arguments.
"""

import socket, argparse
from os import path
from typing import Union
from protocol_handling import _UDP, _TCP, _MODE_TYPEHINT, _get_connection_mode, CONNECTION_PROTOCOL_DEFAULT


parser = argparse.ArgumentParser(description='Receives arbitrary data on the specified port,'
                                             ' and pipes it to a specified location.')


# DEFAULT VALUES <THESE MAY BE EDITED TO YOUR HEART'S CONTENT>
# MAY BE CHANGED BY COMMAND LINE ARGUMENTS
PORT_DEFAULT:           int                     = 9355
CREATE_FILE_DEFAULT:    bool                    = False
BUFFER_SIZE_DEFAULT:    int                     = 4096
DECODE_DEFAULT:      Union[str, None]           = 'utf-8'
TIMEOUT_DEFAULT:     Union[float, int, None]    = 60


# Specify the arguments that the program may receive
parser.add_argument('-p', '--port', type=int, metavar='', default=PORT_DEFAULT,
                    help=f"Which port to listen on. Defaults to {PORT_DEFAULT}")
parser.add_argument('-d', '--destination', type=str, metavar='', default=None,
                    help='Specified file to pipe received data to, default STDOUT')
parser.add_argument('-c', '--connect_mode', type=_get_connection_mode, metavar='', default=CONNECTION_PROTOCOL_DEFAULT,
                    help="Whether to use TCP or UDP when sending and receiving packages. Defaults to 'tcp'. Accepts either 'udp' or 'tcp'")
parser.add_argument('-f', '--create_file', default=CREATE_FILE_DEFAULT, action='store_true',
                    help=f"Whether to create an absent destination file. Default to {CREATE_FILE_DEFAULT}")
parser.add_argument('-b', '--buffer_size', type=int, default=BUFFER_SIZE_DEFAULT, metavar='',
                    help=f"Sets the buffer size for the socket. Defaults to {BUFFER_SIZE_DEFAULT}")
parser.add_argument('-D', '--decode', type=lambda value: None if value.lower() in {'none', ''} else value, default=DECODE_DEFAULT, metavar='',
                    help=f"Determines how the message should be decoded. Defaults to '{DECODE_DEFAULT}'. May be disabled with: '-D none'")
parser.add_argument('-t', '--timeout', type=lambda value: None if value.lower() in {'none', ''} else float(value), default=TIMEOUT_DEFAULT, metavar='',
                    help=f"Determines how long to listen without receiving data. Defaults to '{TIMEOUT_DEFAULT}'. Provided in seconds")
# TODO Kevin: argparse provides poor feedback for incorrect values to the lambda functions above.

args = parser.parse_args()

# try:
#     # This provides PyCharm with autocomplete suggestions.
#     # It does, however, raise an unexceptable SyntaxError when running python < 3.
#     args.port: int
#     args.destination: str
#     args.connect_mode: _MODE_TYPEHINT
#     args.create_file: bool
#     args.buffer_size: int
#     args.decode: Union[str, None]
#     args.timeout: Union[float, int, None]
# except SyntaxError:
#     pass  # In such situations, it's necessary to remove this code.


def _write_to_file(data):

    if args.destination is None:
        return

    with open(args.destination, mode='a+') as file:
        file.write((data.decode(args.decode) if args.decode else data) + '\n')


def main():

    # Check that the file exists (if need be), before we wait for a response.
    if args.destination is not None and not args.create_file and not path.isfile(args.destination):
        raise SystemExit(f"Specified destination <'{args.destination}'> does not exist.")

    with socket.socket(socket.AF_INET, args.connect_mode) as sock:  # socket.AF_INET = ipv4 | socket.SOCK_DGRAM = UDP

        if args.timeout:  # Only set a timeout, if it is not None or 0.
            sock.settimeout(args.timeout)

        sock.bind((socket.gethostname(), args.port))

        while True:  # Continue to receive data, until the user stops the program, or the socket times out.

            if args.connect_mode is _TCP:
                sock.listen(1)
                conn, addr = sock.accept()
                with conn:
                    print('Connected by', addr)
                    while True:
                        data = conn.recv(args.buffer_size)
                        if not data: break
                        print(data)
                        _write_to_file(data)

            elif args.connect_mode is _UDP:
                data, addr = sock.recvfrom(args.buffer_size)
                # TODO Kevin: Add the ability to send the data to a remote destination.
                print(data)
                _write_to_file(data)


if __name__ == '__main__':
    main()
