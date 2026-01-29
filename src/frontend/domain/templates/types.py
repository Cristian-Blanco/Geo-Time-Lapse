from typing import TypedDict, TypeAlias

class TemplateDefItem(TypedDict):
    id: str
    title: str
    description: str
    icon: str
    enabled: bool

TemplateDef: TypeAlias = list[TemplateDefItem]
