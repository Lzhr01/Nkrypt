import subprocess
import sys
import time
import platform
import shlex

def launch_node(node_id, port=None):
    """Launch a P2P node in a new terminal/process"""
    try:
        script = "p2p_node.py"
        cmd = [sys.executable, script, node_id]
        if port:
            cmd.append(str(port))

        quoted_cmd = " ".join(shlex.quote(arg) for arg in cmd)
        system = platform.system()

        if system == "Windows":
            subprocess.Popen(["cmd", "/c", "start", "cmd", "/k", quoted_cmd])

        elif system == "Darwin":  # macOS
            subprocess.Popen([
                "osascript", "-e",
                f'tell app "Terminal" to do script "{quoted_cmd}"'
            ])

        else:  # Linux and others
            terminals = ["gnome-terminal", "konsole", "xterm", "xfce4-terminal", "terminator"]
            launched = False

            for terminal in terminals:
                try:
                    if terminal in ["gnome-terminal", "xfce4-terminal", "terminator"]:
                        subprocess.Popen([terminal, "--", *cmd])
                    else:
                        subprocess.Popen([terminal, "-e", quoted_cmd])
                    launched = True
                    break
                except FileNotFoundError:
                    continue

            if not launched:
                print("\n[ERROR] No suitable terminal emulator found.")
                print(f"Please run manually:\n  {quoted_cmd}")
                return False

        print(f"✓ Launched node '{node_id}'" + (f" on port {port}" if port else ""))
        return True

    except Exception as e:
        print(f"[ERROR] Failed to launch node '{node_id}': {e}")
        return False

def main():
    print("P2P Messaging App Launcher")
    print("=" * 40)

    while True:
        print("\nOptions:")
        print("1. Launch a new node")
        print("2. Quick demo setup (Alice + Bob)")
        print("3. Exit")

        choice = input("\nChoose an option (1-3): ").strip()

        if choice == '1':
            node_id = input("Enter node ID: ").strip()
            if not node_id:
                print(" Node ID cannot be empty!")
                continue

            port_input = input("Enter port (or press Enter for auto): ").strip()
            port = None
            if port_input:
                try:
                    port = int(port_input)
                except ValueError:
                    print(" Invalid port number!")
                    continue

            launch_node(node_id, port)

        elif choice == '2':
            print("\nSetting up demo with Alice and Bob...")
            launch_node("alice", 8001)
            time.sleep(1)
            launch_node("bob", 8002)

            print("\n Demo Instructions:")
            print("1. In Alice's terminal, type: connect bob@localhost:8002 OR :")
            print("2. In Bob's terminal, type: connect alice@localhost:8001 (no need if you already did step 1)")
            print("3. Start chatting with: msg <peer_id> <your message>")

        elif choice == '3':
            print("Goodbye !")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
