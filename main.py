import struct
from typing import BinaryIO, Callable, Any

SERVERS_DAT_PATH = "..."


def read_byte(fp: BinaryIO) -> int:
    byte = fp.read(1)
    if not byte:
        print(f"Read byte: <EOF>")
        return 0

    byte = byte[0]
    print(f"Read byte: {byte}")
    return byte


def read_short(fp: BinaryIO) -> int:
    short = int.from_bytes(fp.read(2), "big", signed=True)
    print(f"Read short: {short}")
    return short


def read_int(fp: BinaryIO) -> int:
    int_ = int.from_bytes(fp.read(4), "big", signed=True)
    print(f"Read int: {int_}")
    return int_


def read_long(fp: BinaryIO) -> int:
    long = int.from_bytes(fp.read(8), "big", signed=True)
    print(f"Read long: {long}")
    return long


def read_float(fp: BinaryIO) -> float:
    float_ = struct.unpack(">f", fp.read(4))[0]
    print(f"Read float: {float_}")
    return float_


def read_double(fp: BinaryIO) -> float:
    double = struct.unpack(">d", fp.read(8))[0]
    print(f"Read double: {double}")
    return double


def read_byte_array(fp: BinaryIO) -> bytes:
    length = read_int(fp)
    bytes_ = fp.read(length)
    print(f"Read bytes: {bytes_.hex()}")
    return bytes_


def read_string(fp: BinaryIO) -> str:
    length = read_short(fp)
    str_ = fp.read(length).decode("utf8")
    print(f"Read string: {str_!r}")
    return str_


def read_list(fp: BinaryIO) -> list:
    tag_id = read_byte(fp)
    reader = readers[tag_id]

    length = read_int(fp)
    list_ = []

    for _ in range(length):
        list_.append(reader(fp))

    print(f"Read list: {list_}")
    return list_


def read_compound(fp: BinaryIO) -> dict:
    compound = {}
    while (tag_id := read_byte(fp)) != 0:
        name = read_string(fp)
        value = readers[tag_id](fp)
        compound[name] = value

    print(f"Read compound: {compound}")
    return compound


readers: dict[int, Callable[[BinaryIO], Any]] = {
    0: lambda fp: None,
    1: read_byte,
    2: read_short,
    3: read_int,
    4: read_long,
    5: read_float,
    6: read_double,
    7: read_byte_array,
    8: read_string,
    9: read_list,
    10: read_compound,
}


def main() -> None:
    with open(SERVERS_DAT_PATH, "rb") as f:
        read_compound(f)


if __name__ == "__main__":
    main()
