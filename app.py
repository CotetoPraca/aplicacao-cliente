import asyncio
import sys
from threading import Thread, Event

from mensagem.mensagem import Mensagem
from protocolo.coap_server import CoapServer
from utils.custom_logger import CustomLogger
from gui.menu_coap import MenuCoap
from gui.menu_mqtt import MenuMqtt
from gui.menu_principal import MenuPrincipal
from protocolo.mqtt_client import MqttClient

try:
    import customtkinter as ctk
except ImportError:
    import tkinter as ctk

class App:
    def __init__(self, parent: ctk.CTk):
        # Configurações da janela
        self.master = parent
        self.master.title("Aplicação Cliente")
        self.master.geometry("300x600")
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

        # Inicializa os frames dos menus
        menu_principal = MenuPrincipal(parent=self.master, switch_frame=self.mudar_frame)
        menu_coap = MenuCoap(parent=self.master, switch_frame=self.mudar_frame, send_message=self._send_coap_message)
        menu_mqtt = MenuMqtt(parent=self.master, switch_frame=self.mudar_frame, send_message=self._send_mqtt_message)

        # Oculta todos os frames inicialmente
        menu_principal.pack_forget()
        menu_coap.pack_forget()
        menu_mqtt.pack_forget()

        self.frames = {
            "menu-principal": menu_principal,
            "menu-mqtt": menu_mqtt,
            "menu-coap": menu_coap
        }

        # Configurações para o servidor Coap
        self.coap_thread = None
        self.coap_loop = None
        self.stop_thread_event = Event()
        self.coap_server = CoapServer(menu_coap.update_text_box)
        self._start_coap_server()

        # Configurações para o servidor MQTT
        self.mqtt_client = MqttClient()
        self.mqtt_client.registrar_message_callback(menu_mqtt.update_text_box)
        self.mqtt_client.connect()

        self.frame_atual = None
        self.mudar_frame("menu-principal")

    def mudar_frame(self, frame_id: str):
        if self.frame_atual is not None:
            self.frame_atual.pack_forget()

        # Atualiza o título e o tamanho da janela conforme o frame
        match frame_id:
            case "menu-principal":
                self.master.title("Aplicação Cliente - Menu")
                self.master.geometry("320x100")
            case "menu-coap":
                self.master.title("Aplicação Cliente - CoAP")
                self.master.geometry("400x700")
            case "menu-mqtt":
                self.master.title("Aplicação Cliente - MQTT")
                self.master.geometry("400x700")

        self.frame_atual = self.frames[frame_id]
        self.frame_atual.pack(expand=True, fill="both")

    def _send_mqtt_message(self, msg: Mensagem):
        self.mqtt_client.publish(msg, "topico/barramento")

    def _send_coap_message(self, msg: Mensagem):
        try:
            CustomLogger.info(f"Enviando mensagem: {msg.to_json_string()}")
            if msg and self.coap_thread and self.coap_thread.is_alive():
                asyncio.run_coroutine_threadsafe(self.coap_server.post(msg), self.coap_server.get_running_future_loop)
        except Exception as e:
            CustomLogger.error(f"Erro ao enviar mensagem: {e}")

    def _start_coap_server(self):
        # Verifica se já existe uma thread do servidor em execução
        if not self.coap_thread or not self.coap_thread.is_alive():
            CustomLogger.info("Iniciando uma nova thread do servidor COAP...")
            self.coap_thread = Thread(target=self._run_coap_server, daemon=True)
            self.coap_thread.start()
            self.coap_server.start_event.wait()
        else:
            CustomLogger.info("A thread do servidor COAP já está em execução.")

    def _run_coap_server(self):
        self.coap_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.coap_loop)
        self.coap_loop.run_until_complete(self.coap_server.start())
        self.coap_loop.run_forever()

    def _stop_coap_server(self):
        if self.coap_loop:
            future = asyncio.run_coroutine_threadsafe(self.coap_server.stop(), self.coap_loop)
            future.result()

            # Interrompe o loop do asyncio e aguarda tarefas pendentes
            self.coap_loop.call_soon_threadsafe(self.coap_loop.stop)

            # Aguarda a finalização das tarefas pendentes
            for task in asyncio.all_tasks(self.coap_loop):
                task.cancel()

            check_for_infinite_loop = 0
            while self.coap_thread.is_alive():
                CustomLogger.warning(f"Aguardando Thread do servidor encerrar... ({check_for_infinite_loop+1}/5)")
                self.coap_thread.join(timeout=3)
                check_for_infinite_loop += 1
                if check_for_infinite_loop > 4:
                    CustomLogger.critical("Possível loop infinito detectado. Tentando forçar encerramento...")
                    self.master.destroy()
                    sys.exit(-1)

            CustomLogger.info("Thread do servidor encerrada.")
            self.coap_loop = None # Limpa a referência para evitar o uso indevido

    def on_close(self):
        CustomLogger.info("Encerrando a aplicação...")

        # Desconecta o cliente MQTT
        self.mqtt_client.disconnect()

        # Desconecta o servidor CoAP
        self._stop_coap_server()
        if self.coap_thread:
            self.coap_thread.join()

        # Encerra a interface do TKinter
        self.master.destroy()

        CustomLogger.info("Aplicação encerrada.")

if __name__ == "__main__":
    try:
        root = ctk.CTk()
        app = App(root)
        root.mainloop()
    except KeyboardInterrupt:
        CustomLogger.warning("Aplicação interrompida.")