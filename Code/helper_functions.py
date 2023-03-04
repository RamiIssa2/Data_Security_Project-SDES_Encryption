import numpy as np


def generate_key(n):
    return np.random.choice([0, 1], size=n, p=[0.5, 0.5])


def convert_text_to_binary(message):
    temp, res = [], []
    for letter in message:
        temp.append(format(ord(letter), '08b'))
    for i in temp:
        for r in i:
            res.append(int(r))

    res = [res[i: i + 12] for i in range(0, len(res), 12)]
    final_res = []
    for rs in res:
        tmp_res = []
        for r in rs:
            tmp_res.append(r)
        for i in range(12 - len(rs)):
            tmp_res.append(0)
        final_res.append(tmp_res)

    return final_res


def convert_binary_to_text(b_text, is_encrypt):
    tmp = []
    for ts in b_text:
        for t in ts:
            tmp.append(t)

    tmp_b_text = [tmp[i: i + 8] for i in range(0, len(tmp), 8)]
    final_text = ""
    for B in tmp_b_text:
        tmp = 0
        for b in B:
            tmp *= 2
            tmp += b
        if tmp != 0 or is_encrypt:
            final_text += chr(tmp)

    return final_text


def xor(a, b):
    assert (len(a) == len(b)), "XOR ERROR"
    res = []
    for i in range(len(a)):
        if a[i] == b[i]:
            res.append(0)
        else:
            res.append(1)
    return res


def f_function(r, k):
    expansion_list = [0, 1, 3, 2, 3, 2, 4, 5]
    s1 = [
            [[1, 0, 1], [0, 1, 0], [0, 0, 1], [1, 1, 0], [0, 1, 1], [1, 0, 0], [1, 1, 1], [0, 0, 0]],
            [[0, 0, 1], [1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 0, 0], [1, 1, 1], [1, 0, 1], [0, 1, 1]]
         ]
    s2 = [
            [[1, 0, 0], [0, 0, 0], [1, 1, 0], [1, 0, 1], [1, 1, 1], [0, 0, 1], [0, 1, 1], [0, 1, 0]],
            [[1, 0, 1], [0, 1, 1], [0, 0, 0], [1, 1, 1], [1, 1, 0], [0, 1, 0], [0, 0, 1], [1, 0, 0]]
         ]

    expanded_r = [r[i] for i in expansion_list]
    xor_res = xor(expanded_r, k)

    left_part = xor_res[0: 4]
    right_part = xor_res[4:]

    s1_index = 0
    for j in range(1, 4):
        s1_index *= 2
        s1_index += left_part[j]
    s1_res = s1[left_part[0]][s1_index]

    s2_index = 0
    for j in range(1, 4):
        s2_index *= 2
        s2_index += right_part[j]
    s2_res = s2[right_part[0]][s2_index]

    final_res = s1_res + s2_res

    return final_res


def get_part_key(key, index):
    res_key = []
    for i in range(8):
        res_key.append(key[(index + i) % len(key)])
    return res_key


def encrypt_decrypt_step(bits, key, index, round_number, is_encrypt):
    old_l = bits[0: 6]
    old_r = bits[6:]

    if (index == round_number and is_encrypt) or (index == -1 and not is_encrypt):
        return old_r + old_l
    else:
        new_l = old_r
        new_r = xor(f_function(old_r, get_part_key(key, index)), old_l)

        if is_encrypt:
            new_index = index + 1
        else:
            new_index = index - 1
        return encrypt_decrypt_step(new_l + new_r, key, new_index, round_number, is_encrypt)


def encrypt(message, key, round_number):
    binary_message = convert_text_to_binary(message)
    final_binary_message = []

    for block in binary_message:
        final_binary_message.append(encrypt_decrypt_step(block, key, 0, round_number, True))
    return convert_binary_to_text(final_binary_message, True)


def decrypt(message, key, round_number):
    binary_message = convert_text_to_binary(message)
    final_binary_message = []

    for block in binary_message:
        final_binary_message.append(encrypt_decrypt_step(block, key, round_number - 1, round_number, False))

    return convert_binary_to_text(final_binary_message, False)


# Examples for using the function without the User Interface
if __name__ == "__main__":
    Key_length = 12
    full_key = generate_key(Key_length)
    rounds = 15

    Input_message = "Rami Issa is the best"

    encrypted_text = encrypt(Input_message, full_key, rounds)
    print(encrypted_text)

    decrypted_text = decrypt(encrypted_text, full_key, rounds)
    print(decrypted_text)

    example = [1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1]
    example_key = [1, 1, 1, 0, 0, 0, 1, 1, 1]
    e = encrypt_decrypt_step(example, example_key, 0, rounds, True)
    print(e)

    o = encrypt_decrypt_step(e, example_key, rounds - 1, rounds, False)
    print(example)
    print(o)
