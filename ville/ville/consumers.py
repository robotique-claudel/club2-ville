from channels.consumer import SyncConsumer
import logging


log = logging.getLogger(__name__)


class objetConsumer(SyncConsumer):

    def websocket_connect(self, event):
        log.info("--NEW CONNECTION--")
        self.send({
            "type": "websocket.accept",
        })

    def websocket_receive(self, event):
        log.info(f"--NEW MESSAGE: {event['text']}--")
        self.send({
            "type": "websocket.send",
            "text": 'event["text"]',
        })

    def websocket_disconnect(self, event):
        log.info("--KILLED CONNECTION--")
        pass
