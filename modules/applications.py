import os
import sys
import subprocess


class DesktopEntry:
    def __init__(self, **kwargs) -> None:
        for arg in kwargs:
            setattr(self, arg, kwargs[arg])

    def __getattr__(self, name) -> None:
        return None


class Module:
    def __init__(self):
        self.name = "applications"
        parsed = []
        entries = os.listdir('/usr/share/applications')
        for entry in entries:
            if entry.endswith('.desktop'):
                with open('/usr/share/applications/' + entry, 'r') as f:
                    lines = f.readlines()
                    kwargs = {}
                    for line in lines:
                        if "=" in line:
                            key = line.split('=')[0]
                            value = "=".join(line.split('=')[1:])
                            kwargs[key.strip()] = value.strip()
                    parsed.append(DesktopEntry(**kwargs))
        self.keywords = [e.Name.lower() for e in parsed]
        self.entries = parsed

    def run(self, query) -> str:
        for e in self.entries:
            for q in query:
                if q.lower() in e.Name.lower():
                    return f"Press enter to launch {e.Name}"

    def enter(self, query, window=None) -> bool:
        for e in self.entries:
            for q in query:
                if q.lower() in e.Name.lower():
                    # window.hide()
                    subprocess.call(e.Exec.replace('%U', '').strip().split(" "))
                    sys.exit()

        return False
