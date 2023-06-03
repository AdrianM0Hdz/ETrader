from typing import TypeVar, Generic, List  # type: ignore


T = TypeVar("T")


class List(Generic[T]):
    def __init__(self) -> None:
        self.items: List[T] = []

    def add_item(self, item: T):
        self.items.append(item)

    def get_list(self) -> List[T]:
        return self.items


class SubType(List[int]):
    def __init__(self, id):
        self.id = id


if __name__ == "__main__":
    inst = List[int]()
    inst.add_item(12)
    print(inst.get_list())

    inst2 = List[str]()
    inst2.add_item("q3")
    print(inst2.get_list())
