def left_rotate(value, shift):
    return ((value << shift) | (value >> (32 - shift))) & 0xFFFFFFFF

def md5(message):
    # Khởi tạo các biến ban đầu
    a = 0x67452301
    b = 0xEFCDAB89
    c = 0x98BADCFE
    d = 0x10325476

    # Tiền xử lý chuỗi văn bản
    original_length = len(message) * 8  # Độ dài ban đầu tính bằng bit
    message += b'\x80'
    while (len(message) * 8) % 512 != 448:
        message += b'\x00'
    message += original_length.to_bytes(8, 'little')

    # Chia chuỗi thành các block 512-bit (64 byte)
    for i in range(0, len(message), 64):
        block = message[i:i+64]
        words = [int.from_bytes(block[j:j+4], 'little') for j in range(0, 64, 4)]
        a0, b0, c0, d0 = a, b, c, d

        # Vòng lặp chính của thuật toán MD5
        for j in range(64):
            if j < 16:
                f = (b & c) | ((~b) & d)
                g = j
            elif j < 32:
                f = (d & b) | ((~d) & c)
                g = (5 * j + 1) % 16
            elif j < 48:
                f = b ^ c ^ d
                g = (3 * j + 5) % 16
            else:
                f = c ^ (b | (~d))
                g = (7 * j) % 16

            # Sử dụng hằng số đúng cho MD5
            if j < 16:
                k = 0x5A827999
            elif j < 32:
                k = 0x6ED9EBA1
            elif j < 48:
                k = 0x8F1BBCDC
            else:
                k = 0xCA62C1D6

            temp = d
            d = c
            c = b
            b = (b + left_rotate((a + f + k + words[g]) & 0xFFFFFFFF, [7, 12, 17, 22, 5, 9, 14, 20, 4, 11, 16, 23, 6, 10, 15, 21][j % 16])) & 0xFFFFFFFF
            a = temp

        # Cập nhật giá trị
        a = (a + a0) & 0xFFFFFFFF
        b = (b + b0) & 0xFFFFFFFF
        c = (c + c0) & 0xFFFFFFFF
        d = (d + d0) & 0xFFFFFFFF

    # Kết hợp các giá trị cuối cùng
    digest = (a.to_bytes(4, 'little') + b.to_bytes(4, 'little') + 
             c.to_bytes(4, 'little') + d.to_bytes(4, 'little'))
    return digest.hex()

# Nhập và xử lý chuỗi
input_string = input("Nhập chuỗi cần băm: ")
md5_hash = md5(input_string.encode('utf-8'))
print("Mã băm MD5 của chuỗi '{}' là: {}".format(input_string, md5_hash))