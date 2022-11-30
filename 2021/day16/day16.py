from funcy import print_durations
import numpy as np
import networkx as nx
import math

# Puzzle: https://adventofcode.com/2021/day/16
# 11000000000000110111101000101001010010001001000000000
# TTTILLLLLLLLLLLLLLLAAAAAAAAAAABBBBBBBBBBBBBBBB

def hextobin(h):
    return bin(int(h, 16))[2:].zfill(len(h) * 4)


def decode_num(b, content_idx):

    cur_idx = content_idx

    num_str = ""

    while int(b[cur_idx]) == 1:
        num_str += b[cur_idx + 1:cur_idx + 5]
        cur_idx += 5

    num_str += b[cur_idx + 1:cur_idx + 5]

    # start of next packet
    return cur_idx + 5, int(num_str, 2)


def parse_packet(bs, i):

    v = int(bs[i : i + 3], 2)
    i += 3

    t = int(bs[i : i + 3], 2)
    i += 3

    match t:
        case 4:
            # Packets with type ID 4 represent a literal value
            # print(f"literal value at {i}")
            i, num = decode_num(bs, i)
            return i, ("val", num)
        # Packets with type ID 0 are sum packets - their value is the sum of the values of their sub-packets. If they only have a single sub-packet, their value is the value of the sub-packet.
        case 0:
            opcode=sum
        # Packets with type ID 1 are product packets - their value is the result of multiplying together the values of their sub-packets. If they only have a single sub-packet, their value is the value of the sub-packet.
        case 1:
            opcode=math.prod
        # Packets with type ID 2 are minimum packets - their value is the minimum of the values of their sub-packets.
        case 2:
            opcode=min
        # Packets with type ID 3 are maximum packets - their value is the maximum of the values of their sub-packets.
        case 3:
            opcode=max
        # Packets with type ID 5 are greater than packets - their value is 1 if the value of the first sub-packet is greater than the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.
        case 5:
            opcode=lambda lst: lst[0] > lst[1]
        # Packets with type ID 6 are less than packets - their value is 1 if the value of the first sub-packet is less than the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.
        case 6:
            opcode=lambda lst: lst[0] < lst[1]
        # Packets with type ID 7 are equal to packets - their value is 1 if the value of the first sub-packet is equal to the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.
        case 7:
            opcode=lambda lst: lst[0] == lst[1]


    # any packet with a type ID other than 4 represent an operator
    # An operator packet contains one or more packets
    # bit immediately after the packet header; this is called the length type ID


    packets = []

    l = int(bs[i])
    i += 1
    # If the length type ID is 0, then the next 15 bits are a number
    # that represents the total length in bits of the sub-packets contained by this packet.
    if l == 0:
        # print(f"l==0 at {i}")
        len_bits = int(bs[i:i+15], 2)
        i += 15
        start_i = i
        min_packet_len = 6 + 1 + 5
        # while i + min_packet_len<= start_i + len_bits:
        while i < start_i + len_bits:
            i, packet = parse_packet(bs, i)
            packets.append(packet)

    # If the length type ID is 1, then the next 11 bits are a number
    # that represents the number of sub-packets immediately contained by this packet
    if l == 1:
        # print(f"l==1 at {i}")
        num_packets = int(bs[i:i+11], 2)
        i += 11
        for pid in range(num_packets):
            i, packet = parse_packet(bs, i)
            packets.append(packet)

    return i, (opcode, packets)

def eval_optree(optree):

    if type(optree) == tuple:
        op, content = optree
        return op(eval_optree(content))

    elif type(optree) == list:
        vals = []
        for (op, content) in optree:
            if op == "val":
                vals.append(content)
            else:
                vals.append(op(eval_optree(content)))

        return tuple(vals)

    assert False
    


def eval_bs(packetstr):
    print(packetstr)
    bs = hextobin(packetstr)
    i = 0

    parse_index, ptree = parse_packet(bs, 0)
    print(ptree)
    res = eval_optree(ptree)
    print(res)
    return res


def add_version_numbers(packetstr):

    print(packetstr)

    bs = hextobin(packetstr)
    i = 0

    vsum = 0

    while True:

        min_packet_len = 6 + 1 + 5
        if i >= len(bs) - min_packet_len:
            break

        v = int(bs[i : i + 3], 2)
        i += 3

        t = int(bs[i : i + 3], 2)
        i += 3

        vsum += v

        # Packets with type ID 4 represent a literal value
        if t == 4:
            # print(f"literal value at {i}")
            i, num = decode_num(bs, i)
            continue

        # any packet with a type ID other than 4 represent an operator
        # An operator packet contains one or more packets
        # bit immediately after the packet header; this is called the length type ID

        l = int(bs[i])
        i += 1
        # If the length type ID is 0, then the next 15 bits are a number
        # that represents the total length in bits of the sub-packets contained by this packet.
        if l == 0:
            # print(f"l==0 at {i}")
            i += 15
            continue

        # If the length type ID is 1, then the next 11 bits are a number
        # that represents the number of sub-packets immediately contained by this packet
        if l == 1:
            # print(f"l==1 at {i}")
            i += 11
            continue

    # print("")

    return vsum


if __name__ == "__main__":

    # assert add_version_numbers("38006f45291200") == 1
    assert add_version_numbers("38006F45291200") == 1 + 6 + 2
    assert add_version_numbers("ee00d40c823060") == 7 + 2 + 4 + 1
    assert add_version_numbers("8A004A801A8002F478") == 16
    assert add_version_numbers("620080001611562C8802118E34") == 12
    assert add_version_numbers("C0015000016115A2E0802F182340") == 23
    assert add_version_numbers("A0016C880162017C3686B18A3D4780") == 31
    print(add_version_numbers(open("input.txt", "r").read()))


    eval_bs("38006F45291200")
    eval_bs("ee00d40c823060")
    # eval_bs("8A004A801A8002F478")
    # eval_bs("620080001611562C8802118E34")
    eval_bs("C0015000016115A2E0802F182340")
    eval_bs("A0016C880162017C3686B18A3D4780")
    
    assert eval_bs("C200B40A82") == 3
    # 04005AC33890 finds the product of 6 and 9, resulting in the value 54.
    assert eval_bs("04005AC33890") == 54
    assert eval_bs("880086C3E88112") == 7
    assert eval_bs("CE00C43D881120") == 9
    assert eval_bs("D8005AC2A8F0") == 1
    assert eval_bs("F600BC2D8F") == 0
    assert eval_bs("9C005AC2F8F0") == 0
    assert eval_bs("9C0141080250320F1802104A08") == 1

    print(eval_bs(open("input.txt", "r").read()))

