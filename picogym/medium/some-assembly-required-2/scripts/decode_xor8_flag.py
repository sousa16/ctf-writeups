# Decodes the flag for Some Assembly Required 2 by XORing each character with 8
encoded = "xakgK\\Ns><m:i1>1991:nkjl<ii1j0n=mm09;<i:u"

flag = ''.join(chr(ord(c) ^ 8) for c in encoded)
print(flag)
