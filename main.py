import time
import os

fs = {
    "/": {
        "bin": {
            "python.exe": "Binary executable",
            "bash.exe": "Shell executable",
            "ping.exe": "Network utility",
            "editor.exe": "Text editor"
        },
        "home": {
            "guest": {
                "notes.txt": "Welcome to Micro Ruby user folder.",
                "todo.txt": "1. Learn Python\n2. Build OS\n3. Become legend"
            }
        },
        "sys": {
            "config.ini": "theme=dark\nversion=0.2",
            "drivers.sys": "Loaded drivers..."
        },
        "kernel": {
            "kernel.img": "Micro Ruby Kernel Image",
            "boot.log": "Boot successful."
        },
        "dev": {
            "mouse.dev": "Connected",
            "keyboard.dev": "Connected"
        },
        "tmp": {},
        "readme.txt": "Welcome to Micro Ruby!"
    }
}

current_path = "/"

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def get_dir(path):
    parts = [p for p in path.split("/") if p]
    node = fs["/"]

    for part in parts:
        if part in node and isinstance(node[part], dict):
            node = node[part]
        else:
            return None
    return node

def split_path(path):
    return [p for p in path.split("/") if p]

def get_parent(path):
    if path == "/":
        return "/"
    parts = split_path(path)
    parts.pop()
    return "/" + "/".join(parts) if parts else "/"

def prompt():
    return f"microruby {current_path}$ "

def cmd_ls():
    folder = get_dir(current_path)
    for item in folder:
        if isinstance(folder[item], dict):
            print("[DIR] ", item)
        else:
            print("[FILE]", item)

def cmd_pwd():
    print(current_path)

def cmd_cd(target):
    global current_path

    if target == "..":
        current_path = get_parent(current_path)
        return

    new = current_path.rstrip("/") + "/" + target
    folder = get_dir(new)

    if folder is not None:
        current_path = new
    else:
        print("Folder not found.")

def cmd_mkdir(name):
    folder = get_dir(current_path)
    if name in folder:
        print("Already exists.")
    else:
        folder[name] = {}
        print("Folder created.")

def cmd_touch(name):
    folder = get_dir(current_path)
    folder[name] = ""
    print("File created.")

def cmd_cat(name):
    folder = get_dir(current_path)

    if name in folder and not isinstance(folder[name], dict):
        print(folder[name])
    else:
        print("File not found.")

def cmd_write(name, text):
    folder = get_dir(current_path)

    if name in folder and not isinstance(folder[name], dict):
        folder[name] = text
        print("Saved.")
    else:
        print("File not found.")

def cmd_rm(name):
    folder = get_dir(current_path)

    if name in folder:
        del folder[name]
        print("Removed.")
    else:
        print("Not found.")

def cmd_rename(old, new):
    folder = get_dir(current_path)

    if old in folder:
        folder[new] = folder.pop(old)
        print("Renamed.")
    else:
        print("Not found.")

def cmd_info():
    print("Micro Ruby OS")
    print("Version: 0.2")
    print("Kernel: RubyCore")
    print("RAM: 512MB Fake")
    print("CPU: Python Virtual CPU")

def cmd_tree(folder=None, indent=""):
    if folder is None:
        folder = get_dir(current_path)

    for name in folder:
        print(indent + "|-- " + name)
        if isinstance(folder[name], dict):
            cmd_tree(folder[name], indent + "   ")

def help_menu():
    print("""
Commands:
ls               - List files
pwd              - Show path
cd folder        - Enter folder
cd ..            - Back
mkdir name       - Create folder
touch file       - Create file
cat file         - Read file
write file text  - Write text
rm file          - Delete file/folder
rename a b       - Rename
tree             - Folder tree
info             - System info
clear            - Clear screen
help             - Show commands
exit             - Shutdown
""")

def main():
    print("Starting Micro Ruby...")
    time.sleep(1)
    print("Loading kernel...")
    time.sleep(1)
    print("Welcome to Micro Ruby OS")
    time.sleep(0.5)

    while True:
        cmd = input(prompt()).strip()

        if cmd == "ls":
            cmd_ls()

        elif cmd == "pwd":
            cmd_pwd()

        elif cmd.startswith("cd "):
            cmd_cd(cmd[3:].strip())

        elif cmd.startswith("mkdir "):
            cmd_mkdir(cmd[6:].strip())

        elif cmd.startswith("touch "):
            cmd_touch(cmd[6:].strip())

        elif cmd.startswith("cat "):
            cmd_cat(cmd[4:].strip())

        elif cmd.startswith("write "):
            parts = cmd.split(" ", 2)
            if len(parts) >= 3:
                cmd_write(parts[1], parts[2])

        elif cmd.startswith("rm "):
            cmd_rm(cmd[3:].strip())

        elif cmd.startswith("rename "):
            parts = cmd.split(" ")
            if len(parts) == 3:
                cmd_rename(parts[1], parts[2])

        elif cmd == "tree":
            cmd_tree()

        elif cmd == "info":
            cmd_info()

        elif cmd == "help":
            help_menu()

        elif cmd == "clear":
            clear()

        elif cmd == "exit":
            print("Shutting down...")
            break

        else:
            print("Unknown command.")

main()
