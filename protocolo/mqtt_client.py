from typing import Callable

import paho.mqtt.client as mqtt

from mensagem.mensagem import Mensagem
from utils.custom_logger import CustomLogger


class MqttClient:
    def __init__(self):
        """Carrega as configurações para o cliente MQTT"""
        self._broker_host = "localhost"
        self._broker_port = 1883
        self._topico_barramento = "topico/barramento"
        self._client_id = "aplicacao_cliente_mqtt"
        self._client_default_topic = "topico/cliente"

        # Inicializa o cliente MQTT
        self.client = mqtt.Client(client_id=self._client_id, clean_session=True)

        # Configura as funções de callback
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        # Lista de callbacks de mensagem registrados
        self.message_callbacks = []


    def on_connect(self, _client, _userdata, _flags, rc):
        """Informa o status de conexão com o broker MQTT."""
        if rc == 0:
            CustomLogger.info(f"Conectando ao broker {self._broker_host} na porta {self._broker_port}.")
        else:
            CustomLogger.error(f"Falha ao conectar. Código de erro: {rc}")

    def on_message(self, _client, _userdata, msg):
        """Define a lógica de callback para quando receber uma mensagem."""
        payload = msg.payload.decode()
        CustomLogger.info(f"Mensagem recebida no tópico '{msg.topic}': {payload}")

        # Chama todos os callbacks de mensagem registrados passando o payload como parâmetro
        for callback in self.message_callbacks:
            callback(payload)

    def registrar_message_callback(self, callback: Callable[[str], None]):
        """Registra um novo callback para mensagens recebidas."""
        self.message_callbacks.append(callback)

    def connect(self):
        """Conecta o cliente MQTT ao broker e inicia o loop da aplicação MQTT."""
        self.client.connect(self._broker_host, self._broker_port)
        self.client.loop_start()
        self.subscribe(self._client_default_topic)
        CustomLogger.info("Cliente MQTT iniciado e aguardando por mensagens.")

    def disconnect(self):
        """Interrompe o loop da aplicação e encerra a conexão com o broker."""
        self.client.loop_stop()
        self.client.disconnect()
        CustomLogger.info("Cliente MQTT parado e desconectado.")

    def publish(self, message:Mensagem, topico=None):
        """Publica uma mensagem no tópico do barramento por padrão."""
        if topico is None:
            topico = self._topico_barramento

        message.adicionar_timestamp_ao_metadata("timestamp_cliente_msg_enviada")

        message_string = message.to_json_string()
        self.client.publish(topico, message_string)
        CustomLogger.info(f"Mensagem publicada no tópico {topico}: {message_string}")

    def subscribe(self, topic):
        """Se inscreve no tópico especificado do broker MQTT."""
        self.client.subscribe(topic)
        CustomLogger.info(f"Inscrito no tópico '{topic}'")