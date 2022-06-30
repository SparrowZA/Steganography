'''==============================================================================
*	This is a proof of concept to test whether by using a master list of tests a
*	number of sub scripts can be created automatically  application.
*
*	Authors: Marc Geffroy
*	Date:   27 Jan 2021
*
*	Last Modified:  28 Jan 2021
=============================================================================='''

import getopt
import Messages


class CmdLnHandler:
    opts = []
    args = []
    mode = ''
    payload = ''
    image = ''
    output = ''
    buffer = 2

    def __init__(self, AArgv):
        try:
            self.opts, self.args = getopt.getopt(AArgv[1:], 'e,d,p:,f:,o:,b:', ['help', 'version'])

            if self.isVersionRequest():
                Messages.version( 'v1.0.0.0' )
            elif self.isHelpRequest():
                Messages.usage()
            elif self.isEncodeMode():
                if len(self.opts) == 5:
                    self.getMode()
                    self.getPayloadFile()
                    self.getImageFile()
                    self.getOutputFile()
                    self.getBuffer()
                else:
                    Messages.error('Incorrect number of parameters.')
                    Messages.usage()
            elif self.isDecodeMode():
                if len(self.opts) == 4:
                    self.getMode()
                    self.getPayloadFile()
                    self.getOutputFile()
                    self.getBuffer()
                else:
                    Messages.error('Incorrect number of parameters.')
                    Messages.usage()
            else:
                Messages.usage()
        except getopt.GetoptError as err:
            Messages.error('Exception occurred while getting command-line options: %s!!\r\n' % str(err))
            Messages.usage()

    def isEncodeMode(self):
        for opt, arg in self.opts:
            if opt == '-e':
                return True
            else:
                return False

    def isDecodeMode(self):
        for opt, arg in self.opts:
            if opt == '-d':
                return True
            else:
                return False

    def isVersionRequest(self):
        for opt, arg in self.opts:
            if opt == '--version':
                return True
            else:
                return False

    def isHelpRequest(self):
        for opt, arg in self.opts:
            if opt == '--help':
                return True
            else:
                return False

    def getMode(self):
        for opt, arg in self.opts:
            if opt == '-e':
                self.mode = opt
                break
            elif opt == '-d':
                self.mode = opt
                break

    def getPayloadFile(self):
        for opt, arg in self.opts:
            if opt == '-p' and arg != '':
                self.payload = arg
            elif opt == '-p' and arg == '':
                Messages.error('No payload file specified.')
                Messages.usage()

    def getImageFile(self):
        for opt, arg in self.opts:
            if opt == '-f' and arg != '':
                self.image = arg
            elif opt == '-f' and arg == '':
                Messages.error('No image file specified.')
                Messages.usage()

    def getOutputFile(self):
        for opt, arg in self.opts:
            if opt == '-o' and arg != '':
                self.output = arg
            elif opt == '-o' and arg == '':
                Messages.error('No output file specified.')
                Messages.usage()

    def getBuffer(self):
        for opt, arg in self.opts:
            if opt == '-b' and arg != '':
                self.buffer = arg
            elif opt == '-b' and arg == '':
                Messages.error('No buffer amount.')
                Messages.usage()
            elif opt == '-b' and int(arg) > 8:
                Messages.error('Buffer must be between 0 and 8.')
                Messages.usage()
