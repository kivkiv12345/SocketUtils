"""
Contains definitions and utilities for handling both TCP and UDP
"""

if __name__ == '__main__':
    raise SystemExit(f"Running '{__file__.split('/')[-1]}' directly is unsupported.")

import socket
from typing import Union, Literal
from argparse import ArgumentTypeError

# Define shorthand connection modes
_TCP = socket.SOCK_STREAM
_UDP = socket.SOCK_DGRAM
_MODE_TYPEHINT = Union[Literal[_TCP], Literal[_UDP]]


# DEFAULT VALUES <THESE MAY BE EDITED TO YOUR HEART'S CONTENT>
# MAY BE CHANGED BY COMMAND LINE ARGUMENTS
CONNECTION_PROTOCOL_DEFAULT: _MODE_TYPEHINT     = _TCP


def _get_connection_mode(value: str) -> _MODE_TYPEHINT:
    """ Checks that a valid connection protocol is specified, and returns the corresponding socket type """
    if (_mode := (_valid_modes := {'udp': _UDP, 'tcp': _UDP}).get(value.lower(), ...)) is ...:
        raise ArgumentTypeError(f"'{value}' is not a valid connection mode. Choices are: {tuple(_valid_modes.keys())}.")
    return _mode