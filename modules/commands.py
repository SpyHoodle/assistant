import os

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk  # noqa: E402

entries = os.listdir('/usr/share/applications')


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
        self.entries = parsed
        self.keywords = [e.name for e in parsed if hasattr(e, 'name')]

    def run(self, args):
        for word in args:
            if word in self.keywords:
                entry = None
                for e in self.entries:
                    if e.Name == word:
                        entry = e
                        break
                os.system(entry.Exec)
                return True

    def enter(self, query, window) -> bool:
        return False
