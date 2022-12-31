import json
import time
import asyncio
import websockets
import logging
from config import *

log = logging.getLogger(__name__)


class WebSocketClass(object):

    def __init__(self, endpoint, api_key, secret_key):
        """
        :return:
        """
        self._endpoint = endpoint
        self._api_key = api_key
        self._secret_key = secret_key
        self._ws = None
        self._running = False
        self._name = 'WebSocketClass'
        self.send_msg_list: list[dict] = []

    @property
    def ws(self):
        return self._ws

    async def _connect(self):
        """
        connect
        :return:
        """
        self._ws = await websockets.connect(self._endpoint)

    async def _start_ws(self):
        """

        :return:
        """
        await self._connect()

    async def _send(self, msg):
        """

        :param msg:
        :return:
        """
        await self._ws.send(json.dumps(msg))

    async def _consume(self):
        while True:
            try:
                if self.send_msg_list:
                    for msg in self.send_msg_list:
                        await self._ws.send(json.dumps(msg))
                    self.send_msg_list = []
                r = await asyncio.wait_for(self._ws.recv(), 5)
                data = json.loads(r).get('data')
                if not data:
                    continue
                data_Q.put(data)
            except asyncio.TimeoutError:
                # ws.recv is hanging when no data is received. by using
                # wait_for we break when no data is received, allowing us
                # to break the loop when needed
                pass

    async def _run_forever(self):
        self._loop = asyncio.get_running_loop()
        # do not start the websocket connection until we subscribe to something
        self._should_run = True
        self._running = False
        while True:
            try:
                if not self._should_run:
                    # when signaling to stop, this is how we break run_forever
                    log.info("{} stream stopped".format(self._name))
                    return
                if not self._running:
                    log.info("starting {} websocket connection".format(
                        self._name))
                    await self._start_ws()
                    self._running = True
                await self._consume()
            except websockets.WebSocketException as wse:
                await self.close()
                self._running = False
                log.warning('data websocket error, restarting connection: ' +
                            str(wse))
            except Exception as e:
                log.exception('error during websocket '
                              'communication: {}'.format(str(e)))
            finally:
                await asyncio.sleep(0.01)

    async def close(self):
        if self._ws:
            await self._ws.close()
            self._ws = None
            self._running = False

    def run(self):
        try:
            asyncio.run(self._run_forever())
        except KeyboardInterrupt:
            print('keyboard interrupt, bye')
            pass


class PrivateChannel(object):
    """
    私有频道
    """
    def login_okx(self):
        """

        :return:
        """
        pass

    def subscribe(self):
        """
        频道订阅
        :return:
        """
        pass

    def unsubscribe(self):
        """
        取消订阅
        :return:
        """


class PublicChannel(WebSocketClass):

    def __init__(self, endpoint, api_key, secret_key):
        super().__init__(endpoint=endpoint, api_key=api_key, secret_key=secret_key)

    def instruments(self, option='subscribe', channel='instruments', inst_type='SWAP'):
        """
        产品频道
        :return:
        """
        request_dict = {
            "op": option,
            "args": [{
                "channel": channel,
                "instType": inst_type
            }]
        }
        self.send_msg_list.append(request_dict)

    def tickers(self, option='subscribe'):
        """
        行情频道
        :return:
        """
        request_dict = {
            "op": option,
            "args": [{
                "channel": "candle1m",
                "instId": "GMT-USDT-SWAP"
            }]
        }
        self.send_msg_list.append(request_dict)

    def open_interest(self):
        """
        持仓总量频道
        :return:
        """
        pass

    def candle(self, option, channel, inst_id):
        """
        K线数据频道
        {
            "op": "subscribe",
            "args": [{
                "channel": "candle1D",
                "instId": "BTC-USDT"
            }]
        }
        :return:
        """
        request_dict = {
            "op": option,
            "args": [{
                "channel": channel,
                "instId": inst_id
            }]
        }
        self.send_msg_list.append(request_dict)


if __name__ == '__main__':
    pub_ws = PublicChannel(OkxPublicTopic, apikey, secretkey)
    pub_ws.tickers()
    pub_ws.run()
    # asyncio.run(pub_ws.start_ws())
    # op = "subscribe"
    # channel = "candle1D"
    # instId = "BTC-USDT"
    # res = pub_ws.candle(op, channel, instId)
    # print(res)
    # asyncio.run(test())
    # asyncio.run(test())



