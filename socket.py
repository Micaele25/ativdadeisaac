import socket
import os

HOST = '127.0.0.1'  # Endereço IP local
PORT = 8000  # Porta que o servidor irá escutar
BUFFER_SIZE = 1024  # Tamanho do buffer de dados

def handle_client(conn):
    with conn:
        # Recebe os dados da conexão
        data = conn.recv(BUFFER_SIZE)
        print("Recebido:", data.decode())

        # Verifica se a solicitação GET é para "/" (raiz)
        if data.startswith(b'GET / HTTP/1.1'):
            try:
                # Lê o conteúdo do arquivo HTML
                with open('index.html', 'rb') as file:
                    html_content = file.read()
                    # Envia o cabeçalho e o conteúdo HTML como resposta
                    conn.sendall(b'HTTP/1.1 200 OK\r\nContent-type: text/html\r\n\r\n' + html_content)
            except FileNotFoundError:
                # Se o arquivo HTML não for encontrado, envia uma mensagem de erro 404
                conn.sendall(b'HTTP/1.1 404 Not Found\r\nContent-type: text/plain\r\n\r\n404 Not Found')
        else:
            # Se a solicitação GET não for para "/", tenta servir o arquivo solicitado
            try:
                # Extrai o caminho do arquivo da solicitação GET
                file_path = data.decode().split()[1]
                # Lê o conteúdo do arquivo solicitado
                with open(file_path.lstrip('/'), 'rb') as file:
                    file_content = file.read()
                    # Obtém o tipo MIME do arquivo
                    content_type = get_content_type(file_path)
                    # Envia o cabeçalho e o conteúdo do arquivo como resposta
                    conn.sendall(b'HTTP/1.1 200 OK\r\nContent-type: ' + content_type + b'\r\n\r\n' + file_content)
            except FileNotFoundError:
                # Se o arquivo solicitado não for encontrado, envia uma mensagem de erro 404
                conn.sendall(b'HTTP/1.1 404 Not Found\r\nContent-type: text/plain\r\n\r\n404 Not Found')

def get_content_type(file_path):
    # Mapeia a extensão do arquivo para o tipo MIME correspondente
    content_types = {
        '.html': b'text/html',
        '.css': b'text/css',
        '.js': b'application/javascript',
        '.jpg': b'image/jpeg',
        '.jpeg': b'image/jpeg',
        '.png': b'image/png',
        '.gif': b'image/gif'
    }
    # Obtém a extensão do arquivo
    _, file_extension = os.path.splitext(file_path)
    # Retorna o tipo MIME correspondente ou 'application/octet-stream' se não for reconhecido
    return content_types.get(file_extension.lower(), b'application/octet-stream')

def main():
    # Cria um socket TCP/IP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Liga o socket ao endereço e à porta especificados
        s.bind((HOST, PORT))
        # Habilita o servidor para aceitar conexões
        s.listen()

        print("Servidor TCP rodando em http://{}:{}".format(HOST, PORT))

        while True:
            # Aceita a próxima conexão que chegar
            conn, addr = s.accept()
            print("Conexão recebida de:", addr)

            # Manipula a conexão em uma thread separada
            handle_client(conn)

if __name__ == "__main__":
    main()
