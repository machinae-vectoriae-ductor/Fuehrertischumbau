"""
Dieser Quellcode ist in Python 3 geschrieben und realisiert die Aufbereitung 
der Anzeigedaten zur Ausgabe über die serielle LZB-Schnittstelle.

This source code is written in Python 3 and realises the preparation of the 
display data for output via the serial LZB interface.

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

TH Köln, hereby disclaims all copyright interest in the software 'SchnittstelleLZB.py'
(a software for preparation of the display data for output via the serial LZB interface).

Wolfgang Evers
Versionsdatum 23.05.2022

"""

AusgabeLM1 = (False,False,False,True ,False,True ,False,False,False,False,False,True,False,True,False,False,False)
AusgabeLM2 = (False,True ,False,False,False,False,False,False,False,False,False,True,False,True,False,False,False)


def convertlist(list):
    #Convert list to integer
    decodelist = [1, 2, 4, 8, 16, 32, 64]
    res = 0
    for i in range(7):
        res = res + decodelist[i]*list[i]
    return(res)

def updateData(Anzeigedaten,LZBDaten):
    ######################## Byte_03
    LZBDaten[2] = int(Anzeigedaten["LZBVsoll"] / 64) & 0x3f
    ######################## Byte_04   
    LZBDaten[3] = int(Anzeigedaten["LZBVsoll"]) % 64
    ######################## Byte_06
    LZBDaten[5] = int(Anzeigedaten["LZBVziel"] / 320) & 0x1
    ######################## Byte_07
    LZBDaten[6] = int((Anzeigedaten["LZBVziel"] % 320) * 0.2)
    ######################## Determine WXZ  
    WXZ = (Anzeigedaten["LZBSziel"] > 399.0)
    ######################## Byte_08    
    if WXZ == True:
        LZBDaten[7] = int(Anzeigedaten["LZBSziel"] / 1600) & 0x3f
    else:
        LZBDaten[7] = int(Anzeigedaten["LZBSziel"] / 12.5) & 0x3f
    ######################## Byte_09
    if WXZ == True:
        LZBDaten[8] = int((Anzeigedaten["LZBSziel"] % 1600) * 0.04) & 0x3f
    else:
        LZBDaten[8] = int((Anzeigedaten["LZBSziel"] % 12.5) * 5.12) & 0x3f
    ######################## Byte_12
    LZBDaten[11] = ( WXZ << 1) + (Anzeigedaten["MFADVZ"] << 2) + (Anzeigedaten["MFADaZ"] << 3) + (Anzeigedaten["MFADdZ"] << 4) + (Anzeigedaten["MFADVS"] << 5)
    ######################## Byte_15
    LZBDaten[14] = AusgabeLM2[Anzeigedaten["LMStoer"]] + (AusgabeLM2[Anzeigedaten["LMV40"]] << 1) + (AusgabeLM2[Anzeigedaten["LMB40"]] << 2) + (AusgabeLM2[Anzeigedaten["LMEnde"]] << 3) + (AusgabeLM2[Anzeigedaten["LMS"]] << 4) + (AusgabeLM2[Anzeigedaten["LMEL"]] << 5)
    ######################## Byte_16
    LZBDaten[15] = AusgabeLM2[Anzeigedaten["LMG"]] + (AusgabeLM2[Anzeigedaten["LMH"]] << 1) + (AusgabeLM2[Anzeigedaten["LMB"]] << 2) + (AusgabeLM2[Anzeigedaten["LMUe"]] << 3) + (AusgabeLM2[Anzeigedaten["LM1000Hz"]] << 4) + (AusgabeLM2[Anzeigedaten["LME40"]] << 5)
    ######################## Byte_17
    LZBDaten[16] = AusgabeLM1[Anzeigedaten["LMStoer"]] + (AusgabeLM1[Anzeigedaten["LMV40"]] << 1) + (AusgabeLM1[Anzeigedaten["LMB40"]] << 2) + (AusgabeLM1[Anzeigedaten["LMEnde"]] << 3) + (AusgabeLM1[Anzeigedaten["LMS"]] << 4) + (AusgabeLM1[Anzeigedaten["LMEL"]] << 5)
    ######################## Byte_18
    LZBDaten[17] = AusgabeLM1[Anzeigedaten["LMG"]] + (AusgabeLM1[Anzeigedaten["LMH"]] << 1) + (AusgabeLM1[Anzeigedaten["LMB"]] << 2) + (AusgabeLM1[Anzeigedaten["LMUe"]] << 3) + (AusgabeLM1[Anzeigedaten["LM1000Hz"]] << 4) + (AusgabeLM1[Anzeigedaten["LME40"]] << 5)
    ######################## Byte_19
    LZBDaten[18] = AusgabeLM2[Anzeigedaten["LM55"]] + (AusgabeLM2[Anzeigedaten["LM70"]] << 1) + (AusgabeLM2[Anzeigedaten["LM85"]] << 2) + (AusgabeLM2[Anzeigedaten["LM500Hz"]] << 3)
    ######################## Byte_20
    LZBDaten[19] = AusgabeLM1[Anzeigedaten["LM55"]] + (AusgabeLM1[Anzeigedaten["LM70"]] << 1) + (AusgabeLM1[Anzeigedaten["LM85"]] << 2) + (AusgabeLM1[Anzeigedaten["LM500Hz"]] << 3)
    ######################## Byte_22
    LZBDaten[21] = (Anzeigedaten["SchnarreLZB"] & 0x3)
    ######################## Byte_32
    LZBDaten[31] = int(Anzeigedaten["Vist"] / 64) & 0x3f
    ######################## Byte_33   
    LZBDaten[32] = int(Anzeigedaten["Vist"]) % 64

    ######################## Calculata Byte_49 - column-parity
    LZBDaten[48] = 0
    array = [0x01,0x02,0x04,0x08,0x10,0x20]
    for i in range(0,6):
        cnt = False           
        for x in range(0,48):
            if LZBDaten[x] & array[i] != 0:
                cnt = not cnt
        if cnt:
            LZBDaten[48] += array[i]

