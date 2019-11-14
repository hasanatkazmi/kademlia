import asyncio
from contextlib import contextmanager

import pytest

from kademlia.network import Server
from kademlia.protocol import KademliaProtocol


@contextmanager
def server_context(server):
    try:
        yield server
    finally:
        server.stop()


@pytest.mark.asyncio
async def test_storing(bootstrap_node):
    with server_context(Server()) as server:
        await server.listen(bootstrap_node[1] + 1)
        await server.bootstrap([bootstrap_node])
        await server.set('key', 'value')
        result = await server.get('key')
        assert result == 'value'


class TestSwappableProtocol:

    def test_default_protocol(self):  # pylint: disable=no-self-use
        """
        An ordinary Server object will initially not have a protocol, but will
        have a KademliaProtocol object as its protocol after its listen()
        method is called.
        """
        loop = asyncio.get_event_loop()
        with server_context(Server()) as server:
            assert server.protocol is None
            loop.run_until_complete(server.listen(8469))
            assert isinstance(server.protocol, KademliaProtocol)

    def test_custom_protocol(self):  # pylint: disable=no-self-use
        """
        A subclass of Server which overrides the protocol_class attribute will
        have an instance of that class as its protocol after its listen()
        method is called.
        """

        # Make a custom Protocol and Server to go with hit.
        class CoconutProtocol(KademliaProtocol):
            pass

        class HuskServer(Server):
            protocol_class = CoconutProtocol

        # An ordinary server does NOT have a CoconutProtocol as its protocol...
        loop = asyncio.get_event_loop()
        with server_context(Server()) as server:
            loop.run_until_complete(server.listen(8469))
            assert not isinstance(server.protocol, CoconutProtocol)

        # ...but our custom server does.
        with server_context(HuskServer()) as husk_server:
            loop.run_until_complete(husk_server.listen(8469))
            assert isinstance(husk_server.protocol, CoconutProtocol)
