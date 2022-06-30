'''
    #
    # This is an application that reads a file and breaks it
    # into 2 bit segments and then hides it in the least significant
    # bits of another string.
    #
'''

_EOFByte = ['0', '0', '0', '0', '0', '0', '0', '0']

def chrToBitArray(ACharacter):
    result = []
    if len(ACharacter) < 2:
        bits = bin(ord(ACharacter))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend(bits[b: b + 2] for b in range(0, len(bits), 2))
        return result
    else:
        print('Length of character to hide was too long')


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
    byte = []
    result = []
    for count in range(0, len(APayload)):
        if len(byte) == 7:
            byte += APayload[count]
            if(byte == _EOFByte): # Check for empty Byte (EoF signaler)
                return result
            result.append(byte)
            byte = []
        else:
            byte += APayload[count]
    return result


def bitsToStr(ABitArray):
    # Takes 2D array of bytes and converts them into a string
    Payload = []
    PayloadByte = ''
    for byte in ABitArray:
        for bit in byte:
            PayloadByte += bit
        Payload.append( chr(int(PayloadByte, 2)))
        PayloadByte = ''
    return Payload


def lftChrToBitArray(ACharacter):
    # Takes a character and returns the 2 least significant bits
    if len(ACharacter) < 2:
        bits = bin(ord(ACharacter))[2:]# [2:] use to remove the "0b" before the binary represention
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


def decodePayload(APayload):
    APayload = removeSpaceFrmString(APayload)
    APayload = getLeastSignificantBit(APayload)
    APayload = bitsToByte(APayload)
    APayload = bitsToStr(APayload)
    return ''.join(APayload)


# =================================================================================
# Main method
# =================================================================================

if __name__ == '__main__':
    finalStrArray = []

    # The string used to hide the file in
    _BaseString = 'Quartan malaria, with its dreaded recurrence of chills and high fever every fourth day, ' \
                  'claimed an untold number of lives in Italy during the Middle Ages. So familiar were its ' \
                  'ominous signs that a fourteenth century Italian poet seeking to fill readers with bone quaking ' \
                  'fear need only conjure the image of a man who in a shivering fit of quartan fever, so ill ' \
                  'his nails have lost all color, trembles all over at the sight of shade. Dante identified ' \
                  'with malaria victims whose suffering he had seen with his own eyes to convey his deathly ' \
                  'fright at having to fly to a lower circle of hell on the back of Geryon, a monster with an ' \
                  'honest looking human face fronting a serpentine body with leonine paws and a scorpions tail. ' \
                  'The writer of those words now experienced firsthand the sweats, chills, and aches of the ' \
                  'debilitating illness.'

    hiddenFileName = 'HideMe.txt'

    # =================================================================================
    # This is the encoding of the payload
    # =================================================================================
    # Read payload file
    with open(hiddenFileName, "r") as txtFile:
        payload = txtFile.read()
    txtFile.close()

    # Encode hider base string to ASCII
    binBaseString = _BaseString.encode('ascii')

    # Break the payload string into array of 2 bits
    payloadArray = strToBitArray(payload)

    if isPayloadLengthLessThanBaseString(payloadArray, _BaseString):
        payload = encodePayload(payloadArray, binBaseString)
    else:
        print('The length of the payload an the hider string were not equal.')
        print('The payload requires ' + str(len(payloadArray)) + ' bytes.')
        print('The hider string was ' + str(len(_BaseString.replace(" ", ""))) + ' bytes.')
        SystemExit

    with open('PayloadFile.txt', "w") as txtFile:
        txtFile.write(payload)
    txtFile.close()

    # =================================================================================
    # This is the decoding of the payload
    # =================================================================================

    DecodedMessage = decodePayload(payload)

    with open('newFile.txt', "w") as txtFile:
        txtFile.write(DecodedMessage)
    txtFile.close()
