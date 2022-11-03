# -*- coding: utf-8 -*-

"""
Dieser Quellcode ist in Python 3 geschrieben und enthält Funktionen zum
Senden und Empfangen von UDP-Nachrichten zwischen den Führertischrechnern
und dem Adapterprogramm.

This source code is written in Python 3 and contains functions for
sending and receiving UDP messages between the driver's desk computers and the
and the adapter programme.

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

TH Koeln, hereby disclaims all copyright interest in the software 'SchnittstelleFT.py'
(a software for sending and receiving UDP messages between
 the driver's desk computers and the and the adapter programme).

Wolfgang Evers
Versionsdatum 23.06.2022

"""

import struct  # Zur Umwandlung von Binärdaten in float

# Verarbeitung Daten für UDP-Telegramm an den Führertisch 1
def UDPAnzeigeDatenErzeugenFT1(Anzeigedaten):
    UDPDaten = bytearray()
    UDPDaten.extend(struct.pack("f", Anzeigedaten["Vist"]))                       # Byte  0- 3
    UDPDaten.extend(struct.pack("f", Anzeigedaten["Fzb"]))                        # Byte  4- 7
    UDPDaten.extend(struct.pack("f", Anzeigedaten["Fzba"]))                       # Byte  8-11
    UDPDaten.extend(struct.pack("f", Anzeigedaten["Fzbsoll"]))                    # Byte 12-15
    UDPDaten.extend(struct.pack("f", Anzeigedaten["Fzbasoll"]))                   # Byte 16-19
    UDPDaten.append ((Anzeigedaten["LMSchleudern"] << 7) +
                     (Anzeigedaten["LMGleiten"]    << 6) +
                     (Anzeigedaten["LMHS"]         << 5) +
                     (Anzeigedaten["LMGetriebe"]   << 4) +
                     (Anzeigedaten["LMZS"]         << 3) +
                     (Anzeigedaten["LMEB"]         << 2) +
                     (Anzeigedaten["LMHAB"]        << 1) +
                      Anzeigedaten["LMSifa"]           )                          # Byte 20
    UDPDaten.append(Anzeigedaten["LMTuer"]    & 0xf)                              # Byte 21
    UDPDaten.append(Anzeigedaten["FSt"]       & 0xff)                             # Byte 22
    UDPDaten.append((Anzeigedaten["LMUe"]     << 4) + Anzeigedaten["LMStoer"])    # Byte 23
    UDPDaten.append((Anzeigedaten["HupePZB"]  << 4) + Anzeigedaten["SummerTuer"]) # Byte 24
    UDPDaten.append (Anzeigedaten["HupeSifa"])                                    # Byte 25
    UDPDaten.extend(struct.pack("f", Anzeigedaten["AFBVsoll"]))                   # Byte 26-29
    UDPDaten.extend(struct.pack("f", Anzeigedaten["Uol"]))                        # Byte 30-33
    UDPDaten.extend(struct.pack("f", Anzeigedaten["Iol"]))                        # Byte 34-37
    UDPDaten.extend(struct.pack("f", Anzeigedaten["Umot"]))                       # Byte 38-41
    UDPDaten.extend(struct.pack("f", Anzeigedaten["Nmot"]))                       # Byte 42-45
    UDPDaten.extend(struct.pack("H", Anzeigedaten["AnzModus"]))                   # Byte 46-47
    return UDPDaten

# Verarbeitung Daten aus dem UDP-Telegramm vom Führertisch 1
def UDPAnzeigeDatenAuswertenFT1(UDPDaten, Anzeigedaten):
    hilf = struct.unpack("f",UDPDaten[ 0: 4])
    Anzeigedaten["Vist"] = hilf[0]
    hilf = struct.unpack("f",UDPDaten[ 4: 8])
    Anzeigedaten["Fzb"] = hilf[0]
    hilf = struct.unpack("f",UDPDaten[ 8:12])
    Anzeigedaten["Fzba"] = hilf[0]
    hilf = struct.unpack("f",UDPDaten[12:16])
    Anzeigedaten["Fzbsoll"] = hilf[0]
    hilf = struct.unpack("f",UDPDaten[16:20])
    Anzeigedaten["Fzbasoll"] = hilf[0]
    Anzeigedaten["LMSchleudern"] = (UDPDaten[20] & 0x80 == 128)
    Anzeigedaten["LMGleiten"]    = (UDPDaten[20] & 0x40 == 64)
    Anzeigedaten["LMHS"]         = (UDPDaten[20] & 0x20 == 32)
    Anzeigedaten["LMGetriebe"]   = (UDPDaten[20] & 0x10 == 16)
    Anzeigedaten["LMZS"]         = (UDPDaten[20] & 0x08 == 8)
    Anzeigedaten["LMEB"]         = (UDPDaten[20] & 0x04 == 4)
    Anzeigedaten["LMHAB"]        = (UDPDaten[20] & 0x02 == 2)
    Anzeigedaten["LMSifa"]       = (UDPDaten[20] & 0x01 == 1)
    Anzeigedaten["LMTuer"]       =  UDPDaten[21]       & 0xf
    Anzeigedaten["FSt"]          =  UDPDaten[22]
    Anzeigedaten["LMUe"]         = (UDPDaten[23] >> 4) & 0xf
    Anzeigedaten["LMStoer"]      =  UDPDaten[23]       & 0xf
    Anzeigedaten["HupePZB"]      = (UDPDaten[24] >> 4) & 0x0f
    Anzeigedaten["SummerTuer"]   =  UDPDaten[24]       & 0xf
    Anzeigedaten["HupeSifa"]     = (UDPDaten[25] & 0x01 == 1)
    hilf = struct.unpack("f",UDPDaten[26:30])
    Anzeigedaten["AFBVsoll"] = hilf[0]
    hilf = struct.unpack("f",UDPDaten[30:34])
    Anzeigedaten["Uol"] = hilf[0]
    hilf = struct.unpack("f",UDPDaten[34:38])
    Anzeigedaten["Iol"] = hilf[0]
    hilf = struct.unpack("f",UDPDaten[38:42])
    Anzeigedaten["Umot"] = hilf[0]
    hilf = struct.unpack("f",UDPDaten[42:46])
    Anzeigedaten["Nmot"] = hilf[0]
    hilf = struct.unpack("H",UDPDaten[46:48])
    Anzeigedaten["AnzModus"] = hilf[0]
    return None

def UDPBedienDatenErzeugenFT1(Bediendaten):
    UDPDaten = bytearray()
    UDPDaten.append(max(0,min(255,(Bediendaten["FS"] << 4) + Bediendaten["RS"] + 1)))
    UDPDaten.extend(struct.pack("f", Bediendaten["AFSZ"]))
    UDPDaten.append(Bediendaten["BS"] & 0xf)
    UDPDaten.extend(struct.pack("f", Bediendaten["ABS"]))
    UDPDaten.append((Bediendaten["TSifa"]  << 7) +
                    (Bediendaten["SLP"]    << 6) +
                    (Bediendaten["SLST"]   << 5) +
                    (Bediendaten["SLSW"]   << 4) +
                    (Bediendaten["TSAN"]   << 3) +
                    (Bediendaten["TSAH"]   << 2) +
                    (Bediendaten["THSA"]   << 1) +
                     Bediendaten["THSE"]       )
    UDPDaten.append((Bediendaten["SZSE"]   << 7) +
                    (Bediendaten["TZSA"]   << 6) +
                    (Bediendaten["Tb"]     << 5) +
                    (Bediendaten["Tf"]     << 4) +
                    (Bediendaten["Tw"]     << 3) +
                    (Bediendaten["STFG0"]  << 2) +
                    (Bediendaten["STFGR"]  << 1) +
                     Bediendaten["STFGL"]      )
    UDPDaten.append((Bediendaten["TZLA"]   << 7) +
                    (Bediendaten["TZLE"]   << 6) +
                    (Bediendaten["TSAND"]  << 5) +
                    (Bediendaten["TSSB"]   << 4) +
                    (Bediendaten["TBL"]    << 3) +
                    (Bediendaten["SFL"]    << 2) +
                    (Bediendaten["SSL"]    << 1) +
                     Bediendaten["TMF"]        )
    UDPDaten.append((Bediendaten["TTFGTZ"] << 7) +
                    (Bediendaten["TTFGT0"] << 6) +
                    (Bediendaten["TFIS"]   << 5)) # +
                    # (Bediendaten[""]   << 4) +
                    # (Bediendaten[""]  << 3) +
                    # (Bediendaten[""]  << 2) +
                    # (Bediendaten[""]  << 1) +
                    #  Bediendaten[""]      )
    return UDPDaten

def UDPBedienDatenAuswertenFT1(UDPDaten, Bediendaten):
    Bediendaten["FS"]     = (UDPDaten[0] >> 4) & 0xf
    Bediendaten["RS"]     = (UDPDaten[0] & 0xf) - 1
    hilf = struct.unpack("f",UDPDaten[1:5])
    Bediendaten["AFSZ"]   = hilf[0]
    Bediendaten["BS"]     = UDPDaten[5]
    hilf = struct.unpack("f",UDPDaten[6:10])
    Bediendaten["ABS"]    = hilf[0]
    Bediendaten["TSifa"]  = (UDPDaten[10] & 0x80 == 128)
    Bediendaten["SLP"]    = (UDPDaten[10] & 0x40 == 64)
    Bediendaten["SLST"]   = (UDPDaten[10] & 0x20 == 32)
    Bediendaten["SLSW"]   = (UDPDaten[10] & 0x10 == 16)
    Bediendaten["TSAN"]   = (UDPDaten[10] & 0x8 == 8)
    Bediendaten["TSAH"]   = (UDPDaten[10] & 0x4 == 4)
    Bediendaten["THSA"]   = (UDPDaten[10] & 0x2 == 2)
    Bediendaten["THSE"]   = (UDPDaten[10] & 0x1 == 1)
    Bediendaten["SZSE"]   = (UDPDaten[11] & 0x80 == 128)
    Bediendaten["TZSA"]   = (UDPDaten[11] & 0x40 == 64)
    Bediendaten["Tb"]     = (UDPDaten[11] & 0x20 == 32)
    Bediendaten["Tf"]     = (UDPDaten[11] & 0x10 == 16)
    Bediendaten["Tw"]     = (UDPDaten[11] & 0x8 == 8)
    Bediendaten["STFG0"]  = (UDPDaten[11] & 0x4 == 4)
    Bediendaten["STFGR"]  = (UDPDaten[11] & 0x2 == 2)
    Bediendaten["STFGL"]  = (UDPDaten[11] & 0x1 == 1)
    Bediendaten["TZLA"]   = (UDPDaten[12] & 0x80 == 128)
    Bediendaten["TZLE"]   = (UDPDaten[12] & 0x40 == 64)
    Bediendaten["TSAND"]  = (UDPDaten[12] & 0x20 == 32)
    Bediendaten["TSSB"]   = (UDPDaten[12] & 0x10 == 16)
    Bediendaten["TBL"]    = (UDPDaten[12] & 0x8 == 8)
    Bediendaten["SFL"]    = (UDPDaten[12] & 0x4 == 4)
    Bediendaten["SSL"]    = (UDPDaten[12] & 0x2 == 2)
    Bediendaten["TMF"]    = (UDPDaten[12] & 0x1 == 1)
    Bediendaten["TTFGTZ"] = (UDPDaten[13] & 0x80 == 128)
    Bediendaten["TTFGT0"] = (UDPDaten[13] & 0x40 == 64)
    Bediendaten["TFIS"]   = (UDPDaten[13] & 0x20 == 32)
    # Bediendaten[""] = (UDPDaten[13] & 0x10 == 16)
    # Bediendaten[""] = (UDPDaten[13] & 0x8 == 8)
    # Bediendaten[""] = (UDPDaten[13] & 0x4 == 4)
    # Bediendaten[""] = (UDPDaten[13] & 0x2 == 2)
    # Bediendaten[""] = (UDPDaten[13] & 0x1 == 1)
    return None

def UDPAnzeigeDatenErzeugenFT2(Anzeigedaten):
    UDPDaten = bytearray()
    UDPDaten.extend(struct.pack("f", Anzeigedaten["DruckHL"]))                    # Byte  0- 3
    UDPDaten.extend(struct.pack("f", Anzeigedaten["DruckC"]))                     # Byte  4- 7
    UDPDaten.extend(struct.pack("f", Anzeigedaten["DruckHB"]))                    # Byte  8-11
    UDPDaten.extend(struct.pack("f", Anzeigedaten["DruckZ"]))                     # Byte 12-15
    UDPDaten.extend(struct.pack("H", Anzeigedaten["AnzModus"]))                   # Byte 16-17
    return UDPDaten

def UDPAnzeigeDatenAuswertenFT2(UDPDaten,Anzeigedaten):
    hilf = struct.unpack("f",UDPDaten[0:4])
    Anzeigedaten["DruckHL"] = hilf[0] # Hauptluftleitungsdruck
    hilf = struct.unpack("f",UDPDaten[4:8])
    Anzeigedaten["DruckC" ] = hilf[0] # Bremszylinderdruck
    hilf = struct.unpack("f",UDPDaten[8:12])
    Anzeigedaten["DruckHB"] = hilf[0] # Hauptluftbehälterdruck
    hilf = struct.unpack("f",UDPDaten[12:16])
    Anzeigedaten["DruckZ"]  = hilf[0] # Zeitbehälterdruck
    hilf = struct.unpack("H",UDPDaten[16:18])
    Anzeigedaten["AnzModus"] = hilf[0]
    return None

def UDPBedienDatenErzeugenFT2(Bediendaten):
    UDPDaten = bytearray()
    UDPDaten.append(((Bediendaten["FbV"] & 0xf) << 4) +
                     (Bediendaten["FbVAg"]      << 3) +
                     (Bediendaten["FbVSchl"]    << 2) +
                     (Bediendaten["ZbVBr"]      << 1) +
                      Bediendaten["ZbVLoe"]         )
    UDPDaten.extend(struct.pack("f", Bediendaten["DruckFbVA"]))
    return UDPDaten

def UDPBedienDatenAuswertenFT2(UDPDaten,Bediendaten):
    Bediendaten["FbV"]        = (UDPDaten[0] >> 4) & 0xf
    Bediendaten["FbVAg"]      = (UDPDaten[0] & 0x8 == 8)
    Bediendaten["FbVSchl"]    = (UDPDaten[0] & 0x4 == 4)
    Bediendaten["ZbVBr"]      = (UDPDaten[0] & 0x2 == 2)
    Bediendaten["ZbVLoe"]     = (UDPDaten[0] & 0x1 == 1)
    hilf = struct.unpack("f",UDPDaten[1:5])
    Bediendaten["DruckFbVA"]  = hilf[0]
    return None

