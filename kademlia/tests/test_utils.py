import hashlib

from unittest.mock import patch

from kademlia.utils import (
    digest,
    generate_node_id,
    shared_prefix,
    solve_puzzle,
    verify_node_id,
    verify_puzzle
)


class TestUtils:
    def test_digest(self):  # pylint: disable=no-self-use
        dig = hashlib.sha1(b'1').digest()
        assert dig == digest(1)

        dig = hashlib.sha1(b'another').digest()
        assert dig == digest('another')

    def test_shared_prefix(self):   # pylint: disable=no-self-use
        args = ['prefix', 'prefixasdf', 'prefix', 'prefixxxx']
        assert shared_prefix(args) == 'prefix'

        args = ['p', 'prefixasdf', 'prefix', 'prefixxxx']
        assert shared_prefix(args) == 'p'

        args = ['one', 'two']
        assert shared_prefix(args) == ''

        args = ['hi']
        assert shared_prefix(args) == 'hi'

    def test_verify_node_id(self):    # pylint: disable=no-self-use
        node_id = bytes.fromhex("f4ba15294077f7033ee8edbc54c5280d35019c82")
        assert verify_node_id(node_id)

        node_id = bytes.fromhex("DEADC0DEDEADC0DEDEADC0DEDEADC0DEDEADC0DE")
        assert verify_node_id(node_id) is False

    def test_generate_node_id(self):    # pylint: disable=no-self-use
        with patch('random.getrandbits',
                   return_value=int("11946451409567480126214625534900978266"
                                    "39567331428301278103177554687013975494"
                                    "49335820030285091194959007423923262718"
                                    "94968214328375482197437381293055281613"
                                    "065")):
            node_id = generate_node_id()
            assert verify_node_id(node_id)

    def test_verify_puzzle(self):    # pylint: disable=no-self-use
        node_id_hex = "12b1e8b6576404516e03143acf433bb9eaf27d08"
        puzzle_hex = "ed595a9f3e067e29626f13a7a0e3424f82d37580"
        assert verify_puzzle(bytes.fromhex(node_id_hex),
                             bytes.fromhex(puzzle_hex))

        puzzle_hex = "DEADC0DEDEADC0DEDEADC0DEDEADC0DEDEADC0DE"
        assert verify_puzzle(bytes.fromhex(node_id_hex),
                             bytes.fromhex(puzzle_hex)) is False

    def test_solve_puzzle(self):    # pylint: disable=no-self-use
        node_id_hex = "12b1e8b6576404516e03143acf433bb9eaf27d08"
        node_id = bytearray.fromhex(node_id_hex)
        with patch('random.getrandbits',
                   return_value=int("9750485504566489265936722583615151170"
                                    "1791131733568188840813358324422814262"
                                    "9224269344346952924643344838739340732"
                                    "0827762023737582427771044272673777528"
                                    "741287")):
            puzzle = solve_puzzle(node_id)
            assert verify_puzzle(node_id, puzzle)
