from collections.abc import Callable

from ..geometry import LinearRing

def signed_area(ring: LinearRing) -> float: ...
def is_ccw_impl(name: None = None) -> Callable[[LinearRing], bool]: ...
