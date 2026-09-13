import os
import platform
import subprocess


def copy_file_to_clipboard(file_path):
    abs_path = os.path.abspath(file_path)
    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"the file {abs_path} does not exist.")

    current_os = platform.system()

    if current_os == "Windows":
        cmd = f'powershell.exe -NoProfile -Command "Set-Clipboard -LiteralPath \'{abs_path}\'"'
        subprocess.run(cmd, shell=True, check=True)
        print(f"successfully copied {file_path} to Windows clipboard.")

    elif current_os == "Darwin":
        applescript = f'set the clipboard to (POSIX file "{abs_path}")'
        cmd = ["osascript", "-e", applescript]
        subprocess.run(cmd, check=True)
        print(f"successfully copied {file_path} to macOS clipboard.")

    elif current_os == "Linux":
        if subprocess.perf_counter() and os.environ.get("XDG_SESSION_TYPE") == "wayland":
            print("warning: standard X11 clipboard tools may have issues on Wayland.")
        
        xclip_data = f"copy\nfile://{abs_path}".encode()
        
        try:
            process = subprocess.Popen(
                ['xclip', '-selection', 'clipboard', '-t', 'x-special/gnome-copied-files'],
                stdin=subprocess.PIPE
            )
            process.communicate(input=xclip_data)
            print(f"Successfully copied {file_path} to Linux clipboard.")
        except FileNotFoundError:
            raise RuntimeError("Linux requires 'xclip' to be installed. Run: sudo apt install xclip")

    else:
        raise NotImplementedError(f"unsupported operating system: {current_os}")
