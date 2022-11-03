#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Dieser Quellcode ist in Python 3 geschrieben und realisiert den Austausch der Daten
zwischen der Führertischhardware und der UDP-Schnittstelle zur Loksimulation.

This source code is written in Python 3 and realises the exchange of the data
between the driver's desk hardware and the UDP interface for locomotive simulation.

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
the software 'Fuehrertischrechner1' (a software for data exchange).

Wolfgang Evers
Versionsdatum 14.10.2022

"""
import time
import socket
import threading
from scipy.interpolate import interp1d
import revpimodio2  # Zum Ansprechen der IOs
import SchnittstelleFT
# import Textausgabe

# Netzwerkdaten
Adap_IP = "192.168.111.11" # IP-Adresse des Rechners mit dem Adapterprogramm
Ft1E_Port = 51436          # Empfangsport des ersten Steuergeräts des Führertischs
Ft1S_Port = 51438          # Sendeport des ersten Steuergeräts des Führertischs

# MFA-Parameter
# FaktorGeschwindigkeit = 10000 / 129  # MFA3/2b 200 km/h = 10000 mV
# FaktorZugkraft        = 10000 / 85   # MFA3/2b 85 kN = 10000 mV
# Zugkraftanzeigekennlinie: 1. Zeile Zugkraft in kN, 2. Zeile Spannung in mV
# Zugkraftanzeigekennlinie=[[0,  85.0],
#                           [0, 10000]] # MFA3/2b
# Zugkraftanzeigefunktion = interp1d(Zugkraftanzeigekennlinie[0], Zugkraftanzeigekennlinie[1], kind='linear')
# FaktorBremskraft      = 10000 / 150  # MFA3/2b 150 kN = 10000 mV
FaktorGeschwindigkeit = 10000 / 129  # MFA7n 180 km/h = 13953 mV
# Zugkraftanzeigekennlinie: 1. Zeile Zugkraft in kN, 2. Zeile Spannung in mV
Zugkraftanzeigekennlinie=[[0,  2.0,  3.5,  7.0, 14.0, 22.0, 30.5, 40.0, 51.0, 62.0,  73.0,  82.5],
                          [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 10800]] # MFA7n
Zugkraftanzeigefunktion = interp1d(Zugkraftanzeigekennlinie[0], Zugkraftanzeigekennlinie[1], kind='quadratic')
FaktorBremskraft      = 10800 / 97.2 # MFA7n   97,2 kN = 10800 mV
FaktorBremskraft2     = FaktorBremskraft / 2

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
                "AnzModus": 5,         # Anzeigemodus
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
AnzeigedatenGrundstellung = Anzeigedaten.copy()

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

stop_threads = False

# revpimodio konfigurieren
rpi = revpimodio2.RevPiModIO(autorefresh=True)
rpi.cycletime = 100

class MFALMThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.start()

    def LMWert(self, Wert, Langsam, Schnell):
        if   Wert ==  1: LMZustand = True        # An
        elif Wert ==  3: LMZustand = Langsam     # Blinken mit 0,5 Hz
        elif Wert ==  5: LMZustand = Schnell     # Blinken mit 1 Hz
        elif Wert == 11: LMZustand = not Langsam # Blinken invertiert mit 0,5 Hz
        elif Wert == 13: LMZustand = not Schnell # Blinken invertiert mit 1 Hz
        else: LMZustand = False
        return LMZustand
        
    def run(self):
        global Anzeigedaten
        Blinkzaehler = 0
# Für die Blinkfrequenz 0,5 Hz:
        Blinkbit1 = [True,  True,  True,  True,  True,
                     True,  True,  True,  True,  True,
                     False, False, False, False, False,
                     False, False, False, False, False]
# Für die Blinkfrequenz 1 Hz:
        Blinkbit2 = [True,  True,  True,  True,  True,
                     False, False, False, False, False,
		             True,  True,  True,  True,  True,
                     False, False, False, False, False]
         
        while True:
            if ((Anzeigedaten["LMUe"] == 0) & (Anzeigedaten["LMTuer"] == 0)):
                Blinkzaehler = 0
            elif (Blinkzaehler >= 19):
                Blinkzaehler = 0
            else:
                Blinkzaehler += 1
                time.sleep(0.1)
# LM Ue
            rpi.io.aLMUe.value = self.LMWert(Anzeigedaten["LMUe"],Blinkbit1[Blinkzaehler], Blinkbit2[Blinkzaehler])
# LM Tueren
            rpi.io.aLMTuer.value = self.LMWert(Anzeigedaten["LMTuer"],Blinkbit1[Blinkzaehler], Blinkbit2[Blinkzaehler])
            if stop_threads:
                break

def AusgabeRevpi(Ausgabedaten):
# LM Sifa
    rpi.io.aLMSifa.value = Ausgabedaten["LMSifa"]
# LM Hohe Abbremsung
    rpi.io.aLMHAB.value = Ausgabedaten["LMHAB"]
# LM Elektrische Bremse
    rpi.io.aLMEB.value = Ausgabedaten["LMEB"]
# Prueftaster Lampen
    rpi.io.aLMPTL.value = False
# LM Notbremse
    rpi.io.aLMNBrems.value = Ausgabedaten["LMNBrems"]
# LM Hauptschalter aus / Getriebe
    if Ausgabedaten["AnzModus"] & 0b100000000000 == 2048:
        rpi.io.aLMHS.value = Ausgabedaten["LMGetriebe"]
    else:
        rpi.io.aLMHS.value = Ausgabedaten["LMHS"]
# LM Zugsammelschiene aus
    rpi.io.aLMZS.value = Ausgabedaten["LMZS"]
# Fahrstufe
    rpi.io.aFstENB.value = bool(Ausgabedaten["AnzModus"] & 0b0001100000000)
    rpi.io.aFstZb0.value = not bool(1 & int(Ausgabedaten["FSt"] / 10))
    rpi.io.aFstZb1.value = not bool(2 & int(Ausgabedaten["FSt"] / 10))
    rpi.io.aFstEb0.value = not bool(1 & int(Ausgabedaten["FSt"] % 10))
    rpi.io.aFstEb1.value = not bool(2 & int(Ausgabedaten["FSt"] % 10))
    rpi.io.aFstEb2.value = not bool(4 & int(Ausgabedaten["FSt"] % 10))
    rpi.io.aFstEb3.value = not bool(8 & int(Ausgabedaten["FSt"] % 10))
# LM Sifa-Hupe
    rpi.io.aHupeSifa.value = Ausgabedaten["HupeSifa"]
# LM PZB-Hupe
    bool(Ausgabedaten["HupePZB"])
# Geschwindigkeit
    rpi.io.aVist.value = int(Ausgabedaten["Vist"] * FaktorGeschwindigkeit)
# Zug-/Bremskraft
    if Ausgabedaten["Fzb"] > 0:
        if Ausgabedaten["AnzModus"] & 0b0000000000001 == 1:
            rpi.io.aFzba.value = int(Zugkraftanzeigefunktion(max(0,min(Ausgabedaten["Fzba"],max(Zugkraftanzeigekennlinie[0])))))
        else:
            rpi.io.aFzba.value = 0
    else:
        if Ausgabedaten["AnzModus"] & 0b0000000000110 == 2:
            rpi.io.aFzba.value = int(Ausgabedaten["Fzb"] * FaktorBremskraft)
        elif Ausgabedaten["AnzModus"] & 0b0000000000110 == 4:
            rpi.io.aFzba.value = int(Ausgabedaten["Fzb"] * FaktorBremskraft2)
        else:
            rpi.io.aFzba.value = 0
# Äußerer Zeiger Zug-/Bremskraft
    if Ausgabedaten["Fzb"] > 0:
        if Ausgabedaten["AnzModus"] & 0b0000000011000 == 8:
            if Ausgabedaten["LMSchleudern"] == True:
                rpi.io.aFzba2.value = 5000
            else: rpi.io.aFzba2.value = 0
        elif Ausgabedaten["AnzModus"] & 0b0000000011000 == 16:
            rpi.io.aFzba2.value = int(Zugkraftanzeigefunktion(max(0,min(Ausgabedaten["Fzbasoll"],max(Zugkraftanzeigekennlinie[0])))))
        elif Ausgabedaten["AnzModus"] & 0b0000000011000 == 24:
            rpi.io.aFzba2.value = int(Zugkraftanzeigefunktion(max(0,min(Ausgabedaten["Fzba"],max(Zugkraftanzeigekennlinie[0])))))
        else:
            rpi.io.aFzba2.value = 0
    else:
        if Ausgabedaten["AnzModus"] & 0b0000001100000 == 32:
            if Ausgabedaten["LMGleiten"] == True:
                rpi.io.aFzba2.value = -5000
            else: rpi.io.aFzba2.value = 0
        elif Ausgabedaten["AnzModus"] & 0b0000001100000 == 64:
            rpi.io.aFzba2.value = int(Ausgabedaten["Fzbsoll"] * FaktorBremskraft)
        elif Ausgabedaten["AnzModus"] & 0b0000001100000 == 96:
            rpi.io.aFzba2.value = int(Ausgabedaten["Fzb"] * FaktorBremskraft)
        elif Ausgabedaten["AnzModus"] & 0b0000001100000 == 128:
            rpi.io.aFzba2.value = int(Ausgabedaten["Fzb"] * FaktorBremskraft2)
        elif Ausgabedaten["AnzModus"] & 0b0000001100000 == 160:
            rpi.io.aFzba2.value = int(Ausgabedaten["Fzb"] * FaktorBremskraft2)
        else:
            rpi.io.aFzba2.value = 0
# Fahrdrahtspannung
    if (Ausgabedaten["AnzModus"] & 0b0010000000000) and (Ausgabedaten["FSt"] > 0):
         rpi.io.aUol.value = int(min(Ausgabedaten["Umot"], 660) * 16.6666666)
    else:
         rpi.io.aUol.value = int(min(Ausgabedaten["Uol"], 21000) * 0.5)
# Oberstrom
    if Ausgabedaten["AnzModus"] & 0b0100000000000:
        rpi.io.aIol.value = int(Ausgabedaten["Nmot"] * 5.0)
    else:
        rpi.io.aIol.value = int(min(Ausgabedaten["Iol"], 500) * 20.0)
    return None

class BedienungThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        global Bediendaten
        while True:
            Bediendatenalt = Bediendaten.copy()
# Fahrschalter
            if rpi.io.eFSNSE.value == True and rpi.io.eFSAB.value == False and rpi.io.eFSFA.value == False and rpi.io.eFSAUF.value == False and rpi.io.eFSFGZ.value == False:
                Bediendaten["FS"] = 0
            elif rpi.io.eFSNSE.value == False and rpi.io.eFSAB.value == True and rpi.io.eFSFA.value == False and rpi.io.eFSAUF.value == False and rpi.io.eFSFGZ.value == False:
                Bediendaten["FS"] = 1
            elif rpi.io.eFSNSE.value == False and rpi.io.eFSAB.value == False and rpi.io.eFSFA.value == True and rpi.io.eFSAUF.value == False and rpi.io.eFSFGZ.value == False:
                Bediendaten["FS"] = 2
            elif rpi.io.eFSNSE.value == False and rpi.io.eFSAB.value == False and rpi.io.eFSFA.value == False and rpi.io.eFSAUF.value == True and rpi.io.eFSFGZ.value == False:
                Bediendaten["FS"] = 3
            elif rpi.io.eFSNSE.value == False and rpi.io.eFSAB.value == False and rpi.io.eFSFA.value == False and rpi.io.eFSAUF.value == True and rpi.io.eFSFGZ.value == True:
                Bediendaten["FS"] = 4
            # else:
            #     print("\tStörung Fahrschalter " + str(rpi.io.eFSNSA.value) + str(rpi.io.eFSNSE.value) + str(rpi.io.eFSAB.value) + str(rpi.io.eFSFA.value) + str(rpi.io.eFSAUF.value) + str(rpi.io.eFSFGZ.value))
            if Bediendaten["FS"] == 4:
                Bediendaten["AFSZ"] = min(max(((rpi.io.eAFSZ1.value - 3000) / 42.5),0.0),100.0)
            else:
                Bediendaten["AFSZ"] = 0
# Richtungsschalter
            if rpi.io.eRSR.value == True and rpi.io.eRS0.value == True and rpi.io.eRSMV.value == False and rpi.io.eRSV.value == False:
                Bediendaten["RS"] = -1
            elif rpi.io.eRSR.value == False and rpi.io.eRS0.value == True and rpi.io.eRSMV.value == True and rpi.io.eRSV.value == False:
                Bediendaten["RS"] = 1
            elif rpi.io.eRSR.value == False and rpi.io.eRS0.value == True and rpi.io.eRSMV.value == True and rpi.io.eRSV.value == True:
                Bediendaten["RS"] = 2
            elif rpi.io.eRSR.value == False and rpi.io.eRSMV.value == False and rpi.io.eRSV.value == False:
                Bediendaten["RS"] = 0
            # else:
            #     print("\tStörung Richtungsschalter " + str(rpi.io.eRSR.value) + str(rpi.io.eRS0.value) + str(rpi.io.eRSMV.value) + str(rpi.io.eRSV.value))
# Bremssteller    
            Bremsstellerwert = min(max((((10000 - rpi.io.eABSSW.value) / 85.0) - 15.0),0.0),100.0)
            if rpi.io.eBSFE.value == True and rpi.io.eBSBE.value == False and rpi.io.eBSB2.value == False and rpi.io.eBSB3.value == False and rpi.io.eBSB4.value == False and rpi.io.eBSSBE.value == False:
                Bediendaten["BS"] = 15
                Bediendaten["ABS"] =   0.0
            elif          rpi.io.eBSFE.value == False and rpi.io.eBSBE.value == True and rpi.io.eBSB2.value == True and rpi.io.eBSB3.value == False and rpi.io.eBSB4.value == False and rpi.io.eBSSBE.value == False and Bremsstellerwert < 20.0:
                Bediendaten["BS"] =  1
                Bediendaten["ABS"] = Bremsstellerwert
            elif          rpi.io.eBSFE.value == False and rpi.io.eBSBE.value == True and rpi.io.eBSB2.value == False and rpi.io.eBSB3.value == True and rpi.io.eBSB4.value == False and rpi.io.eBSSBE.value == False and Bremsstellerwert > 18.0 and Bremsstellerwert < 30.0:
                Bediendaten["BS"] =  1
                Bediendaten["ABS"] = Bremsstellerwert
            elif          rpi.io.eBSFE.value == False and rpi.io.eBSBE.value == True and rpi.io.eBSB2.value == True and rpi.io.eBSB3.value == True and rpi.io.eBSB4.value == False and rpi.io.eBSSBE.value == False and Bremsstellerwert > 28.0 and Bremsstellerwert < 42.0:
                Bediendaten["BS"] =  1
                Bediendaten["ABS"] = Bremsstellerwert
            elif          rpi.io.eBSFE.value == False and rpi.io.eBSBE.value == True and rpi.io.eBSB2.value == False and rpi.io.eBSB3.value == False and rpi.io.eBSB4.value == True and rpi.io.eBSSBE.value == False and Bremsstellerwert > 40.0 and Bremsstellerwert < 56.0:
                Bediendaten["BS"] =  1
                Bediendaten["ABS"] = Bremsstellerwert
            elif          rpi.io.eBSFE.value == False and rpi.io.eBSBE.value == True and rpi.io.eBSB2.value == True and rpi.io.eBSB3.value == False and rpi.io.eBSB4.value == True and rpi.io.eBSSBE.value == False and Bremsstellerwert > 54.0 and Bremsstellerwert < 68.0:
                Bediendaten["BS"] =  1
                Bediendaten["ABS"] = Bremsstellerwert
            elif          rpi.io.eBSFE.value == False and rpi.io.eBSBE.value == True and rpi.io.eBSB2.value == False and rpi.io.eBSB3.value == True and rpi.io.eBSB4.value == True and rpi.io.eBSSBE.value == False and Bremsstellerwert > 66.0 and Bremsstellerwert < 93.0:
                Bediendaten["BS"] =  1
                Bediendaten["ABS"] = Bremsstellerwert
            elif          rpi.io.eBSFE.value == False and rpi.io.eBSBE.value == True and rpi.io.eBSB2.value == True and rpi.io.eBSB3.value == True and rpi.io.eBSB4.value == True and rpi.io.eBSSBE.value == False and Bremsstellerwert > .0:
                Bediendaten["BS"] =  1
                Bediendaten["ABS"] = Bremsstellerwert
            elif          rpi.io.eBSFE.value == False and rpi.io.eBSBE.value == True and rpi.io.eBSB2.value == True and rpi.io.eBSB3.value == True and rpi.io.eBSB4.value == True and rpi.io.eBSSBE.value == True:
                Bediendaten["BS"] =  2
                Bediendaten["ABS"] = 100.0
            # else:
            #     print("\tStörung Bremssteller " + str(rpi.io.eBSFE.value) + str(rpi.io.eBSBE.value) + str(rpi.io.eBSB2.value) + str(rpi.io.eBSB3.value) + str(rpi.io.eBSB4.value) + str(rpi.io.eBSSBE.value))
# Taster Sifa
            Bediendaten["TSifa"] = rpi.io.eFSSIFA.value or rpi.io.eTFSIFA.value
# Taster Stromabnehmer nieder
            Bediendaten["TSAN"] = rpi.io.eTSAN.value
# Taster Stromabnehmer hoch
            Bediendaten["TSAH"] = rpi.io.eTSAH.value
# Taster Hauptschalter Aus
            Bediendaten["THSA"] = rpi.io.eTHSA.value
# Taster Hauptschalter Ein
            Bediendaten["THSE"] = rpi.io.eTHSE.value
# Taster Makrofon
            Bediendaten["TMF"] = rpi.io.eTMF.value or rpi.io.eTFMF.value
# Taster Indusi Wachsam
            Bediendaten["Tw"] = rpi.io.eTw.value
# Taster Indusi Frei
            Bediendaten["Tf"] = rpi.io.eTf.value
# Taster Indusi Befehl
            Bediendaten["Tb"] = rpi.io.eTb.value
# Eingang DIO1 I1
#            Bediendaten["DI1I1"] = rpi.io.I_1.value	
# Eingang DIO1 I2
#            Bediendaten["DI1I2"] = rpi.io.I_2.value	
# Eingang DIO1 I3
#            Bediendaten["DI1I3"] = rpi.io.I_3.value	
# Taster Leuchtmelder prüfen
#            Bediendaten["DI1I4"] = rpi.io.I_4.value	
# Taster Störung quittieren
#            Bediendaten["DI1I5"] = not rpi.io.I_5.value	
# Fahrschalter Schnell-Auf-Befehl
#            Bediendaten["DI1I6"] = rpi.io.I_6.value	
# Taster Bremse lösen
            Bediendaten["TBL"] = rpi.io.eTBL.value	
# Taster Schleuderschutzbremse
            Bediendaten["TSSB"] = rpi.io.eTSSB.value	
# Schalter Luftpresser
            Bediendaten["SLP"] = rpi.io.eSLP.value	
# Schalter Lüfter stark
            Bediendaten["SLST"] = rpi.io.eSLST.value	
# Schalter Lüfter schwach
            Bediendaten["SLSW"] = rpi.io.eSLSW.value	
# Taster Sanden
            Bediendaten["TSAND"] = rpi.io.eTSAND.value	
# Schalter Zugsammelschiene Ein
            Bediendaten["SZSE"] = rpi.io.eSZSE.value	
# Taster Zugsammelschiene An
            Bediendaten["TZSA"] = rpi.io.eTZSA.value	
# Taster FIS-Fortschaltung
#            Bediendaten["TFIS"] = rpi.io.I_9_i04.value	
# Taster Türfreigabe TZ
            Bediendaten["TTFGTZ"] = rpi.io.eTTFGTZ.value	
# Taster Türfreigabe T0
            Bediendaten["TTFGT0"] = not rpi.io.eTTFGTZ0.value	
# Schalter Türfreigabe 0
            Bediendaten["STFG0"] = rpi.io.eSTFG0.value	
# Schalter Türfreigabe rechts
            Bediendaten["STFGR"] = rpi.io.eSTFGR.value	
# Schalter Türfreigabe links
            Bediendaten["STFGL"] = rpi.io.eSTFGL.value	
# Taster Zugbeleuchtung Aus
            Bediendaten["TZLA"] = rpi.io.eTZLA.value	
# Taster Zugbeleuchtung Ein
            Bediendaten["TZLE"] = rpi.io.eTZLE.value	
# Schalter Fernlicht
            Bediendaten["SFL"] = rpi.io.eSFL.value	
# Schalter Heizen
#            Bediendaten["DI4I10"] = rpi.io.I_10_i05.value	
# Schalter Lüften
#            Bediendaten["DI4I11"] = rpi.io.I_11_i05.value	
# Schalter Signallicht Ein
            Bediendaten["SSL"] = rpi.io.eSSL.value	
# Führerraumleuchte
#            Bediendaten["DI4I13"] = rpi.io.I_13_i05.value	
# DI4I14
#            Bediendaten["DI4I14"] = rpi.io.I_14_i05.value	
#
            # Textausgabe.Textbedienanzeige(Bediendaten,Bediendatenalt)
            SchnittstelleFT.UDPBedienDatenErzeugenFT1(Bediendaten)
            if Bediendatenalt != Bediendaten:
                Ft1SSocket.sendto(SchnittstelleFT.UDPBedienDatenErzeugenFT1(Bediendaten),(Adap_IP, Ft1S_Port))
            time.sleep(0.1)
            if stop_threads:
                break


# Beginn des Hauptprogrammes
BUFFER_SIZE = 1024

Ft1ESocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
Ft1SSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    MFALMThread()
    BedienungThread()
    Ft1ESocket.bind(("", Ft1E_Port))
    # i = -90.0
    while True:
        daten, addr = Ft1ESocket.recvfrom(BUFFER_SIZE)
        # msg = "Message from Loksim {}".format(daten)
        # msg_2 = "Adress from Loksim {}".format(addr[0])
        # print(str(msg),"  ", str(msg_2))
        # print("Anzahl der Zeichen des UDP-Pakets:\t",len(daten))
        SchnittstelleFT.UDPAnzeigeDatenAuswertenFT1(daten,Anzeigedaten)
        # Textausgabe.Textanzeige(Anzeigedaten,Anzeigedatenalt)
        # Anzeigedatenalt = Anzeigedaten.copy()
        # Anzeigedaten["AnzModus"] = 83
        # Anzeigedaten["Fzba"] = i
        # Anzeigedaten["Fzbasoll"] = i
        # Anzeigedaten["Fzb"] = i
        # Anzeigedaten["Fzbsoll"] = i
        # print(i, int(Zugkraftanzeigefunktion(max(0,min(Anzeigedaten["Fzba"],max(Zugkraftanzeigekennlinie[0]))))))
        # if i < 80.0:
        #     i = i + 5.0
        # else:
        #     i = -90.0
        AusgabeRevpi(Anzeigedaten)
        # time.sleep(2)
finally:
    Ft1ESocket.close()
    Ft1SSocket.close()
    stop_threads = True 
    Anzeigedaten = AnzeigedatenGrundstellung
    AusgabeRevpi(Anzeigedaten)

