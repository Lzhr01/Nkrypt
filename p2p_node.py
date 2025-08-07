import socket
import threading
import json
import time
import sys
from datetime import datetime
from cryptography.fernet import Fernet

class P2PNode:
    def __init__(self, node_id, host='localhost', port=None):
        self.node_id = node_id
        self.host = host
        self.port = port or self._find_free_port()
        self.socket = None
        self.peers = {}  # {peer_id: (host, port)}
        self.connections = {}  # {peer_id: socket}
        self.keys = {}  # {peer_id: shared_key}
        self.running = False
        self.key = Fernet.generate_key()  # Symmetric key for this session
        self.cipher = Fernet(self.key)

    def _find_free_port(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            return s.getsockname()[1]

    def start(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            self.running = True

            print(f"Node '{self.node_id}' started on {self.host}:{self.port}")
            print(f"Your connection info: {self.node_id}@{self.host}:{self.port}")
            print("=" * 60)

            threading.Thread(target=self._listen_for_connections, daemon=True).start()
            self._command_interface()

        except Exception as e:
            print(f"Error starting node: {e}")
            self.stop()

    def _listen_for_connections(self):
        while self.running:
            try:
                client_socket, addr = self.socket.accept()
                threading.Thread(target=self._handle_incoming_connection, args=(client_socket, addr)).start()
            except Exception as e:
                if self.running:
                    print(f"Error accepting connection: {e}")

    def _handle_incoming_connection(self, client_socket, addr):
        try:
            data = client_socket.recv(1024).decode('utf-8')
            handshake = json.loads(data)

            if handshake.get('type') == 'handshake':
                peer_id = handshake.get('node_id')
                peer_key = handshake.get('key').encode()

                if peer_id in self.connections:
                    client_socket.close()
                    return

                response = {
                    'type': 'handshake_response',
                    'node_id': self.node_id,
                    'status': 'accepted',
                    'key': self.key.decode()
                }
                client_socket.send(json.dumps(response).encode('utf-8'))

                self.connections[peer_id] = client_socket
                self.keys[peer_id] = Fernet(peer_key)
                print(f"Peer '{peer_id}' connected from {addr}")

                threading.Thread(target=self._receive_messages, args=(peer_id, client_socket)).start()

        except Exception as e:
            print(f"Error handling incoming connection: {e}")
            client_socket.close()

    def connect_to_peer(self, peer_info):
        try:
            peer_id, address = peer_info.split('@')
            host, port = address.split(':')
            port = int(port)

            if peer_id == self.node_id or peer_id in self.connections:
                return

            peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peer_socket.connect((host, port))

            handshake = {
                'type': 'handshake',
                'node_id': self.node_id,
                'key': self.key.decode()
            }
            peer_socket.send(json.dumps(handshake).encode('utf-8'))

            response = json.loads(peer_socket.recv(1024).decode('utf-8'))
            if response.get('status') == 'accepted':
                self.connections[peer_id] = peer_socket
                self.peers[peer_id] = (host, port)
                peer_key = response['key'].encode()
                self.keys[peer_id] = Fernet(peer_key)
                print(f"Connected to peer '{peer_id}' at {host}:{port}")

                threading.Thread(target=self._receive_messages, args=(peer_id, peer_socket)).start()

        except Exception as e:
            print(f"Failed to connect to '{peer_info}': {e}")

    def _receive_messages(self, peer_id, peer_socket):
        while self.running:
            try:
                data = peer_socket.recv(2048).decode('utf-8')
                if not data:
                    break
                message = json.loads(data)
                # print(f"Encrypted message recieved from {peer_id} : <== {message} ==>. Decrypting... ") """ Uncomment this line to see the encrypted message recieved, unnecessary but fun """
                if message.get('type') == 'chat_message':
                    encrypted = message.get('content').encode()
                    decrypted = self.cipher.decrypt(encrypted).decode()
                    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] {peer_id}: {decrypted}\n>> ", end="", flush=True)
            except:
                break

        if peer_id in self.connections:
            del self.connections[peer_id]
        peer_socket.close()

    def send_message(self, peer_id, content):
        if peer_id not in self.connections:
            print(f"Not connected to '{peer_id}'")
            return

        try:
            encrypted = self.keys[peer_id].encrypt(content.encode()).decode()
            message = {
                'type': 'chat_message',
                'content': encrypted,
                'timestamp': datetime.now().isoformat()
            }
            self.connections[peer_id].send(json.dumps(message).encode('utf-8'))
            print(f"[{datetime.now().strftime('%H:%M:%S')}] You -> {peer_id}: {content}")
        except Exception as e:
            print(f"Error sending message: {e}")

    def _command_interface(self):
        print("\nCommands:")
        print("  connect <peer_id@host:port>")
        print("  msg <peer_id> <message>")
        print("  list")
        print("  quit")
        while self.running:
            try:
                command = input(">> ").strip()
                if not command:
                    continue
                parts = command.split(' ', 2)
                cmd = parts[0].lower()

                if cmd in ('quit', 'exit'):
                    break
                elif cmd == 'connect' and len(parts) >= 2:
                    self.connect_to_peer(parts[1])
                elif cmd == 'msg' and len(parts) >= 3:
                    self.send_message(parts[1], parts[2])
                elif cmd == 'list':
                    for peer_id in self.connections:
                        print(f"- {peer_id}")
            except (KeyboardInterrupt, EOFError):
                break

        self.stop()

    def stop(self):
        print("Shutting down node...")
        self.running = False
        for conn in self.connections.values():
            try:
                conn.close()
            except:
                pass
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
        print("Node stopped.")


def main():
    if len(sys.argv) < 2:
        node_id = input("Enter your node ID: ").strip()
    else:
        node_id = sys.argv[1]

    port = int(sys.argv[2]) if len(sys.argv) >= 3 else None
    node = P2PNode(node_id, port=port)
    node.start()


if __name__ == "__main__":
    main()
