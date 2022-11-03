"""
Dieser Quellcode ist in Python 3 geschrieben und realisiert eine Textausgabe
der Daten der Simulationen Loksim3D, Zusi 2 und Zusi 3.

This source code is written in Python 3 and implements a console output
of the data of the simulations Loksim3D, Zusi 2 and Zusi 3.

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

TH Köln, hereby disclaims all copyright interest in the software 'Textausgabe.py'
(a software for Tconsole output of the data of the simulations
Loksim3D, Zusi 2 and Zusi 3).

Wolfgang Evers
Versionsdatum 14.10.2022

"""

import datetime

AusgabeBool = ("AUS","EIN")
AusgabeLM = ("AUS","EIN","2","Blinken mit 0,5 Hz","4","Blinken mit 1 Hz","6","7","8","9","10","Blinken invertiert mit 0,5 Hz","12","Blinken invertiert mit 1 Hz","13","14","15")
AusgabeHupe = ("AUS","Intervall mit Frequenz 1","Intervall mit Frequenz 2","AN")
AusgabeSA = ("0","gehoben","wird gehoben","wird gesenkt","gesenkt")

def Textanzeige(Textanzeigedaten,Textanzeigedatenalt):
    if Textanzeigedaten["Vist"] != Textanzeigedatenalt["Vist"]:
        print("\tGeschwindigkeit " + str(round(Textanzeigedaten["Vist"],1)) + " km/h")

    if Textanzeigedaten["Fzb"] != Textanzeigedatenalt["Fzb"]:
        print("\tZug-/Bremskraft gesamt " + str(round(Textanzeigedaten["Fzb"],2)) + " kN")

    if Textanzeigedaten["Fzba"] != Textanzeigedatenalt["Fzba"]:
        print("\tZug-/Bremskraft pro Achse " + str(Textanzeigedaten["Fzba"]) + " kN")

    if Textanzeigedaten["Fzbrel"] != Textanzeigedatenalt["Fzbrel"]:
        print("\tZug-/Bremskraft relativ " + str(Textanzeigedaten["Fzba"]) + " %")

    if Textanzeigedaten["Fzbsoll"] != Textanzeigedatenalt["Fzbsoll"]:
        print("\tZug-/Bremskraft-Soll gesamt " + str(Textanzeigedaten["Fzbsoll"]) + " kN")

    if Textanzeigedaten["Fzbasoll"] != Textanzeigedatenalt["Fzbasoll"]:
        print("\tZug-/Bremskraft-Soll pro Achse " + str(Textanzeigedaten["Fzbasoll"]) + " kN")

    if Textanzeigedaten["Fzbrel"] != Textanzeigedatenalt["Fzbrel"]:
        print("\tZug-/Bremskraft-Soll relativ " + str(Textanzeigedaten["Fzba"]) + " %")

    if Textanzeigedaten["LMSchleudern"] != Textanzeigedatenalt["LMSchleudern"]:
        if Textanzeigedaten["LMSchleudern"] == True:
            ausgabe = "EIN"
        elif Textanzeigedaten["LMSchleudern"] == False:
            ausgabe = "AUS"
        print("\tLeuchtmelder Schleudern " + ausgabe)

    if Textanzeigedaten["LMGleiten"] != Textanzeigedatenalt["LMGleiten"]:
        if Textanzeigedaten["LMGleiten"] == True:
            ausgabe = "EIN"
        elif Textanzeigedaten["LMGleiten"] == False:
            ausgabe = "AUS"
        print("\tLeuchtmelder Gleiten " + ausgabe)

    if Textanzeigedaten["LMHS"] != Textanzeigedatenalt["LMHS"]:
        if Textanzeigedaten["LMHS"] == False:
            ausgabe = "EIN"
        elif Textanzeigedaten["LMHS"] == True:
            ausgabe = "AUS"
        print("\tHauptschalter " + ausgabe)

    if Textanzeigedaten["LMSA"] != Textanzeigedatenalt["LMSA"]:
        if (Textanzeigedaten["LMSA"] >= 1) & (Textanzeigedaten["LMSA"] <= 3):
            print("\tStromabnehmer " + str(AusgabeLM[Textanzeigedaten["LMSA"]]))
        else:
            print("\tStromabnehmer " + str(Textanzeigedaten["LMSA"]))

    if Textanzeigedaten["LMZS"] != Textanzeigedatenalt["LMZS"]:
        if Textanzeigedaten["LMZS"] == False:
            ausgabe = "EIN"
        elif Textanzeigedaten["LMZS"] == True:
            ausgabe = "AUS"
        print("\tZugsammelschiene " + ausgabe)

    if Textanzeigedaten["LMEB"] != Textanzeigedatenalt["LMEB"]:
        if Textanzeigedaten["LMEB"] == True:
            ausgabe = "EIN"
        elif Textanzeigedaten["LMEB"] == False:
            ausgabe = "AUS"
        print("\tLeuchtmelder Elektrische Bremse " + ausgabe)

    if Textanzeigedaten["LMHAB"] != Textanzeigedatenalt["LMHAB"]:
        if Textanzeigedaten["LMHAB"] == True:
            ausgabe = "EIN"
        elif Textanzeigedaten["LMHAB"] == False:
            ausgabe = "AUS"
        print("\tLeuchtmelder Hohe Abbremsung " + ausgabe)

    if Textanzeigedaten["LMNBrems"] != Textanzeigedatenalt["LMNBrems"]:
        if Textanzeigedaten["LMNBrems"] == True:
            ausgabe = "EIN"
        elif Textanzeigedaten["LMNBrems"] == False:
            ausgabe = "AUS"
        print("\tLeuchtmelder Notbremsung " + ausgabe)

    if Textanzeigedaten["LMSifa"] != Textanzeigedatenalt["LMSifa"]:
        if (Textanzeigedaten["LMSifa"] == True) or (Textanzeigedaten["LMSifa"] == False):
            print("\tLeuchtmelder Sifa " + str(AusgabeLM[Textanzeigedaten["LMSifa"]]))
        else:
            print("\tLeuchtmelder Sifa " + str(Textanzeigedaten["LMSifa"]))

    if Textanzeigedaten["LMTuer"] != Textanzeigedatenalt["LMTuer"]:
        if (Textanzeigedaten["LMTuer"] >= 0) & (Textanzeigedaten["LMTuer"] <= 15):
            print("\tLeuchtmelder Türen " + str(AusgabeLM[Textanzeigedaten["LMTuer"]]))
        else:
            print("\tLeuchtmelder Türen " + str(Textanzeigedaten["LMTuer"]))

    if Textanzeigedaten["FSt"] != Textanzeigedatenalt["FSt"]:
        print("\tFahrstufe " + str(Textanzeigedaten["FSt"]))

    if Textanzeigedaten["LM85"] != Textanzeigedatenalt["LM85"]:
        if (Textanzeigedaten["LM85"] >= 0) & (Textanzeigedaten["LM85"] <= 15):
            print("\tLeuchtmelder 85 " + str(AusgabeLM[Textanzeigedaten["LM85"]]))
        else:
            print("\tLeuchtmelder 85 " + str(Textanzeigedaten["LM85"]))

    if Textanzeigedaten["LM70"] != Textanzeigedatenalt["LM70"]:
        if (Textanzeigedaten["LM70"] >= 0) & (Textanzeigedaten["LM70"] <= 15):
            print("\tLeuchtmelder 70 " + str(AusgabeLM[Textanzeigedaten["LM70"]]))
        else:
            print("\tLeuchtmelder 70 " + str(Textanzeigedaten["LM70"]))

    if Textanzeigedaten["LM55"] != Textanzeigedatenalt["LM55"]:
        if (Textanzeigedaten["LM55"] >= 0) & (Textanzeigedaten["LM55"] <= 15):
            print("\tLeuchtmelder 55 " + str(AusgabeLM[Textanzeigedaten["LM55"]]))
        else:
            print("\tLeuchtmelder 55 " + str(Textanzeigedaten["LM85"]))

    if Textanzeigedaten["LM1000Hz"] != Textanzeigedatenalt["LM1000Hz"]:
        if (Textanzeigedaten["LM1000Hz"] >= 0) & (Textanzeigedaten["LM1000Hz"] <= 15):
            print("\tLeuchtmelder PZB 1000Hz " + str(AusgabeLM[Textanzeigedaten["LM1000Hz"]]))
        else:
            print("\tLeuchtmelder PZB 1000Hz " + str(Textanzeigedaten["LM1000Hz"]))

    if Textanzeigedaten["LM500Hz"] != Textanzeigedatenalt["LM500Hz"]:
        if (Textanzeigedaten["LM500Hz"] >= 0) & (Textanzeigedaten["LM500Hz"] <= 15):
            print("\tLeuchtmelder 500 Hz " + str(AusgabeLM[Textanzeigedaten["LM500Hz"]]))
        else:
            print("\tLeuchtmelder 500 Hz " + str(Textanzeigedaten["LM500Hz"]))

    if Textanzeigedaten["LMB40"] != Textanzeigedatenalt["LMB40"]:
        if (Textanzeigedaten["LMB40"] >= 0) & (Textanzeigedaten["LMB40"] <= 15):
            print("\tLeuchtmelder Befehl 40 " + str(AusgabeLM[Textanzeigedaten["LMB40"]]))
        else:
            print("\tLeuchtmelder Befehl 40 " + str(Textanzeigedaten[""]))

    if Textanzeigedaten["LMH"] != Textanzeigedatenalt["LMH"]:
        if (Textanzeigedaten["LMH"] >= 0) & (Textanzeigedaten["LMH"] <= 15):
            print("\tLeuchtmelder H (Nothalt) " + str(AusgabeLM[Textanzeigedaten["LMH"]]))
        else:
            print("\tLeuchtmelder H (Nothalt) " + str(Textanzeigedaten["LMH"]))

    if Textanzeigedaten["LMG"] != Textanzeigedatenalt["LMG"]:
        if (Textanzeigedaten["LMG"] >= 0) & (Textanzeigedaten["LMG"] <= 15):
            print("\tLeuchtmelder G (Geschwindigkeit " + str(AusgabeLM[Textanzeigedaten["LMG"]]))
        else:
            print("\tLeuchtmelder G (Geschwindigkeit " + str(Textanzeigedaten["LMG"]))

    if Textanzeigedaten["LME40"] != Textanzeigedatenalt["LME40"]:
        if (Textanzeigedaten["LME40"] >= 0) & (Textanzeigedaten["LME40"] <= 15):
            print("\tLeuchtmelder E40 (Ersatzauftrag) " + str(AusgabeLM[Textanzeigedaten["LME40"]]))
        else:
            print("\tLeuchtmelder E40 (Ersatzauftrag) " + str(Textanzeigedaten["LME40"]))

    if Textanzeigedaten["LMEL"] != Textanzeigedatenalt["LMEL"]:
        if (Textanzeigedaten["LMEL"] >= 0) & (Textanzeigedaten["LMEL"] <= 15):
            print("\tLeuchtmelder EL " + str(AusgabeLM[Textanzeigedaten["LMEL"]]))
        else:
            print("\tLeuchtmelder EL " + str(Textanzeigedaten["LMEL"]))

    if Textanzeigedaten["LMEnde"] != Textanzeigedatenalt["LMEnde"]:
        if (Textanzeigedaten["LMEnde"] >= 0) & (Textanzeigedaten["LMEnde"] <= 15):
            print("\tLeuchtmelder Ende " + str(AusgabeLM[Textanzeigedaten["LMEnde"]]))
        else:
            print("\tLeuchtmelder Ende " + str(Textanzeigedaten["LMEnde"]))

    if Textanzeigedaten["LMV40"] != Textanzeigedatenalt["LMV40"]:
        if (Textanzeigedaten["LMV40"] >= 0) & (Textanzeigedaten["LMV40"] <= 15):
            print("\tLeuchtmelder V40 " + str(AusgabeLM[Textanzeigedaten["LMV40"]]))
        else:
            print("\tLeuchtmelder V40 " + str(Textanzeigedaten["LMV40"]))

    if Textanzeigedaten["LMB"] != Textanzeigedatenalt["LMB"]:
        if (Textanzeigedaten["LMB"] >= 0) & (Textanzeigedaten["LMB"] <= 15):
            print("\tLeuchtmelder B (Betrieb) " + str(AusgabeLM[Textanzeigedaten["LMB"]]))
        else:
            print("\tLeuchtmelder B (Betrieb) " + str(Textanzeigedaten["LMB"]))

    if Textanzeigedaten["LMS"] != Textanzeigedatenalt["LMS"]:
        if (Textanzeigedaten["LMS"] >= 0) & (Textanzeigedaten["LMS"] <= 15):
            print("\tLeuchtmelder S (Schnellbremsung) " + str(AusgabeLM[Textanzeigedaten["LMS"]]))
        else:
            print("\tLeuchtmelder S (Schnellbremsung) " + str(Textanzeigedaten["LMS"]))

    if Textanzeigedaten["LMUe"] != Textanzeigedatenalt["LMUe"]:
        if (Textanzeigedaten["LMUe"] >= 0) & (Textanzeigedaten["LMUe"] <= 15):
            print("\tLeuchtmelder Ü (Übertragung) " + str(AusgabeLM[Textanzeigedaten["LMUe"]]))
        else:
            print("\tLeuchtmelder Ü (Übertragung) " + str(Textanzeigedaten["LMUe"]))

    if Textanzeigedaten["LMPZB"] != Textanzeigedatenalt["LMPZB"]:
        if (Textanzeigedaten["LMPZB"] == True) or (Textanzeigedaten["LMPZB"] == False):
            print("\tLeuchtmelder PZB " + str(AusgabeLM[Textanzeigedaten["LMPZB"]]))
        else:
            print("\tLeuchtmelder PZB " + str(Textanzeigedaten["LMPZB"]))

    if Textanzeigedaten["LMGNT"] != Textanzeigedatenalt["LMGNT"]:
        if (Textanzeigedaten["LMGNT"] == True) or (Textanzeigedaten["LMGNT"] == False):
            print("\tLeuchtmelder GNT " + str(AusgabeLM[Textanzeigedaten["LMGNT"]]))
        else:
            print("\tLeuchtmelder GNT " + str(Textanzeigedaten["LMGNT"]))

    if Textanzeigedaten["LMGNTUe"] != Textanzeigedatenalt["LMGNTUe"]:
        if (Textanzeigedaten["LMGNTUe"] == True) or (Textanzeigedaten["LMGNTUe"] == False):
            print("\tLeuchtmelder GNT Ü " + str(AusgabeLM[Textanzeigedaten["LMGNTUe"]]))
        else:
            print("\tLeuchtmelder GNT Ü " + str(Textanzeigedaten["LMGNTUe"]))

    if Textanzeigedaten["LMGNTG"] != Textanzeigedatenalt["LMGNTG"]:
        if (Textanzeigedaten["LMGNTG"] == True) or (Textanzeigedaten["LMGNTG"] == False):
            print("\tLeuchtmelder GNT G " + str(AusgabeLM[Textanzeigedaten["LMGNTG"]]))
        else:
            print("\tLeuchtmelder GNT G " + str(Textanzeigedaten["LMGNTG"]))

    if Textanzeigedaten["LMGNTS"] != Textanzeigedatenalt["LMGNTS"]:
        if (Textanzeigedaten["LMGNTS"] == True) or (Textanzeigedaten["LMGNTS"] == False):
            print("\tLeuchtmelder GNT S " + str(AusgabeLM[Textanzeigedaten["LMGNTS"]]))
        else:
            print("\tLeuchtmelder GNT S " + str(Textanzeigedaten["LMGNTS"]))

    if Textanzeigedaten["LMStoer"] != Textanzeigedatenalt["LMStoer"]:
        if (Textanzeigedaten["LMStoer"] >= 0) & (Textanzeigedaten["LMStoer"] <= 15):
            print("\tLeuchtmelder Störung " + str(AusgabeLM[Textanzeigedaten["LMStoer"]]))
        else:
            print("\tLeuchtmelder Störung " + str(Textanzeigedaten["LMStoer"]))

    if Textanzeigedaten["HupePZB"] != Textanzeigedatenalt["HupePZB"]:
        if (Textanzeigedaten["HupePZB"] >= 0) & (Textanzeigedaten["HupePZB"] <= 3):
            print("\tPZB-Hupe " + str(AusgabeHupe[Textanzeigedaten["HupePZB"]]))
        else:
            print("\tPZB-Hupe " + str(Textanzeigedaten["HupePZB"]))

    if Textanzeigedaten["SchnarreLZB"] != Textanzeigedatenalt["SchnarreLZB"]:
        if (Textanzeigedaten["SchnarreLZB"] >= 0) & (Textanzeigedaten["SchnarreLZB"] <= 3):
            print("\tLZB-Schnarre " + str(AusgabeHupe[Textanzeigedaten["SchnarreLZB"]]))
        else:
            print("\tLZB-Schnarre " + str(Textanzeigedaten["SchnarreLZB"]))

    if Textanzeigedaten["HupeSifa"] != Textanzeigedatenalt["HupeSifa"]:
            print("\tSifa-Hupe " + str(AusgabeBool[Textanzeigedaten["HupeSifa"]]))

    if Textanzeigedaten["ZbSifa"] != Textanzeigedatenalt["ZbSifa"]:
        if (Textanzeigedaten["ZbSifa"] == True) or (Textanzeigedaten["ZbSifa"] == False):
            print("\tSifa-Zwangsbremse " + str(AusgabeLM[Textanzeigedaten["ZbSifa"]]))
        else:
            print("\tSifa-Zwangsbremse " + str(Textanzeigedaten["ZbSifa"]))

    if Textanzeigedaten["LZBVsoll"] != Textanzeigedatenalt["LZBVsoll"]:
        print("\tLZB Soll-Geschwindigkeit " + str(Textanzeigedaten["LZBVsoll"]) + " km/h")

    if Textanzeigedaten["LZBVziel"] != Textanzeigedatenalt["LZBVziel"]:
        print("\tLZB Ziel-Geschwindigkeit " + str(Textanzeigedaten["LZBVziel"]) + " km/h")

    if Textanzeigedaten["LZBSziel"] != Textanzeigedatenalt["LZBSziel"]:
        print("\tLZB Ziel-Entfernung " + str(Textanzeigedaten["LZBSziel"]) + " m")

    # if Textanzeigedaten["LZBZeig"] != Textanzeigedatenalt["LZBZeig"]:
    #     if Textanzeigedaten["LZBZeig"] == True:
    #         ausgabe = "EIN"
    #     elif Textanzeigedaten["LZBZeig"] == False:
    #         ausgabe = "AUS"
    #     print("\tLZB-Führungsgrößen zeigen " + ausgabe)

    if Textanzeigedaten["BRH"] != Textanzeigedatenalt["BRH"]:
        print("\tBRH-Wert (Bremshundertstel) " + str(Textanzeigedaten["BRH"]) + " %")

    if Textanzeigedaten["BRA"] != Textanzeigedatenalt["BRA"]:
        print("\tBRA-Wert (Bremsart) " + str(Textanzeigedaten["BRA"]))

    if Textanzeigedaten["ZL"] != Textanzeigedatenalt["ZL"]:
        print("\tZL-Wert (Zuglänge) " + str(Textanzeigedaten["ZL"]) + " m")

    if Textanzeigedaten["VMZ"] != Textanzeigedatenalt["VMZ"]:
        print("\tVMZ-Wert (Höchstgeschwindigkeit) " + str(Textanzeigedaten["VMZ"]) + " km/h")

    if Textanzeigedaten["ZDK"] != Textanzeigedatenalt["ZDK"]:
        if Textanzeigedaten["ZDK"] == False:
            ausgabe = "EIN"
        elif Textanzeigedaten["ZDK"] == True:
            ausgabe = "AUS"
        print("\tZugdatenanzeige in der MFA " + ausgabe)

    if Textanzeigedaten["LZBSystem"] != Textanzeigedatenalt["LZBSystem"]:
        print("\tBauart des LZB/PZB-System " + str(Textanzeigedaten["LZBSystem"]))

    if Textanzeigedaten["PZBZa"] != Textanzeigedatenalt["PZBZa"]:
        print("\tPZB-Zugart (1:U, 2:M, 3:O) " + str(Textanzeigedaten["PZBZa"]))

    if Textanzeigedaten["AFBaktiv"] != Textanzeigedatenalt["AFBaktiv"]:
        if (Textanzeigedaten["AFBaktiv"] == True) or (Textanzeigedaten["AFBaktiv"] == False):
            print("\tAFB aktiv " + str(AusgabeLM[Textanzeigedaten["AFBaktiv"]]))
        else:
            print("\tAFB aktiv " + str(Textanzeigedaten["AFBaktiv"]))

    if Textanzeigedaten["AFBVsoll"] != Textanzeigedatenalt["AFBVsoll"]:
        print("\tAFB Soll-Geschwindigkeit " + str(Textanzeigedaten["AFBVsoll"]) + " km/h")

    if Textanzeigedaten["Uol"] != Textanzeigedatenalt["Uol"]:
        print("\tFahrdrahtspannung " + str(Textanzeigedaten["Uol"]) + " V")

    if Textanzeigedaten["Iol"] != Textanzeigedatenalt["Iol"]:
        print("\tOberstrom " + str(Textanzeigedaten["Iol"]) + " A")

    if Textanzeigedaten["Umot"] != Textanzeigedatenalt["Umot"]:
        print("\tMotorspannung " + str(Textanzeigedaten["Umot"]) + " V")

    if Textanzeigedaten["Nmot"] != Textanzeigedatenalt["Nmot"]:
        print("\tDieselmotordrehzahl " + str(Textanzeigedaten["Nmot"]) + " ")

    if Textanzeigedaten["DruckHB"] != Textanzeigedatenalt["DruckHB"]:
        print("\tDruck Hauptluftbehälter " + str(round(Textanzeigedaten["DruckHB"],3)) + " bar")

    if Textanzeigedaten["DruckHL"] != Textanzeigedatenalt["DruckHL"]:
        print("\tDruck Hauptluftleitung " + str(round(Textanzeigedaten["DruckHL"],3)) + " bar")

    if Textanzeigedaten["DruckZ"] != Textanzeigedatenalt["DruckZ"]:
        print("\tDruck Zeitbehälter " + str(round(Textanzeigedaten["DruckZ"],3)) + " bar")

    if Textanzeigedaten["DruckC"] != Textanzeigedatenalt["DruckC"]:
        print("\tDruck Bremszylinder " + str(round(Textanzeigedaten["DruckC"],3)) + " bar")

    if Textanzeigedaten["TuerSystem"] != Textanzeigedatenalt["TuerSystem"]:
        print("\tTürsystem " + str(Textanzeigedaten["TuerSystem"]))

    if Textanzeigedaten["TuerL"] != Textanzeigedatenalt["TuerL"]:
        if (Textanzeigedaten["TuerL"] & 0x1) == 1:
            ausgabe = "freigegeben"
        elif (Textanzeigedaten["TuerL"] & 0x1) == 0:
            ausgabe = "nicht freigegeben"
        print("\tTüren links sind " + ausgabe)

    if Textanzeigedaten["TuerR"] != Textanzeigedatenalt["TuerR"]:
        if (Textanzeigedaten["TuerR"] & 0x1) == 1:
            ausgabe = "freigegeben"
        elif (Textanzeigedaten["TuerR"] & 0x1) == 0:
            ausgabe = "nicht freigegeben"
        print("\tTüren rechts sind " + ausgabe)

    if Textanzeigedaten["SimZeit"] != Textanzeigedatenalt["SimZeit"]:
       Simulationszeit = datetime.datetime.fromtimestamp(Textanzeigedaten["SimZeit"])
       print("Simulationszeit : ", Simulationszeit.strftime('%H:%M:%S'))

    if Textanzeigedaten["Zugnr"] != Textanzeigedatenalt["Zugnr"]:
        print("\tZugnummer " + str(Textanzeigedaten["Zugnr"]))

    if Textanzeigedaten["Streckenkm"] != Textanzeigedatenalt["Streckenkm"]:
        print("\tStreckenkilometer " + str(Textanzeigedaten["Streckenkm"]) + " m")

    if Textanzeigedaten["Simkm"] != Textanzeigedatenalt["Simkm"]:
        print("\tRelative Position " + str(Textanzeigedaten["Simkm"]) + " m")

    if Textanzeigedaten["VmaxTfz"] != Textanzeigedatenalt["VmaxTfz"]:
        print("\tHöchstgeschwindigkeit des Tfz " + str(Textanzeigedaten["VmaxTfz"]) + " km/h")

    if Textanzeigedaten["NVR"] != Textanzeigedatenalt["NVR"]:
        print("\tEindeutige Fahrzeugnummer des Tfz " + str(Textanzeigedaten["NVR"]))
    return None

def Anzeigemodusanzeige(Textanzeigedaten):
    print("\tAnzeigemodus: ", Textanzeigedaten["AnzModus"])
    if Textanzeigedaten["AnzModus"] & 0b0000000000001:
        print("\tInnerer Zugkraftanzeiger zeigt Zugkraft pro Achse")
    else:
        print("\tInnerer Zugkraftanzeiger ohne Funktion")
    if Textanzeigedaten["AnzModus"] & 0b0000000000110 == 2:
        print("\tInnerer Bremskraftanzeiger zeigt Bremskraft des Triebfahrzeugs")
    elif Textanzeigedaten["AnzModus"] & 0b0000000000110 == 4:
        print("\tInnerer Bremskraftanzeiger zeigt Bremskraft des Drehgestells 1")
    else:
        print("\tInnerer Bremskraftanzeiger ohne Funktion")
    if (Textanzeigedaten["AnzModus"] & 0b0000000011000 == 8):
        print("\tÄußerer Zugkraftanzeiger zeigt Schleudern")
    elif (Textanzeigedaten["AnzModus"] & 0b0000000011000 == 16):
        print("\tÄußerer Zugkraftanzeiger zeigt Sollzugkraft pro Achse")
    elif (Textanzeigedaten["AnzModus"] & 0b0000000011000 == 24):
        print("\tÄußerer Zugkraftanzeiger zeigt Zugkraft zweite Lok pro Achse")
    else:
        print("\tÄußerer Zugkraftanzeiger ohne Funktion")
    if (Textanzeigedaten["AnzModus"] & 0b0000001100000 == 32):
        print("\tÄußerer Bremskraftanzeiger zeigt Gleiten")
    elif (Textanzeigedaten["AnzModus"] & 0b0000001100000 == 64):
        print("\tÄußerer Bremskraftanzeiger zeigt Sollbremskraft des Triebfahrzeugs")
    elif (Textanzeigedaten["AnzModus"] & 0b0000001100000 == 96):
        print("\tÄußerer Bremskraftanzeiger zeigt Bremskraft der zweiten Lok")
    elif (Textanzeigedaten["AnzModus"] & 0b0000001100000 == 128):
        print("\tÄußerer Bremskraftanzeiger zeigt Bremskraft des Drehgestells 2")
    elif (Textanzeigedaten["AnzModus"] & 0b0000001100000 == 160):
        print("\tÄußerer Bremskraftanzeiger zeigt Bremskraft eines Drehgestells der zweiten Lok")
    else:
        print("\tÄußerer Bremskraftanzeiger ohne Funktion")
    if Textanzeigedaten["AnzModus"] & 0b0001100000000 == 256:
        print("\tFahrstufenanzeige")
    elif Textanzeigedaten["AnzModus"] & 0b0001100000000 == 512:
        print("\tSollfahrstufenanzeige")
    else:
        print("\tkeine Fahrstufenanzeige")
    if Textanzeigedaten["AnzModus"] & 0b0010000000000:
        print("\tFahrdrahtspannung, sonst Motorspannung bei Fahrstufe > 0")
    else:
        print("\tFahrdrahtspannung")
    if Textanzeigedaten["AnzModus"] & 0b0100000000000:
        print("\tDieselmotordrehzahl")
    else:
        print("\tOberstrom")
    if Textanzeigedaten["AnzModus"] & 0b1000000000000:
        print("\tManometer zeigt 5 bar minus Zeitbehälterdruck")
    else:
        print("\tManometer zeigt Zeitbehälterdruck")
    
def Textbedienanzeige(Textbediendaten,Textbediendatenalt):
    if Textbediendaten["FS"] != Textbediendatenalt["FS"]:
        if Textbediendaten["FS"] == 0:
            ausgabe = "Nullstellung"
        elif Textbediendaten["FS"] == 1:
            ausgabe = "Ab-Befehl"
        elif Textbediendaten["FS"] == 2:
            ausgabe = "Fahrt"
        elif Textbediendaten["FS"] == 3:
            ausgabe = "Auf-Befehl"
        elif Textbediendaten["FS"] == 4:
            ausgabe = "Zugkraftvorgabe " + str(round(Textbediendaten["AFSZ"],1)) + " %"
        else:
            ausgabe = "Fehler"
        print("\tFahrschalterstellung " + ausgabe)

    if Textbediendaten["AFSZ"] != Textbediendatenalt["AFSZ"]:
        print("\tFahrschalter Zugkraftvorgabe " + str(round(Textbediendaten["AFSZ"],1)) + " %")

    if Textbediendaten["Sollfahrstufe"] != Textbediendatenalt["Sollfahrstufe"]:
        print("\tFahrschalter Sollfahrstufe " + Textbediendaten["Sollfahrstufe"])

    if Textbediendaten["RS"] != Textbediendatenalt["RS"]:
        if Textbediendaten["RS"] == -1:
            ausgabe = "R-Stellung"
        elif Textbediendaten["RS"] == 0:
            ausgabe = "0-Stellung"
        elif Textbediendaten["RS"] == 1:
            ausgabe = "M-Stellung"
        elif Textbediendaten["RS"] == 2:
            ausgabe = "V-Stellung"
        else:
            ausgabe = "Fehler"
        print("\tRichtungsschalter " + ausgabe)

    if Textbediendaten["TSifa"] != Textbediendatenalt["TSifa"]:
        if Textbediendaten["TSifa"] == True:
            ausgabe = "EIN"
        elif Textbediendaten["TSifa"] == False:
            ausgabe = "AUS"
        print("\tTaster Sifa " + ausgabe)

    if Textbediendaten["FbV"] != Textbediendatenalt["FbV"]:
        if Textbediendaten["FbV"] == 0:
            ausgabe = "Mittelstellung"
        elif Textbediendaten["FbV"] == 1:
            ausgabe = "Betriebsbremse"
        elif Textbediendaten["FbV"] == 2:
            ausgabe = "Schnellbremse"
        elif Textbediendaten["FbV"] == 14:
            ausgabe = "Füllstoß"
        elif Textbediendaten["FbV"] == 15:
            ausgabe = "Fahrt"
        else:
            ausgabe = "Fehler"
        print("\tFührerbremsventilstellung " + ausgabe)

    if abs(Textbediendaten["DruckFbVA"] - Textbediendatenalt["DruckFbVA"]) > 0.05:
        print("\tFührerbremsventil A-Druck " + str(round(Textbediendaten["DruckFbVA"],3)) + " bar")

    if Textbediendaten["FbVAg"] != Textbediendatenalt["FbVAg"]:
        if Textbediendaten["FbVAg"] == True:
            ausgabe = "EIN"
        elif Textbediendaten["FbVAg"] == False:
            ausgabe = "AUS"
        print("\tFührerbremsventil Angleicher " + ausgabe)

    if Textbediendaten["FbVSchl"] != Textbediendatenalt["FbVSchl"]:
        if Textbediendaten["FbVSchl"] == True:
            ausgabe = "EIN"
        elif Textbediendaten["FbVSchl"] == False:
            ausgabe = "AUS"
        print("\tFührerbremsventil Schlüssel " + ausgabe)

    if Textbediendaten["BS"] != Textbediendatenalt["BS"]:
        if Textbediendaten["BS"] == 0:
            ausgabe = "Mittelstellung"
        elif Textbediendaten["BS"] == 1:
            ausgabe = "Betriebsbremse"
        elif Textbediendaten["BS"] == 2:
            ausgabe = "Schnellbremse"
        elif Textbediendaten["BS"] == 14:
            ausgabe = "Füllstoß"
        elif Textbediendaten["BS"] == 15:
            ausgabe = "Fahrt"
        else:
            ausgabe = "Fehler"
        print("\tBremsstellerstellung " + ausgabe)

    if abs(Textbediendaten["ABS"] - Textbediendatenalt["ABS"]) > 1.0:
        print("\tBremssteller Sollwert Bremskraft " + str(int(round(Textbediendaten["ABS"],0))) + " %")

    if Textbediendaten["ZbVBr"] != Textbediendatenalt["ZbVBr"]:
        if Textbediendaten["ZbVBr"] == True:
            ausgabe = "EIN"
        elif Textbediendaten["ZbVBr"] == False:
            ausgabe = "AUS"
        print("\tZusatzbremsventil Bremsen " + ausgabe)

    if Textbediendaten["ZbVLoe"] != Textbediendatenalt["ZbVLoe"]:
        if Textbediendaten["ZbVLoe"] == True:
            ausgabe = "EIN"
        elif Textbediendaten["ZbVLoe"] == False:
            ausgabe = "AUS"
        print("\tZusatzbremsventil Lösen " + ausgabe)

    if Textbediendaten["SLP"] != Textbediendatenalt["SLP"]:
        if Textbediendaten["SLP"] == True:
            ausgabe = "EIN"
        elif Textbediendaten["SLP"] == False:
            ausgabe = "AUS"
        print("\tSchalter Luftpresser " + ausgabe)

    if Textbediendaten["SLST"] != Textbediendatenalt["SLST"]:
        if Textbediendaten["SLST"] == True:
            ausgabe = "EIN"
        elif Textbediendaten["SLST"] == False:
            ausgabe = "AUS"
        print("\tSchalter Lüfter stark " + ausgabe)

    if Textbediendaten["SLSW"] != Textbediendatenalt["SLSW"]:
        if Textbediendaten["SLSW"] == True:
            ausgabe = "EIN"
        elif Textbediendaten["SLSW"] == False:
            ausgabe = "AUS"
        print("\tSchalter Lüfter schwach " + ausgabe)

    if Textbediendaten["TSAN"] != Textbediendatenalt["TSAN"]:
        if Textbediendaten["TSAN"] == True:
            ausgabe = "EIN"
        elif Textbediendaten["TSAN"] == False:
            ausgabe = "AUS"
        print("\tTaster Stromabnehmer nieder " + ausgabe)

    if Textbediendaten["TSAH"] != Textbediendatenalt["TSAH"]:
        if Textbediendaten["TSAH"] == True:
            ausgabe = "EIN"
        elif Textbediendaten["TSAH"] == False:
            ausgabe = "AUS"
        print("\tTaster Stromabnehmer hoch " + ausgabe)

    if Textbediendaten["THSA"] != Textbediendatenalt["THSA"]:
        if Textbediendaten["THSA"] == True:
            ausgabe = "EIN"
        elif Textbediendaten["THSA"] == False:
            ausgabe = "AUS"
        print("\tTaster Hauptschalter Aus " + ausgabe)

    if Textbediendaten["THSE"] != Textbediendatenalt["THSE"]:
        if Textbediendaten["THSE"] == True:
            ausgabe = "EIN"
        elif Textbediendaten["THSE"] == False:
            ausgabe = "AUS"
        print("\tTaster Hauptschalter Ein " + ausgabe)

    if Textbediendaten["SZSE"] != Textbediendatenalt["SZSE"]:
        if Textbediendaten["SZSE"] == True:
            ausgabe = "EIN"
        elif Textbediendaten["SZSE"] == False:
            ausgabe = "AUS"
        print("\tSchalter Zugsammelschiene Ein " + ausgabe)

    if Textbediendaten["TZSA"] != Textbediendatenalt["TZSA"]:
        if Textbediendaten["TZSA"] == True:
            ausgabe = "EIN"
        elif Textbediendaten["TZSA"] == False:
            ausgabe = "AUS"
        print("\tTaster Zugsammelschiene An " + ausgabe)

    if Textbediendaten["Tb"] != Textbediendatenalt["Tb"]:
        if Textbediendaten["Tb"] == True:
            ausgabe = "EIN"
        elif Textbediendaten["Tb"] == False:
            ausgabe = "AUS"
        print("\tTaster Indusi Befehl " + ausgabe)

    if Textbediendaten["Tf"] != Textbediendatenalt["Tf"]:
        if Textbediendaten["Tf"] == True:
            ausgabe = "EIN"
        elif Textbediendaten["Tf"] == False:
            ausgabe = "AUS"
        print("\tTaster Indusi Frei " + ausgabe)

    if Textbediendaten["Tw"] != Textbediendatenalt["Tw"]:
        if Textbediendaten["Tw"] == True:
            ausgabe = "EIN"
        elif Textbediendaten["Tw"] == False:
            ausgabe = "AUS"
        print("\tTaster Indusi Wachsam " + ausgabe)

    if Textbediendaten["STFG0"] != Textbediendatenalt["STFG0"]:
        if Textbediendaten["STFG0"] == True:
            ausgabe = "EIN"
        elif Textbediendaten["STFG0"] == False:
            ausgabe = "AUS"
        print("\tSchalter Türfreigabe 0 " + ausgabe)

    if Textbediendaten["STFGR"] != Textbediendatenalt["STFGR"]:
        if Textbediendaten["STFGR"] == True:
            ausgabe = "EIN"
        elif Textbediendaten["STFGR"] == False:
            ausgabe = "AUS"
        print("\tSchalter Türfreigabe rechts " + ausgabe)

    if Textbediendaten["STFGL"] != Textbediendatenalt["STFGL"]:
        if Textbediendaten["STFGL"] == True:
            ausgabe = "EIN"
        elif Textbediendaten["STFGL"] == False:
            ausgabe = "AUS"
        print("\tSchalter Türfreigabe links " + ausgabe)

    if Textbediendaten["TZLA"] != Textbediendatenalt["TZLA"]:
        if Textbediendaten["TZLA"] == True:
            ausgabe = "EIN"
        elif Textbediendaten["TZLA"] == False:
            ausgabe = "AUS"
        print("\tTaster Zugbeleuchtung Aus " + ausgabe)

    if Textbediendaten["TZLE"] != Textbediendatenalt["TZLE"]:
        if Textbediendaten["TZLE"] == True:
            ausgabe = "EIN"
        elif Textbediendaten["TZLE"] == False:
            ausgabe = "AUS"
        print("\tTaster Zugbeleuchtung Ein " + ausgabe)

    if Textbediendaten["TSAND"] != Textbediendatenalt["TSAND"]:
        if Textbediendaten["TSAND"] == True:
            ausgabe = "EIN"
        elif Textbediendaten["TSAND"] == False:
            ausgabe = "AUS"
        print("\tTaster Sanden " + ausgabe)

    if Textbediendaten["TSSB"] != Textbediendatenalt["TSSB"]:
        if Textbediendaten["TSSB"] == True:
            ausgabe = "EIN"
        elif Textbediendaten["TSSB"] == False:
            ausgabe = "AUS"
        print("\tTaster Schleuderschutzbremse " + ausgabe)

    if Textbediendaten["TBL"] != Textbediendatenalt["TBL"]:
        if Textbediendaten["TBL"] == True:
            ausgabe = "EIN"
        elif Textbediendaten["TBL"] == False:
            ausgabe = "AUS"
        print("\tTaster Bremse lösen " + ausgabe)

    if Textbediendaten["SFL"] != Textbediendatenalt["SFL"]:
        if Textbediendaten["SFL"] == True:
            ausgabe = "EIN"
        elif Textbediendaten["SFL"] == False:
            ausgabe = "AUS"
        print("\tSchalter Fernlicht " + ausgabe)

    if Textbediendaten["SSL"] != Textbediendatenalt["SSL"]:
        if Textbediendaten["SSL"] == True:
            ausgabe = "EIN"
        elif Textbediendaten["SSL"] == False:
            ausgabe = "AUS"
        print("\tSchalter Signallicht " + ausgabe)

    if Textbediendaten["TMF"] != Textbediendatenalt["TMF"]:
        if Textbediendaten["TMF"] == True:
            ausgabe = "EIN"
        elif Textbediendaten["TMF"] == False:
            ausgabe = "AUS"
        print("\tTaster Makrofon " + ausgabe)

    if Textbediendaten["TTFGTZ"] != Textbediendatenalt["TTFGTZ"]:
        if Textbediendaten["TTFGTZ"] == True:
            ausgabe = "EIN"
        elif Textbediendaten["TTFGTZ"] == False:
            ausgabe = "AUS"
        print("\tTaster Türfreigabe TZ " + ausgabe)

    if Textbediendaten["TTFGT0"] != Textbediendatenalt["TTFGT0"]:
        if Textbediendaten["TTFGT0"] == True:
            ausgabe = "EIN"
        elif Textbediendaten["TTFGT0"] == False:
            ausgabe = "AUS"
        print("\tTaster Türfreigabe T0 " + ausgabe)

    if Textbediendaten["TFIS"] != Textbediendatenalt["TFIS"]:
        if Textbediendaten["TFIS"] == True:
            ausgabe = "EIN"
        elif Textbediendaten["TFIS"] == False:
            ausgabe = "AUS"
        print("\tTaster FIS-Fortschaltung " + ausgabe)

    # if Textbediendaten["DI1I1"] != Textbediendatenalt["DI1I1"]:
    #     if Textbediendaten["DI1I1"] == True:
    #         ausgabe = "EIN"
    #     elif Textbediendaten["DI1I1"] == False:
    #         ausgabe = "AUS"
    #     print("\tEingang DIO1 I1 " + ausgabe)

    # if Textbediendaten["DI1I2"] != Textbediendatenalt["DI1I2"]:
    #     if Textbediendaten["DI1I2"] == True:
    #         ausgabe = "EIN"
    #     elif Textbediendaten["DI1I2"] == False:
    #         ausgabe = "AUS"
    #     print("\tEingang DIO1 I2 " + ausgabe)

    # if Textbediendaten["DI1I3"] != Textbediendatenalt["DI1I3"]:
    #     if Textbediendaten["DI1I3"] == True:
    #         ausgabe = "EIN"
    #     elif Textbediendaten["DI1I3"] == False:
    #         ausgabe = "AUS"
    #     print("\tEingang DIO1 I3 " + ausgabe)

    # if Textbediendaten["DI1I4"] != Textbediendatenalt["DI1I4"]:
    #     if Textbediendaten["DI1I4"] == True:
    #         ausgabe = "EIN"
    #     elif Textbediendaten["DI1I4"] == False:
    #         ausgabe = "AUS"
    #     print("\tTaster Leuchtmelder prüfen " + ausgabe)

    # if Textbediendaten["DI1I5"] != Textbediendatenalt["DI1I5"]:
    #     if Textbediendaten["DI1I5"] == True:
    #         ausgabe = "EIN"
    #     elif Textbediendaten["DI1I5"] == False:
    #         ausgabe = "AUS"
    #     print("\tTaster Störung quittieren " + ausgabe)

    # if Textbediendaten["DI1I6"] != Textbediendatenalt["DI1I6"]:
    #     if Textbediendaten["DI1I6"] == True:
    #         ausgabe = "EIN"
    #     elif Textbediendaten["DI1I6"] == False:
    #         ausgabe = "AUS"
    #     print("\tFahrschalter Schnell-Auf-Befehl " + ausgabe)

    # if Textbediendaten["DI4I10"] != Textbediendatenalt["DI4I10"]:
    #     if Textbediendaten["DI4I10"] == True:
    #         ausgabe = "EIN"
    #     elif Textbediendaten["DI4I10"] == False:
    #         ausgabe = "AUS"
    #     print("\tSchalter Heizen " + ausgabe)

    # if Textbediendaten["DI4I11"] != Textbediendatenalt["DI4I11"]:
    #     if Textbediendaten["DI4I11"] == True:
    #         ausgabe = "EIN"
    #     elif Textbediendaten["DI4I11"] == False:
    #         ausgabe = "AUS"
    #     print("\tSchalter Lüften " + ausgabe)

    # if Textbediendaten["DI4I12"] != Textbediendatenalt["DI4I12"]:
    #     if Textbediendaten["DI4I12"] == True:
    #         ausgabe = "EIN"
    #     elif Textbediendaten["DI4I12"] == False:
    #         ausgabe = "AUS"
    #     print("\tEingang DI4I12 " + ausgabe)

    # if Textbediendaten["DI4I13"] != Textbediendatenalt["DI4I13"]:
    #     if Textbediendaten["DI4I13"] == True:
    #         ausgabe = "EIN"
    #     elif Textbediendaten["DI4I13"] == False:
    #         ausgabe = "AUS"
    #     print("\tFührerraumleuchte " + ausgabe)

    # if Textbediendaten["DI4I14"] != Textbediendatenalt["DI4I14"]:
    #     if Textbediendaten["DI4I14"] == True:
    #         ausgabe = "EIN"
    #     elif Textbediendaten["DI4I14"] == False:
    #         ausgabe = "AUS"
    #     print("\tEingang DI4I14 " + ausgabe)

    return None
