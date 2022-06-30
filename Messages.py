'''==============================================================================
*   These are formatted message dialogues for the SCM script generator tool.
*
*   Author: Marc Geffroy
*   Date: 21 Apr 2021
*
*	Modified: 28 Apr 2021
=============================================================================='''
import os
import sys
import datetime
import time

def usage():
    print("""
    =====================================================
    +++++++++++++++++++++++++++++++++++++++++++++++++++++
                    
                    *** Encrypting Tool ***
                    -----------------------             
               
    +++++++++++++++++++++++++++++++++++++++++++++++++++++
    =====================================================
    
    usage:  Steganography.py [--help]
            Steganography.py [--version]
            Steganography.py [-e] [-p=file] [-f=file] [-b=integer] 
            Steganography.py [-d] [-p=file] [-b=integer]
            
    Examples:
            Steganography.py -e -p "HideMe.txt" -f "NothingHere.png"
                                
    Arguments:
    --help       - Display help.
    --version    - Display the version.
    -e           - Select encoder mode.
    -d           - Select decoder mode.
    -p           - Select payload file.
    -f           - Select File to hide payload in.
    -b           - Buffer size in bits (Not being used yet).
    
    Report bugs to Marc at Marc.Geffroy@cobham.com
    
    """)
    sys.exit(1)

#==============================================================================

def version( AVersion ):
    print("""
    =====================================================
    +++++++++++++++++++++++++++++++++++++++++++++++++++++
                    
                    *** Encrypting Tool ***
                    -----------------------             
               
    +++++++++++++++++++++++++++++++++++++++++++++++++++++
    =====================================================
    
		      Version:""" + AVersion + '\n\n')
    sys.exit(1)

#==============================================================================

def info(message, output = None):
    if output is None:
        out = sys.stdout
    else:
        out = open(output, 'w')
    try:
        out.write(time.strftime("%b %d %Y %H:%M:%S", time.localtime()) + " | Info: " + str(message) + '\n')
    finally:
        if output is not None:
            out.close()

#==============================================================================

def warning(message, output = None):
    if output is None:
        out = sys.stdout
    else:
        out = open(output, 'w')
    try:
        out.write(time.strftime("%b %d %Y %H:%M:%S", time.localtime()) + " | Warning: " + message + '\n')
    finally:
        if output is not None:
            out.close()

#==============================================================================

def error(message, output = None):
    if output is None:
        out = sys.stdout
    else:
        out = open(output, 'w')
    try:
        out.write(time.strftime("%b %d %Y %H:%M:%S", time.localtime()) + " | ERROR: " + message + '\n')
    finally:
        if output is not None:
            out.close()

#==============================================================================

def debug(message, output = None):
    try:
        out = open("debug.txt", 'w')
        out.write(time.strftime("%b %d %Y %H:%M:%S", time.localtime()) + message + '\n')
    finally:
        out.close()