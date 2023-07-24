test_bytes = b'\x12\x34\x56\x73\x0a\x1b\x2c\x3d'

xor_gt = 3
xor = test_bytes[0]
for b in test_bytes[1:]:
    xor = xor ^ b

assert xor == xor_gt