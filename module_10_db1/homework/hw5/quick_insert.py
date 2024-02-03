from typing import Union, List

Number = Union[int, float, complex]


def find_insert_position(array: List[Number], number: Number) -> int:
    for i in range(0, len(array) - 1):
        if number >= array[i] and number <= array[i + 1]:
            return i + 1
        elif number < array[i]:
            return i
    else:
        return len(array)


if __name__ == "__main__":
    A: List[Number] = [1, 2, 3, 3, 3, 5]
    x: Number = 4
    insert_position: int = find_insert_position(A, x)
    assert insert_position == 5

    A: List[Number] = [1, 2, 3, 3, 3, 5]
    x: Number = 4
    A.insert(insert_position, x)
    assert A == sorted(A)
