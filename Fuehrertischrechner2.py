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
the software 'Fuehrertischrechner2' (a software for data exchange).

Wolfgang Evers
Versionsdatum 14.10.2022

"""
import time
import socket
import threading
import revpimodio2  # Zum Ansprechen der IOs
import SchnittstelleFT
# import Textausgabe
import Testfunktionen

# Netzwerkdaten
Adap_IP = "192.168.111.11" # IP-Adresse des Rechners mit dem Adapterprogramm
Ft2E_Port = 51437          # Empfangsport des zweiten Steuergeräts des Führertischs
Ft2S_Port = 51439          # Sendeport des zweiten Steuergeräts des Führertischs

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
                "AnzModus": 3,         # Anzeigemodus
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

Bediendaten = {"FS": 0,          # Fahrschalterstellung
               "AFSZ": 0.0,      # Fahrschalter Sollwert Zugkraft in %
               "RS": 0,          # Richtungsschalter Stellung
               "TSifa": False,   # Taster Sifa
               "FbV": 0,         # Führerbremsventilstellung
               "DruckFbVA": 0.0, # Führerbremsventil A-Druck in bar
               "FbVAg": False,   # Führerbremsventil Angleicher
               "FbVSchl": False, # Führerbremsventil Schlüssel
               "BS": 0.0,        # Bremssteller Sollwert Bremskraft in %
               "ZbVBr": False,   # Zusatzbremsventil Bremsen
               "ZbVLoe": False,  # Zusatzbremsventil Lösen
               "SLP": False,     # Schalter Luftpresser
               "SLST": False,    # Schalter Lüfter stark
               "SLSW": False,    # Schalter Lüfter schwach
               "TSAN": False,    # Taster Stromabnehmer nieder
               "TSAH": False,    # Taster Stromabnehmer hoch
               "THSA": False,    # Taster Hauptschalter Aus
               "THSE": False,    # Taster Hauptschalter Ein
               "SZSE": False,    # Schalter Zugsammelschiene Ein
               "TZSA": False,    # Taster Zugsammelschiene An
               "Tb": False,      # Taster Indusi Befehl
               "Tf": False,      # Taster Indusi Frei
               "Tw": False,      # Taster Indusi Wachsam
               "STFG0": False,   # Schalter Türfreigabe 0
               "STFGR": False,   # Schalter Türfreigabe rechts
               "STFGL": False,   # Schalter Türfreigabe links
               "TZLA": False,    # Taster Zugbeleuchtung Aus
               "TZLE": False,    # Taster Zugbeleuchtung Ein
               "TSAND": False,   # Taster Sanden
               "TSSB": False,    # Taster Schleuderschutzbremse
               "TBL": False,     # Taster Bremse lösen
               "SFL": False,     # Schalter Fernlicht
               "SSL": False,     # Schalter Signallicht
               "TMF": False,     # Taster Makrofon
               "TTFGTZ": False,  # Taster Türfreigabe TZ
               "TTFGT0": False,  # Taster Türfreigabe T0
               "TFIS": False}    # Taster FIS-Fortschaltung
#               "DI1I1": False,   # 
#               "DI1I2": False,   # 
#               "DI1I3": False,   # 
#               "DI1I4": False,   # Taster Leuchtmelder prüfen
#               "DI1I5": False,   # Taster Störung quittieren
#               "DI1I6": False,   # Fahrschalter Schnell-Auf-Befehl
#               "DI4I10": False,  # Schalter Heizen
#               "DI4I11": False,  # Schalter Lüften
#               "DI4I12": False,  # 
#               "DI4I13": False,  # 
#               "DI4I14": False}  # 

stop_threads = False

# revpimodio konfigurieren
rpi = revpimodio2.RevPiModIO(autorefresh=True)
rpi.cycletime = 100


def AusgabeRevpi(Ausgabedaten):
# Druck Hauptluftleitung
    rpi.io.aDruckHL.value = int(4000.0 + (Ausgabedaten["DruckHL"] * 1600.0))
# Druck Bremszylinder
    rpi.io.aDruckC.value = int(4000.0 + (Ausgabedaten["DruckC"] * 1600.0))
# Druck Hauptluftbehälter
    rpi.io.aDruckHB.value = int(4000.0 + (Ausgabedaten["DruckHB"] * 1600.0))
# Druck Zeitbehälter
    if Ausgabedaten["AnzModus"] & 0b1000000000000:
        rpi.io.aDruckZ.value = int(4000.0 + ((5.0 - Ausgabedaten["DruckZ"]) * 1600.0))
    else:
        rpi.io.aDruckZ.value = int(4000.0 + (Ausgabedaten["DruckZ"] * 1600.0))
    return None

class BedienungThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        global Bediendaten
        DruckFbVLalt = (rpi.io.eDruckFbVL.value - 3950.0)/1600.0
        DruckFbVZalt = (rpi.io.eDruckFbVZ.value - 3950.0)/1600.0
        FbVFS = False
        while True:
            Bediendatenalt = Bediendaten.copy()
# Versorgungsdruck
            DruckVers = (rpi.io.eDruckVers.value - 3950.0)/1600.0
            # print("Versorgungsdruck: ",DruckVers , " bar")
# Führerbremsventil A-Druck
            Bediendaten["DruckFbVA"] = (rpi.io.eDruckFbVA.value - 3950.0)/1600.0
            # print("A-Druck: ",Bediendaten["DruckFbVA"], " bar")
# Führerbremsventil
            DruckFbVL = (rpi.io.eDruckFbVL.value - 3950.0)/1600.0
            # print("Füllstoß: ",DruckFbVL , " bar")
            DruckFbVLalt = min(DruckFbVLalt, DruckVers) 
            if DruckVers < 5.0:
                FbVFS = False
            else:
                if (not FbVFS) and (DruckFbVL > DruckVers - 1.0):
                    FbVFS = True
                    DruckFbVLalt = DruckFbVL
                elif FbVFS and ((DruckFbVL < 0.8) or ((DruckFbVL + 0.15) < DruckFbVLalt)):
                    FbVFS = False
                    DruckFbVLalt = DruckFbVL
                elif abs(DruckFbVL - DruckFbVLalt) > 0.25:
                    DruckFbVLalt = DruckFbVL
            if (not FbVFS) and (not rpi.io.eFbVFFs.value) and rpi.io.eFbVBb.value:
                Bediendaten["FbV"] = 1  # Betriebsbremse
            elif (not FbVFS) and (not rpi.io.eFbVFFs.value) and (not rpi.io.eFbVBb.value) and (DruckFbVL < 4.0):
                Bediendaten["FbV"] = 2  # Schnellbremse
            elif FbVFS and rpi.io.eFbVFFs.value and (not rpi.io.eFbVBb.value):
                Bediendaten["FbV"] = 14 # Füllstoß
            elif (not FbVFS) and rpi.io.eFbVFFs.value and (not rpi.io.eFbVBb.value):
                Bediendaten["FbV"] = 15 # Fahrt
            else:
                Bediendaten["FbV"] = 0  # Abschluss
                print("Fehler Führerbremsventil")
# Führerbremsventil Angleicher
            DruckFbVZ = (rpi.io.eDruckFbVZ.value - 3950.0)/1600.0
            # print("Angleicher: ",DruckFbVZ , " bar")
            DruckFbVZalt = min(DruckFbVZalt, DruckVers) 
            if DruckVers < 5.0:
                Bediendaten["FbVAg"] = False
            else:
                if (not Bediendaten["FbVAg"]) and ((DruckFbVZ < 0.8) or ((DruckFbVZ + 0.2) < DruckFbVZalt)):
                    Bediendaten["FbVAg"] = True
                    DruckFbVZalt = DruckFbVZ
                elif Bediendaten["FbVAg"] and ((DruckFbVZ > DruckVers - 1.0) or (DruckFbVZ > (DruckFbVZalt + 0.2))):
                    Bediendaten["FbVAg"] = False
                    DruckFbVZalt = DruckFbVZ
                elif abs(DruckFbVZ - DruckFbVZalt) > 0.25:
                    DruckFbVZalt = DruckFbVZ
# Führerbremsventil Schlüssel
            Bediendaten["FbVSchl"] = (rpi.io.eDruckFbVAb.value > 10000)
#            print("AB-Druck: ",(rpi.io.eDruckFbVAb.value - 3950.0)/1600.0, " bar")
# Zusatzbremsventil Bremsen
            Bediendaten["ZbVBr"] = (not rpi.io.eZbVBr.value) and (not rpi.io.eZbVLoe.value)
# Zusatzbremsventil Lösen
            Bediendaten["ZbVLoe"] = rpi.io.eZbVBr.value and rpi.io.eZbVLoe.value
# Zusatzbremsventil Fehler
            if Bediendaten["ZbVBr"] and Bediendaten["ZbVLoe"]:
                Bediendaten["ZbVBr"] = False
                Bediendaten["ZbVLoe"] = False
                print("Fehler Zusatzbremsventil")
# Bediendaten senden           
            # Textausgabe.Textbedienanzeige(Bediendaten,Bediendatenalt)
            if Bediendatenalt != Bediendaten:
                Ft2SSocket.sendto(SchnittstelleFT.UDPBedienDatenErzeugenFT2(Bediendaten),(Adap_IP, Ft2S_Port))
            time.sleep(0.1)
            if stop_threads:
                break

# Beginn des Hauptprogrammes
BUFFER_SIZE = 1024

Ft2ESocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
Ft2SSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    BedienungThread()
    Ft2ESocket.bind(("", Ft2E_Port))
    while True:
        daten, addr = Ft2ESocket.recvfrom(BUFFER_SIZE)
        # msg = "Message from Loksim {}".format(daten)
        # msg_2 = "Adress from Loksim {}".format(addr[0])
        # print(str(msg),"  ", str(msg_2))
        # print("Anzahl der Zeichen des UDP-Pakets:\t",len(daten))
        SchnittstelleFT.UDPAnzeigeDatenAuswertenFT2(daten,Anzeigedaten)
        # Textausgabe.Textanzeige(Anzeigedaten,Anzeigedatenalt)
        # Anzeigedatenalt = Anzeigedaten.copy()
        AusgabeRevpi(Anzeigedaten)
finally:
    Ft2ESocket.close()
    Ft2SSocket.close()
    stop_threads = True 
    Testfunktionen.AusgabeReset(Anzeigedaten)
    AusgabeRevpi(Anzeigedaten)

