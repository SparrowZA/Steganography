import Messages
from cv2 import cv2
import os

class Encoder:
    payloadFile = ''
    imageFile = ''
    output = ''
    bufferSize = 0
    _Eof = ['11', '11', '11', '11', '11', '11', '11', '11', '11', '11', '11', '11',
            '01', '00', '01', '01', '01', '00', '11', '11', '01', '00', '01', '10']

    def __init__(self, APayload, AImgFile, AOutput, ABufferSize = 2):
        self.payloadFile = APayload
        self.imageFile = AImgFile
        self.output = AOutput
        self.bufferSize = ABufferSize
        # vPayloadBin = self.readFileBin(APayload)
        # payloadBinArray = encode.strToBitArray(rawPayload)

    def encode(self):
        payloadBin = self.readFileBin(self.payloadFile)

        img = self.readImgFile(self.imageFile)
        Messages.info('Image read.')

        #Convert binary file into array of bit pairs
        payloadArr = self._convertFileToBinArr(payloadBin)
        Messages.info('Payload converted into 2-bit array.')

        payloadImg = self._encodeToImg(payloadArr, img, self.bufferSize)
        Messages.info('Finished encoding payload into img.')

        Messages.info('Writing img to file.')
        self.writeBinToImg(payloadImg, self.output)

    def _encodeToImg(self, APayload, AImg, Abuf):
        # Retrieve image properties: Width, length, channels (RGB)
        imgWidth = len(AImg[:])
        imgLength = len(AImg[0, :])
        imgChannels = len(AImg[0, 0, :])
        countPayload = 0
        countEof = 0

        if len(APayload) < (imgWidth * imgLength * imgChannels):
            for widPxl in range(0, imgWidth):
                for lenPxl in range(0, imgLength):
                    for chn in range(0, imgChannels):
                        if countPayload < (len(APayload)):
                            bufferedByte = self.zeroRightMostBits(AImg[widPxl, lenPxl, chn], Abuf)
                            if countPayload < len(APayload):
                                AImg[widPxl, lenPxl, chn] = (int(bufferedByte, 2) | int(APayload[countPayload], 2))
                            else:
                                AImg[widPxl, lenPxl, chn] = int(bufferedByte, Abuf)
                            countPayload += 1
                        elif (countPayload < (len(APayload) + 24)) and (countEof < 24):
                            if countEof == 0:
                                Messages.info('Starting to encode EoF')
                            bufferedByte = self.zeroRightMostBits(AImg[widPxl, lenPxl, chn], Abuf)
                            AImg[widPxl, lenPxl, chn] = (int(bufferedByte, 2) | int(self._Eof[countEof], 2))
                            countEof += 1
                        else:
                            return AImg
        else:
            Messages.error("The payload you are trying to embedded is bigger than the picture.")

        Messages.info('Encoding done.')
        return AImg

    def _convertFileToBinArr(self, APayloadBin):
        result = []
        for byte in APayloadBin:
            result += self.byteToBitArray(byte, self.bufferSize)
        return result

    @staticmethod
    def addBuffer(Abits, ABufferSize):
        while len(Abits) < ABufferSize:
            Abits = Abits + '0'
        return Abits

    @staticmethod
    def byteToBitArray(AByte, ABufferSize):
        result = []
        bits = bin(AByte)[2:]
        bits = '00000000'[len(bits):] + bits
        for b in range(0, len(bits), ABufferSize):
            x = bits[b: b + ABufferSize]
            if len(x) != ABufferSize:
                x = Encoder.addBuffer(x, ABufferSize)
            result.append(x)
        return result

    @staticmethod
    def zeroRightMostBits(ABinaryValue, Abuf):
        # Messages.info(bin(ABinaryValue))
        # Messages.info(ABinaryValue)
        bits = bin(ABinaryValue)[2:]
        x = '00000000'[len(bits):] + bits
        x = x[:-Abuf]
        x = bin(int(x, 2) << Abuf)
        return x

    @staticmethod
    def writeBinToImg(APayloadImg, AImgName):
        cv2.imwrite(AImgName, APayloadImg)
    
    @staticmethod
    def readFileBin(APayload):
        try:
            with open(APayload, 'rb') as file:
                Messages.info('Found payload file.')
                payloadBin = file.read()
                Messages.info('Read payload.')
            file.close()
            Messages.info('closed payload file.')
            return payloadBin
        except:
            Messages.error('Something went very wrong!')

    @staticmethod
    def readImgFile(AImgFile):
        try:
            if os.path.isfile(AImgFile):
                img = cv2.imread(AImgFile, cv2.IMREAD_COLOR)
                Messages.info('Reading image file.')
                return img
            else:
                Messages.error('Could not find file.')
        except:
            Messages.error('Something went very wrong!')
