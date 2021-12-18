# Returns (version, type, consumed, remaining)
def parse_header(stream: str):
    return (int(stream[0:3], 2), int(stream[3:6], 2), 6, stream[6:])


# Returns (value, consumed, remaining)
def parse_literal_value(stream: str):
    value_binary_string = []
    consumed = 0

    while True:
        (part, stream) = (stream[:5], stream[5:])
        consumed += 5

        value_binary_string.append(part[1:])
        if part[0] == "0":
            break

    return (int("".join(value_binary_string), 2), consumed, stream)


# Returns (consumed, remaining)
def parse_operator(stream: str):
    (length_type_id, stream) = (stream[:1], stream[1:])
    consumed = 1

    if length_type_id == "0":
        (length_bits_bin, stream) = (stream[:15], stream[15:])
        consumed += 15

        length_bits = int(length_bits_bin, 2)
        print(f"We have {length_bits} bits following")

        children_consumed = 0
        while children_consumed < length_bits:
            (packet_consumed, stream) = parse_packet(stream)
            children_consumed += packet_consumed
            consumed += packet_consumed
    else:
        (num_packets_bin, stream) = (stream[:11], stream[11:])
        consumed += 11

        num_packets = int(num_packets_bin, 2)
        print(f"We have {num_packets} following")

        for _ in range(num_packets):
            (packet_consumed, stream) = parse_packet(stream)
            consumed += packet_consumed

    return (consumed, stream)

version_sum = 0

# Returns (consumed, remaining)
def parse_packet(stream: str):
    global version_sum

    consumed = 0

    (version, type, header_size, stream) = parse_header(stream)
    version_sum += version
    consumed += header_size

    if type == 4:
        (value, packet_consumed, stream) = parse_literal_value(stream)
        consumed += packet_consumed

        print(f"Literal value packet parsed: {value}")

        return (consumed, stream)
    else:
        (packet_consumed, stream) = parse_operator(stream)
        consumed += packet_consumed

        print(f"Operator packet parsed")

        return (consumed, stream)


def parse_packet_hex(stream_hex: str):
    stream_length = len(stream_hex)
    binary_packet = format(int(stream_hex, 16), f"0{4 * stream_length}b")
    parse_packet(binary_packet)


# parse_packet_hex("D2FE28")
version_sum = 0
parse_packet_hex("8A004A801A8002F478")
print(f"Version sum: {version_sum}")
assert(version_sum == 16)

version_sum = 0
parse_packet_hex("620080001611562C8802118E34")
print(f"Version sum: {version_sum}")
assert(version_sum == 12)

version_sum = 0
parse_packet_hex("C0015000016115A2E0802F182340")
print(f"Version sum: {version_sum}")
assert(version_sum == 23)

version_sum = 0
parse_packet_hex("A0016C880162017C3686B18A3D4780")
print(f"Version sum: {version_sum}")
assert(version_sum == 31)

version_sum = 0
packet = open("task16/input.txt").read()
parse_packet_hex(packet)
print(f"Version sum: {version_sum}")