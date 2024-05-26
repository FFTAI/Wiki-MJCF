from typing import TypeVar, Dict

K = TypeVar("K")
V = TypeVar("V")


def _update_with_defaults(
    dictionary: Dict[K, V] = None, defaults: Dict[K, V] = None
) -> Dict[K, V]:
    updated_dict = {} if defaults is None else dict(defaults.items())
    updated_dict.update(dictionary if dictionary is not None else {})
    return updated_dict
