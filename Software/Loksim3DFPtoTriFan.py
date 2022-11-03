#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Dieser Quellcode ist in Python 3 geschrieben und empfängt die Fahrplandaten von LokSim3D
und sendet sie an TriFan.

This source code is written in Python 3 and receives the timetable data from LokSim3D
and forwards them to TriFan.

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
from datetime import datetime
import socket
import threading
import struct

Zusi_IP = ""            # Höre Zusi auf allen Adressen
Zusi_Port = 1436        # Beachte Port 1436 von Zusi 3
Loksim_IP = ""          # Höre Loksim vom localhost
QEBuLa_IP = ""          # Adresse des QEBuLa-Rechners
QEBuLa_Port1 = 10005    # Port 10005 für QEBuLa-Fahrplandaten
QEBuLa_Port2 = 10006    # Port 10006 für QEBuLa-Zugdaten

Zugdaten = {"Vist": 0.0,           # Geschwindigkeit in km/h
            "TuerL": 0,            # Status Türen links
            "TuerR": 0,            # Status Türen rechts
            "Simkm": 0,            # Relative Position in m
            "SimZeit": 0,          # Simulationszeit im UNIX-Format
            "Zugnr": 0,            # Zugnummer
            "VmaxTfz": 200,        # Höchstgeschwindigkeit des Tfz in km/h
            "NVR": ""}             # Eindeutige Fahrzeugnummer des Tfz

Zugdatenalt = Zugdaten.copy()

SendeLock = threading.Lock()

FplLS3D = ""
FplZusi3 = ""
icon = 0
vmax = 0.0

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

ACK_HELLO = bytes([0x00, 0x00, 0x00, 0x00, # Knoten
                    0x01, 0x00,             # Verbindungsaufbau
                    0x00, 0x00, 0x00, 0x00, # Knoten
                    0x02, 0x00,             # ACK_HELLO-Befehl
                    0x09, 0x00, 0x00, 0x00, # Länge 9 Bytes -> es folgt ein Attribut
                    0x01, 0x00,
                    0x33, 0x2E, 0x30, 0x2E, # String "3.0.1.0"
                    0x31, 0x2E, 0x30,
                    0x03, 0x00, 0x00, 0x00, # Länge 3 Bytes -> es folgt ein Attribut
                    0x03, 0x00,
                    0x00,                   # Verbindung akzeptiert
                    0x0A, 0x00, 0x00, 0x00, # Länge 10 Bytes -> es folgt ein Attribut
                    0x04, 0x00,
                    0x00, 0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00, 0x00, # Fahrplananfangszeit
                    0xFF, 0xFF, 0xFF, 0xFF, # Ende Knoten
                    0xFF, 0xFF, 0xFF, 0xFF])

ACK_NEEDED_DATA = bytes([0x00, 0x00, 0x00, 0x00, # Knoten
                         0x02, 0x00,             # Client-Anwendung Typ 2 (Fahrpult)
                         0x00, 0x00, 0x00, 0x00, # Knoten
                         0x04, 0x00,             # ACK_NEEDED_DATA-Befehl
                         0x03, 0x00, 0x00, 0x00, # Länge 3 Bytes -> es folgt ein Attribut
                         0x01, 0x00,
                         0x00,                   # Befehl akzeptiert
                         0xFF, 0xFF, 0xff, 0xFF, # Ende Knoten
                         0xFF, 0xFF, 0xff, 0xFF])

i = 0
j = 0
z = 0

stop_threads = False

def ZusiWordzuInt(Speicher):
    AnzeigeWordWert = struct.unpack("H", Speicher[:2])  # Umwandlung von Binärdaten in word
    AnzeigeWordWert = AnzeigeWordWert[0]
    return AnzeigeWordWert

def ZusiStringtoString(Speicher,Laenge):
    AnzeigeString = Speicher[:Laenge].decode('iso-8859-1')
    return AnzeigeString

def FplLS3D2Zusi3(FplLS3DString):
    FplLS3DZeile = ""
    FplLS3DDic = ""
    FplZusi3Zeile = ""
    FplZusi3String = ""
    Startbahnhof = ""
    Endbahnhof = ""
    
    FplLS3DZeile = FplLS3DString.split('\n')
    # print ("Fahrplanzeilen: ",len(FplLS3DZeile)-1)
    for i in range(0,len(FplLS3DZeile)-1):
        FplLS3DDic = FplLS3DZeile[i].split(';')
        print ("Datenzeile",i,":", FplLS3DDic)
        try:
            FplZusi3Zeile = '<FplZeile FplLaufweg="' + str(float(FplLS3DDic[0])) + '">\n\n'
# Tunnelfunktion auskommentiert, da Loksim3D leider auch jede Überführung für einen Tunnel hält.
            # if len(FplLS3DDic[7]) > 0:
            #     if FplLS3DDic[7] == '1':
            #         FplZusi3Zeile += '<FplTunnel FplNameText=" " FplTunnelAnfang="1"/>\n\n'
            #     elif FplLS3DDic[7] == '3':
            #         FplZusi3Zeile += '<FplTunnel/>\n\n'
            if len(FplLS3DDic[8]) > 0:
                if FplLS3DDic[8] == 'e1': # Zugfunk Beginn oder Bereichswechsel 
                    FplZusi3Zeile += '<FplIcon FplIconNr="1"/>\n\n'
                elif FplLS3DDic[8] == 'e2': # Ende Zugfunk
                    FplZusi3Zeile += '<FplIcon FplIconNr="2"/>\n\n'
                elif FplLS3DDic[8] == 'd1': # GNT
                    FplZusi3Zeile += '<FplIcon FplIconNr="3"/>\n\n'
                elif FplLS3DDic[8] == 'd2': # GNT ENde
                    FplZusi3Zeile += '<FplIcon FplIconNr="4"/>\n\n'
                elif FplLS3DDic[8] == 'c1': # LZB
                    FplZusi3Zeile += '<FplIcon FplIconNr="5"/>\n\n'
                elif FplLS3DDic[8] == 'c2': # LZB Ende
                    FplZusi3Zeile += '<FplIcon FplIconNr="6"/>\n\n'
                elif FplLS3DDic[8] == 'a1': # verkürzter Vorsignalabstand
                    FplZusi3Zeile += '<FplIcon FplIconNr="7"/>\n\n'
                elif FplLS3DDic[8] == 'b1': # Durchrutschweg nicht ausreichend
                    FplZusi3Zeile += '<FplIcon FplIconNr="8"/>\n\n'
                elif FplLS3DDic[8] == 'f1': # Fahrleitungs-Schutzstrecke
                    FplZusi3Zeile += '<FplIcon FplIconNr="12"/>\n\n'
                elif FplLS3DDic[8] == 'f2':
                    FplZusi3Zeile += '<FplIcon FplIconNr="14"/>\n\n'
                elif FplLS3DDic[8] == 'f3': # Stromabnehmer senken
                    FplZusi3Zeile += '<FplIcon FplIconNr="15"/>\n\n'
                elif FplLS3DDic[8] == 'f4':
                    FplZusi3Zeile += '<FplIcon FplIconNr="16"/>\n\n'
                elif FplLS3DDic[8] == 'y1': # Ende des anschließenden Weichenbereichs
                    FplZusi3Zeile += '<FplIcon FplIconNr="17"/>\n\n'
                elif FplLS3DDic[8] == 'f5': # Oberstrombegrenzung
                    FplZusi3Zeile += '<FplIcon FplIconNr="18"/>\n\n'
                elif FplLS3DDic[8] == 'f6': # Elektrifizierungsende
                    FplZusi3Zeile += '<FplIcon FplIconNr="19"/>\n\n'
                elif FplLS3DDic[8] == 'g1': # Heizverbot
                    FplZusi3Zeile += '<FplIcon FplIconNr="20"/>\n\n'
                elif FplLS3DDic[8] == 'g2': # Heizverbot Ende
                    FplZusi3Zeile += '<FplIcon FplIconNr="21"/>\n\n'
            if (len(FplLS3DDic[9]) > 0
            and not (FplLS3DDic[8] == 'c1' and FplLS3DDic[9] == '[ LZB ]')
            and not (FplLS3DDic[8] == 'c2' and FplLS3DDic[9] == '[ LZB ] Ende')):
                FplZusi3Zeile += '<FplName FplNameText="' + FplLS3DDic[9] + '"/>\n\n'
            if len(FplLS3DDic[1]) > 0:
                try:
                    vmax = float(FplLS3DDic[1])/3.6
                    FplZusi3Zeile += '<FplvMax vMax="' + str(vmax) + '"/>\n\n'
                except:
                    print('Höchstgeschwindigkeit im Fahrplan kein Zahl!')
            if len(FplLS3DDic[4]) > 0:
                FplZusi3Zeile += '<Fplkm km="' + FplLS3DDic[4] + '"/>\n\n'
            if len(FplLS3DDic[11]) > 0:
                FplZusi3Zeile += '<FplAnk Ank="' + datetime.today().strftime('%Y-%m-%d') + ' ' + FplLS3DDic[11] + '"/>\n\n'
                if len(FplLS3DDic[9]) > 0:
                    Endbahnhof = FplLS3DDic[9]
            if len(FplLS3DDic[12]) > 0:
                FplZusi3Zeile += '<FplAbf Abf="' + datetime.today().strftime('%Y-%m-%d') + ' ' + FplLS3DDic[12] + '"/>\n\n'
                if len(Startbahnhof) == 0 and len(FplLS3DDic[9]) > 0:
                    Startbahnhof = FplLS3DDic[9]
            FplZusi3Zeile += "</FplZeile>\n\n"
            FplZusi3String += FplZusi3Zeile
            print ("FplZusi3Zeile: ", FplZusi3Zeile)
        except:
            print('Position im Fahrplan keine Zahl!')
    FplZusi3Head  = '<?xml version="1.0" encoding="UTF-8"?>\n\n<Zusi>\n\n'
    FplZusi3Head += '<Info DateiTyp="Buchfahrplan" Version="A.1" MinVersion="A.1">\n\n'
    FplZusi3Head += '<AutorEintrag/>\n\n</Info>\n\n'
    FplZusi3Head += '<Buchfahrplan Gattung="TH" Nummer="42" Zuglauf="' + Startbahnhof + ' - ' + Endbahnhof + '" BR="111" Masse="270000" spMax="44.44444444444444" '
    FplZusi3Head += 'Bremsh="1.42" Laenge="126.0" kmStart="0.0" BremsstellungZug="5">\n\n'
    FplZusiEnd = '</Buchfahrplan>\n\n</Zusi>\n\n'
    FplZusi3String = FplZusi3Head + FplZusi3String + FplZusiEnd
    return FplZusi3String


class FahrplanEinlesenThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        global Zugdaten
        FplDatenSocket.bind((Loksim_IP, QEBuLa_Port1))
        FplLS3DString = ""
        FplLS3DStringalt = ""
        while True:
            data, addr = FplDatenSocket.recvfrom(81920) # buffer size is 81920 bytes
            # print(str("Adress from Loksim {}".format(addr[0])))
            # print("Anzahl der Zeichen des UDP-Pakets:\t",len(data))
            FplLS3DString = data.decode()
            if FplLS3DStringalt != FplLS3DString:
                FplZusi3 = FplLS3D2Zusi3(FplLS3DString)
                # with open("EBuLa.xml", "r", encoding="utf-8-sig") as EBuLaDatei:
                #         FplZusi3 = EBuLaDatei.read()
                # EBuLaDatei.close()
                FplZusi3BA = FplZusi3.encode(encoding = 'utf-8-sig')
                print(FplZusi3BA)
                while (not Verbindungsergebnis) or (not Datenanforderungsergebnis):
                    time.sleep(1)
                TCPFplSendeDaten = bytearray()
                TCPFplSendeDaten.extend((0x00, 0x00, 0x00, 0x00,
                                         0x02, 0x00,
                                         0x00, 0x00, 0x00, 0x00,
                                         0x0C, 0x00))
                # TCPFplSendeDaten.extend((0x09, 0x00, 0x00, 0x00))
                TCPFplSendeDaten.extend(struct.pack("I", (len(FplZusi3BA) + 2)))
                TCPFplSendeDaten.extend((0x04, 0x00))              # Fahrplan.xml
                # TCPFplSendeDaten.extend((0xEF, 0xBB, 0xBF, 0x3C,
                #                          0x3F, 0x78, 0x6C))
                TCPFplSendeDaten.extend(FplZusi3BA)
                TCPFplSendeDaten.extend((0xFF, 0xFF, 0xFF, 0xFF,
                                         0xFF, 0xFF, 0xFF, 0xFF))
                SendeLock.acquire()
                ZusiConn.send(TCPFplSendeDaten)
                SendeLock.release()
                with open("EBuLa.xml", "w", encoding="utf-8-sig") as EBuLaDatei:
                    EBuLaDatei.write(FplZusi3)
                EBuLaDatei.close()
                # print (TCPFplSendeDaten)
                # print (FplZusi3)
                FplLS3DStringalt = FplLS3DString
            if stop_threads:
                FplDatenSocket.close()    
                break
    
class ZugdatenEinlesenThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        global Zugdaten
        ZugdatenSocket.bind((QEBuLa_IP, QEBuLa_Port2))
        while True:
            while (not Verbindungsergebnis) or (not Datenanforderungsergebnis):
                time.sleep(1)
            UDPDaten, addr = ZugdatenSocket.recvfrom(1024)
            # print(str("Adress from Loksim {}".format(addr[0])))
            # print("Anzahl der Zeichen des UDP-Pakets:\t",len(UDPDaten))
            hilf = struct.unpack("I",UDPDaten[ 0: 4])
            Zugdaten["SimZeit"] = hilf[0]
            # print("Simulationszeit: ", datetime.time(datetime.fromtimestamp(Zugdaten["SimZeit"] - 3600)))
            # print("Datum: ", date.today())
            # print("Datum: ", int(time.time() / 86400))
            hilf = struct.unpack("H",UDPDaten[ 4: 6])
            # print("Höchstgeschwindigkeit: ", hilf[0], " km/h")
            hilf = struct.unpack("I",UDPDaten[ 6:10])
            Zugdaten["Simkm"] = hilf[0]
            # print("Streckenposition: ", Zugdaten["Simkm"], "m")
            TCPSendeDaten = bytearray()
            TCPSendeDaten.extend((0x00, 0x00, 0x00, 0x00,
                                  0x02, 0x00,
                                  0x00, 0x00, 0x00, 0x00,
                                  0x0A, 0x00,
                                  0x06, 0x00, 0x00, 0x00,
                                  0x01, 0x00))              # Geschwindigkeit
            TCPSendeDaten.extend(struct.pack("f", 10.0))
            TCPSendeDaten.extend((0x06, 0x00, 0x00, 0x00,
                                  0x19, 0x00))              # Zurückgelegter Gesamtweg
            TCPSendeDaten.extend(struct.pack("f", Zugdaten["Simkm"]))
            TCPSendeDaten.extend((0x06, 0x00, 0x00, 0x00,
                                  0x23, 0x00))              # LM Uhrzeit (digital) 
            TCPSendeDaten.extend(struct.pack("f", Zugdaten["SimZeit"] / 86400.0))
            TCPSendeDaten.extend((0x06, 0x00, 0x00, 0x00,
                                  0x4B, 0x00))              # Datum
            TCPSendeDaten.extend(struct.pack("f", (int(time.time() / 86400)) + 25569))
            # TCPSendeDaten.extend((0x06, 0x00, 0x00, 0x00,
                                  # 0x66, 0x00,               # Status Türen 
                                  # 0x00, 0x00, 0x00, 0x00,
                                  # ))
            TCPSendeDaten.extend((0xFF, 0xFF, 0xFF, 0xFF,
                                  0xFF, 0xFF, 0xFF, 0xFF))
            # print("".join("\\x%02x" % i for i in TCPSendeDaten))
            SendeLock.acquire()
            ZusiConn.send(TCPSendeDaten)
            SendeLock.release()
            if stop_threads:
                ZugdatenSocket.close()    
                break
    
# Beginn des Hauptprogrammes

ZusiSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # Erstellen des TCP Socket für Zusi
FplDatenSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
ZugdatenSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP

try:
    FahrplanEinlesenThread()
    ZugdatenEinlesenThread()
    ZusiSocket.bind((Zusi_IP, Zusi_Port))  # Binde Socket an die Netzwerkadresse
    ZusiSocket.listen(1)  # lausche ob es eine TCP Verbindung gibt
    ZusiConn, ZusiAddress = ZusiSocket.accept()  # TCP Verbindung wurde hergestellt
    print('Connection address:', ZusiAddress[0])  # IP-Adresse des Partners
    while True:
# Empfang der Daten
        if Ebene == 0:
            nodeId = [0,0,0,0,0,0]
        # Lese 6 Bytes für die Paketlänge und die ID aus dem Buffer
        for i in range(0,4):
            data = ZusiConn.recv(1)
            PaketLaengeBytearray[i] = data[0]
        PacketLaenge = struct.unpack("I", PaketLaengeBytearray)  # Prüfen wie viele Bytes nun folgen
        PacketLaenge = PacketLaenge[0]
        if PacketLaenge == 0x00000000: # Länge = 0 kennzeichnet den Knoten im Unterschied zum Attribut
            for i in range(0,2):
                data = ZusiConn.recv(1)
                NodeIDBytearray[i] = data[0]
            nodeIDtmp = struct.unpack("H", NodeIDBytearray)  # NodeID der aktuellen Ebene ermitteln
            nodeId[Ebene] = nodeIDtmp[0]
            # print("Ebene: ", Ebene, "Paketlänge: ", PacketLaenge, "NodeID: ", nodeId)
            Ebene += 1
            LetzterKnotenNeu = True
        elif PacketLaenge == 0xFFFFFFFF: # Kennzeichnung des Knoten-Endes
            # print("Ebene: ", Ebene, "Knoten-ID: ", nodeId, "Ende")
            if Ebene == 1:
                if (nodeId[0] == 0x0001) & (nodeId[1] == 0x0001):
                    ZusiConn.send(ACK_HELLO)
                    Verbindungsergebnis = True
                    print("ACK_HELLO gesendet")
                elif (nodeId[0] == 0x0002) & (nodeId[1] == 0x0003):
                    ZusiConn.send(ACK_NEEDED_DATA)
                    Datenanforderungsergebnis = True
                    print("ACK_NEEDED_DATA gesendet")
            Ebene -= 1
            LetzterKnotenNeu = False
        else:
            for i in range(0,2):
                data = ZusiConn.recv(1)
                NodeIDBytearray[i] = data[0]
            nodeIDtmp = struct.unpack("H", NodeIDBytearray)  # NodeID der aktuellen Ebene ermitteln
            nodeId[Ebene] = nodeIDtmp[0]
            # print("---------------------------")
            # print("Der empfangene Befehl von Zusi3 auf Ebene ", Ebene, " hat ", hex(PacketLaenge)," Bytes und die ID", hex(nodeId[Ebene]))
            # print("Nodes: ", hex(nodeId[0]), hex(nodeId[1]), hex(nodeId[2]), hex(nodeId[3]), hex(nodeId[4]), hex(nodeId[5]))
            for i in range(0,PacketLaenge-2):
                data = ZusiConn.recv(1)
                Speicher[i] = data[0]
                # print("Daten: " + str(i) + "  " + hex(Speicher[i]) )
            if (nodeId[0] == 0x0001) & (nodeId[1] == 0x0001): # HELLO
                if nodeId[2] == 0x0001:
                    print("Protokollversion: ", ZusiWordzuInt(Speicher))
                elif nodeId[2] == 0x0002:
                    print("Client-Typ: ", ZusiWordzuInt(Speicher))
                elif nodeId[2] == 0x0003:
                    print("Client-Name: ", ZusiStringtoString(Speicher,PacketLaenge-2))
                elif nodeId[2] == 0x0004:
                    print("Versionsnummer des Clients: ", ZusiStringtoString(Speicher,PacketLaenge-2))
            elif (nodeId[0] == 0x0002) & (nodeId[1] == 0x0003): # NEEDED_DATA
                if nodeId[2] == 0x000A:
                    if nodeId[3] == 0x0001:
                        print("Anforderung Führerstandsanzeige-ID: ", ZusiWordzuInt(Speicher))
                if nodeId[2] == 0x000B:
                    if nodeId[3] == 0x0001:
                        print("Anforderung Führerstandsbedienungs-ID: ", ZusiWordzuInt(Speicher))
                if nodeId[2] == 0x000C:
                    if nodeId[3] == 0x0001:
                        print("Anforderung Programmdaten-ID: ", ZusiWordzuInt(Speicher))
            else:
                print("Ebene: ", Ebene, "Paketlänge: ", PacketLaenge, "NodeID: ", nodeId)
finally:
    ZusiSocket.close()
    stop_threads = True 
