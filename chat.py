import socket
import threading


host = '10.113.60.206' # Endereço IP do seu computador
porta = 12345

ipserver = '10.113.60.230'
portserver = 12345

contatos = [('Albert','10.113.60.207'),('Eu','10.113.60.206')]


socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_server.bind((host, porta))


print(f"Servidor UDP aguardando mensagens em {host}:{porta}")
print("Contatos disponíveis:")
for contato in contatos:
    print(contato[0])


enderecos_contatos = {nome: ip for nome, ip in contatos}


lock = threading.Lock()


# Função para receber mensagens
def receber_mensagens():
    while True:
        try:
        # Recebe os dados e o endereço do remetente
            dados, endereco = socket_server.recvfrom(1024) # Tamanho do buffer é 1024 bytes
            mensagem = dados.decode('utf-8')
            print(f"Recebido de {endereco[0]}:{endereco[1]}: {mensagem}")
            if endereco[0]== ipserver:
                atualizaLista(endereco,mensagem)
            
        except UnicodeDecodeError:
            print(f"Recebido de {endereco[0]}:{endereco[1]}: Erro de decodificação (não UTF-8)")
# Inicializa uma thread para receber mensagens
thread_recebimento = threading.Thread(target=receber_mensagens)
thread_recebimento.daemon = True
thread_recebimento.start()


def atualizaLista(endereco,mensagem):
    
    try:
        contatos_strings = mensagem.split('\n')
        contatos.clear()  
        for contato_str in contatos_strings:
            if contato_str:
                print(contato_str.split(','))
                nome, ip = contato_str.split(',')
                contatos.append((nome, ip))
        
        enderecos_contatos.clear()
        enderecos_contatos.update(dict(contatos))
        
        print("Contatos atualizados:")
        for contato in contatos:
            print(f"{contato[0]}: {contato[1]}")
    except UnicodeDecodeError:
        print(f"Recebido de {endereco[0]}:{endereco[1]}: Erro de decodificação (não UTF-8)")

def enviar_mensagens():
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


    while True:
        mensagem = input("Digite a mensagem (no formato 'destinatario_mensagem' ou '/entrar_nome' para iniciar/sair de um chat privado): ")
        if mensagem == "\sair":
            print("Encerrando o programa...")
            print("Fechando portas de escuta:")
            #thread_recebimento.join()
            break
        else:
            if mensagem.startswith('.entrar '):
                destinatario = mensagem[8:]
                cliente_socket.sendto(mensagem.encode('utf-8'),(ipserver, portserver))


            elif mensagem.startswith('.contatos'):
                destinatario = mensagem[8:]
                cliente_socket.sendto(mensagem.encode('utf-8'),(ipserver, portserver))
                #atualizaLista()
            elif mensagem.startswith('.sair '):
                destinatario = mensagem[8:]
                cliente_socket.sendto(mensagem.encode('utf-8'),(ipserver, portserver))
            elif mensagem.startswith('.') and '_' in mensagem:
                mensagem = mensagem[1:]
                nome_destinatario, mensagem = mensagem.split('_', 1)

                if nome_destinatario in enderecos_contatos:
                    print(nome_destinatario)
                    destino_ip = enderecos_contatos[nome_destinatario]
                    end_destino_ip = (destino_ip, porta)
                    cliente_socket.sendto(mensagem.encode('utf-8'), end_destino_ip)
                else:
                    print(f"Erro: {nome_destinatario} não é um contato válido.")


            else:
                
                cliente_socket.sendto(mensagem.encode('utf-8'), ("192.168.60.230", portserver))


thread_envio = threading.Thread(target=enviar_mensagens)
thread_envio.start()


thread_envio.join()
print("Threads encerradas.")
socket_server.close()
print("Socket encerrado. Bye Bye")


