import importlib
from typing import cast

from frontend.presentation.views.base_page import BasePage

class ViewResolver:
    @staticmethod
    def resolve(dotted_path: str) -> type[BasePage]:
        module_path, cls_name = dotted_path.split(":")
        module = importlib.import_module(module_path)
        cls = getattr(module, cls_name)
        return cast(type[BasePage], cls)
