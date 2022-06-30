def chrToBitArray(ACharacter):
    result = []
    bits = bin(ACharacter)[2:]
    bits = '00000000'[len(bits):] + bits
    result.extend(bits[b: b + 2] for b in range(0, len(bits), 2))
    return result


def strToBitArray(APayload):
    result = []
    for x in APayload:
        result += chrToBitArray(x)
    return result


def zeroRightMostBits(ABinaryValue):
    x = bin(ABinaryValue)[:-2]
    x = bin(int(x, 2) << 2)
    return x


def removeSpaceFrmString(AStr):
    return AStr.replace(" ", "")


def isPayloadLengthLessThanBaseString(APayloadArray, ABaseStr):
    # Remove white spaces from hider base string
    if len(APayloadArray) <= len(removeSpaceFrmString(ABaseStr)):
        return True
    else:
        return False


def byteArrToStr(AByteArr):
    result = ''
    for byte in AByteArr:
        result += chr(byte)
    return result


def PayloadBaseLengthDif(APayloadBitArray, ABinBaseString):
    if((len(str(ABinBaseString).replace(" ", "")) - len(APayloadBitArray)) >= 3):
        return 3
    else:
        return ABinBaseString - APayloadBitArray


def encodePayload(APayloadBitArray, ABinBaseString):
    # Take each byte from the hider string. Zero the 2 least significant
    # bits and OR the payload bits to the byte.
    # lenDif = PayloadBaseLengthDif(APayloadBitArray, ABinBaseString)
    count = 0
    finalStrArray = []
    for i in range(0, len(ABinBaseString) - 1):
        if (ABinBaseString[i] != 32) and (count < (len(APayloadBitArray) + 4)):  # Only change if the char is not a space
            bufferedByte = zeroRightMostBits(ABinBaseString[i])
            if(count < len(APayloadBitArray)):
                finalStrArray.append((int(bufferedByte, 2) | int(APayloadBitArray[count], 2)))
            else:
                finalStrArray.append(int(bufferedByte, 2))
            count += 1
        else:
            finalStrArray.append(ABinBaseString[i])
    return byteArrToStr(finalStrArray)


def bitsToByte(APayload):
    # Takes an array of bits and returns a 2D array of Bytes
    _EOFByte = ['0', '0', '0', '0', '0', '0', '0', '0']
    byte = []
    result = []
    for count in range(0, len(APayload)):
        if len(byte) == 7:
            byte += APayload[count]
            # if(byte == _EOFByte): # Check for empty Byte (EoF signaler)
            #     return result
            result.append(byte)
            byte = []
        else:
            byte += APayload[count]
    return result


def bitsToInt(ABitArray):
    # Takes 2D array of bytes and converts them into a string
    Payload = []
    PayloadByte = ''
    for byte in ABitArray:
        # for bit in byte:
        #     PayloadByte += bit
        Payload.append( int(PayloadByte, 2) )
        # Payload += ( int(PayloadByte, 2))
        PayloadByte = ''
    return bytes(Payload)


def lftChrToBitArray(ACharacter):
    # Takes a character and returns the 2 least significant bits
    if len(ACharacter) < 2:
        bits = bin(ord(ACharacter))[2:]
        result = bits[-2:]
        return result
    else:
        print('Length of character to hide was too long')


def getLeastSignificantBit(APayload):
    # Takes a string and returns an array of bits
    result = []
    for x in APayload:
        result += lftChrToBitArray(x)
    return result