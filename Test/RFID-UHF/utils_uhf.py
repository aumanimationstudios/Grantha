#!/usr/bin/python2
# *-* coding: utf-8 *-*

from binascii import hexlify, unhexlify
import collections


# class returnData:
#     01_22 = "REQUEST_FAIL"


def severalTimesPollingCommandGen(pollingtime):
    """
    Generate Several times polling command based on given decimal number.
    :param pollingtime:
    :return pollingCommandFinal:
    """
    pollingtimeHex = hex(pollingtime)

    pollingCommand = "0027000322" + pollingtimeHex[2:].zfill(4)

    checksum = checksumCalculator(pollingCommand)

    pollingCommandFinal = "BB"+pollingCommand+checksum+"7E"

    return (pollingCommandFinal)


def readVerifier(dataHex):
    """
    Verifier for single and Multi Polling Command Response Frames.
    :param dataHex:
    :return dataDict:
    """
    dataArray = dataHex.split("7EBB")

    cleanDataArray = []

    for x in dataArray:
        if x.startswith("BB"):
            if(x.endswith("7E")):
                y = x[2:-2]
                cleanDataArray.append(y)
            else:
                y = x[2:]
                cleanDataArray.append(y)

        elif x.endswith("7E"):
            z = x[:-2]
            cleanDataArray.append(z)

        else:
            cleanDataArray.append(x)

    dataDict = collections.OrderedDict()
    # print (cleanDataArray)

    for x in cleanDataArray:
        Type = x[0:2]

        Command = x[2:4]

        if len(x) == 44:
            if Type == '02' and Command == '22':
                EPC = x[14:38]
                RSSI = x[8:10]
                returnDict = {}
                returnDict["EPC"] = EPC
                returnDict["RSSI"] = RSSI
                dataDict[EPC] = returnDict
                # print (dataDict)

            # elif Type == '01' and Command == 'FF':
            #     # print "No Cards Detected!"
            #     # self.ui.textEdit01.setTextColor(self.redColor)
            #     # msg = "NO CARDS DETECTED!"
            #     return (dataDict)

    # if not dataDict:
    #     # print "No Cards Detected!"
    #     # self.ui.textEdit01.setTextColor(self.redColor)
    #     msg = "NO CARDS DETECTED!"
    #     return (msg)
    #
    # else:
    return (dataDict)
            # return (x)
            # self.ui.textEdit01.setTextColor(self.blueColor)
            # self.ui.textEdit01.append(x)



def setPowerCommandGen(power):
    """
    Generate set power command based on given decimal number.
    :param power:
    :return setCommandFinal:
    """
    powerHex = hex(power)
    setCommand = "00B60002" + powerHex[2:].zfill(4)

    checksum = checksumCalculator(setCommand)

    setCommandFinal = "BB"+setCommand+checksum+"7E"

    return setCommandFinal


def checksumCalculator(hexStr):
    """
    Calculate checksum of a given hex string.
    :param hexStr:
    :return checksumHex:
    """
    byteStr = hex_to_bytes(hexStr)

    checksum = 0
    for ch in byteStr:
        checksum += ord(ch)

    checksumHex = hex(checksum)
    return (checksumHex[-2:].upper())

#-------------------------------------------------------------------------------

def bytes_to_hex( byteStr ):
    """
    Convert a byte string to it's hex string representation e.g. for output.
    """
    # Uses list comprehension which is a fractionally faster implementation than
    # the alternative, more readable, implementation below
    #
    #    hex = []
    #    for aChar in byteStr:
    #        hex.append( "%02X " % ord( aChar ) )
    #
    #    return ''.join( hex ).strip()
    return ''.join( [ "%02X" % ord( x ) for x in byteStr ] ).strip()

#-------------------------------------------------------------------------------

def hex_to_bytes( hexStr ):
    """
    Convert a string hex byte values into a byte string. The Hex Byte values may
    or may not be space separated.
    """
    # The list comprehension implementation is fractionally slower in this case
    #
    #    hexStr = ''.join( hexStr.split(" ") )
    #    return ''.join( ["%c" % chr( int ( hexStr[i:i+2],16 ) ) \
    #                                   for i in range(0, len( hexStr ), 2) ] )
    bytes = []
    hexStr = ''.join( hexStr.split(" ") )
    for i in range(0, len(hexStr), 2):
        bytes.append( chr( int (hexStr[i:i+2], 16 ) ) )
    return ''.join( bytes )

