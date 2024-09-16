#!/usr/bin/env python3

#   Send GetUID command to the first inserted card
#   Copyright (C) 2024  Numericoach
#
#   This library is free software; you can redistribute it and/or
#   modify it under the terms of the GNU Lesser General Public
#   License as published by the Free Software Foundation; either
#   version 2.1 of the License, or (at your option) any later version.
#
#   This library is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#   Lesser General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public
#   License along with this library; if not, write to the Free Software
#   Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from smartcard.CardType import AnyCardType
from smartcard.CardRequest import CardRequest
from smartcard.util import toHexString

# 10 seconds timeout
TIMEOUT = 10

# Wait for a card insertion
cardrequest = CardRequest(timeout=TIMEOUT, cardType=AnyCardType())
print(f"Insert a card within {TIMEOUT} seconds")
cardservice = cardrequest.waitforcard()

# Connect to the card
cardservice.connection.connect()

# Get information
print("Using:", cardservice.connection.getReader())
print("Card ATR:", toHexString(cardservice.connection.getATR()))

# define the APDUs used in this script
# 5321-903_b.4_omnikey_contactless_developer_guide_en.pdf
# page 82, A.7.1 Getting the Card UID (PC/SC 2.01)

GETUID = [0xFF, 0xCA, 0x00, 0x00, 0x00]

# Get UID
data, sw1, sw2 = cardservice.connection.transmit(GETUID)
print("UID:", toHexString(data))
print("SW: %02X %02X" % (sw1, sw2))

card_number = int.from_bytes(data, byteorder='little')
print("Card number:", card_number)
