
def _convertFileToBinArr(APayloadBin, ABufferSize):
    result = []
    for byte in APayloadBin:
        result += byteToBitArray(byte, ABufferSize)
    return result

def byteToBitArray(AByte, ABufferSize):
    result = []
    bits = bin(AByte)[2:]
    bits = '00000000'[len(bits):] + bits
    for b in range(0, len(bits), ABufferSize):
        x = bits[b: b + ABufferSize]
        if len(x) != ABufferSize:
            x = addBuffer(x, ABufferSize)
        result.append(x)
    return result

def addBuffer(Abits, ABufferSize):
    while len(Abits) < ABufferSize:
        Abits = Abits + '0'
    return Abits

if __name__=='__main__':
    payload = 'Test'.encode('ascii')
    print(payload)

    _convertFileToBinArr(payload, 3)