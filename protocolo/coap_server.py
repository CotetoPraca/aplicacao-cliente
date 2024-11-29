import asyncio
import aiocoap
from aiocoap import Message, CREATED, POST, Context
from aiocoap.resource import Resource, Site
from collections.abc import Callable
from threading import Event

from mensagem.mensagem import Mensagem
from utils.custom_logger import CustomLogger


class CoapServer(Resource):
    def __init__(self, update_callback:Callable[[str], None]=None):
        """Configurações iniciais do servidor CoAP"""
        super().__init__()
        self._context = None
        self._running_future = None
        self._textbox_update_callback = update_callback
        self.start_event = Event()

    async def start(self) -> None:
        """Configura a incialização do servidor CoAP. Por padrão configura com a URI localhost:5684/coap/cliente."""
        site = Site()
        try:
            site.add_resource(['coap', 'cliente'], self) # Configura para acesso no recurso /coap/cliente
            self._context = await aiocoap.Context.create_server_context(site, bind=('127.0.0.1', 5684))
            CustomLogger.info("Servidor iniciado.")
            self.start_event.set()
            self._running_future = asyncio.get_running_loop().create_future()
            await self._running_future
        except Exception as e:
            CustomLogger.error(f"Falha ao iniciar o servidor CoAP: {e}")

    async def stop(self) -> None:
        """Encerra o servidor CoAP."""
        if self._context:
            await self._context.shutdown()
        if self._running_future:
            self._running_future.set_result(None)
        CustomLogger.info("Servidor encerrado.")

    async def render_post(self, request: aiocoap.Message) -> aiocoap.Message:
        """
        Rendereriza requisições de POST, aciona a função de callback, o que permite o processamento de mensagens
        recebidas, e retorna o ACK informando que a mensagem foi recebida.

        :param request: Mensagem do protocolo CoAP.
        :return: A mensagem ACK com a confirmação do recebimento.
        """
        payload = request.payload.decode()
        CustomLogger.info(f"Mensagem recebida no servidor CoAP: {payload}")

        if self._textbox_update_callback:
            self._textbox_update_callback(payload)

        return Message(code=CREATED, payload=b'Mensagem recebida.', token=request.token)

    @classmethod
    async def post(cls, msg: Mensagem) -> None:
        """Realiza a requisição POST ao servidor CoAP do S3B"""
        msg.adicionar_timestamp_ao_metadata("timestamp_cliente_msg_enviada")
        request = Message(code=POST, uri="coap://localhost:5683/coap/barramento", payload=msg.to_json_string().encode())
        try:
            client_context = await Context.create_client_context()
            response = await client_context.request(request).response
            CustomLogger.info(f"Confirmação de envio recebida: {response}")
        except Exception as e:
            CustomLogger.error(f"Erro ao enviar mensagem: {e}")

    @property
    def get_running_future_loop(self):
        """Auxiliar para identificar a thread em que o CoAP está sendo executado"""
        if self._running_future:
            return self._running_future.get_loop()