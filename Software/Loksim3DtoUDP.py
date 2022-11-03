#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Dieser Quellcode ist in Python 3 geschrieben und realisiert einen UDP Server für die Simulation LokSim3D.

This source code is written in Python 3 and implements a UDP server for the simulation LokSim3D.

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

TH Köln, hereby disclaims all copyright interest in
the software 'UDP-Server-Loksim3D' (a software for UDP Server for Loksim3D).

Wolfgang Evers
Versionsdatum 03.11.2022

"""
import time
import socket
import threading
import vjoy
import serial
import SchnittstelleLZB
import SchnittstelleFT
import Textausgabe

# Netzwerkdaten
Loksim_IP = "127.0.0.1"   # Höre Loksim vom localhost
Loksim_Port = 51435       # Beachte Port 51435 von Loksim3D
Ft1_IP = "192.168.111.12" # Adresse des ersten Steuergeräts des Führertischs
Ft1E_Port = 51436         # Empfangsport des ersten Steuergeräts des Führertischs
Ft1S_Port = 51438         # Sendeport des ersten Steuergeräts des Führertischs
Ft2_IP = "192.168.111.13" # Adresse des zweiten Steuergeräts des Führertischs
Ft2E_Port = 51437         # Empfangsport des zweiten Steuergeräts des Führertischs
Ft2S_Port = 51439         # Sendeport des zweiten Steuergeräts des Führertischs

serLZB = serial.Serial(
    port='COM2',
    baudrate=1200,
    bytesize=serial.SEVENBITS,
    parity=serial.PARITY_EVEN,
    stopbits=serial.STOPBITS_TWO)

Anzeigedaten = {"Vist": 0.0,           # Geschwindigkeit in km/h
                "Fzb": 0.0,            # Zug-/Bremskraft gesamt in kN
                "Fzba": 0.0,           # Zug-/Bremskraft pro Achse in kN
                "Fzbrel": 0.0,         # Zug-/Bremskraftkraft relativ in %
                "Fzbsoll": 0.0,        # Zug-/Bremskraft-Soll gesamt in kN
                "Fzbasoll": 0.0,       # Zug-/Bremskraft-Soll pro Achse in kN
                "Fzbsollrel": 0.0,     # Zug-/Bremskraft-Soll relativ in %
                "LMSchleudern": False, # Leuchtmelder Schleudern
                "LMGleiten": False,    # Leuchtmelder Gleiten
                "LMHS": False,         # Leuchtmelder Hauptschalter aus
                "LMGetriebe": False,   # Leuchtmelder Getriebe
                "LMSA": 0,             # Leuchtmelder Stromabnehmer
                "LMZS": False,         # Leuchtmelder Zugsammelschiene
                "LMEB": False,         # Leuchtmelder Elektrische Bremse
                "LMHAB": False,        # Leuchtmelder Hohe Abbremsung
                "LMNBrems": 0,         # Leuchtmelder Notbremsung
                "LMSifa": False,       # Leuchtmelder Sifa
                "LMTuer": 0,           # Leuchtmelder Türen
                "FSt": 0,              # Fahrstufe
                "LM85": 0,             # Leuchtmelder 85
                "LM70": 0,             # Leuchtmelder 70
                "LM55": 0,             # Leuchtmelder 55
                "LM1000Hz": 0,         # Leuchtmelder 1000 Hz
                "LM500Hz": 0,          # Leuchtmelder 500 Hz
                "LMB40": 0,            # Leuchtmelder Befehl 40
                "LMH": 0,              # Leuchtmelder H (Nothalt)
                "LMG": 0,              # Leuchtmelder G (Geschwindigkeit)
                "LME40": 0,            # Leuchtmelder E40 (Ersatzauftrag)
                "LMEL": 0,             # Leuchtmelder EL
                "LMEnde": 0,           # Leuchtmelder Ende
                "LMV40": 0,            # Leuchtmelder V40
                "LMB": 0,              # Leuchtmelder B (Betrieb)
                "LMS": 0,              # Leuchtmelder S (Schnellbremsung)
                "LMUe": 0,             # Leuchtmelder Ü (Übertragung)
                "LMLZBStoer": 0,       # Leuchtmelder LZB Störung
                "LMPZB": True,         # Leuchtmelder PZB
                "LMGNT": False,        # Leuchtmelder GNT
                "LMGNTUe": 0,          # Leuchtmelder GNT Ü
                "LMGNTG": 0,           # Leuchtmelder GNT G
                "LMGNTS": 0,           # Leuchtmelder GNT S
                "LMStoer": 0,          # Leuchtmelder Störung
                "HupePZB": 0,          # PZB-Hupe
                "SchnarreLZB": 0,      # LZB-Schnarre
                "SummerTuer": 0,       # Tür-Summer
                "HupeSifa": False,     # Sifa-Hupe
                "ZbSifa": False,       # Sifa-Zwangsbremse
                "LZBVsoll": 0.0,       # LZB Soll-Geschwindigkeit in km/h
                "LZBVziel": 0.0,       # LZB Ziel-Geschwindigkeit in km/h
                "LZBSziel": 0.0,       # LZB Zielentfernung in m
                "MFADVZ": True,        # MFA Dunkelschaltung LZBVziel
                "MFADaZ": True,        # MFA Dunkelschaltung LZBSziel analog
                "MFADdZ": True,        # MFA Dunkelschaltung LZBSziel digital
                "MFADVS": True,        # MFA Dunkelschaltung LZBVsoll
                "BRH": 0,              # BRH-Wert (Bremshundertstel) in %
                "BRA": 0,              # BRA-Wert (Bremsart)
                "ZL": 0,               # ZL-Wert (Zuglänge) in m
                "VMZ": 0,              # VMZ-Wert (Höchstgeschwindigkeit) in km/h
                "ZDK": False,          # Zugdatenanzeige in der MFA
                "LZBSystem": 0,        # Bauart des LZB/PZB-System
                "PZBZa": 0,            # PZB-Zugart (1:U, 2:M, 3:O)
                "AFBaktiv": False,     # AFB aktiv
                "AFBVsoll": 200,       # AFB Soll-Geschwindigkeit in km/h
                "Uol": 0.0,            # Fahrleitungsspannung in V
                "Iol": 0.0,            # Oberstrom in A
                "Umot": 0.0,           # Motorspannung in V
                "Nmot": 0.0,           # Dieselmotordrehzahl in 1/min
                "AnzModus": 299,       # Anzeigemodus
                "DruckHB": 0.0,        # Druck Hauptluftbehälter in bar
                "DruckHL": 0.0,        # Druck Hauptluftleitung in bar
                "DruckZ": 0.0,         # Druck Zeitbehälter in bar
                "DruckC": 0.0,         # Druck Bremszylinder in bar
                "TuerSystem": 0,       # Türsystem
                "TuerL": 0,            # Status Türen links
                "TuerR": 0,            # Status Türen rechts
                "Streckenkm": 0,       # Streckenkilometer in m
                "Simkm": 0,            # Relative Position in m
                "SimZeit": 0,          # Simulationszeit im UNIX-Format
                "Zugnr": 0,            # Zugnummer
                "VmaxTfz": 200,        # Höchstgeschwindigkeit des Tfz in km/h
                "NVR": ""}             # Eindeutige Fahrzeugnummer des Tfz


Anzeigedatenalt = Anzeigedaten.copy()

LZBDaten =     [0x61,    #Byte_01 - Statisch  - Start
                0x00,    #Byte_02 - Statisch  - Irrelevant für MFA   
                0x00,    #Byte_03 - Dynamisch - VIst
                0x00,    #Byte_04 - Dynamisch - VSoll
                0x00,    #Byte_05 - Statisch  - Irrelevant für MFA 
                0x00,    #Byte_06 - Dynamisch - VZiel
                0x00,    #Byte_07 - Dynamisch - VZiel
                0x00,    #Byte_08 - Dynamisch - SZiel
                0x00,    #Byte_09 - Dynamisch - SZiel
                0x00,    #Byte_10 - Statisch  - Irrelevant für MFA 
                0x00,    #Byte_11 - Statisch  - Irrelevant für MFA 
                0x00,    #Byte_12 - Dynamisch - WXZ, D(VZ, aZ, dZ, VS)
                0x00,    #Byte_13 - Statisch  - Irrelevant für MFA 
                0x00,    #Byte_14 - Statisch  - Irrelevant für MFA 
                0x00,    #Byte_15 - Dynamisch - LM(Stoer, V40, B40, Ende, S, EL)
                0x00,    #Byte_16 - Dynamisch - LM(G, H, B, Ue, 1000Hz, E40)
                0x00,    #Byte_17 - Dynamisch - ALT LM(Stoer, V40, B40, Ende, S, EL)
                0x00,    #Byte_18 - Dynamisch - ALT LM(G, H, B, Ue, 1000Hz, E40)
                0x00,    #Byte_19 - Dynamisch - LM(55, 70, 85, 500Hz)
                0x00,    #Byte_20 - Dynamisch - ALT LM(55, 70, 85, 500Hz)
                0x00,    #Byte_21 - Statisch  - Irrelevant für MFA 
                0x00,    #Byte_22 - Dynamisch - Schnarr1, Schnarr2
                0x00,    #Byte_23 - Statisch  - Irrelevant für MFA 
                0x00,    #Byte_24 - Statisch  - Irrelevant für MFA 
                0x00,    #Byte_25 - Statisch  - Irrelevant für MFA 
                0x00,    #Byte_26 - Statisch  - Irrelevant für MFA 
                0x00,    #Byte_27 - Statisch  - Irrelevant für MFA 
                0x00,    #Byte_28 - Statisch  - Irrelevant für MFA 
                0x00,    #Byte_29 - Statisch  - Irrelevant für MFA 
                0x00,    #Byte_30 - Statisch  - Irrelevant für MFA 
                0x00,    #Byte_31 - Statisch  - Irrelevant für MFA 
                0x00,    #Byte_32 - Statisch  - Irrelevant für MFA 
                0x00,    #Byte_33 - Statisch  - Irrelevant für MFA 
                0x00,    #Byte_34 - Statisch  - Irrelevant für MFA 
                0x00,    #Byte_35 - Statisch  - Irrelevant für MFA 
                0x00,    #Byte_36 - Statisch  - Irrelevant für MFA 
                0x00,    #Byte_37 - Statisch  - Irrelevant für MFA
                0x00,    #Byte_38 - Statisch  - Irrelevant für MFA
                0x00,    #Byte_39 - Statisch  - Irrelevant für MFA
                0x00,    #Byte_40 - Statisch  - Irrelevant für MFA
                0x00,    #Byte_41 - Statisch  - Irrelevant für MFA
                0x00,    #Byte_42 - Statisch  - Irrelevant für MFA
                0x00,    #Byte_43 - Statisch  - Irrelevant für MFA
                0x00,    #Byte_44 - Statisch  - Irrelevant für MFA
                0x00,    #Byte_45 - Statisch  - Irrelevant für MFA
                0x00,    #Byte_46 - Statisch  - Irrelevant für MFA
                0x00,    #Byte_47 - Statisch  - Irrelevant für MFA
                0x00,    #Byte_48 - Statisch  - Irrelevant für MFA
                0x00,    #Byte_49 - Dynamisch - Spaltenparität
                0x7F]    #Byte_50 - Statisch  - Telegramm Ende

Bediendaten = {"FS"              : 0,     # Fahrschalterstellung
               "AFSZ"            : 0.0,   # Fahrschalter Sollwert Zugkraft in %
               "Sollfahrstufe"   : 0,     # Nachlaufsteuerung Sollfahrstufe
               "RS"              : 0,     # Richtungsschalter Stellung
               "TSifa"           : False, # Taster Sifa
               "FbV"             : 0,     # Führerbremsventilstellung
               "DruckFbVA"       : 0.0,   # Führerbremsventil A-Druck in bar
               "FbVAg"           : False, # Führerbremsventil Angleicher
               "FbVSchl"         : False, # Führerbremsventil Schlüssel
               "BS"              : 0,     # Bremsstellerstellung
               "ABS"             : 0.0,   # Bremssteller Sollwert Bremskraft in %
               "ZbVBr"           : False, # Zusatzbremsventil Bremsen
               "ZbVLoe"          : False, # Zusatzbremsventil Lösen
               "SLP"             : False, # Schalter Luftpresser
               "SLST"            : False, # Schalter Lüfter stark
               "SLSW"            : False, # Schalter Lüfter schwach
               "TSAN"            : False, # Taster Stromabnehmer nieder
               "TSAH"            : False, # Taster Stromabnehmer hoch
               "THSA"            : False, # Taster Hauptschalter Aus
               "THSE"            : False, # Taster Hauptschalter Ein
               "SZSE"            : False, # Schalter Zugsammelschiene Ein
               "TZSA"            : False, # Taster Zugsammelschiene An
               "Tb"              : False, # Taster Indusi Befehl
               "Tf"              : False, # Taster Indusi Frei
               "Tw"              : False, # Taster Indusi Wachsam
               "STFG0"           : False, # Schalter Türfreigabe 0
               "STFGR"           : False, # Schalter Türfreigabe rechts
               "STFGL"           : False, # Schalter Türfreigabe links
               "TZLA"            : False, # Taster Zugbeleuchtung Aus
               "TZLE"            : False, # Taster Zugbeleuchtung Ein
               "TSAND"           : False, # Taster Sanden
               "TSSB"            : False, # Taster Schleuderschutzbremse
               "TBL"             : False, # Taster Bremse lösen
               "SFL"             : False, # Schalter Fernlicht
               "SSL"             : False, # Schalter Signallicht
               "TMF"             : False, # Taster Makrofon
               "TTFGTZ"          : False, # Taster Türfreigabe TZ
               "TTFGT0"          : False, # Taster Türfreigabe T0
               "TFIS"            : False, # Taster FIS-Fortschaltung
#               "DI1I1"           : False, # 
#               "DI1I2"           : False, # 
#               "DI1I3"           : False, # 
#               "DI1I4"           : False, # Taster Leuchtmelder prüfen
#               "DI1I5"           : False, # Taster Störung quittieren
#               "DI1I6"           : False, # Fahrschalter Schnell-Auf-Befehl
#               "DI4I10"          : False, # Schalter Heizen
#               "DI4I11"          : False, # Schalter Lüften
#               "DI4I12"          : False, # 
#               "DI4I13"          : False, # 
#               "DI4I14"          : False, #
               }

TuerenAuf = False

EBuLaString = ""

stop_threads = False

# Verarbeitung Daten aus UDP-Telegramm
def UDPDatenAuswerten(UDPDaten,Anzeigedaten):
#    IndicatorHupe = (0, 3, 0, 1, 0, 2, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0)
    Anzeigedaten["LMB40"] = (UDPDaten[0] >> 4) & 0xf
    Anzeigedaten["LM1000Hz"] = UDPDaten[0] & 0xf
    Anzeigedaten["LM500Hz"] = (UDPDaten[1] >> 4) & 0xf
    Anzeigedaten["LM85"] = UDPDaten[1] & 0xf
    Anzeigedaten["LM70"] = (UDPDaten[2] >> 4) & 0xf
    Anzeigedaten["LM55"] = UDPDaten[2] & 0xf
    Anzeigedaten["LMH"] = (UDPDaten[3] >> 4) & 0xf
    Anzeigedaten["LMG"] = UDPDaten[3] & 0xf
    Anzeigedaten["LME40"] = (UDPDaten[4] >> 4) & 0xf
    Anzeigedaten["LMEL"] = UDPDaten[4] & 0xf
    Anzeigedaten["LMEnde"] = (UDPDaten[5] >> 4) & 0xf
    Anzeigedaten["LMV40"] = UDPDaten[5] & 0xf
    Anzeigedaten["LMB"] = (UDPDaten[6] >> 4) & 0xf
    Anzeigedaten["LMS"] = UDPDaten[6] & 0xf
    Anzeigedaten["LMUe"] = (UDPDaten[7] >> 4) & 0xf
    Anzeigedaten["LMStoer"] = UDPDaten[7] & 0xf
    Anzeigedaten["HupePZB"] = (UDPDaten[8] >> 4) & 0xf
    Anzeigedaten["SchnarreLZB"] = UDPDaten[8] & 0xf
    Anzeigedaten["MFADVZ"] = not (UDPDaten[9] & 0x80 == 128)
    Anzeigedaten["MFADaZ"] = not (UDPDaten[9] & 0x80 == 128)
    Anzeigedaten["MFADdZ"] = not (UDPDaten[9] & 0x80 == 128)
    Anzeigedaten["MFADVS"] = not (UDPDaten[9] & 0x80 == 128)
    Anzeigedaten["ZDK"] = (UDPDaten[9] & 0x40 == 64)
    Anzeigedaten["LZBVsoll"] = (UDPDaten[10] + (UDPDaten[11] << 8)) * 0.1
    Anzeigedaten["LZBVziel"] = (UDPDaten[12] + (UDPDaten[13] << 8)) * 0.1
    Anzeigedaten["LZBSziel"] = UDPDaten[14] + (UDPDaten[15] << 8)
    Anzeigedaten["BRH"] = UDPDaten[16] + (UDPDaten[17] << 8)
    Anzeigedaten["ZL"] = UDPDaten[18] + (UDPDaten[19] << 8)
    Anzeigedaten["VMZ"] = UDPDaten[20] + (UDPDaten[21] << 8)
    Anzeigedaten["BRA"] = (UDPDaten[22] >> 4) & 0xf
    Anzeigedaten["LMHS"] =  (UDPDaten[22] & 0x8 == 8)
    Anzeigedaten["LMHAB"] =  (UDPDaten[22] & 0x4 == 4)
    Anzeigedaten["IndMtEB"] =  (UDPDaten[22] & 0x2 == 2)
    Anzeigedaten["IndMtHvtl"] =  (UDPDaten[22] & 0x1 == 1)
    # Anzeigedaten["LMNBrems"] = (UDPDaten[23] >> 4) & 0xf
    Anzeigedaten["LMSchleudern"] =  (UDPDaten[23] & 0x8 == 8)
    Anzeigedaten["LMGleiten"] =  (UDPDaten[23] & 0x4 == 4)
    Anzeigedaten["LMSifa"] =  (UDPDaten[23] & 0x2 == 2)
    Anzeigedaten["HupeSifa"] =  (UDPDaten[23] & 0x1 == 1)
    Anzeigedaten["LMTuer"] = max(((UDPDaten[24] >> 4) & 0xf), (UDPDaten[24] & 0xf))
    Anzeigedaten["TuerL"] = UDPDaten[25] & 0xf
    Anzeigedaten["TuerR"] = (UDPDaten[25] >> 4) & 0xf
    Anzeigedaten["LMSA"] = UDPDaten[26] & 0xf
    Anzeigedaten["Vist"] = (UDPDaten[27] + (UDPDaten[28] << 8)) * 0.1
    Anzeigedaten["AFBVsoll"] = UDPDaten[29] + (UDPDaten[30] << 8)
    Anzeigedaten["Fzb"] = (UDPDaten[31] + (UDPDaten[32] << 8)) * 0.04 - ((UDPDaten[33] + (UDPDaten[34] << 8)) * 0.01)
    Anzeigedaten["Fzba"] = Anzeigedaten["Fzb"] * 0.25
    Anzeigedaten["Uol"] = UDPDaten[35] + (UDPDaten[36] << 8)
    Anzeigedaten["Iol"] = UDPDaten[37] + (UDPDaten[38] << 8)
    # Anzeigedaten["FStW"] = UDPDaten[39]
    Anzeigedaten["FSt"] = UDPDaten[40]
    Anzeigedaten["DruckHL"] = (UDPDaten[41] + (UDPDaten[42] << 8)) * 0.001
    Anzeigedaten["DruckC"] = (UDPDaten[43] + (UDPDaten[44] << 8)) * 0.001
    Anzeigedaten["DruckHB"] = (UDPDaten[45] + (UDPDaten[46] << 8)) * 0.001
    Anzeigedaten["DruckZ"] = (UDPDaten[47] + (UDPDaten[48] << 8)) * 0.001
    return None

def Loksimskala(Echtwert):
# Diese Funktion rechnet einen Wert vom 0 - 100 % in die Loksim3D-Skalierung um.
    if Echtwert <= 0.0:
        Sendewert = 0
    elif Echtwert > 0.0 and Echtwert < 50.0:
        Sendewert = 2500 + int(Echtwert * 211.2)
    elif Echtwert == 50.0:
        Sendewert = 16000
    elif Echtwert > 50.0 and Echtwert < 100.0:
        Sendewert = 8640 + int(Echtwert * 211.2)
    else:
        Sendewert = 32000
    return Sendewert

def BedienungnachLoksim(Anzeigedaten,Sendebediendaten, Sendebediendatenalt, TuerenAuf):
    if Sendebediendaten["FbV"] == 2:
        DBremse = 0
    elif Sendebediendaten["FbV"] == 1:
        DBremse = Loksimskala(max(0.0,min(100.0,(Sendebediendaten["DruckFbVA"] - 3.35) * 78)))
    else:
        DBremse = 32000
    if Sendebediendaten["BS"] == 2 or Sendebediendaten["FbV"] == 2:
        EBremse = 32000
    elif Sendebediendaten["BS"] == 1:
        EBremse = Loksimskala(Sendebediendaten["ABS"])
    else:
        EBremse = 0
    if Sendebediendaten["FS"] == 1:
        AufAb = 0
    elif Sendebediendaten["FS"] == 3:
        AufAb = 32000
    else:
        AufAb = 16000
    if Sendebediendaten["FS"] == 4:
        Zugkraft = Loksimskala(0.5 * Sendebediendaten["AFSZ"] + 50)
    else:
        Zugkraft = 0
    vj.update(vj.generateJoystickPosition(wAxisX = DBremse, wAxisY = EBremse, wAxisZ = AufAb, wSlider = 16000, wAxisXRot = Zugkraft, wAxisYRot = 16000, wAxisZRot = 16000))
    vj.setButton( 1,  Sendebediendaten["RS"] ==  2)
    vj.setButton( 2, (Sendebediendaten["RS"] ==  0 or Sendebediendaten["RS"] == 1))
    vj.setButton( 3,  Sendebediendaten["RS"] == -1 )
    vj.setButton( 4, ((Anzeigedaten["LMSA"] == 4 or Anzeigedaten["LMSA"] == 3) and Sendebediendaten["TSAH"] == True) or ((Anzeigedaten["LMSA"] == 2 or Anzeigedaten["LMSA"] == 1) and Sendebediendaten["TSAN"] == True))
    vj.setButton( 5, ((Anzeigedaten["LMHS"] == True and Sendebediendaten["THSE"] == True) or (Anzeigedaten["LMHS"] == False and Sendebediendaten["THSA"] == True)))
    vj.setButton( 6, Sendebediendaten["FbV"] == 2)
    vj.setButton( 7, Sendebediendaten["FS"] == 0)
    vj.setButton( 8, Sendebediendaten["TSifa"] )
    vj.setButton( 9, Sendebediendaten["Tw"] )
    vj.setButton(10, Sendebediendaten["Tf"] )
    vj.setButton(11, Sendebediendaten["Tb"] )
    vj.setButton(12, Sendebediendaten["TMF"] )
    vj.setButton(13, Sendebediendaten["TSAND"] )
    vj.setButton(14, Sendebediendaten["SSL"] )
    vj.setButton(15, Sendebediendaten["SFL"] )
    vj.setButton(16, TuerenAuf)
    vj.setButton(17, Sendebediendaten["FS"] == 4)
    vj.setButton(18, False)
    return None

class LZBSendenThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        while True:
            time.sleep(0.48)
            serLZB.write(serial.to_bytes(LZBDaten))
            if stop_threads:
                break

class Bedienung1Thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        global Bediendaten
        global TuerenAuf
        while True:
            daten, addr = Ft1SSocket.recvfrom(1024)
            # msg = "Message from Loksim {}".format(daten)
            # msg_2 = "Adress from Loksim {}".format(addr[0])
            # print(str(msg),"  ", str(msg_2))
            # print("Anzahl der Zeichen des UDP-Pakets:\t",len(daten))
            Bediendaten1alt = Bediendaten.copy()
            SchnittstelleFT.UDPBedienDatenAuswertenFT1(daten,Bediendaten)
            if Bediendaten["TTFGTZ"] == True:
                TuerenAuf = False
            elif Bediendaten["TTFGT0"] == True:
                TuerenAuf = True
            Textausgabe.Textbedienanzeige(Bediendaten,Bediendaten1alt)
            BedienungnachLoksim(Anzeigedaten, Bediendaten, Bediendaten1alt, TuerenAuf)
            if stop_threads:
                break

class Bedienung2Thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        global Bediendaten
        global TuerenAuf
        while True:
            daten, addr = Ft2SSocket.recvfrom(1024)
            # msg = "Message from Loksim {}".format(daten)
            # msg_2 = "Adress from Loksim {}".format(addr[0])
            # print(str(msg),"  ", str(msg_2))
            # print("Anzahl der Zeichen des UDP-Pakets:\t",len(daten))
            Bediendaten2alt = Bediendaten.copy()
            SchnittstelleFT.UDPBedienDatenAuswertenFT2(daten,Bediendaten)
            # Textausgabe.Textbedienanzeige(Bediendaten,Bediendaten2alt)
            BedienungnachLoksim(Anzeigedaten, Bediendaten, Bediendaten2alt, TuerenAuf)
            if stop_threads:
                break

# Beginn des Hauptprogrammes

BUFFER_SIZE = 1024

LoksimSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Erstellen des UDP Socket für Loksim3D
Ft1ESocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # Erstellen des UDP Empfangs-Socket für den Führertischrechner 1
Ft1SSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # Erstellen des UDP Sende-Socket für den Führertischrechner 1
Ft2ESocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # Erstellen des UDP Empfangs-Socket für den Führertischrechner 2
Ft2SSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # Erstellen des UDP Sende-Socket für den Führertischrechner 2

try:
    LoksimSocket.bind((Loksim_IP, Loksim_Port))
    Ft1SSocket.bind(("", Ft1S_Port))
    Ft2SSocket.bind(("", Ft2S_Port))
    vj = vjoy.vJoy()
    vj.open()
    SchnittstelleLZB.updateData(Anzeigedaten,LZBDaten)
    LZBSendenThread()
    Bedienung1Thread()
    Bedienung2Thread()
    while True:
        daten, addr = LoksimSocket.recvfrom(BUFFER_SIZE)
        # msg = "Message from Loksim {}".format(daten)
        # msg_2 = "Address from Loksim {}".format(addr[0])
        # print(str(msg),"  ", str(msg_2))
        # print("Anzahl der Zeichen des UDP-Pakets:\t",len(daten))
        UDPDatenAuswerten(daten,Anzeigedaten)
        Ft1ESocket.sendto(SchnittstelleFT.UDPAnzeigeDatenErzeugenFT1(Anzeigedaten),(Ft1_IP, Ft1E_Port))
        Ft2ESocket.sendto(SchnittstelleFT.UDPAnzeigeDatenErzeugenFT2(Anzeigedaten),(Ft2_IP, Ft2E_Port))
        SchnittstelleLZB.updateData(Anzeigedaten,LZBDaten)
        Textausgabe.Textanzeige(Anzeigedaten,Anzeigedatenalt)
        Anzeigedatenalt = Anzeigedaten.copy()
finally:
    LoksimSocket.close()
    Ft1ESocket.close()
    Ft1SSocket.close()
    Ft2ESocket.close()
    Ft2SSocket.close()
    vj.close()
    stop_threads = True 

