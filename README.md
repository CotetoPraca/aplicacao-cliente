# Aplicação Cliente (S3B)

Aplicação cliente usada para testar as funcionalidades do Small Scale Service Bus (S3B)

Esse projeto utiliza os pacotes:

- aiocoap: para configurar o protocolo CoAP
- paho-mqtt: para configurar o protocolo MQTT
- customertkinter: apenas para personalização da interface

Ao iniciar o cliente se conecta ao broker MQTT do S3B, portanto ele deve ser executado
após a inicialização do barramento para funcionar corretamente. Sua inicialização é
feita a partir da classe `App` no arquivo `app.py`.

Se a aplicação de destino usar um protocolo diferente do configurado no cliente,
é preciso que a aplicação de destino envie uma mensagem com ação `CADASTRAR_ENDPOINT`
ao S3B usando o protocolo que deseja cadastrar como padrão para comunicações futuras.

O mesmo para atualizar o protocolo de algum endereço. Quando o S3B recebe uma
mensagem de um novo endereço, ele automaticamente armazena o protocolo usado como
a preferência para comunicações futuras. Para alterar essa configuração, basta
enviar o `CADASTRAR_ENDPOINT` usando o novo endereço e protocolo.