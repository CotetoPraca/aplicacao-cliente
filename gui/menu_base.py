import customtkinter as ctk
from utils.custom_logger import CustomLogger
from mensagem.mensagem import Mensagem
from typing import Callable

class MenuBase(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTk, switch_frame: Callable[[str], None], send_message: Callable[[Mensagem], None]):
        super().__init__(parent)
        self.switch_frame = switch_frame
        self.send_message = send_message

        # Variáveis para armazenar o drift de cada par de sistemas
        self.offset_barramento_cliente = 0
        self.offset_barramento_servidor = 0
        self.offset_barramento_embarcado = 0

        # Configuração do Frame
        self.pack(expand=True, fill="both")

        # Configura os frames secundários
        self.fixed_fields_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.fixed_fields_frame.pack(expand=True, side="top", anchor="center")

        self.cadastrar_endpoint_form_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.cadastrar_endpoint_form_frame.pack(expand=True, side="top", anchor="center")

        self.consultar_acao_form_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.consultar_acao_form_frame.pack(expand=True, side="top", anchor="center")

        self.consultar_moeda_form_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.consultar_moeda_form_frame.pack(expand=True, side="top", anchor="center")

        self.consultar_sensor_form_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.consultar_sensor_form_frame.pack(expand=True, side="top", anchor="center")

        self.consultar_status_form_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.consultar_status_form_frame.pack(expand=True, side="top", anchor="center")

        self.consultar_vazao_form_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.consultar_vazao_form_frame.pack(expand=True, side="top", anchor="center")

        self.controle_manual_form_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.controle_manual_form_frame.pack(expand=True, side="top", anchor="center")

        self.iniciar_sistema_form_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.iniciar_sistema_form_frame.pack(expand=True, side="top", anchor="center")

        self.pausar_sistema_form_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.pausar_sistema_form_frame.pack(expand=True, side="top", anchor="center")

        self.parar_todas_valvulas_form_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.parar_todas_valvulas_form_frame.pack(expand=True, side="top", anchor="center")

        self.textbox_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.textbox_frame.pack(expand=True, side="bottom", anchor="s", fill="both")

        self._criar_campos_formulario()
        self._criar_caixa_texto()

        # Botão para voltar ao Menu Principal
        self.back_button = ctk.CTkButton(self, text="Voltar", command=lambda: self.switch_frame("menu-principal"))
        self.back_button.pack(expand=True, side="bottom", anchor="s", padx=25, pady=10)

        # Atualiza a visibilidade dos campos de formulário com base na ação selecionada
        self._update_form_fields(self.combobox_acao.get())

    def _criar_campos_formulario(self):
        """Configura os frames do formulário com seus respectivos campos."""
        # Define a lista de opções do combobox
        opcoes_combox_acao = [
            "CADASTRAR_ENDPOINT", "CONSULTAR_ACAO", "CONSULTAR_MOEDA", "CONSULTAR_SENSOR", "CONSULTAR_STATUS",
            "CONSULTAR_VAZAO", "CONTROLE_MANUAL", "INICIAR_SISTEMA", "PAUSAR_SISTEMA", "PARAR_TODAS_VALVULAS"
        ]
        default_combox_acao = ctk.StringVar(value=opcoes_combox_acao[0])

        # Configuração do Frame dos campos fixos
        self.label_acao = ctk.CTkLabel(self.fixed_fields_frame, text="Ação:")
        self.label_acao.grid(row=0, column=0, padx=5, pady=10, sticky="ew")
        self.combobox_acao = ctk.CTkComboBox(self.fixed_fields_frame, values=opcoes_combox_acao,
                                             variable=default_combox_acao, command=self._update_form_fields)
        self.combobox_acao.grid(row=0, column=1, padx=5, pady=10, sticky="ew")

        self.label_origem = ctk.CTkLabel(self.fixed_fields_frame, text="Origem:")
        self.label_origem.grid(row=1, column=0, padx=5, pady=10, sticky="ew")
        self.entry_origem = ctk.CTkEntry(self.fixed_fields_frame)
        self.entry_origem.grid(row=1, column=1, padx=5, pady=10, sticky="ew")

        self.label_destino = ctk.CTkLabel(self.fixed_fields_frame, text="Destino:")
        self.label_destino.grid(row=2, column=0, padx=5, pady=10, sticky="ew")
        self.entry_destino = ctk.CTkEntry(self.fixed_fields_frame)
        self.entry_destino.grid(row=2, column=1, padx=5, pady=10, sticky="ew")

        # Configuração do Frame do formulário de CADASTRAR_ENDPOINT
        self.send_button = ctk.CTkButton(self.cadastrar_endpoint_form_frame, text="Enviar Mensagem",
                                         command=self._send_message)
        self.send_button.grid(row=0, columnspan=2, padx=5, pady=10, sticky="ew")

        # Configuração do Frame do formulário de CONSULTAR_ACAO
        self.label_simbolo_acao = ctk.CTkLabel(self.consultar_acao_form_frame, text="Símbolo da Ação:")
        self.label_simbolo_acao.grid(row=0, column=0, padx=5, pady=10, sticky="ew")
        self.entry_simbolo_acao = ctk.CTkEntry(self.consultar_acao_form_frame)
        self.entry_simbolo_acao.grid(row=0, column=1, padx=5, pady=10, sticky="ew")

        self.send_button = ctk.CTkButton(self.consultar_acao_form_frame, text="Enviar Mensagem",
                                         command=self._send_message)
        self.send_button.grid(row=1, columnspan=2, padx=5, pady=10, sticky="ew")

        # Configuração do Frame do formulário de CONSULTAR_MOEDA
        self.label_moeda_ref = ctk.CTkLabel(self.consultar_moeda_form_frame, text="Moeda de Referência:")
        self.label_moeda_ref.grid(row=0, column=0, padx=5, pady=10, sticky="ew")
        self.entry_moeda_ref = ctk.CTkEntry(self.consultar_moeda_form_frame)
        self.entry_moeda_ref.grid(row=0, column=1, padx=5, pady=10, sticky="ew")

        self.label_moeda_dest = ctk.CTkLabel(self.consultar_moeda_form_frame, text="Moeda de Destino:")
        self.label_moeda_dest.grid(row=1, column=0, padx=5, pady=10, sticky="ew")
        self.entry_moeda_dest = ctk.CTkEntry(self.consultar_moeda_form_frame)
        self.entry_moeda_dest.grid(row=1, column=1, padx=5, pady=10, sticky="ew")

        self.label_valor_a_converter = ctk.CTkLabel(self.consultar_moeda_form_frame, text="Valor a Converter:")
        self.label_valor_a_converter.grid(row=2, column=0, padx=5, pady=10, sticky="ew")
        self.entry_valor_a_converter = ctk.CTkEntry(self.consultar_moeda_form_frame)
        self.entry_valor_a_converter.grid(row=2, column=1, padx=5, pady=10, sticky="ew")

        self.send_button = ctk.CTkButton(self.consultar_moeda_form_frame, text="Enviar Mensagem",
                                         command=self._send_message)
        self.send_button.grid(row=3, columnspan=2, padx=5, pady=10, sticky="ew")

        # Configuração do Frame do formulário de CONSULTAR_SENSOR
        self.label_sensor = ctk.CTkLabel(self.consultar_sensor_form_frame, text="Sensor:")
        self.label_sensor.grid(row=0, column=0, padx=5, pady=10, sticky="ew")
        self.entry_sensor = ctk.CTkEntry(self.consultar_sensor_form_frame)
        self.entry_sensor.grid(row=0, column=1, padx=5, pady=10, sticky="ew")

        self.label_sensor_data_inicio = ctk.CTkLabel(self.consultar_sensor_form_frame, text="Data de Início (YYYY-MM-DD):")
        self.label_sensor_data_inicio.grid(row=1, column=0, padx=5, pady=10, sticky="ew")
        self.entry_sensor_data_inicio = ctk.CTkEntry(self.consultar_sensor_form_frame)
        self.entry_sensor_data_inicio.grid(row=1, column=1, padx=5, pady=10, sticky="ew")

        self.label_sensor_hora_inicio = ctk.CTkLabel(self.consultar_sensor_form_frame, text="Horário de Início (HH:MM):")
        self.label_sensor_hora_inicio.grid(row=2, column=0, padx=5, pady=10, sticky="ew")
        self.entry_sensor_hora_inicio = ctk.CTkEntry(self.consultar_sensor_form_frame)
        self.entry_sensor_hora_inicio.grid(row=2, column=1, padx=5, pady=10, sticky="ew")

        self.label_sensor_data_fim = ctk.CTkLabel(self.consultar_sensor_form_frame, text="Data de Fim (YYYY-MM-DD):")
        self.label_sensor_data_fim.grid(row=3, column=0, padx=5, pady=10, sticky="ew")
        self.entry_sensor_data_fim = ctk.CTkEntry(self.consultar_sensor_form_frame)
        self.entry_sensor_data_fim.grid(row=3, column=1, padx=5, pady=10, sticky="ew")

        self.label_sensor_hora_fim = ctk.CTkLabel(self.consultar_sensor_form_frame, text="Horário de Fim (HH:MM):")
        self.label_sensor_hora_fim.grid(row=4, column=0, padx=5, pady=10, sticky="ew")
        self.entry_sensor_hora_fim = ctk.CTkEntry(self.consultar_sensor_form_frame)
        self.entry_sensor_hora_fim.grid(row=4, column=1, padx=5, pady=10, sticky="ew")

        self.send_button = ctk.CTkButton(self.consultar_sensor_form_frame, text="Enviar Mensagem",
                                         command=self._send_message)
        self.send_button.grid(row=5, columnspan=2, padx=5, pady=10, sticky="ew")

        # Configuração do Frame do formulário de CONSULTAR_STATUS

        self.send_button = ctk.CTkButton(self.consultar_status_form_frame, text="Enviar Mensagem",
                                         command=self._send_message)
        self.send_button.grid(row=0, columnspan=2, padx=5, pady=10, sticky="ew")

        # Configuração do Frame do formulário de CONSULTAR_VAZAO

        self.label_vazao_data_inicio = ctk.CTkLabel(self.consultar_vazao_form_frame, text="Data de Início (YYYY-MM-DD):")
        self.label_vazao_data_inicio.grid(row=0, column=0, padx=5, pady=10, sticky="ew")
        self.entry_vazao_data_inicio = ctk.CTkEntry(self.consultar_vazao_form_frame)
        self.entry_vazao_data_inicio.grid(row=0, column=1, padx=5, pady=10, sticky="ew")

        self.label_vazao_hora_inicio = ctk.CTkLabel(self.consultar_vazao_form_frame, text="Horário de Início (HH:MM):")
        self.label_vazao_hora_inicio.grid(row=1, column=0, padx=5, pady=10, sticky="ew")
        self.entry_vazao_hora_inicio = ctk.CTkEntry(self.consultar_vazao_form_frame)
        self.entry_vazao_hora_inicio.grid(row=1, column=1, padx=5, pady=10, sticky="ew")

        self.label_vazao_data_fim = ctk.CTkLabel(self.consultar_vazao_form_frame, text="Data de Fim (YYYY-MM-DD):")
        self.label_vazao_data_fim.grid(row=2, column=0, padx=5, pady=10, sticky="ew")
        self.entry_vazao_data_fim = ctk.CTkEntry(self.consultar_vazao_form_frame)
        self.entry_vazao_data_fim.grid(row=2, column=1, padx=5, pady=10, sticky="ew")

        self.label_vazao_hora_fim = ctk.CTkLabel(self.consultar_vazao_form_frame, text="Horário de Fim (HH:MM):")
        self.label_vazao_hora_fim.grid(row=3, column=0, padx=5, pady=10, sticky="ew")
        self.entry_vazao_hora_fim = ctk.CTkEntry(self.consultar_vazao_form_frame)
        self.entry_vazao_hora_fim.grid(row=3, column=1, padx=5, pady=10, sticky="ew")

        self.send_button = ctk.CTkButton(self.consultar_vazao_form_frame, text="Enviar Mensagem",
                                         command=self._send_message)
        self.send_button.grid(row=4, columnspan=2, padx=5, pady=10, sticky="ew")

        # Configuração do Frame do formulário de CONTROLE_MANUAL

        self.label_ponto_irrigacao = ctk.CTkLabel(self.controle_manual_form_frame, text="Pontos de Irrigação:")
        self.label_ponto_irrigacao.grid(row=0, column=0, padx=5, pady=10, sticky="ew")
        self.checkbox_ponto_irrigacao_1 = ctk.CTkCheckBox(self.controle_manual_form_frame, text="1",
                                                          variable=ctk.StringVar(value=""), onvalue="1", offvalue="")
        self.checkbox_ponto_irrigacao_1.grid(row=0, column=1, padx=5, pady=10, sticky="ew")
        self.checkbox_ponto_irrigacao_2 = ctk.CTkCheckBox(self.controle_manual_form_frame, text="2",
                                                          variable=ctk.StringVar(value=""), onvalue="2", offvalue="")
        self.checkbox_ponto_irrigacao_2.grid(row=1, column=1, padx=5, pady=10, sticky="ew")
        self.checkbox_ponto_irrigacao_3 = ctk.CTkCheckBox(self.controle_manual_form_frame, text="3",
                                                          variable=ctk.StringVar(value=""), onvalue="3", offvalue="")
        self.checkbox_ponto_irrigacao_3.grid(row=2, column=1, padx=5, pady=10, sticky="ew")

        self.send_button = ctk.CTkButton(self.controle_manual_form_frame, text="Enviar Mensagem",
                                         command=self._send_message)
        self.send_button.grid(row=3, columnspan=2, padx=5, pady=10, sticky="ew")

        # Configuração do Frame do formulário de INICIAR_SISTEMA

        self.send_button = ctk.CTkButton(self.iniciar_sistema_form_frame, text="Enviar Mensagem",
                                         command=self._send_message)
        self.send_button.grid(row=0, columnspan=2, padx=5, pady=10, sticky="ew")

        # Configuração do Frame do formulário de PAUSAR_SISTEMA

        self.send_button = ctk.CTkButton(self.pausar_sistema_form_frame, text="Enviar Mensagem",
                                         command=self._send_message)
        self.send_button.grid(row=0, columnspan=2, padx=5, pady=10, sticky="ew")

        # Configuração do Frame do formulário de PARAR_TODAS_VALVULAS

        self.send_button = ctk.CTkButton(self.parar_todas_valvulas_form_frame, text="Enviar Mensagem",
                                         command=self._send_message)
        self.send_button.grid(row=0, columnspan=2, padx=5, pady=10, sticky="ew")


    def _criar_caixa_texto(self):
        """Cria a caixa de texto para exibir mensagens"""
        self.textbox = ctk.CTkTextbox(self.textbox_frame)
        self.textbox.pack(expand=True, fill="both", padx=3, pady=10)

    def _update_form_fields(self, acao):
        self.label_destino.grid_forget()
        self.entry_destino.grid_forget()
        self.cadastrar_endpoint_form_frame.pack_forget()
        self.consultar_acao_form_frame.pack_forget()
        self.consultar_moeda_form_frame.pack_forget()
        self.consultar_sensor_form_frame.pack_forget()
        self.consultar_status_form_frame.pack_forget()
        self.consultar_vazao_form_frame.pack_forget()
        self.controle_manual_form_frame.pack_forget()
        self.iniciar_sistema_form_frame.pack_forget()
        self.pausar_sistema_form_frame.pack_forget()
        self.parar_todas_valvulas_form_frame.pack_forget()

        if acao == "CADASTRAR_ENDPOINT":
            self.cadastrar_endpoint_form_frame.pack(expand=True, side="top", anchor="center")
        else:
            self.entry_destino.grid(row=2, column=1, padx=5, pady=10, sticky="ew")
            self.label_destino.grid(row=2, column=0, padx=5, pady=10, sticky="ew")

            if acao == "CONSULTAR_ACAO":
                self.consultar_acao_form_frame.pack(expand=True, side="top", anchor="center")
            elif acao == "CONSULTAR_MOEDA":
                self.consultar_moeda_form_frame.pack(expand=True, side="top", anchor="center")
            elif acao == "CONSULTAR_SENSOR":
                self.consultar_sensor_form_frame.pack(expand=True, side="top", anchor="center")
            elif acao == "CONSULTAR_STATUS":
                self.consultar_status_form_frame.pack(expand=True, side="top", anchor="center")
            elif acao == "CONSULTAR_VAZAO":
                self.consultar_vazao_form_frame.pack(expand=True, side="top", anchor="center")
            elif acao == "CONTROLE_MANUAL":
                self.controle_manual_form_frame.pack(expand=True, side="top", anchor="center")
            elif acao == "INICIAR_SISTEMA":
                self.iniciar_sistema_form_frame.pack(expand=True, side="top", anchor="center")
            elif acao == "PAUSAR_SISTEMA":
                self.pausar_sistema_form_frame.pack(expand=True, side="top", anchor="center")
            elif acao == "PARAR_TODAS_VALVULAS":
                self.parar_todas_valvulas_form_frame.pack(expand=True, side="top", anchor="center")

    def _insert_msg_in_textbox(self, msg: str):
        obj_mensagem = Mensagem.from_json_string(msg)
        obj_mensagem.adicionar_timestamp_ao_metadata("timestamp_cliente_msg_recebida")
        log_mensagem = "Dados recebidos:\n"
        log_mensagem += "\n".join(f"  - {k}: {v}" for k, v in obj_mensagem.conteudo.items() if k != "metadata")
        log_mensagem += "\n"

        if "metadata" in obj_mensagem.conteudo:
            relatorio_latencia = self._gerar_relatorio_latencia(obj_mensagem.conteudo["metadata"], obj_mensagem.origem)
            log_mensagem += "  - Relatório de Latência:\n" + relatorio_latencia
            CustomLogger.info(f"Relatorio de latencias:\n{relatorio_latencia}")

        self.textbox.insert(ctk.END, log_mensagem + "\n\n")

    def _gerar_mensagem_do_form(self) -> Mensagem:
        acao = self.combobox_acao.get()
        origem = self.entry_origem.get()
        destino = self.entry_destino.get()
        conteudo = {}

        if acao is None or origem is None:
            CustomLogger.info("Os campos de ação e origem não podem ser vazios.")
            raise Exception()

        if acao == "CADASTRAR_ENDPOINT":
            destino = ""
        elif acao == "CONSULTAR_ACAO":
            conteudo = { "simboloAcao": self.entry_simbolo_acao.get() }
        elif acao == "CONSULTAR_MOEDA":
            conteudo = {
                "moedaReferencia": self.entry_moeda_ref.get(),
                "moedaDestino": self.entry_moeda_dest.get(),
                "valorAConverter": float(self.entry_valor_a_converter.get())
            }
        elif acao == "CONSULTAR_SENSOR":
            conteudo = {
                "sensor": self.entry_sensor.get(),
                "periodoInicio": f"{self.entry_sensor_data_inicio.get()} {self.entry_sensor_hora_inicio.get()}:00",
                "periodoFim": f"{self.entry_sensor_data_fim.get()} {self.entry_sensor_hora_fim.get()}:00"
            }
        elif acao == "CONSULTAR_STATUS":
            pass
        elif acao == "CONSULTAR_VAZAO":
            conteudo = {
                "periodoInicio": f"{self.entry_vazao_data_inicio.get()} {self.entry_vazao_hora_inicio.get()}:00",
                "periodoFim": f"{self.entry_vazao_data_fim.get()} {self.entry_vazao_hora_fim.get()}:00"
            }
        elif acao == "CONTROLE_MANUAL":
            pontos_de_irrigacao = (f"{self.checkbox_ponto_irrigacao_1.get()}{self.checkbox_ponto_irrigacao_2.get()}"
                                   f"{self.checkbox_ponto_irrigacao_3.get()}")
            conteudo = { "pontos": pontos_de_irrigacao }
        elif acao == "INICIAR_SISTEMA":
            pass
        elif acao == "PAUSAR_SISTEMA":
            pass
        elif acao == "PARAR_TODAS_VALVULAS":
            pass

        mensagem = Mensagem(
            acao=acao,
            origem=origem,
            destino=destino,
            conteudo=conteudo
        )
        return mensagem

    def _send_message(self):
        msg = self._gerar_mensagem_do_form()
        self.send_message(msg)

    def update_text_box(self, message: str):
        self.master.after(0, self._insert_msg_in_textbox, message)

    def _gerar_relatorio_latencia(self, metadata: dict, origem: str) -> str:
        """
        Gera o relatório de latência com base nas medições retornadas no dicionário 'metadata'.
        Os reajustes de timestamp são baseados no nó mais distante no fluxo do mensagem.

        :param metadata: Dicionário com os metadados da mensagem.
        :return: Um string formatada com as latências calculadas
        """
        relatorio = ""
        latencia_total = 0

        cliente_enviou = None
        cliente_recebeu = None
        barramento_enviou_cliente = None
        barramento_enviou_servidor = None
        barramento_enviou_embarcado = None
        barramento_recebeu_cliente = None
        barramento_recebeu_servidor = None
        barramento_recebeu_embarcado = None
        servidor_enviou = None
        servidor_recebeu = None
        embarcado_enviou = None
        embarcado_recebeu = None

        latencia_rtt_cliente = 0
        latencia_rtt_barramento = 0


        if "barramento" in origem:
            cliente_enviou = metadata.get("timestamp_cliente_msg_enviada", 0)
            barramento_recebeu_cliente = metadata.get("timestamp_bus_msg_recebida_cliente", 0)
            barramento_enviou_cliente = metadata.get("timestamp_bus_msg_enviada_cliente", 0)
            cliente_recebeu = metadata.get("timestamp_cliente_msg_recebida", 0)

        if "servidor" in origem:
            cliente_enviou = metadata.get("timestamp_cliente_msg_enviada", 0)
            barramento_recebeu_cliente = metadata.get("timestamp_bus_msg_recebida_cliente", 0)
            barramento_enviou_servidor = metadata.get("timestamp_bus_msg_enviada_servidor", 0)
            servidor_recebeu = metadata.get("timestamp_servidor_msg_recebida", 0)
            servidor_enviou = metadata.get("timestamp_servidor_msg_enviada", 0)
            barramento_recebeu_servidor = metadata.get("timestamp_bus_msg_recebida_servidor", 0)
            barramento_enviou_cliente = metadata.get("timestamp_bus_msg_enviada_cliente", 0)
            cliente_recebeu = metadata.get("timestamp_cliente_msg_recebida", 0)

        if "embarcado" in origem:
            cliente_enviou = metadata.get("timestamp_cliente_msg_enviada", 0)
            barramento_recebeu_cliente = metadata.get("timestamp_bus_msg_recebida_cliente", 0)
            barramento_enviou_embarcado = metadata.get("timestamp_bus_msg_enviada_embarcado", 0)
            embarcado_recebeu = metadata.get("timestamp_embarcado_msg_recebida", 0)
            embarcado_enviou = metadata.get("timestamp_embarcado_msg_enviada", 0)
            barramento_recebeu_embarcado = metadata.get("timestamp_bus_msg_recebida_embarcado", 0)
            barramento_enviou_cliente = metadata.get("timestamp_bus_msg_enviada_cliente", 0)
            cliente_recebeu = metadata.get("timestamp_cliente_msg_recebida", 0)


        # Calcula o RTT (Round Tip Time) supondo latência de envio e recebimento simétricas
        if cliente_recebeu and cliente_enviou:
            rtt_cliente = cliente_recebeu - cliente_enviou
            latencia_rtt_cliente = rtt_cliente / 2

        if barramento_recebeu_servidor and barramento_enviou_servidor:
            rtt_barramento = barramento_recebeu_servidor - barramento_enviou_servidor
            latencia_rtt_barramento = rtt_barramento / 2
        elif barramento_recebeu_embarcado and barramento_enviou_embarcado:
            rtt_barramento = barramento_recebeu_embarcado - barramento_enviou_embarcado
            latencia_rtt_barramento = rtt_barramento / 2

        # Calcula o offset para o barramento e reajusta o timestamp para o nó mais distante (servidor ou embarcado)
        if barramento_enviou_servidor and servidor_recebeu and servidor_enviou and barramento_recebeu_servidor:
            latencia_envio = servidor_recebeu - barramento_enviou_servidor
            latencia_recebimento = barramento_recebeu_servidor - servidor_enviou
            novo_offset_b_s = ((latencia_envio + latencia_recebimento) / 2 ) + latencia_rtt_barramento
            self.offset_barramento_servidor = (0.7 * self.offset_barramento_servidor) + (0.3 * novo_offset_b_s)

            # Reajusta o timestamp do barramento em relação ao relógio do servidor
            barramento_enviou_servidor -= self.offset_barramento_servidor
            barramento_recebeu_servidor -= self.offset_barramento_servidor

        elif barramento_enviou_embarcado and embarcado_recebeu and embarcado_enviou and barramento_recebeu_embarcado:
            latencia_envio = embarcado_recebeu - barramento_enviou_embarcado
            latencia_recebimento = barramento_recebeu_embarcado - embarcado_enviou
            novo_offset_b_e = ((latencia_envio + latencia_recebimento) / 2 ) + latencia_rtt_barramento
            self.offset_barramento_embarcado = (0.7 * self.offset_barramento_embarcado) + (0.3 * novo_offset_b_e)

            # Reajusta o timestamp do barramento em relação ao relógio do embarcado
            barramento_enviou_embarcado -= self.offset_barramento_embarcado
            barramento_recebeu_embarcado -= self.offset_barramento_embarcado

        # Calcula o offset do cliente em relação ao barramento já ajustado
        if cliente_enviou and barramento_recebeu_cliente and barramento_enviou_cliente and cliente_recebeu:
            latencia_envio = barramento_recebeu_cliente - cliente_enviou
            latencia_recebimento = cliente_recebeu - barramento_enviou_cliente
            novo_offset_b_c = ((latencia_envio + latencia_recebimento) / 2 ) + latencia_rtt_cliente
            self.offset_barramento_cliente = (0.7 * self.offset_barramento_cliente) + (0.3 * novo_offset_b_c)

            # Reajusta o timestamp do cliente em relação ao do embarcado
            cliente_enviou -= self.offset_barramento_cliente
            cliente_recebeu -= self.offset_barramento_cliente

        # Cliente -> Barramento
        if cliente_enviou and barramento_recebeu_cliente:
            latencia_cliente_barramento = abs(barramento_recebeu_cliente - cliente_enviou - latencia_rtt_cliente)
            latencia_total += latencia_cliente_barramento
            relatorio += (
                f"    * Cliente enviou a mensagem: {cliente_enviou} (Inicio)\n"
                f"    * Barramento recebeu do cliente: {barramento_recebeu_cliente} "
                f"({latencia_cliente_barramento:.4f} ms / {latencia_total:.4f} ms)\n"
            )

        # Barramento verifica o destino da mensagem
        if barramento_recebeu_cliente:
            if barramento_enviou_servidor:
                latencia_barramento_c_to_s = abs(barramento_enviou_servidor - barramento_recebeu_cliente)
                latencia_total += latencia_barramento_c_to_s
                relatorio += (
                    f"    * Barramento enviou para servidor: {barramento_enviou_servidor} "
                    f"({latencia_barramento_c_to_s:.4f} ms / {latencia_total:.4f} ms)\n"
                )
            elif barramento_enviou_embarcado:
                latencia_barramento_c_to_e = abs(barramento_enviou_embarcado - barramento_recebeu_cliente)
                latencia_total += latencia_barramento_c_to_e
                relatorio += (
                    f"    * Barramento enviou para embarcado: {barramento_enviou_embarcado} "
                    f"({latencia_barramento_c_to_e:.4f} ms / {latencia_total:.4f} ms)\n"
                )

        # Barramento -> Servidor
        if barramento_enviou_servidor and servidor_recebeu:
            latencia_barramento_servidor = abs(servidor_recebeu - barramento_enviou_servidor - latencia_rtt_barramento)
            latencia_total += latencia_barramento_servidor
            relatorio += (
                f"    * Servidor recebeu: {servidor_recebeu} "
                f"({latencia_barramento_servidor:.4f} ms / {latencia_total:.4f} ms)\n"
            )

        # Servidor processa a mensagem
        if servidor_recebeu and servidor_enviou:
            latencia_servidor = abs(servidor_enviou - servidor_recebeu)
            latencia_total += latencia_servidor
            relatorio += (
                f"    * Servidor enviou a resposta: {servidor_enviou} "
                f"({latencia_servidor:.4f} ms / {latencia_total:.4f} ms)\n"
            )

        # Servidor -> Barramento
        if servidor_enviou and barramento_recebeu_servidor:
            latencia_servidor_barramento = abs(barramento_recebeu_servidor - servidor_enviou - latencia_rtt_barramento)
            latencia_total += latencia_servidor_barramento
            relatorio += (
                f"    * Barramento recebeu do servidor: {barramento_recebeu_servidor} "
                f"({latencia_servidor_barramento:.4f} ms / {latencia_total:.4f} ms)\n"
            )

        # Barramento -> Embarcado
        if barramento_enviou_embarcado and embarcado_recebeu:
            latencia_barramento_embarcado = abs(embarcado_recebeu - barramento_enviou_embarcado - latencia_rtt_barramento)
            latencia_total += latencia_barramento_embarcado
            relatorio += (
                f"    * Embarcado recebeu: {embarcado_recebeu} "
                f"({latencia_barramento_embarcado:.4f} ms / {latencia_total:.4f} ms)\n"
            )

        # Embarcado processa a mensagem
        if embarcado_recebeu and embarcado_enviou:
            latencia_embarcado = abs(embarcado_enviou - embarcado_recebeu)
            latencia_total += latencia_embarcado
            relatorio += (
                f"    * Embarcado enviou a resposta: {embarcado_enviou} "
                f"({latencia_embarcado:.4f} ms / {latencia_total:.4f} ms)\n"
            )

        # Embarcado -> Barramento
        if barramento_enviou_embarcado and barramento_recebeu_embarcado:
            latencia_embarcado_barramento = abs(barramento_recebeu_embarcado - barramento_enviou_embarcado)
            latencia_total += latencia_embarcado_barramento
            relatorio += (
                f"    * Barramento recebeu do embarcado: {barramento_recebeu_embarcado} "
                f"({latencia_embarcado_barramento:.4f} ms / {latencia_total:.4f} ms)\n"
            )

        # Barramento verifica o destino da mensagem
        if barramento_enviou_cliente:
            if barramento_recebeu_servidor:
                latencia_barramento_s_to_c = abs(barramento_recebeu_servidor - barramento_enviou_cliente)
                latencia_total += latencia_barramento_s_to_c
                relatorio += (
                    f"    * Barramento enviou para cliente: {barramento_enviou_cliente} "
                    f"({latencia_barramento_s_to_c:.4f} ms / {latencia_total:.4f} ms)\n"
                )

            if barramento_recebeu_embarcado:
                latencia_barramento_e_to_c = abs(barramento_enviou_cliente - barramento_recebeu_embarcado)
                latencia_total += latencia_barramento_e_to_c
                relatorio += (
                    f"    * Barramento enviou para cliente: {barramento_enviou_cliente} "
                    f"({latencia_barramento_e_to_c:.4f} ms / {latencia_total:.4f} ms)\n"
                )

        # Barramento -> Cliente
        if barramento_enviou_cliente and cliente_recebeu:
            latencia_barramento_cliente = abs(cliente_recebeu - barramento_enviou_cliente - latencia_rtt_cliente)
            latencia_total += latencia_barramento_cliente
            relatorio += (
                f"    * Cliente recebeu: {cliente_recebeu} "
                f"({latencia_barramento_cliente:.4f} ms / {latencia_total:.4f} ms)\n"
            )

        return relatorio
