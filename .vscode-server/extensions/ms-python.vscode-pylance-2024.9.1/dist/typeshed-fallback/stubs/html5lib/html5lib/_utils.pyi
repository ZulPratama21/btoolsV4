from _typeshed import Incomplete
from collections.abc import Mapping
from typing import Any

supports_lone_surrogates: bool

class MethodDispatcher(dict[Any, Any]):
    default: Any
    def __init__(self, items=()) -> None: ...
    def __getitem__(self, key): ...
    def __get__(self, instance, owner: Incomplete | None = None): ...

class BoundMethodDispatcher(Mapping[Any, Any]):
    instance: Any
    dispatcher: Any
    def __init__(self, instance, dispatcher) -> None: ...
    def __getitem__(self, key): ...
    def get(self, key, default): ...  # type: ignore[override]
    def __iter__(self): ...
    def __len__(self) -> int: ...
    def __contains__(self, key): ...

def isSurrogatePair(data): ...
def surrogatePairToCodepoint(data): ...
def moduleFactoryFactory(factory): ...