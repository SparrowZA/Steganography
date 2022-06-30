import Messages
from cv2 import cv2
import os

class Decoder:
    imgFile = ''
    buffer = 0

    def __init__(self, AImgFile, ABufferSize=2):
        self.imgFile = AImgFile
        self.buffer = ABufferSize

    def decode(self):
        Messages.info('Reading Image.')
        payloadImg = self.readImgFile(self.imgFile)

        Messages.info('Getting payload')
        payload = self.getPayloadBitArray(payloadImg)

        Messages.info('byteArrToBin')
        payload = self.byteArrToBin(payload)
        return payload

    def getPayloadBitArray(self, AImg):
        # Retrieve image properties: Width, length, channels (RGB)
        imgWidth = len(AImg[:])
        imgLength = len(AImg[0, :])
        imgChannels = len(AImg[0, 0, :])
        payload = []
        byte = ''
        _Eof = ['11111111', '11111111', '11111111',
                '01000101', '01001111', '01000110']

        for widPxl in range(0, imgWidth):
            for lenPxl in range(0, imgLength):
                for chn in range(0, imgChannels):
                    byte += self.intToBitArray(AImg[widPxl, lenPxl, chn], self.buffer, 1)
                    if len(byte) == 8:
                        # if len(payload) > 2683594:
                        #     Messages.info('Byte: ' + byte)

                        payload.append(byte)
                        if payload[-6:] == _Eof:
                            Messages.info(len(payload))
                            Messages.info(payload[-6:])
                            return payload[:-6]
                        byte = ''
        return payload

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
            Messages.error('Something went terribly wrong!')

    @staticmethod
    def intToBitArray(AValue, ABuffer=8, ADir=0):
        result = ''
        if ADir == 1:
            bits = bin(AValue)[2:]
            bits = '00000000'[len(bits):] + bits
            result = bits[-ABuffer:]
        else:
            bits = bin(ord(AValue))[2:]
            bits = '00000000'[len(bits):] + bits
            result = bits[:ABuffer]
        return result

    @staticmethod
    def byteArrToBin(APayload):
        payload = []
        for byte in APayload:
            payload.append(int(byte, 2))
        return bytes(payload)