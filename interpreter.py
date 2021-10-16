import importlib
import os
import typing


class Interpreter:
    def __init__(self) -> None:
        extensions = []
        modules = [f for f in os.listdir("modules") if f.endswith(".py")]

        for n, f in enumerate(modules):
            name = ".".join(f.split(".")[:-1])
            print(f"\033[93m[{n + 1}/{len(modules)}] Importing module {name}", end="\r")
            try:
                module = importlib.import_module("modules." + name)
                if not hasattr(module, "Module"):
                    print(f"\033[91m[{n + 1}/{len(modules)}] Module {name} has no Module class\033[0m")
                    continue
                print(f"\033[92m[{n + 1}/{len(modules)}] Loaded module {name}      \033[0m")
                extensions.append(module.Module())
            except Exception as e:
                print(f"\033[91m[{n + 1}/{len(modules)}] Error importing module {name}: {e}\033[0m")

        self.extensions = extensions
        self.keywords = {}
        for extension in extensions:
            for keyword in extension.keywords:
                if keyword in self.keywords:
                    self.keywords[keyword].append(extension.name)
                    continue
                self.keywords[keyword] = [extension.name]
        print("\033[92mLoaded all modules\033[0m")

    def get_response(self, query) -> typing.List[str]:
        query = query.lower().split()
        responses = []
        for word in query:
            if word in self.keywords:
                for module in self.keywords[word]:
                    if module in responses:
                        continue
                    responses.append(module)
        responses = [module.run(query) for module in self.extensions if module.name in responses and module.run(query) is not None]
        return responses

    def enter_pressed(self, query, window) -> bool:
        query = query.get_text().lower().split()
        responses = []
        for word in query:
            if word in self.keywords:
                for module in self.keywords[word]:
                    if module in responses:
                        continue
                    responses.append(module)
        for module in self.extensions:
            if module.name in responses:
                if module.enter(query, window=window):
                    return True
        return False
