import json
import time


class Mensagem:
    def __init__(self, acao: str, origem: str, destino: str, conteudo: dict):
        """Define os campos esperados de uma mensagem"""
        self.acao = acao
        self.origem = origem
        self.destino = destino
        self.conteudo = conteudo

    def to_json_string(self) -> str:
        """Converte os dados do objeto em uma string json"""
        json_str = {
            "acao": self.acao,
            "origem": self.origem,
            "destino": self.destino,
            "conteudo": self.conteudo
        }
        return json.dumps(json_str)

    @classmethod
    def from_json_string(cls, json_str: str):
        """Converte uma string json em um objeto Mensagem"""
        json_obj = json.loads(json_str)
        return cls(
            acao=json_obj["acao"],
            origem=json_obj["origem"],
            destino=json_obj["destino"],
            conteudo=json_obj["conteudo"]
        )

    def adicionar_timestamp_ao_metadata(self, campo: str):
        """Adiciona um timestamp ao campo 'metadata' dentro do conteúdo da mensagem."""
        metadata = self.conteudo.get("metadata", {})
        metadata[campo] = int(time.time() * 1000)
        self.conteudo["metadata"] = metadata
