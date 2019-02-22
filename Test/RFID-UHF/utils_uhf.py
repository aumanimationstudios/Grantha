#!/usr/bin/python2
# *-* coding: utf-8 *-*

from binascii import hexlify, unhexlify

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
    return (checksumHex[-2:])

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

