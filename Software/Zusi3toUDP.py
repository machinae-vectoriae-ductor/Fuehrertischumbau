#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Dieser Quellcode ist in Python 3 geschrieben und realisiert einen TCP-Client fuer die Simulation Zusi 3.
Nach dem Start des TCP-Clients meldet sich dieser bei Zusi 3 durch Angabe der IP-Adresse und Port an.
Die empfangenen Anzeige- und Statusdaten werden aufbereitet und über UDP an die im Führertisch verbauten Rechner ausgegeben, über eine serielle Schnittstelle zu einer LZB-MFA übertragen und auf der Textkonsole ausgegeben.
Zudem werden per UDP Bediendaten von den Führertischrechnern empfangen, aufbereitet und an Zusi 3 geschickt.
Der Algorithmus zum Empfangen der Daten ist von QDmi (https://github.com/nonesense84/QDmi) von Jens Eggert inspiriert. 

This source code is written in Python 3 and implements a TCP client for the simulation Zusi 3.
After starting the TCP client, it logs on to Zusi 3 by specifying the IP address and port.
The received display and status data are processed and output via UDP to the computers installed in the driver's desk, transmitted via a serial interface to an LZB-MFA and output on the text console.
In addition, operating data is received from the driver's desk computers via UDP, processed and sent to Zusi 3.
The algorithm for receiving the data is inspired by QDmi (https://github.com/nonesense84/QDmi) by Jens Eggert.

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

TH Koeln, hereby disclaims all copyright interest in
the software 'Zusi3toUDP' (a software for TCP Client for Zusi 3).

Wolfgang Evers
Versionsdatum 20.05.2022

"""

import socket
import threading
import struct
import math
import time
import serial
import SchnittstelleLZB
import SchnittstelleFT
import Textausgabe

# Netzwerkdaten
Zusi_IP = "127.0.0.1"     # Zusi-Adresse
Zusi_Port = 1436          # Beachte Port 1436 von Zusi 3
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

# Zähler für Schleifen
i = 0

Speicher = bytearray(65525)  # Speicher für die eingelesenen TCP-Pakete
PaketLaengeBytearray = bytearray(4)
NodeIDBytearray = bytearray(2)
anzFolgenderBytes = int(0)
rohdatenEinlesen = bool(0)
rohdatenWeiterverarbeiten = bool(0)
Ebene = 0
LetzterKnotenNeu = False
Verbindungsergebnis = False
Datenanforderungsergebnis = False

HELLO = bytes([0x00, 0x00, 0x00, 0x00, # Knoten
               0x01, 0x00,             # Verbindungsaufbau
               0x00, 0x00, 0x00, 0x00, # Knoten
               0x01, 0x00,             # Hello-Befehl
               0x04, 0x00, 0x00, 0x00, # Länge 4 Bytes -> es folgt ein Attribut
               0x01, 0x00,
               0x02, 0x00,             # Protokoll-Version "2"
               0x04, 0x00, 0x00, 0x00, # Länge 4 Bytes -> es folgt ein Attribut
               0x02, 0x00,
               0x02, 0x00,             # Client-Typ "Fahrpult"
               0x0A, 0x00, 0x00, 0x00, # Länge 10 Bytes -> es folgt ein Attribut
               0x03, 0x00,
               0x54, 0x48, 0x20, 0x4B,
               0x6F, 0x65, 0x6C, 0x6E, # String "TH Koeln"
               0x05, 0x00, 0x00, 0x00, # Länge 5 Bytes -> es folgt ein Attribut
               0x04, 0x00,             # Version
               0x30, 0x2E, 0x31,       # String "0.1"
               0xFF, 0xFF, 0xff, 0xFF, # Ende Knoten
               0xFF, 0xFF, 0xff, 0xFF])



NEEDED_DATA = bytes([0x00, 0x00, 0x00, 0x00,                         # Knoten Ebene 0
                     0x02, 0x00,                                     # Client-Anwendung Typ 2 (Fahrpult)
                     0x00, 0x00, 0x00, 0x00,                         # Knoten Ebene 1
                     0x03, 0x00,                                     # NEEDED_DATA-Befehl
                     0x00, 0x00, 0x00, 0x00,                         # Knoten Ebene 2
                     0x0A, 0x00,                                     # Untergruppe Führerstandsanzeigen
                     0x04, 0x00, 0x00, 0x00, 0x01, 0x00, 0x01, 0x00, # Geschwindigkeit
                     0x04, 0x00, 0x00, 0x00, 0x01, 0x00, 0x02, 0x00, # Druck Hauptluftleitung
                     0x04, 0x00, 0x00, 0x00, 0x01, 0x00, 0x03, 0x00, # Druck Bremszylinder
                     0x04, 0x00, 0x00, 0x00, 0x01, 0x00, 0x04, 0x00, # Druck Hauptluftbehälter
                     0x04, 0x00, 0x00, 0x00, 0x01, 0x00, 0x09, 0x00, # Zugkraft gesamt
                     0x04, 0x00, 0x00, 0x00, 0x01, 0x00, 0x0A, 0x00, # Zugkraft pro Achse
                     0x04, 0x00, 0x00, 0x00, 0x01, 0x00, 0x0D, 0x00, # Oberstrom
                     0x04, 0x00, 0x00, 0x00, 0x01, 0x00, 0x0E, 0x00, # Fahrleitungsspannung
                     # 0x04, 0x00, 0x00, 0x00, 0x01, 0x00, 0x0F, 0x00, # Motordrehzahl
                     0x04, 0x00, 0x00, 0x00, 0x01, 0x00, 0x13, 0x00, # Hauptschalter
                     0x04, 0x00, 0x00, 0x00, 0x01, 0x00, 0x15, 0x00, # Fahrstufe
                     0x04, 0x00, 0x00, 0x00, 0x01, 0x00, 0x17, 0x00, # AFB-Sollgeschwindigkeit
                     0x04, 0x00, 0x00, 0x00, 0x01, 0x00, 0x19, 0x00, # Zurückgelegter Gesamtweg
                     0x04, 0x00, 0x00, 0x00, 0x01, 0x00, 0x1A, 0x00, # LM Getriebe
                     0x04, 0x00, 0x00, 0x00, 0x01, 0x00, 0x1B, 0x00, # LM Schleudern
                     0x04, 0x00, 0x00, 0x00, 0x01, 0x00, 0x1C, 0x00, # LM Gleiten
                     0x04, 0x00, 0x00, 0x00, 0x01, 0x00, 0x20, 0x00, # LM Hochabbremsung
                     0x04, 0x00, 0x00, 0x00, 0x01, 0x00, 0x21, 0x00, # LM Schnellbremsung
                     0x04, 0x00, 0x00, 0x00, 0x01, 0x00, 0x22, 0x00, # Status Notbremsung
                     0x04, 0x00, 0x00, 0x00, 0x01, 0x00, 0x23, 0x00, # LM Uhrzeit (digital)
                     0x04, 0x00, 0x00, 0x00, 0x01, 0x00, 0x36, 0x00, # AFB an
                     0x04, 0x00, 0x00, 0x00, 0x01, 0x00, 0x55, 0x00, # Stromabnehmer
                     0x04, 0x00, 0x00, 0x00, 0x01, 0x00, 0x5E, 0x00, # Druck Zeitbehälter
                     0x04, 0x00, 0x00, 0x00, 0x01, 0x00, 0x61, 0x00, # Kilometrierung (Zugspitze)
                     0x04, 0x00, 0x00, 0x00, 0x01, 0x00, 0x63, 0x00, # Motorspannung
                     0x04, 0x00, 0x00, 0x00, 0x01, 0x00, 0x64, 0x00, # Status Sifa
                     0x04, 0x00, 0x00, 0x00, 0x01, 0x00, 0x65, 0x00, # Status Zugbeeinﬂussung
                     0x04, 0x00, 0x00, 0x00, 0x01, 0x00, 0x66, 0x00, # Status Türsystem
                     0x04, 0x00, 0x00, 0x00, 0x01, 0x00, 0x8E, 0x00, # Status Zug
                     0xFF, 0xFF, 0xFF, 0xFF,                         # Ende Knoten Ebene 2
                     0x00, 0x00, 0x00, 0x00,                         # Knoten Ebene 2
                     0x0C, 0x00,                                     # Untergruppe DATA_PROG
                     0x04, 0x00, 0x00, 0x00, 0x01, 0x00, 0x01, 0x00, # Aktuelle Zugdatei
                     0x04, 0x00, 0x00, 0x00, 0x01, 0x00, 0x02, 0x00, # Aktuelle Zugnummer
                     0x04, 0x00, 0x00, 0x00, 0x01, 0x00, 0x04, 0x00, # Buchfahrplanrohdatei
                     0xFF, 0xFF, 0xFF, 0xFF,                         # Ende Knoten Ebene 2
                     0x00, 0x00, 0x00, 0x00,                         # Knoten Ebene 2
                     0x0B, 0x00,                                     # Untergruppe DATA_OPERATION
                     0x04, 0x00, 0x00, 0x00, 0x01, 0x00, 0x01, 0x00, # Betätigungsvorgang
                     0x04, 0x00, 0x00, 0x00, 0x01, 0x00, 0x02, 0x00, # Kombischalter Hebelpositionen
                     0xFF, 0xFF, 0xFF, 0xFF,                         # Ende Knoten Ebene 2
                     0xFF, 0xFF, 0xFF, 0xFF,                         # Ende Knoten Ebene 1
                     0xFF, 0xFF, 0xFF, 0xFF])                        # Ende Knoten Ebene 0

# Gemäß Protokoll wird ein zweites NEEDED_DATA-befehl benötigt zum Anfordern der Daten
NEEDED_DATA2 = bytes([0x04, 0x00, 0x00, 0x00, # Paketlaenge = 4
                      0x00, 0x03,             # Befehl NEEDED_DATA
                      0x00, 0x00])            # Befehlsvorrat Letzter Befehl

def ZusiBytezuLM(Speicher):
    if Speicher[0] == 0:
        AnzeigeLMWert = 0
    elif Speicher[0] == 1:
        AnzeigeLMWert = 1
    elif Speicher[0] == 2:
        AnzeigeLMWert = 3
    elif Speicher[0] == 3:
        AnzeigeLMWert = 11
    else:
        AnzeigeLMWert = 5
    return AnzeigeLMWert

def ZusiWordzuInt(Speicher):
    AnzeigeWordWert = struct.unpack("H", Speicher[:2])  # Umwandlung von Binärdaten in word
    AnzeigeWordWert = AnzeigeWordWert[0]
    return AnzeigeWordWert

def ZusiSmallIntzuInt(Speicher):
    AnzeigeSmallIntWert = struct.unpack("h", Speicher[:2])  # Umwandlung von Binärdaten in word
    AnzeigeSmallIntWert = AnzeigeSmallIntWert[0]
    return AnzeigeSmallIntWert

def ZusiSinglezuBool(Speicher):
    AnzeigeSingleWert = struct.unpack("f", Speicher[:4])  # Umwandlung von Binärdaten in float
    AnzeigeBoolWert = bool(AnzeigeSingleWert[0])  # Umwandlung von float in bool
    return AnzeigeBoolWert

def ZusiSinglezuInt(Speicher):
    AnzeigeSingleWert = struct.unpack("f", Speicher[:4])  # Umwandlung von Binärdaten in float
    if math.isnan(AnzeigeSingleWert[0]):
        AnzeigeIntWert = 0
    else:
        AnzeigeIntWert = int(AnzeigeSingleWert[0])  # Umwandlung von float in int
    return AnzeigeIntWert

def ZusiSinglezuInt1000(Speicher):
    AnzeigeSingleWert = struct.unpack("f", Speicher[:4])  # Umwandlung von Binärdaten in float
    if math.isnan(AnzeigeSingleWert[0]):
        AnzeigeIntWert = 0
    else:
        AnzeigeIntWert = int(AnzeigeSingleWert[0] * 1000)  # Umwandlung von float in int
    return AnzeigeIntWert

def ZusiSinglezuFloat(Speicher):
    AnzeigeFloatWert = struct.unpack("f", Speicher[:4])  # Umwandlung von Binärdaten in float
    AnzeigeFloatWert = AnzeigeFloatWert[0]
    return AnzeigeFloatWert

def ZusiStringtoString(Speicher,Laenge):
    AnzeigeString = Speicher[:Laenge].decode('iso-8859-1')
    return AnzeigeString

def BedienungnachZusiElement(Tastaturzuordnung,Tastaturkommando,Tastaturaktion,Kombischalterfunktion,Spezialparameter):
    Schalterdaten = bytearray()
    Schalterdaten.extend((0x00, 0x00, 0x00, 0x00,
                           0x01, 0x00,
                            0x04, 0x00, 0x00, 0x00, 0x01, 0x00))
    Schalterdaten.extend(struct.pack("H", Tastaturzuordnung))
    Schalterdaten.extend((  0x04, 0x00, 0x00, 0x00, 0x02, 0x00))
    Schalterdaten.extend(struct.pack("H", Tastaturkommando))
    Schalterdaten.extend((  0x04, 0x00, 0x00, 0x00, 0x03, 0x00))
    Schalterdaten.extend(struct.pack("H", Tastaturaktion))
    Schalterdaten.extend((  0x04, 0x00, 0x00, 0x00, 0x04, 0x00))
    Schalterdaten.extend(struct.pack("h", Kombischalterfunktion))
    Schalterdaten.extend((  0x06, 0x00, 0x00, 0x00, 0x05, 0x00))
    Schalterdaten.extend(struct.pack("f", Spezialparameter))
    Schalterdaten.extend((  0xFF, 0xFF, 0xFF, 0xFF))
    return Schalterdaten

def BedienungnachZusi(Sendebediendaten,Sendebediendatenalt):
    TCPSendeDaten = bytearray()
    while (not Verbindungsergebnis) or (not Datenanforderungsergebnis):
        time.sleep(1)
    TCPSendeDaten.extend((0x00, 0x00, 0x00, 0x00,
                      0x02, 0x00,
                       0x00, 0x00, 0x00, 0x00,
                       0x0A, 0x01))
# Fahrschalter
    if Sendebediendaten["FS"] != Sendebediendatenalt["FS"]:
        TCPSendeDaten.extend(BedienungnachZusiElement(0x01, 0x00, 0x07, Sendebediendaten["FS"], 0.0))
# Bislang ist nur ein Auf-Ab-Fahrschalter implementiert
    # if Sendebediendaten["AFSZ"] != Sendebediendatenalt["AFSZ"]:
    #     if Sendebediendaten["FS"] == 4:
    #         TCPSendeDaten.extend(BedienungnachZusiElement(0x01, 0x00, 0x00, 0x10, 1.0))
    #     else:
    #         TCPSendeDaten.extend(BedienungnachZusiElement(0x01, 0x00, 0x00, 0x10, 0.0))
    #     TCPSendeDaten.extend(BedienungnachZusiElement(0x01, 0x00, 0x07, Sendebediendaten["FS"], 0.0))
# Steller dynamische Bremse
    if Sendebediendaten["BS"] != Sendebediendatenalt["BS"]:
        Bremssteller = 9
        if Sendebediendaten["BS"] <= 7.0:
            Bremssteller = 9
        elif Sendebediendaten["BS"] <= 24.0:
            Bremssteller = 8
        elif Sendebediendaten["BS"] <= 37.0:
            Bremssteller = 7
        elif Sendebediendaten["BS"] <= 45.0:
            Bremssteller = 6
        elif Sendebediendaten["BS"] <= 57.0:
            Bremssteller = 5
        elif Sendebediendaten["BS"] <= 60.0:
            Bremssteller = 4
        elif Sendebediendaten["BS"] <= 73.0:
            Bremssteller = 3
        elif Sendebediendaten["BS"] <= 85.0:
            Bremssteller = 2
        else :
            Bremssteller = 1
        TCPSendeDaten.extend(BedienungnachZusiElement(0x02, 0x00, 0x07, Bremssteller, 0.0))
# Führerbremsventil
# Da die Druckluft am jetzigen Stundplatz des Führertisches fehlt,
# ist das FbV provisorisch mit dem E-Bremssteller verbunden
        TCPSendeDaten.extend(BedienungnachZusiElement(0x04, 0x00, 0x07, Bremssteller, 0.0))
# Angleicher
    if Sendebediendaten["FbVAg"] != Sendebediendatenalt["FbVAg"]:
        if Sendebediendaten["FbVAg"]:
            TCPSendeDaten.extend(BedienungnachZusiElement(0x29, 0x1F, 0x01, 0x00, 0.0))
        else:
            TCPSendeDaten.extend(BedienungnachZusiElement(0x29, 0x20, 0x02, 0x00, 0.0))
# Zusatzbremsventil
    if Sendebediendaten["ZbVBr"] != Sendebediendatenalt["ZbVBr"]:
        if Sendebediendaten["ZbVBr"]:
            TCPSendeDaten.extend(BedienungnachZusiElement(0x05, 0x00, 0x07, 0x00, 0.0))
        else:
            TCPSendeDaten.extend(BedienungnachZusiElement(0x05, 0x00, 0x07, 0x01, 0.0))
    if Sendebediendaten["ZbVLoe"] != Sendebediendatenalt["ZbVLoe"]:
        if Sendebediendaten["ZbVLoe"]:
            TCPSendeDaten.extend(BedienungnachZusiElement(0x05, 0x00, 0x07, 0x02, 0.0))
        else:
            TCPSendeDaten.extend(BedienungnachZusiElement(0x05, 0x00, 0x07, 0x01, 0.0))
# Richtungsschalter
    if Sendebediendaten["RS"] != Sendebediendatenalt["RS"]:
        if Sendebediendaten["RS"] ==  2:
            TCPSendeDaten.extend(BedienungnachZusiElement(0x07, 0x00, 0x07, 0x03, 0.0))
        elif Sendebediendaten["RS"] ==  1:
            TCPSendeDaten.extend(BedienungnachZusiElement(0x07, 0x00, 0x07, 0x02, 0.0))
        elif Sendebediendaten["RS"] ==  0:
            TCPSendeDaten.extend(BedienungnachZusiElement(0x07, 0x00, 0x07, 0x01, 0.0))
        elif Sendebediendaten["RS"] == -1:
            TCPSendeDaten.extend(BedienungnachZusiElement(0x07, 0x00, 0x07, 0x00, 0.0))
# Sander
    if Sendebediendaten["TSAND"] != Sendebediendatenalt["TSAND"]:
        if Sendebediendaten["TSAND"]:
            TCPSendeDaten.extend(BedienungnachZusiElement(0x09, 0x2F, 0x01, 0x00, 0.0))
        else:
            TCPSendeDaten.extend(BedienungnachZusiElement(0x09, 0x30, 0x02, 0x00, 0.0))
# Türen
# Türschalter noch nicht richtig implementiert
    # if Sendebediendaten["STFG0"] != Sendebediendatenalt["STFG0"]:
    #     if Sendebediendaten["STFG0"]:
    #         TCPSendeDaten.extend(BedienungnachZusiElement(0x0A, 0x2F, 0x01, 0x00, 0.0))
    #     else:
    #         TCPSendeDaten.extend(BedienungnachZusiElement(0x0A, 0x30, 0x02, 0x00, 0.0))
    # if Sendebediendaten["SFL"] != Sendebediendatenalt["SFL"]:
    #     if Sendebediendaten["SFL"]:
    #         TCPSendeDaten.extend(BedienungnachZusiElement(0x0B, 0x2F, 0x01, 0x00, 0.0))
    #     else:
    #         TCPSendeDaten.extend(BedienungnachZusiElement(0x0B, 0x30, 0x02, 0x00, 0.0))
# Pfeife
    if Sendebediendaten["TMF"] != Sendebediendatenalt["TMF"]:
        if Sendebediendaten["TMF"]:
            TCPSendeDaten.extend(BedienungnachZusiElement(0x0C, 0x45, 0x01, 0x00, 0.0))
        else:
            TCPSendeDaten.extend(BedienungnachZusiElement(0x0C, 0x46, 0x02, 0x00, 0.0))
# Lüfter
    if (Bediendaten["SLST"] != Sendebediendatenalt["SLST"]) or (Bediendaten["SLSW"] != Bediendaten["SLSW"]):
        if Bediendaten["SLST"] or Bediendaten["SLSW"]:
            TCPSendeDaten.extend(BedienungnachZusiElement(0x0E, 0x49, 0x01, 0x00, 0.0))
        else:
            TCPSendeDaten.extend(BedienungnachZusiElement(0x0E, 0x4A, 0x02, 0x00, 0.0))
# Zugbeeinflussung
    if Sendebediendaten["Tw"] != Sendebediendatenalt["Tw"]:
        if Sendebediendaten["Tw"]:
            TCPSendeDaten.extend(BedienungnachZusiElement(0x0F, 0x33, 0x01, 0x00, 0.0))
        else:
            TCPSendeDaten.extend(BedienungnachZusiElement(0x0F, 0x34, 0x02, 0x00, 0.0))
    if Sendebediendaten["Tf"] != Sendebediendatenalt["Tf"]:
        if Sendebediendaten["Tf"]:
            TCPSendeDaten.extend(BedienungnachZusiElement(0x0F, 0x35, 0x01, 0x00, 0.0))
        else:
            TCPSendeDaten.extend(BedienungnachZusiElement(0x0F, 0x36, 0x02, 0x00, 0.0))
    if Sendebediendaten["Tb"] != Sendebediendatenalt["Tb"]:
        if Sendebediendaten["Tb"]:
            TCPSendeDaten.extend(BedienungnachZusiElement(0x0F, 0x37, 0x01, 0x00, 0.0))
        else:
            TCPSendeDaten.extend(BedienungnachZusiElement(0x0F, 0x38, 0x02, 0x00, 0.0))
# Sifa
    if Sendebediendaten["TSifa"] != Sendebediendatenalt["TSifa"]:
        if Sendebediendaten["TSifa"]:
            TCPSendeDaten.extend(BedienungnachZusiElement(0x10, 0x39, 0x01, 0x00, 0.0))
        else:
            TCPSendeDaten.extend(BedienungnachZusiElement(0x10, 0x3A, 0x02, 0x00, 0.0))
# Hauptschalter
    if Sendebediendaten["THSE"] != Sendebediendatenalt["THSE"]:
        if Sendebediendaten["THSE"]:
            TCPSendeDaten.extend(BedienungnachZusiElement(0x11, 0x4F, 0x01, 0x00, 0.0))
        else:
            TCPSendeDaten.extend(BedienungnachZusiElement(0x11, 0x50, 0x02, 0x00, 0.0))
    if Sendebediendaten["THSA"] != Sendebediendatenalt["THSA"]:
        if Sendebediendaten["THSA"]:
            TCPSendeDaten.extend(BedienungnachZusiElement(0x11, 0x51, 0x01, 0x00, 0.0))
        else:
            TCPSendeDaten.extend(BedienungnachZusiElement(0x11, 0x52, 0x02, 0x00, 0.0))
# Schleuderschutz
    if Sendebediendaten["TSSB"] != Sendebediendatenalt["TSSB"]:
        if Sendebediendaten["TSSB"]:
            TCPSendeDaten.extend(BedienungnachZusiElement(0x13, 0x31, 0x01, 0x00, 0.0))
        else:
            TCPSendeDaten.extend(BedienungnachZusiElement(0x13, 0x32, 0x02, 0x00, 0.0))
# Lokbremse lösen (noch nicht richtig implementiert)
    # if Sendebediendaten["TBL"] != Sendebediendatenalt["TBL"]:
    #     if Sendebediendaten["TBL"]:
    #         TCPSendeDaten.extend(BedienungnachZusiElement(0x15, 0x, 0x01, 0x00, 0.0))
    #     else:
    #         TCPSendeDaten.extend(BedienungnachZusiElement(0x15, 0x, 0x02, 0x00, 0.0))
# Stromabnehmer
    if Sendebediendaten["TSAH"] != Sendebediendatenalt["TSAH"]:
        if Sendebediendaten["TSAH"]:
            TCPSendeDaten.extend(BedienungnachZusiElement(0x2B, 0x53, 0x01, 0x00, 0.0))
        else:
            TCPSendeDaten.extend(BedienungnachZusiElement(0x2B, 0x54, 0x02, 0x00, 0.0))
    if Sendebediendaten["TSAN"] != Sendebediendatenalt["TSAN"]:
        if Sendebediendaten["TSAN"]:
            TCPSendeDaten.extend(BedienungnachZusiElement(0x2B, 0x55, 0x01, 0x00, 0.0))
        else:
            TCPSendeDaten.extend(BedienungnachZusiElement(0x2B, 0x56, 0x02, 0x00, 0.0))
# Luftpresser (noch nicht richtig implementiert)
    # if Sendebediendaten["TLP"] != Sendebediendatenalt["TLP"]:
    #     if Sendebediendaten["TLP"]:
    #         TCPSendeDaten.extend(BedienungnachZusiElement(0x2D, 0x, 0x01, 0x00, 0.0))
    #     else:
    #         TCPSendeDaten.extend(BedienungnachZusiElement(0x2D, 0x, 0x02, 0x00, 0.0))
#
# Sendevorlage
    # if Sendebediendaten[""] != Sendebediendatenalt[""]:
    #     if Sendebediendaten[""]:
    #         TCPSendeDaten.extend(BedienungnachZusiElement(0x3, 0x, 0x01, 0x00, 0.0))
    #     else:
    #         TCPSendeDaten.extend(BedienungnachZusiElement(0x3, 0x, 0x02, 0x00, 0.0))
#
    TCPSendeDaten.extend((0xFF, 0xFF, 0xFF, 0xFF,
                    0xFF, 0xFF, 0xFF, 0xFF))
    # print("".join("\\x%02x" % i for i in TCPSendeDaten))
    ZusiSocket.send(TCPSendeDaten)
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
        while True:
            Bediendaten1alt = Bediendaten.copy()
            daten, addr = Ft1SSocket.recvfrom(1024)
            # msg = "Message from Loksim {}".format(daten)
            # msg_2 = "Adress from Loksim {}".format(addr[0])
            # print(str(msg),"  ", str(msg_2))
            # print("Anzahl der Zeichen des UDP-Pakets:\t",len(daten))
            SchnittstelleFT.UDPBedienDatenAuswertenFT1(daten,Bediendaten)
            Textausgabe.Textbedienanzeige(Bediendaten,Bediendaten1alt)
            BedienungnachZusi(Bediendaten,Bediendaten1alt)
            if stop_threads:
                break

class Bedienung2Thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        global Bediendaten
        while True:
            Bediendaten2alt = Bediendaten.copy()
            daten, addr = Ft2SSocket.recvfrom(1024)
            # msg = "Message from Loksim {}".format(daten)
            # msg_2 = "Adress from Loksim {}".format(addr[0])
            # print(str(msg),"  ", str(msg_2))
            # print("Anzahl der Zeichen des UDP-Pakets:\t",len(daten))
            SchnittstelleFT.UDPBedienDatenAuswertenFT2(daten,Bediendaten)
            Textausgabe.Textbedienanzeige(Bediendaten,Bediendaten2alt)
            BedienungnachZusi(Bediendaten,Bediendaten2alt)
            if stop_threads:
                break


# Beginn des Hauptprogrammes

ZusiSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Erstellen des TCP Socket für Zusi
Ft1ESocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Erstellen des UDP Empfangs-Socket für den Führertischrechner 1
Ft1SSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Erstellen des UDP Sende-Socket für den Führertischrechner 1
Ft2ESocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Erstellen des UDP Empfangs-Socket für den Führertischrechner 2
Ft2SSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Erstellen des UDP Sende-Socket für den Führertischrechner 2

try:
    ZusiSocket.connect((Zusi_IP, Zusi_Port))  # Binde Socket an die Netzwerkadresse
    Ft1SSocket.bind(("", Ft1S_Port))
    Ft2SSocket.bind(("", Ft2S_Port))
    ZusiSocket.send(HELLO)
    SchnittstelleLZB.updateData(Anzeigedaten,LZBDaten)
    LZBSendenThread()
    Bedienung1Thread()
    Bedienung2Thread()
    while True:
# Empfang der Daten
        if Ebene == 0:
            nodeId = [0,0,0,0,0,0]
        # Lese 6 Bytes für die Paketlänge und die ID aus dem Buffer
        for i in range(0,4):
            data = ZusiSocket.recv(1)
            PaketLaengeBytearray[i] = data[0]
        PacketLaenge = struct.unpack("I", PaketLaengeBytearray)  # Prüfen wie viele Bytes nun folgen
        PacketLaenge = PacketLaenge[0]
        if PacketLaenge == 0x00000000: # Länge = 0 kennzeichnet den Knoten im Unterschied zum Attribut
            for i in range(0,2):
                data = ZusiSocket.recv(1)
                NodeIDBytearray[i] = data[0]
            nodeIDtmp = struct.unpack("H", NodeIDBytearray)  # NodeID der aktuellen Ebene ermitteln
            nodeId[Ebene] = nodeIDtmp[0]
            Ebene += 1
            LetzterKnotenNeu = True
        elif PacketLaenge == 0xFFFFFFFF: # Kennzeichnung des Knoten-Endes
            if LetzterKnotenNeu & (nodeId[0] == 0x0002) & (nodeId[1] == 0x000A): # Schreiben der Daten
                Ft1ESocket.sendto(SchnittstelleFT.UDPAnzeigeDatenErzeugenFT1(Anzeigedaten),(Ft1_IP, Ft1E_Port))
                Ft2ESocket.sendto(SchnittstelleFT.UDPAnzeigeDatenErzeugenFT2(Anzeigedaten),(Ft2_IP, Ft2E_Port))
                SchnittstelleLZB.updateData(Anzeigedaten,LZBDaten)
                # Textausgabe.Textanzeige(Anzeigedaten,Anzeigedatenalt)
                Anzeigedatenalt = Anzeigedaten.copy()
            elif Ebene == 1:
               if not Verbindungsergebnis:
                   ZusiSocket.send(HELLO)
                   print("HELLO gesendet")
               elif not Datenanforderungsergebnis:
                   ZusiSocket.send(NEEDED_DATA)
                   print("NEEDED_DATA gesendet")
            Ebene -= 1
            LetzterKnotenNeu = False
        else:
            for i in range(0,2):
                data = ZusiSocket.recv(1)
                NodeIDBytearray[i] = data[0]
            nodeIDtmp = struct.unpack("H", NodeIDBytearray)  # NodeID der aktuellen Ebene ermitteln
            nodeId[Ebene] = nodeIDtmp[0]
            # print("---------------------------")
            # print("Der empfangene Befehl von Zusi3 auf Ebene ", Ebene, " hat ", hex(PacketLaenge)," Bytes und die ID", hex(nodeId[Ebene]))
            # print("Nodes: ", hex(nodeId[0]), hex(nodeId[1]), hex(nodeId[2]), hex(nodeId[3]), hex(nodeId[4]), hex(nodeId[5]))
            for i in range(0,PacketLaenge-2):
                data = ZusiSocket.recv(1)
                Speicher[i] = data[0]
                # print("Daten: " + str(i) + "  " + hex(Speicher[i]) )
            if (nodeId[0] == 0x0001) & (nodeId[1] == 0x0002): # ACK_HELLO
                if nodeId[2] == 0x0001:
                    print("ZusiVersion: ", ZusiStringtoString(Speicher,PacketLaenge-2))
                elif nodeId[2] == 0x0002:
                    print("Verbindungsinfo: ", ZusiStringtoString(Speicher,PacketLaenge-2))
                elif nodeId[2] == 0x0003:
                    Verbindungsergebnis = not bool(Speicher[0])
                    print("Verbindungsergebnis: ", Verbindungsergebnis)
                elif nodeId[2] == 0x0005:
                    print("Version des TCP-Protokolls: ", ZusiStringtoString(Speicher,PacketLaenge-2))
            elif (nodeId[0] == 0x0002) & (nodeId[1] == 0x0004): # ACK_NEEDED_DATA
                if nodeId[2] == 0x0001:
                    Datenanforderungsergebnis = not bool(Speicher[0])
                    print("Ergebnis Datenanforderung: ", Datenanforderungsergebnis)
            elif (nodeId[0] == 0x0002) & (nodeId[1] == 0x000A): # DATA_FTD
                if nodeId[2] == 0x0001:   # Geschwindigkeit
                    Anzeigedaten["Vist"] = abs(ZusiSinglezuFloat(Speicher) * 3.6)
                elif nodeId[2] == 0x0002: # Druck Hauptluftleitung
                    Anzeigedaten["DruckHL"] = ZusiSinglezuFloat(Speicher)
                elif nodeId[2] == 0x0003: # Druck Bremszylinder
                    Anzeigedaten["DruckC"] = ZusiSinglezuFloat(Speicher)
                elif nodeId[2] == 0x0004: # Druck Hauptluftbehälter
                    Anzeigedaten["DruckHB"] = ZusiSinglezuFloat(Speicher)
                elif nodeId[2] == 0x0009: # Zugkraft gesamt
                    Anzeigedaten["Fzb"] = ZusiSinglezuFloat(Speicher) * 0.001
                elif nodeId[2] == 0x000A: # Zugkraft pro Achse
                    Anzeigedaten["Fzba"] = ZusiSinglezuFloat(Speicher) * 0.001
                elif nodeId[2] == 0x000D: # Oberstrom
                    Anzeigedaten["Iol"] = ZusiSinglezuFloat(Speicher)
                elif nodeId[2] == 0x000E: # Fahrleitungsspannung
                    Anzeigedaten["Uol"] = ZusiSinglezuFloat(Speicher)
                elif nodeId[2] == 0x000F: # Motordrehzahl
                    Anzeigedaten["Nmot"] = ZusiSinglezuFloat(Speicher)
                elif nodeId[2] == 0x0013: # Hauptschalter
                    Anzeigedaten["LMHS"] = ZusiSinglezuBool(Speicher)
                elif nodeId[2] == 0x0015: # Fahrstufe
                    Anzeigedaten["FSt"] = ZusiSinglezuInt(Speicher)
                elif nodeId[2] == 0x0017: # AFB-Sollgeschwindigkeit
                    Anzeigedaten["AFBVsoll"] = ZusiSinglezuFloat(Speicher) * 3.6
                elif nodeId[2] == 0x0019: # Zurückgelegter Gesamtweg
                    Anzeigedaten["Simkm"] = ZusiSinglezuInt(Speicher)
                elif nodeId[2] == 0x001A: # LM Getriebe
                    Anzeigedaten["LMGetriebe"] = ZusiSinglezuBool(Speicher)
                elif nodeId[2] == 0x001B: # LM Schleudern
                    Anzeigedaten["LMSchleudern"] = ZusiSinglezuBool(Speicher)
                elif nodeId[2] == 0x001C: # LM Gleiten
                    Anzeigedaten["LMGleiten"] = ZusiSinglezuBool(Speicher)
                elif nodeId[2] == 0x0020: # LM Hochabbremsung
                    Anzeigedaten["LMHAB"] = ZusiSinglezuBool(Speicher)
                elif nodeId[2] == 0x0021: # LM Schnellbremsung
                    Anzeigedaten["LMS"] = ZusiSinglezuBool(Speicher)
                elif nodeId[2] == 0x0022: # Status Notbremsung
                    if nodeId[3] == 0x0001: # Bauart Notbremssystem
                        print(ZusiStringtoString(Speicher,PacketLaenge-2))
                    if nodeId[3] == 0x0007: # Status Melder Notbremsung
                        Anzeigedaten["LMNBrems"] = ZusiBytezuLM(Speicher)
                elif nodeId[2] == 0x0023: # LM Uhrzeit (digital)
                    Anzeigedaten["SimZeit"] = round(ZusiSinglezuFloat(Speicher) * 86400)
                elif nodeId[2] == 0x0036: # AFB an
                    Anzeigedaten["AFBaktiv"] = ZusiSinglezuBool(Speicher)
                elif nodeId[2] == 0x0055: # Stromabnehmer
                    # print("Stromabnehmerstellung: ", ZusiSinglezuInt(Speicher))
                    Anzeigedaten["LMSA"] = ZusiSinglezuInt(Speicher)
                elif nodeId[2] == 0x005E: # Druck Zeitbehälter
                    Anzeigedaten["DruckZ"] = ZusiSinglezuFloat(Speicher)
                elif nodeId[2] == 0x0061: # Kilometrierung (Zugspitze)
                    Anzeigedaten["Streckenkm"] = ZusiSinglezuInt1000(Speicher)
                elif nodeId[2] == 0x0063: # Motorspannung
                    Anzeigedaten["Umot"] = ZusiSinglezuInt(Speicher)
                elif nodeId[2] == 0x0064: # Status Sifa
                    # if nodeId[3] == 0x0001: # Bauart Sifasystem
                        # print(ZusiStringtoString(Speicher,PacketLaenge-2))
                    if nodeId[3] == 0x0002: # Status Sifa-Leuchtmelder
                        Anzeigedaten["LMSifa"] = int(Speicher[0])
                    if nodeId[3] == 0x0003: # Status Sifa-Hupe
                        if int(Speicher[0]) == 0:
                            Anzeigedaten["HupeSifa"] = False
                        else:
                            Anzeigedaten["HupeSifa"] = True
                elif nodeId[2] == 0x0065: # Status Zugbeeinﬂussung
                    if nodeId[3] == 0x0001: # Bauart Zugbeeinflussungssystem
                        BauartZugbeeinflussung = ZusiStringtoString(Speicher,PacketLaenge-2)
                        if ("Indusi" in BauartZugbeeinflussung):
                            Anzeigedaten["LZBSystem"] = 1
                        # elif ("PZB90/I60" in BauartZugbeeinflussung):
                        # elif ("LZB80 CIR-ELKE PZB90 V2.0" in BauartZugbeeinflussung):
                        # elif ("EBICAB 500" in BauartZugbeeinflussung):
                        # elif ("PZB90/I60R - V2.0" in BauartZugbeeinflussung):
                        # elif ("" in BauartZugbeeinflussung):
                        # elif ("" in BauartZugbeeinflussung):
                        # elif ("" in BauartZugbeeinflussung):
                        # elif ("" in BauartZugbeeinflussung):
                        # elif ("" in BauartZugbeeinflussung):
                        # elif ("" in BauartZugbeeinflussung):
                        # elif ("" in BauartZugbeeinflussung):
                        # elif ("" in BauartZugbeeinflussung):
                        else:
                            Anzeigedaten["LZBSystem"] = 7
                        # print("Bauart der Zugbeeinflussung: ", BauartZugbeeinflussung)
                    elif nodeId[3] == 0x0002: # System aus der Indusi-Familie - Einstellungen
                        if nodeId[4] == 0x0001: # Zugart
                            Anzeigedaten["PZBZa"] = max(0,min(3,int(Speicher[0]) - 1))
                        elif nodeId[4] == 0x0006: # Aktive Zugdaten
                            if nodeId[5] == 0x0001: # BRH-Wert (Bremshundertstel)
                                Anzeigedaten["BRH"] = ZusiWordzuInt(Speicher)
                            elif nodeId[5] == 0x0002: # BRA-Wert (Bremsart)
                                Anzeigedaten["BRA"] = ZusiWordzuInt(Speicher)
                            elif nodeId[5] == 0x0003: # ZL-Wert (Zuglänge) in m
                                Anzeigedaten["ZL"] = ZusiWordzuInt(Speicher)
                            elif nodeId[5] == 0x0004: # VMZ-Wert (Höchstgeschwindigkeit) in km/h
                                Anzeigedaten["VMZ"] = ZusiWordzuInt(Speicher)
                    elif nodeId[3] == 0x0003: # System aus der Indusi-Familie - Betriebsdaten
                        # if nodeId[4] == 0x0002: # Zustand Zugbeeinflussung
                            # print("Zustand Zugbeeinflussung ",ZusiSinglezuInt(Speicher))
                        if nodeId[4] == 0x0006: # Status Melder Zugart U
                            if Anzeigedaten["LZBSystem"] == 1:
                                Anzeigedaten["LM55"] = ZusiBytezuLM(Speicher)
                        elif nodeId[4] == 0x0007: # Status Melder Zugart M
                            if Anzeigedaten["LZBSystem"] == 1:
                                Anzeigedaten["LM70"] = ZusiBytezuLM(Speicher)
                        elif nodeId[4] == 0x0008: # Status Melder Zugart O
                            if Anzeigedaten["LZBSystem"] == 1:
                                Anzeigedaten["LM85"] = ZusiBytezuLM(Speicher)
                        elif nodeId[4] == 0x0009: # Status Indusi-Hupe
# Da die Indusi-Hipe von Zusi nicht richtig angesteuert wird,
# geht das Signal versuchsweise auf den LM Zugsammelschiene
                        #     if int(Speicher[0]) == 0:
                                # Anzeigedaten["HupePZB"] = 0
                            # else:
                                # Anzeigedaten["HupePZB"] = 3
                            if int(Speicher[0]) == 0:
                                Anzeigedaten["LMZS"] = False
                            else:
                                Anzeigedaten["LMZS"] = True
                        elif nodeId[4] == 0x0021: # Sollgeschwindigkeit in m/s
                            Anzeigedaten["LZBVsoll"] = ZusiSinglezuFloat(Speicher) * 3.6
                            if (Anzeigedaten["LZBVsoll"] >= 0.0):
	                            Anzeigedaten["MFADVS"] = False
                            else:
	                            Anzeigedaten["MFADVS"] = True
                        elif nodeId[4] == 0x0022: # Zielgeschwindigkeit in m/s (Wert<0 → dunkel)
                            Anzeigedaten["LZBVziel"] = int(round(ZusiSinglezuFloat(Speicher) * 3.6,0))
                            if (Anzeigedaten["LZBVziel"] >= 0.0):
	                            Anzeigedaten["MFADVZ"] = False
                            else:
                                Anzeigedaten["MFADVZ"] = True
                        elif nodeId[4] == 0x0023: # Zielweg in m (Wert<0 → dunkel)
                            Anzeigedaten["LZBSziel"] = ZusiSinglezuFloat(Speicher)
                            if (Anzeigedaten["LZBSziel"] >= 0.0):
	                            Anzeigedaten["MFADaZ"] = False
	                            Anzeigedaten["MFADdZ"] = False
                            else:
	                            Anzeigedaten["MFADaZ"] = True
	                            Anzeigedaten["MFADdZ"] = True
                        elif nodeId[4] == 0x0024: # Status Melder G
                            Anzeigedaten["LMG"] = ZusiBytezuLM(Speicher)
                        elif nodeId[4] == 0x0027: # Zugdatenanzeige im MFA aktiv
                            Anzeigedaten["ZDK"] = int(Speicher[0])
                        elif nodeId[4] == 0x002F: # Status Melder 1000 Hz
                            Anzeigedaten["LM1000Hz"] = ZusiBytezuLM(Speicher)
                        elif nodeId[4] == 0x0030: # Status Melder Zugart O
                            if Anzeigedaten["LZBSystem"] == 7:
                                Anzeigedaten["LM85"] = ZusiBytezuLM(Speicher)
                        elif nodeId[4] == 0x0031: # Status Melder Zugart M
                            if Anzeigedaten["LZBSystem"] == 7:
                                Anzeigedaten["LM70"] = ZusiBytezuLM(Speicher)
                        elif nodeId[4] == 0x0032: # Status Melder Zugart U
                            if Anzeigedaten["LZBSystem"] == 7:
                                Anzeigedaten["LM55"] = ZusiBytezuLM(Speicher)
                        elif nodeId[4] == 0x0033: # Status Melder 500 Hz
                            Anzeigedaten["LM500Hz"] = ZusiBytezuLM(Speicher)
                        elif nodeId[4] == 0x0034: # Status Melder Befehl 40
                            Anzeigedaten["LMB40"] = ZusiBytezuLM(Speicher)
                        elif nodeId[4] == 0x0038: # Status Melder H
                            Anzeigedaten["LMH"] = ZusiBytezuLM(Speicher)
                        elif nodeId[4] == 0x0039: # Status Melder E40
                            Anzeigedaten["LME40"] = ZusiBytezuLM(Speicher)
                        elif nodeId[4] == 0x003A: # Status Melder Ende
                            Anzeigedaten["LMEnde"] = ZusiBytezuLM(Speicher)
                        elif nodeId[4] == 0x003B: # Status Melder B
                            Anzeigedaten["LMB"] = ZusiBytezuLM(Speicher)
                        elif nodeId[4] == 0x003C: # Status Melder Ü
                            Anzeigedaten["LMUe"] = ZusiBytezuLM(Speicher)
                        elif nodeId[4] == 0x003D: # Status Melder EL
                            Anzeigedaten["LMEL"] = ZusiBytezuLM(Speicher)
                        elif nodeId[4] == 0x003E: # Status Melder V40
                            Anzeigedaten["LMV40"] = ZusiBytezuLM(Speicher)
                        elif nodeId[4] == 0x003F: # Status Melder S
                            Anzeigedaten["LMS"] = ZusiBytezuLM(Speicher)
                    elif nodeId[3] == 0x0007: # System aus der ZUB-Familie - Betriebsdaten
                        if nodeId[4] == 0x0001: # Status Melder GNT
                            Anzeigedaten["LMGNT"] = ZusiBytezuLM(Speicher)
                        elif nodeId[4] == 0x0002: # Status Melder GNT Ü
                            Anzeigedaten["LMGNTUe"] = ZusiBytezuLM(Speicher)
                        elif nodeId[4] == 0x0003: # Status Melder GNT G
                            Anzeigedaten["LMGNTG"] = ZusiBytezuLM(Speicher)
                        elif nodeId[4] == 0x0004: # Status Melder GNT S
                            Anzeigedaten["LMGNTS"] = ZusiBytezuLM(Speicher)
                elif nodeId[2] == 0x0066: # Status Türsystem
                    # if nodeId[3] == 0x0001: # Bezeichnung des Systems
                        # print(ZusiStringtoString(Speicher,PacketLaenge-2))
                    if nodeId[3] == 0x000D: # Status Türmelder links+rechts
                        Anzeigedaten["LMTuer"] = ZusiBytezuLM(Speicher)
                elif nodeId[2] == 0x008E:   # Status Zug
                    if nodeId[3] == 0x0001: # Fahrzeug
                        if nodeId[4] == 0x0001: # Fahrzeugdateiname
                            print("Fahrzeugdateiname: ", ZusiStringtoString(Speicher,PacketLaenge-2))
                        # elif nodeId[4] == 0x0002: # Beschreibung
                            # print("Beschreibung: ", ZusiStringtoString(Speicher,PacketLaenge-2))
                        # elif nodeId[4] == 0x0004: # Vorhandenes Zugbeeinflussungssystem
                        #     print("Vorhandenes Zugbeeinflussungssystem: ", ZusiStringtoString(Speicher,PacketLaenge-2))
                        # elif nodeId[4] == 0x0005: # Fahrzeughöchstgeschwindigkeit
                            # print("Fahrzeughöchstgeschwindigkeit: ", round(ZusiSinglezuFloat(Speicher) * 3.6), " km/h")
                        elif nodeId[4] == 0x0006: # Baureihenangabe
                            print("Baureihe: ", ZusiStringtoString(Speicher,PacketLaenge-2))
                        elif nodeId[4] == 0x000B: # NVR-Nummer
                            print("NVR-Nummer: ", ZusiStringtoString(Speicher,PacketLaenge-2))
                        # elif nodeId[4] == 0x001C: # Bezeichnung der Bremsbauart
                        #     print("Bezeichnung der Bremsbauart: ", ZusiStringtoString(Speicher,PacketLaenge-2))
                        elif nodeId[4] == 0x0021: # Interne Fahrzeugnummer
                            print("Interne Fahrzeugnummer: ", ZusiStringtoString(Speicher,PacketLaenge-2))
            elif (nodeId[0] == 0x0002) & (nodeId[1] == 0x000B): # DATA_OPERATION
                # if nodeId[2] == 0x0001:   # Betätigungsvorgang
                #     if nodeId[3] == 0x0001: # Tastaturzuordnung
                #         print("Betätigungsvorgang Tastaturzuordnung: ", hex(ZusiWordzuInt(Speicher)))
                #     elif nodeId[3] == 0x0002: # Tastaturkommando
                #         print("Betätigungsvorgang Tastaturkommando: ", hex(ZusiWordzuInt(Speicher)))
                #     elif nodeId[3] == 0x0003: # Tastaturaktion
                #         print("Betätigungsvorgang Tastaturaktion: ", hex(ZusiWordzuInt(Speicher)))
                #     elif nodeId[3] == 0x0004: # Schalterposition
                #         print("Betätigungsvorgang Schalterposition: ", hex(ZusiWordzuInt(Speicher)))
                #     elif nodeId[3] == 0x0005: # Spezialparameter
                #         print("Betätigungsvorgang Spezialparameter: ", ZusiSinglezuFloat(Speicher))
                if nodeId[2] == 0x0002:   # Kombischalter Hebelpositionen
                    if nodeId[3] == 0x0001: # Name des Kombischalters
                        print("Name des Kombischalters: ", ZusiStringtoString(Speicher,PacketLaenge-2))
                    elif nodeId[3] == 0x0002: # 
                        if nodeId[4] == 0x0001: # Kombischalterfunktion
                            print("Kombischalterfunktion: ", hex(ZusiWordzuInt(Speicher)))
                        elif nodeId[4] == 0x0002: # Beschreibung
                            print("Kombischalter Parameter: ", ZusiSinglezuFloat(Speicher))
                    elif nodeId[3] == 0x0003: # 
                        print("Kombischalter Aktuelle Raste : ", ZusiSmallIntzuInt(Speicher))
                    elif nodeId[3] == 0x0004: # 
                        print("Kombischalter Mittelstellung : ", ZusiSmallIntzuInt(Speicher))
                    elif nodeId[3] == 0x0005: # 
                        print("Kombischalter Maximale Rastennummer : ", ZusiSinglezuFloat(Speicher))
            elif (nodeId[0] == 0x0002) & (nodeId[1] == 0x000C): # DATA_FTD
                if nodeId[2] == 0x0001:   # Aktuelle Zugdatei, Dateiname relativ zum Zusi-Verzeichnis
                    print("Aktuelle Zugdatei: ", ZusiStringtoString(Speicher,PacketLaenge-2))
                elif nodeId[2] == 0x0002:   # Aktuelle Zugnummer
                    print("Aktuelle Zugnummer: ", ZusiStringtoString(Speicher,PacketLaenge-2))
                elif nodeId[2] == 0x0004:   # Buchfahrplanrohdatei
                    EBuLaString = ZusiStringtoString(Speicher,PacketLaenge-2)
                    print("Fahrplan:", EBuLaString)

finally:
    ZusiSocket.close()
    Ft1ESocket.close()
    Ft1SSocket.close()
    Ft2ESocket.close()
    Ft2SSocket.close()
    stop_threads = True 
