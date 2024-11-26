from datetime import datetime

import customtkinter as ctk

from gui.menu_base import MenuBase
from typing import Callable

from mensagem.mensagem import Mensagem


class MenuCoap(MenuBase):
    def __init__(self, parent: ctk.CTk, switch_frame: Callable[[str], None], send_message: Callable[[Mensagem], None]):
        super().__init__(parent, switch_frame, send_message)
        self._inicializa_campos_teste()

    def _inicializa_campos_teste(self):
        """Insere valores iniciais nos campos de entrada para testes."""
        self.entry_origem.insert(0, "192.168.0.8:5684/coap/cliente")
        self.entry_destino.insert(0, "192.168.0.8:5682/coap/servidor")
        self.entry_simbolo_acao.insert(0, "IBM")
        self.entry_moeda_ref.insert(0, "CAD")
        self.entry_moeda_dest.insert(0, "BRL")
        self.entry_valor_a_converter.insert(0, "1")
        self.entry_sensor.insert(0, "umidade1")


