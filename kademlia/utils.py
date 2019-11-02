"""
General catchall for functions that don't make sense as methods.
"""
import hashlib
import operator
import asyncio
import random


async def gather_dict(dic):
    cors = list(dic.values())
    results = await asyncio.gather(*cors)
    return dict(zip(dic.keys(), results))


def digest(string):
    if not isinstance(string, bytes):
        string = str(string).encode('utf8')
    return hashlib.sha1(string).digest()


def shared_prefix(args):
    """
    Find the shared prefix between the strings.

    For instance:

        sharedPrefix(['blahblah', 'blahwhat'])

    returns 'blah'.
    """
    i = 0
    while i < min(map(len, args)):
        if len(set(map(operator.itemgetter(i), args))) != 1:
            break
        i += 1
    return args[0][:i]


def bytes_to_bit_string(bites):
    bits = [bin(bite)[2:].rjust(8, '0') for bite in bites]
    return "".join(bits)


def generate_node_id(leading_zeros_bits=18):
    while True:
        node_id = digest(bin(random.getrandbits(512))[2:])
        if verify_node_id(node_id, leading_zeros_bits):
            return node_id


def verify_node_id(node_id, leading_zeros_bits=18):
    node_id_hash = digest(node_id)
    return int(bytes_to_bit_string(node_id_hash)[:leading_zeros_bits]) == 0


def solve_puzzle(node_id, leading_zeros_bits=8):
    while True:
        puzzle_proof = digest(bin(random.getrandbits(512))[2:])
        if verify_puzzle(node_id, puzzle_proof, leading_zeros_bits):
            return puzzle_proof


def verify_puzzle(node_id, puzzle_proof, leading_zeros_bits=8):
    node_id_leading_bits = bytes_to_bit_string(node_id)[:leading_zeros_bits]
    puz_leading_bits = bytes_to_bit_string(puzzle_proof)[:leading_zeros_bits]
    for node_id_bit, x_bit in zip(node_id_leading_bits, puz_leading_bits):
        if node_id_bit == x_bit:
            return False
    return True
