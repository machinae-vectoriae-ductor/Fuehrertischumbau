#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import xml.etree.ElementTree as ET

z3orgpfad = r"C:\Program Files (x86)\Zusi3\_ZusiData\RollingStock"
z3zielpfad = r"C:\Users\Public\Documents\Zusi3\RollingStock"

zahlfst = 0

for dirpath, dirname, filename in os.walk(z3orgpfad):
    for i in range(len(filename)):
        if r".ftd" in filename[i]:
            zahlfst += 1
            geaendert = False
            z3reldateiname = os.path.join(os.path.relpath(dirpath, z3orgpfad), filename[i])
            z3orgdateiname = os.path.join(z3orgpfad, z3reldateiname)
            z3zieldateiname = os.path.join(z3zielpfad, z3reldateiname)
            print(z3reldateiname)
            treeftd = ET.parse(z3orgdateiname)
            nftd_root = treeftd.getroot()
            for j in range(len(nftd_root)):
                if "Fuehrerstand" in nftd_root[j].tag:
                    for k in range(len(nftd_root[j])):
                        if "Funktionalitaeten" in nftd_root[j][k].tag:
                            for l in range(len(nftd_root[j][k])):
                                # print(nftd_root[j][k][l].tag)
                                if "Angleicher" in nftd_root[j][k][l].tag:
                                    if ("FktName" in nftd_root[j][k][l].attrib) and ("Tastaturzuordnung" in nftd_root[j][k][l].attrib):
                                        if nftd_root[j][k][l].attrib["Tastaturzuordnung"] != "41":
                                            print("Alt: Funktion " + nftd_root[j][k][l].attrib["FktName"] + ", Tastaturzuordnung " + nftd_root[j][k][l].attrib["Tastaturzuordnung"])
                                            nftd_root[j][k][l].attrib["Tastaturzuordnung"] = "41"
                                            print("Neu: Funktion " + nftd_root[j][k][l].attrib["FktName"] + ", Tastaturzuordnung " + nftd_root[j][k][l].attrib["Tastaturzuordnung"])
                                            geaendert = True
                                if ("TuerenSAT" in nftd_root[j][k][l].tag or "TuerenUICWTB" in nftd_root[j][k][l].tag):
                                    schaltertyp = True
                                    if ("FktName" in nftd_root[j][k][l].attrib):
                                        if ("SchalterTyp" in nftd_root[j][k][l].attrib):
                                            if nftd_root[j][k][l].attrib["SchalterTyp"] != "1":
                                                schaltertyp = False
                                        else:
                                            schaltertyp = False
                                        if not schaltertyp:
                                            print("Alt: Funktion " + nftd_root[j][k][l].attrib["FktName"] + ", Drehschalter")
                                            nftd_root[j][k][l].attrib["SchalterTyp"] = "1"
                                            print("Neu: Funktion " + nftd_root[j][k][l].attrib["FktName"] + ", Taster")
                                            geaendert = True
                                if ("TuerenTAV" in nftd_root[j][k][l].tag or "TuerenSST" in nftd_root[j][k][l].tag):
                                    taster = True
                                    schaltertyp = True
                                    if ("FktName" in nftd_root[j][k][l].attrib):
                                        if ("Taster" in nftd_root[j][k][l].attrib):
                                            if nftd_root[j][k][l].attrib["Taster"] != "1":
                                                taster = False
                                        else:
                                            taster = False
                                    if ("FktName" in nftd_root[j][k][l].attrib):
                                        if ("SchalterTyp" in nftd_root[j][k][l].attrib):
                                            if nftd_root[j][k][l].attrib["SchalterTyp"] != "1":
                                                schaltertyp = False
                                        else:
                                            schaltertyp = False
                                        if not taster:
                                            print("Alt: Funktion " + nftd_root[j][k][l].attrib["FktName"] + ", Schalter")
                                            nftd_root[j][k][l].attrib["Taster"] = "1"
                                            print("Neu: Funktion " + nftd_root[j][k][l].attrib["FktName"] + ", Taster")
                                            geaendert = True
                                        if not schaltertyp:
                                            print("Alt: Funktion " + nftd_root[j][k][l].attrib["FktName"] + ", Drehschalter")
                                            nftd_root[j][k][l].attrib["Taster"] = "1"
                                            nftd_root[j][k][l].attrib["SchalterTyp"] = "1"
                                            print("Neu: Funktion " + nftd_root[j][k][l].attrib["FktName"] + ", Zwei Taster")
                                            geaendert = True
                                if ("Sander" in nftd_root[j][k][l].tag or "Pfeife" in nftd_root[j][k][l].tag or
                                    "Notaus" in nftd_root[j][k][l].tag or "LokbremseEntlueften" in nftd_root[j][k][l].tag or 
                                    "Schleuderschutzbremse" in nftd_root[j][k][l].tag or "AFBEinAus" in nftd_root[j][k][l].tag or
                                    "Luefter" in nftd_root[j][k][l].tag or "LuftpresserAus" in nftd_root[j][k][l].tag or
                                    "TuerenTB0" in nftd_root[j][k][l].tag):
                                    taster = True
                                    if ("FktName" in nftd_root[j][k][l].attrib):
                                        if ("Taster" in nftd_root[j][k][l].attrib):
                                            if not "1" in nftd_root[j][k][l].attrib["Taster"]:
                                                taster = False
                                        else:
                                            taster = False
                                        if not taster:
                                            print("Alt: Funktion " + nftd_root[j][k][l].attrib["FktName"] + ", Schalter")
                                            print(nftd_root[j][k][l].attrib)
                                            nftd_root[j][k][l].attrib["Taster"] = "1"
                                            print("Neu: Funktion " + nftd_root[j][k][l].attrib["FktName"] + ", Taster")
                                            geaendert = True
                                            print(nftd_root[j][k][l].attrib)
                                if "Sifa_ZeitZeit" in nftd_root[j][k][l].tag:
                                   for soundsifa in nftd_root.iter('SoundSifa'): 
                                       nftd_root[j][k][l].remove(soundsifa)
                                       print("Sifa-Hupe gelöscht")
 
            if geaendert:
                print(z3orgdateiname + " -> " + z3zieldateiname)
                ET.indent(treeftd, space=" ", level=0)
                os.makedirs(os.path.dirname(z3zieldateiname), exist_ok=True)
                treeftd.write(
                    z3zieldateiname, encoding="UTF-8", xml_declaration=True
                    )

                                        
print("Zahl der Führerstandsdateien: " + str(zahlfst))


# for ikonv in range(len(nkonv_root)):
#     if "Pfade" in nkonv_root[ikonv].tag:
#         if "Zusi2Pfad" in nkonv_root[ikonv].attrib:
#             nftd_fstd = nkonv_root[ikonv].attrib["Zusi2Pfad"]
#         try:
#             z2pfad = os.environ["ZUSI2_DATAPATH"]
#             print("Verwende Pfad Zusi2-Pfad aus der Umgebungsvariable: " + z2pfad)
#         except:
#             print(
#                 "Umgebungsvariable für den Zusi3-Pfad nicht gesetzt. Verwende Pfad aus der XML-Datei: "
#                 + z2pfad
#             )
#         if "Zusi3Pfad" in nkonv_root[ikonv].attrib:
#             z3pfad = nkonv_root[ikonv].attrib["Zusi3Pfad"]
#             print("Verwende Pfad Zusi3-Pfad aus der Umgebungsvariable: " + z3pfad)
#         try:
#             z3pfad = os.environ["ZUSI3_DATAPATH"]
#         except:
#             print(
#                 "Umgebungsvariable für den Zusi3-Pfad nicht gesetzt. Verwende Pfad aus der XML-Datei: "
#                 + z3pfad
#             )
#     if "Strecke" in nkonv_root[ikonv].tag:
#         if ("Streckendatei" in nkonv_root[ikonv].attrib) and (
#             "Zielverzeichnis" in nkonv_root[ikonv].attrib
#         ):
#             zielverzeichnis_rel = nkonv_root[ikonv].attrib["Zielverzeichnis"]
#             (st3_name, rekursionstiefe) = strecke.conv_str(
#                 z2pfad,
#                 nkonv_root[ikonv].attrib["Streckendatei"],
#                 z3pfad,
#                 zielverzeichnis_rel,
#             )
#             for jkonv in range(len(nkonv_root[ikonv])):
#                 if "Fahrplan" in nkonv_root[ikonv][jkonv].tag:
#                     if "Fahrplandatei" in nkonv_root[ikonv][jkonv].attrib:
#                         fahrplan.conv_fpn(
#                             z2pfad,
#                             nkonv_root[ikonv][jkonv].attrib["Fahrplandatei"],
#                             st3_name,
#                             z3pfad,
#                             zielverzeichnis_rel,
#                             rekursionstiefe,
#                         )
