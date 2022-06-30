import encode

import Messages
import CmdLineHandler
import sys
import Encoder
import Decoder
import os

# Static globals
# Eof = 0xFFFEOF
_Eof = ['11', '11', '11', '11', '11', '11', '11', '11', '11', '11', '11', '11',
        '01', '00', '01', '01', '01', '00', '11', '11', '01', '00', '01', '10']

def writeBinFile(APayload, AFileName):
    with open(AFileName, 'wb') as txtFile:
        txtFile.write(APayload)
    txtFile.close()

    # ==============================================================================

if __name__ == '__main__':
    cmdHandler = CmdLineHandler.CmdLnHandler(sys.argv)

    if cmdHandler.isEncodeMode():
        Messages.info('Encoder selected.')
        encoderObj = Encoder.Encoder(cmdHandler.payload, cmdHandler.image, cmdHandler.output, int(cmdHandler.buffer))
        encoderObj.encode()
        Messages.info('Finished encoding. Find encoded image saved as ' + cmdHandler.output)
    elif cmdHandler.isDecodeMode():
        Messages.info('Decoder selected.')
        decoderObj = Decoder.Decoder(cmdHandler.payload, 2)
        endPayload = decoderObj.decode()
        writeBinFile(endPayload, cmdHandler.output)
        Messages.info('Finished decoding. Payload saved to ' + cmdHandler.output)
