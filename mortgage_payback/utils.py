from typing import Any, Iterable, List
import inspect

Money = float


class Utils:
    @staticmethod
    def get_all_fields(obj):
        return inspect.getmembers(obj)

    @staticmethod
    def get_all_fields_values(obj, exclude_list: List[str] = ()) -> Iterable[Any]:
        for name, value in Utils.get_all_fields(obj):
            if name.startswith("_") or inspect.ismethod(value):
                continue
            if name in exclude_list:
                continue
            yield f"{name}: {value}"
