from typing import Callable

import customtkinter as ctk

class MenuPrincipal(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTk, switch_frame: Callable[[str], None]):
        """Configura o menu principal da aplicação, com a seleção do protocolo a ser usado."""
        super().__init__(parent)
        self.switch_frame = switch_frame

        # Configuração do Frame
        self.pack(expand=True, fill="both")

        # Configura um painel secundário para os botões
        self.menu_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.menu_frame.pack(expand=True, side="top", anchor="center")

        # Configura os botões de escolha de interface
        self._criar_botoes()

    def _criar_botoes(self):
        """Configura os botões no Menu Principal."""
        self.button_mqtt = ctk.CTkButton(self.menu_frame, text="MQTT", command=lambda: self.switch_frame("menu-mqtt"))
        self.button_mqtt.grid(row=0, columnspan=2, padx=5, pady=10)

        self.button_coap = ctk.CTkButton(self.menu_frame, text="COAP", command=lambda: self.switch_frame("menu-coap"))
        self.button_coap.grid(row=1, columnspan=2, padx=5, pady=10)