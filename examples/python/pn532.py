#!/usr/bin/python
# Author: Zion Orent <zorent@ics.com>
# Copyright (c) 2015 Intel Corporation.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import time, sys, signal, atexit
import pyupm_pn532 as upmPn532

def main():
    # Instantiate an PN532 on I2C bus 0 (default) using gpio 3 for the
    # IRQ, and gpio 2 for the reset pin.
    myNFC = upmPn532.PN532(3, 2)

    ## Exit handlers ##
    # This stops python from printing a stacktrace when you hit control-C
    def SIGINTHandler(signum, frame):
        raise SystemExit

    # This lets you run code on exit
    def exitHandler():
        print "Exiting"
        sys.exit(0)

    # Register exit handlers
    atexit.register(exitHandler)
    signal.signal(signal.SIGINT, SIGINTHandler)

    if (not myNFC.init()):
        print "init() failed"
        sys.exit(0)

    vers = myNFC.getFirmwareVersion()

    if (vers):
        print "Got firmware version: %08x" % vers
    else:
        print "Could not identify PN532"
        sys.exit(0)

    # Now scan and identify any cards that come in range (1 for now)

    # Retry forever
    myNFC.setPassiveActivationRetries(0xff)

    myNFC.SAMConfig()

    uidSize = upmPn532.uint8Array(0)
    uid = upmPn532.uint8Array(7)

    while (1):
        for i in range(7):
            uid.__setitem__(i, 0)
        if (myNFC.readPassiveTargetID(upmPn532.PN532.BAUD_MIFARE_ISO14443A,
                                      uid, uidSize, 2000)):
            # found a card
            print "Found a card: UID len", uidSize.__getitem__(0)
            print "UID: ",
            for i in range(uidSize.__getitem__(0)):
                print "%02x" % uid.__getitem__(i),
            print
            print "SAK: %02x" % myNFC.getSAK()
            print "ATQA: %04x" % myNFC.getATQA()
            print
            time.sleep(1)
        else:
            print "Waiting for a card...\n"

if __name__ == '__main__':
    main()
