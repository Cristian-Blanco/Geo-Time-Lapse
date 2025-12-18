import importlib

class ControllerResolver:
    @staticmethod
    def resolve(dotted_path: str):
        module_path, cls_name = dotted_path.split(":")
        module = importlib.import_module(module_path)
        return getattr(module, cls_name)
