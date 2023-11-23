from dateutil import parser
import threading
import datetime
import socket
import time

dados_cliente = {} # Dados do cliente

# Função para iniciar o recebimento do horário do relógio
def iniciarRecebimentoTempoRelogio(conector, endereco):
    while True:
        string_tempo_relogio = conector.recv(1024).decode()
        tempo_relogio = parser.parse(string_tempo_relogio)
        diferenca_tempo_relogio = datetime.datetime.now() - tempo_relogio

        dados_cliente[endereco] = {
            "tempo_relogio"     : tempo_relogio,
            "diferenca_tempo": diferenca_tempo_relogio,
            "conector"      : conector
        }

        print("Dados atualizados no cliente "+ str(endereco), end = "\n\n")
        time.sleep(5)

# Função para iniciar a conexão com os clientes
def iniciarConexao(servidor_mestre):
    contador_cliente = 0
    while contador_cliente < 4:
        conector_mestre_cliente, addr = servidor_mestre.accept()
        endereco_cliente = str(addr[0]) + ":" + str(addr[1])

        print(endereco_cliente + " conectado com sucesso!")

        thread_atual = threading.Thread(target=iniciarRecebimentoTempoRelogio, args=(conector_mestre_cliente, endereco_cliente, ))
        thread_atual.start()

        contador_cliente += 1

# Função para calcular a média da diferença de horário
def getMediaDiferencaRelogio():
    lista_diferenca_tempo = [cliente['diferenca_tempo'] for cliente in dados_cliente.values()]
    media_diferenca_relogio = sum(lista_diferenca_tempo, datetime.timedelta()) / len(dados_cliente)
    return media_diferenca_relogio

# Função para sincronizar todos os relógios
def sincronizarTodosRelogios():
    while True:
        print("Processo de sincronização ativo!")
        print("Número de clientes a serem sincronizados: " + str(len(dados_cliente)))

        if dados_cliente:
            media_diferenca_relogio = getMediaDiferencaRelogio()

            for endereco_cliente, cliente in dados_cliente.items():
                try:
                    tempo_sincronizado = datetime.datetime.now() + media_diferenca_relogio
                    cliente['conector'].send(tempo_sincronizado.strftime("%H:%M:%S").encode())
                except Exception as e:
                    print("Algo deu errado ao enviar o tempo sincronizado para o cliente " + str(endereco_cliente))
        else :
            print("Sem clientes a serem sincronizados no momento.")

        print("\n\n")
        time.sleep(5)

# Função para iniciar o servidor de relógio
def iniciarServidorRelogio(porta = 8080):
    servidor_mestre = socket.socket()
    servidor_mestre.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    print("Socket no nó mestre criado com sucesso!\n")

    servidor_mestre.bind(('', porta))

    servidor_mestre.listen(10)
    print("Servidor de relógio iniciado...\n")

    print("Iniciando conexões...\n")
    thread_mestre = threading.Thread(target=iniciarConexao, args=(servidor_mestre, ))
    thread_mestre.start()

    print("Iniciando o processo de sincronização...\n")
    thread_sincronizacao = threading.Thread(target=sincronizarTodosRelogios, args=())
    thread_sincronizacao.start()

if __name__ == '__main__':
    iniciarServidorRelogio(porta = 8080)
