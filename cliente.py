from dateutil import parser
import threading
import datetime
import socket 
import time
import random

# Função para iniciar o envio do horário para o servidor
def iniciarEnvioTempo(cliente):
    while True:
        diferenca_tempo = datetime.timedelta(seconds=random.randint(-10, 10))
        tempo_relogio = datetime.datetime.now() + diferenca_tempo
        cliente.send(tempo_relogio.strftime("%H:%M:%S").encode())
        print("Horário a ser ajustado: " + tempo_relogio.strftime("%H:%M:%S")) # Mostra o tempo errado

        print("Horário enviado com sucesso!", end = "\n\n")
        time.sleep(5)

# Função para iniciar o recebimento do horário do servidor
def iniciarRecebimentoTempo(cliente):
    while True:
        tempo_sincronizado = parser.parse(cliente.recv(1024).decode())
        print("Horário sincronizado com sucesso! Agora é: " + tempo_sincronizado.strftime("%H:%M:%S"), end = "\n\n")

# Função para iniciar o cliente
def iniciarCliente(porta = 8080):
    cliente = socket.socket()         
    cliente.connect(('127.0.0.1', porta)) 

    print("Iniciando thread para o envio do horário ao servidor...\n")
    thread_envio_tempo = threading.Thread(target=iniciarEnvioTempo, args=(cliente, ))
    thread_envio_tempo.start()

    print("Iniciando thread para o recebimento do horário sincronizado pelo servidor...\n")
    thread_recebimento_tempo = threading.Thread(target=iniciarRecebimentoTempo, args=(cliente, ))
    thread_recebimento_tempo.start()

if __name__ == '__main__':
    iniciarCliente(porta = 8080)
