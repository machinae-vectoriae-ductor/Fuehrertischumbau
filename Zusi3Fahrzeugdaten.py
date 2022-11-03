"""
Dieser Quellcode ist in Python 3 geschrieben und ist ein Datenspeicher
für die Parameter der verschiedenen Fahrzeuge.

This source code is written in Python 3 and is a data repository
for the parameters of the different vehicles.

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

TH Köln, hereby disclaims all copyright interest in the software 'Zusi3-Fahrzeugdaten.py'
(a data repository for the parameters of the different vehicles).

Wolfgang Evers
Versionsdatum 31.10.2022

"""

def Fahrzeugdaten(Zugverbandsdaten, Anzeigedaten):
    Kombischalterwerte = {"FSAUS"    :     0, # Fahrschalterstellung Schnellaus
                          "FSAB"     :     1, # Fahrschalterstellung Ab
                          "FSFAHRT"  :     2, # Fahrschalterstellung Fahrt
                          "FSAUF"    :     3, # Fahrschalterstellung Auf
                          "FSFZMIN"  :     4, # Fahrschalterstellung kleinste Zugkraftvorgabe
                          "FSFZMAX"  :    11, # Fahrschalterstellung größte Zugkraftvorgabe
                          "Nachlauf" : False, # Nachlaufsteuerung vorhanden
                          "SW0"      :     1, # Schaltwerksstufe 0
                          "SWMAX"    :    40, # größte Schaltwerksstufe
                          "BSSB"     :     0, # Bremssteller Schnellbremsstellung
                          "BSMAX"    :     1, # Bremssteller größte Bremskraftvorgabe
                          "BSMIN"    :     8, # Bremssteller kleinste Bremskraftvorgabe
                          "BSFahr"   :     9, # Bremssteller Fahrstellung
                          "BSFue"    :    10, # Bremssteller Füllstellung
                          "FbVSB"    :     0, # Führerbremsventil Schnellbremsstellung
                          "FbV35"    :     1, # Führerbremsventil Regelstellung 3,5 bar
                          "FbV47"    :     8, # Führerbremsventil Regelstellung 4,7 bar
                          "FbVFahr"  :     9, # Führerbremsventil Fahrstellung
                          "FbVFue"   :    10, # Führerbremsventil Füllstellung
                          "RSR"      :     0, # Richtungschalterstellung R
                          "RS0"      :     1, # Richtungschalterstellung 0
                          "RSM"      :     2, # Richtungschalterstellung M
                          "RSV"      :     3  # Richtungschalterstellung V
                         }
    if "101.rv.fzg" in Zugverbandsdaten[0]["Fahrzeugdateiname"]:
        Kombischalterwerte = {"FSAUS"    :     0, # Fahrschalterstellung Schnellaus
                              "FSAB"     :     1, # Fahrschalterstellung Ab
                              "FSFAHRT"  :     2, # Fahrschalterstellung Fahrt
                              "FSAUF"    :     3, # Fahrschalterstellung Auf
                              "FSFZMIN"  :     4, # Fahrschalterstellung kleinste Zugkraftvorgabe
                              "FSFZMAX"  :    11, # Fahrschalterstellung größte Zugkraftvorgabe
                              "Nachlauf" : False, # Nachlaufsteuerung vorhanden
                              "SW0"      :     1, # Schaltwerksstufe 0
                              "SWMAX"    :    40, # größte Schaltwerksstufe
                              "BSSB"     :     0, # Bremssteller Schnellbremsstellung
                              "BSMAX"    :     1, # Bremssteller größte Bremskraftvorgabe
                              "BSMIN"    :     8, # Bremssteller kleinste Bremskraftvorgabe
                              "BSFahr"   :     9, # Bremssteller Fahrstellung
                              "BSFue"    :    10, # Bremssteller Füllstellung
                              "FbVSB"    :     0, # Führerbremsventil Schnellbremsstellung
                              "FbV35"    :     1, # Führerbremsventil Regelstellung 3,5 bar
                              "FbV47"    :     8, # Führerbremsventil Regelstellung 4,7 bar
                              "FbVFahr"  :     9, # Führerbremsventil Fahrstellung
                              "FbVFue"   :    10, # Führerbremsventil Füllstellung
                              "RSR"      :     0, # Richtungschalterstellung R
                              "RS0"      :     1, # Richtungschalterstellung 0
                              "RSM"      :     2, # Richtungschalterstellung M
                              "RSV"      :     3  # Richtungschalterstellung V
                             }
        Anzeigedaten["AnzModus"] = 1 + 2 + 16 + 64 + 0 + 0 + 4096
    elif "103.rv.fzg" in Zugverbandsdaten[0]["Fahrzeugdateiname"]:
        Kombischalterwerte = {"FSAUS"    :     0, # Fahrschalterstellung Schnellaus
                              "FSAB"     :     1, # Fahrschalterstellung Ab
                              "FSFAHRT"  :     2, # Fahrschalterstellung Fahrt
                              "FSAUF"    :     3, # Fahrschalterstellung Auf
                              "FSFZMIN"  :     4, # Fahrschalterstellung kleinste Zugkraftvorgabe
                              "FSFZMAX"  :    11, # Fahrschalterstellung größte Zugkraftvorgabe
                              "Nachlauf" :  True, # Nachlaufsteuerung vorhanden
                              "SW0"      :     1, # Schaltwerksstufe 0
                              "SWMAX"    :    40, # größte Schaltwerksstufe
                              "BSSB"     :     0, # Bremssteller Schnellbremsstellung
                              "BSMAX"    :     1, # Bremssteller größte Bremskraftvorgabe
                              "BSMIN"    :     8, # Bremssteller kleinste Bremskraftvorgabe
                              "BSFahr"   :     9, # Bremssteller Fahrstellung
                              "BSFue"    :    10, # Bremssteller Füllstellung
                              "FbVSB"    :     0, # Führerbremsventil Schnellbremsstellung
                              "FbV35"    :     1, # Führerbremsventil Regelstellung 3,5 bar
                              "FbV47"    :     6, # Führerbremsventil Regelstellung 4,7 bar
                              "FbVFahr"  :     8, # Führerbremsventil Fahrstellung
                              "FbVFue"   :     9, # Führerbremsventil Füllstellung
                              "RSR"      :     0, # Richtungschalterstellung R
                              "RS0"      :     1, # Richtungschalterstellung 0
                              "RSM"      :     2, # Richtungschalterstellung M
                              "RSV"      :     3  # Richtungschalterstellung V
                             }
        Anzeigedaten["AnzModus"] = 1 + 4 + 8 + 128 + 512 + 1024 + 0 + 0
    elif "E10.rv.fzg" in Zugverbandsdaten[0]["Fahrzeugdateiname"]:
        Kombischalterwerte = {"FSAUS"    :     0, # Fahrschalterstellung Schnellaus
                              "FSAB"     :     1, # Fahrschalterstellung Ab
                              "FSFAHRT"  :     2, # Fahrschalterstellung Fahrt
                              "FSAUF"    :     3, # Fahrschalterstellung Auf
                              "FSFZMIN"  :     4, # Fahrschalterstellung kleinste Zugkraftvorgabe
                              "FSFZMAX"  :    11, # Fahrschalterstellung größte Zugkraftvorgabe
                              "Nachlauf" :  True, # Nachlaufsteuerung vorhanden
                              "SW0"      :     1, # Schaltwerksstufe 0
                              "SWMAX"    :    29, # größte Schaltwerksstufe
                              "BSSB"     :     0, # Bremssteller Schnellbremsstellung
                              "BSMAX"    :     1, # Bremssteller größte Bremskraftvorgabe
                              "BSMIN"    :     8, # Bremssteller kleinste Bremskraftvorgabe
                              "BSFahr"   :    10, # Bremssteller Fahrstellung
                              "BSFue"    :    11, # Bremssteller Füllstellung
                              "FbVSB"    :     0, # Führerbremsventil Schnellbremsstellung
                              "FbV35"    :     1, # Führerbremsventil Regelstellung 3,5 bar
                              "FbV47"    :     6, # Führerbremsventil Regelstellung 4,7 bar
                              "FbVFahr"  :     8, # Führerbremsventil Fahrstellung
                              "FbVFue"   :     9, # Führerbremsventil Füllstellung
                              "RSR"      :     0, # Richtungschalterstellung R
                              "RS0"      :     1, # Richtungschalterstellung 0
                              "RSM"      :     2, # Richtungschalterstellung M
                              "RSV"      :     3  # Richtungschalterstellung V
                             }
        if ("E10 402" in Zugverbandsdaten[0]["Beschreibung"] or "110 467-8" in Zugverbandsdaten[0]["Beschreibung"]
         or "110 415-7" in Zugverbandsdaten[0]["Beschreibung"] or "110 292-0" in Zugverbandsdaten[0]["Beschreibung"]
         or "110 348-0" in Zugverbandsdaten[0]["Beschreibung"] or "110 365-4" in Zugverbandsdaten[0]["Beschreibung"]
         or "110 439-7" in Zugverbandsdaten[0]["Beschreibung"] or "110 360-5" in Zugverbandsdaten[0]["Beschreibung"]
         or "114 498-9" in Zugverbandsdaten[0]["Beschreibung"] or "110 107-0" in Zugverbandsdaten[0]["Beschreibung"]
         or "110 469-4" in Zugverbandsdaten[0]["Beschreibung"]):
            Kombischalterwerte = {"FSAUS"    :     0, # Fahrschalterstellung Schnellaus
                                  "FSAB"     :     1, # Fahrschalterstellung Ab
                                  "FSFAHRT"  :     2, # Fahrschalterstellung Fahrt
                                  "FSAUF"    :     3, # Fahrschalterstellung Auf
                                  "FSFZMIN"  :     4, # Fahrschalterstellung kleinste Zugkraftvorgabe
                                  "FSFZMAX"  :    11, # Fahrschalterstellung größte Zugkraftvorgabe
                                  "Nachlauf" :  True, # Nachlaufsteuerung vorhanden
                                  "SW0"      :     0, # Schaltwerksstufe 0
                                  "SWMAX"    :    28, # größte Schaltwerksstufe
                                  "BSSB"     :     0, # Bremssteller Schnellbremsstellung
                                  "BSMAX"    :     1, # Bremssteller größte Bremskraftvorgabe
                                  "BSMIN"    :     9, # Bremssteller kleinste Bremskraftvorgabe
                                  "BSFahr"   :    10, # Bremssteller Fahrstellung
                                  "BSFue"    :    11, # Bremssteller Füllstellung
                                  "FbVSB"    :     0, # Führerbremsventil Schnellbremsstellung
                                  "FbV35"    :     1, # Führerbremsventil Regelstellung 3,5 bar
                                  "FbV47"    :     9, # Führerbremsventil Regelstellung 4,7 bar
                                  "FbVFahr"  :    11, # Führerbremsventil Fahrstellung
                                  "FbVFue"   :    12, # Führerbremsventil Füllstellung
                                  "RSR"      :     0, # Richtungschalterstellung R
                                  "RS0"      :     1, # Richtungschalterstellung 0
                                  "RSM"      :     2, # Richtungschalterstellung M
                                  "RSV"      :     3  # Richtungschalterstellung V
                                 }
            
        Anzeigedaten["AnzModus"] = 1 + 2 + 0 + 0 + 256 + 1024 + 0 + 0
    elif "111.rv.fzg" in Zugverbandsdaten[0]["Fahrzeugdateiname"]:
        Kombischalterwerte = {"FSAUS"    :     0, # Fahrschalterstellung Schnellaus
                              "FSAB"     :     1, # Fahrschalterstellung Ab
                              "FSFAHRT"  :     2, # Fahrschalterstellung Fahrt
                              "FSAUF"    :     3, # Fahrschalterstellung Auf
                              "FSFZMIN"  :     2, # Fahrschalterstellung kleinste Zugkraftvorgabe
                              "FSFZMAX"  :     2, # Fahrschalterstellung größte Zugkraftvorgabe
                              "Nachlauf" : False, # Nachlaufsteuerung vorhanden
                              "SW0"      :     1, # Schaltwerksstufe 0
                              "SWMAX"    :    29, # größte Schaltwerksstufe
                              "BSSB"     :     0, # Bremssteller Schnellbremsstellung
                              "BSMAX"    :     1, # Bremssteller größte Bremskraftvorgabe
                              "BSMIN"    :     8, # Bremssteller kleinste Bremskraftvorgabe
                              "BSFahr"   :     9, # Bremssteller Fahrstellung
                              "BSFue"    :    10, # Bremssteller Füllstellung
                              "FbVSB"    :     0, # Führerbremsventil Schnellbremsstellung
                              "FbV35"    :     1, # Führerbremsventil Regelstellung 3,5 bar
                              "FbV47"    :     8, # Führerbremsventil Regelstellung 4,7 bar
                              "FbVFahr"  :     9, # Führerbremsventil Fahrstellung
                              "FbVFue"   :    10, # Führerbremsventil Füllstellung
                              "RSR"      :     0, # Richtungschalterstellung R
                              "RS0"      :     1, # Richtungschalterstellung 0
                              "RSM"      :     2, # Richtungschalterstellung M
                              "RSV"      :     3  # Richtungschalterstellung V
                             }
        Anzeigedaten["AnzModus"] = 1 + 2 + 8 + 32 + 256 + 1024 + 0 + 4096
    elif "120.rv.fzg" in Zugverbandsdaten[0]["Fahrzeugdateiname"]:
        Kombischalterwerte = {"FSAUS"    :     0, # Fahrschalterstellung Schnellaus
                              "FSAB"     :     1, # Fahrschalterstellung Ab
                              "FSFAHRT"  :     2, # Fahrschalterstellung Fahrt
                              "FSAUF"    :     3, # Fahrschalterstellung Auf
                              "FSFZMIN"  :     4, # Fahrschalterstellung kleinste Zugkraftvorgabe
                              "FSFZMAX"  :    11, # Fahrschalterstellung größte Zugkraftvorgabe
                              "Nachlauf" : False, # Nachlaufsteuerung vorhanden
                              "SW0"      :     1, # Schaltwerksstufe 0
                              "SWMAX"    :    40, # größte Schaltwerksstufe
                              "BSSB"     :     0, # Bremssteller Schnellbremsstellung
                              "BSMAX"    :     1, # Bremssteller größte Bremskraftvorgabe
                              "BSMIN"    :     8, # Bremssteller kleinste Bremskraftvorgabe
                              "BSFahr"   :     9, # Bremssteller Fahrstellung
                              "BSFue"    :    10, # Bremssteller Füllstellung
                              "FbVSB"    :     0, # Führerbremsventil Schnellbremsstellung
                              "FbV35"    :     1, # Führerbremsventil Regelstellung 3,5 bar
                              "FbV47"    :     8, # Führerbremsventil Regelstellung 4,7 bar
                              "FbVFahr"  :     9, # Führerbremsventil Fahrstellung
                              "FbVFue"   :    10, # Führerbremsventil Füllstellung
                              "RSR"      :     0, # Richtungschalterstellung R
                              "RS0"      :     1, # Richtungschalterstellung 0
                              "RSM"      :     2, # Richtungschalterstellung M
                              "RSV"      :     3  # Richtungschalterstellung V
                             }
        Anzeigedaten["AnzModus"] = 1 + 2 + 16 + 64 + 0 + 0 + 0 + 4096
    elif "E40.rv.fzg" in Zugverbandsdaten[0]["Fahrzeugdateiname"]:
        Kombischalterwerte = {"FSAUS"    :     0, # Fahrschalterstellung Schnellaus
                              "FSAB"     :     1, # Fahrschalterstellung Ab
                              "FSFAHRT"  :     2, # Fahrschalterstellung Fahrt
                              "FSAUF"    :     3, # Fahrschalterstellung Auf
                              "FSFZMIN"  :     2, # Fahrschalterstellung kleinste Zugkraftvorgabe
                              "FSFZMAX"  :     2, # Fahrschalterstellung größte Zugkraftvorgabe
                              "Nachlauf" :  True, # Nachlaufsteuerung vorhanden
                              "SW0"      :     1, # Schaltwerksstufe 0
                              "SWMAX"    :    29, # größte Schaltwerksstufe
                              "BSSB"     :     0, # Bremssteller Schnellbremsstellung
                              "BSMAX"    :     1, # Bremssteller größte Bremskraftvorgabe
                              "BSMIN"    :     8, # Bremssteller kleinste Bremskraftvorgabe
                              "BSFahr"   :     9, # Bremssteller Fahrstellung
                              "BSFue"    :    10, # Bremssteller Füllstellung
                              "FbVSB"    :     0, # Führerbremsventil Schnellbremsstellung
                              "FbV35"    :     1, # Führerbremsventil Regelstellung 3,5 bar
                              "FbV47"    :     6, # Führerbremsventil Regelstellung 4,7 bar
                              "FbVFahr"  :     8, # Führerbremsventil Fahrstellung
                              "FbVFue"   :     9, # Führerbremsventil Füllstellung
                              "RSR"      :     0, # Richtungschalterstellung R
                              "RS0"      :     1, # Richtungschalterstellung 0
                              "RSM"      :     2, # Richtungschalterstellung M
                              "RSV"      :     3  # Richtungschalterstellung V
                             }
        Anzeigedaten["AnzModus"] = 1 + 0 + 0 + 0 + 256 + 1024 + 0 + 0
    elif "E41.rv.fzg" in Zugverbandsdaten[0]["Fahrzeugdateiname"]:
        Kombischalterwerte = {"FSAUS"    :     0, # Fahrschalterstellung Schnellaus
                              "FSAB"     :     1, # Fahrschalterstellung Ab
                              "FSFAHRT"  :     2, # Fahrschalterstellung Fahrt
                              "FSAUF"    :     3, # Fahrschalterstellung Auf
                              "FSFZMIN"  :     2, # Fahrschalterstellung kleinste Zugkraftvorgabe
                              "FSFZMAX"  :     2, # Fahrschalterstellung größte Zugkraftvorgabe
                              "Nachlauf" : False, # Nachlaufsteuerung vorhanden
                              "SW0"      :     1, # Schaltwerksstufe 0
                              "SWMAX"    :    29, # größte Schaltwerksstufe
                              "BSSB"     :     0, # Bremssteller Schnellbremsstellung
                              "BSMAX"    :     1, # Bremssteller größte Bremskraftvorgabe
                              "BSMIN"    :     8, # Bremssteller kleinste Bremskraftvorgabe
                              "BSFahr"   :     9, # Bremssteller Fahrstellung
                              "BSFue"    :    10, # Bremssteller Füllstellung
                              "FbVSB"    :     0, # Führerbremsventil Schnellbremsstellung
                              "FbV35"    :     1, # Führerbremsventil Regelstellung 3,5 bar
                              "FbV47"    :     6, # Führerbremsventil Regelstellung 4,7 bar
                              "FbVFahr"  :     8, # Führerbremsventil Fahrstellung
                              "FbVFue"   :     9, # Führerbremsventil Füllstellung
                              "RSR"      :     0, # Richtungschalterstellung R
                              "RS0"      :     1, # Richtungschalterstellung 0
                              "RSM"      :     2, # Richtungschalterstellung M
                              "RSV"      :     3  # Richtungschalterstellung V
                             }
        Anzeigedaten["AnzModus"] = 1 + 0 + 0 + 0 + 256 + 1024 + 0 + 0
    elif "E50.rv.fzg" in Zugverbandsdaten[0]["Fahrzeugdateiname"]:
        Kombischalterwerte = {"FSAUS"    :     0, # Fahrschalterstellung Schnellaus
                              "FSAB"     :     1, # Fahrschalterstellung Ab
                              "FSFAHRT"  :     2, # Fahrschalterstellung Fahrt
                              "FSAUF"    :     3, # Fahrschalterstellung Auf
                              "FSFZMIN"  :     4, # Fahrschalterstellung kleinste Zugkraftvorgabe
                              "FSFZMAX"  :    11, # Fahrschalterstellung größte Zugkraftvorgabe
                              "Nachlauf" :  True, # Nachlaufsteuerung vorhanden
                              "SW0"      :     1, # Schaltwerksstufe 0
                              "SWMAX"    :    29, # größte Schaltwerksstufe
                              "BSSB"     :     0, # Bremssteller Schnellbremsstellung
                              "BSMAX"    :     1, # Bremssteller größte Bremskraftvorgabe
                              "BSMIN"    :     8, # Bremssteller kleinste Bremskraftvorgabe
                              "BSFahr"   :     9, # Bremssteller Fahrstellung
                              "BSFue"    :    10, # Bremssteller Füllstellung
                              "FbVSB"    :     0, # Führerbremsventil Schnellbremsstellung
                              "FbV35"    :     1, # Führerbremsventil Regelstellung 3,5 bar
                              "FbV47"    :     6, # Führerbremsventil Regelstellung 4,7 bar
                              "FbVFahr"  :     8, # Führerbremsventil Fahrstellung
                              "FbVFue"   :     9, # Führerbremsventil Füllstellung
                              "RSR"      :     0, # Richtungschalterstellung R
                              "RS0"      :     1, # Richtungschalterstellung 0
                              "RSM"      :     2, # Richtungschalterstellung M
                              "RSV"      :     3  # Richtungschalterstellung V
                             }
        Anzeigedaten["AnzModus"] = 1 + 2 + 0 + 0 + 256 + 1024 + 0 + 0
    elif "151.rv.fzg" in Zugverbandsdaten[0]["Fahrzeugdateiname"]:
        Kombischalterwerte = {"FSAUS"    :     0, # Fahrschalterstellung Schnellaus
                              "FSAB"     :     1, # Fahrschalterstellung Ab
                              "FSFAHRT"  :     2, # Fahrschalterstellung Fahrt
                              "FSAUF"    :     3, # Fahrschalterstellung Auf
                              "FSFZMIN"  :     4, # Fahrschalterstellung kleinste Zugkraftvorgabe
                              "FSFZMAX"  :    11, # Fahrschalterstellung größte Zugkraftvorgabe
                              "Nachlauf" :  True, # Nachlaufsteuerung vorhanden
                              "SW0"      :     1, # Schaltwerksstufe 0
                              "SWMAX"    :    29, # größte Schaltwerksstufe
                              "BSSB"     :     0, # Bremssteller Schnellbremsstellung
                              "BSMAX"    :     1, # Bremssteller größte Bremskraftvorgabe
                              "BSMIN"    :     8, # Bremssteller kleinste Bremskraftvorgabe
                              "BSFahr"   :     9, # Bremssteller Fahrstellung
                              "BSFue"    :    10, # Bremssteller Füllstellung
                              "FbVSB"    :     0, # Führerbremsventil Schnellbremsstellung
                              "FbV35"    :     1, # Führerbremsventil Regelstellung 3,5 bar
                              "FbV47"    :     6, # Führerbremsventil Regelstellung 4,7 bar
                              "FbVFahr"  :     8, # Führerbremsventil Fahrstellung
                              "FbVFue"   :     9, # Führerbremsventil Füllstellung
                              "RSR"      :     0, # Richtungschalterstellung R
                              "RS0"      :     1, # Richtungschalterstellung 0
                              "RSM"      :     2, # Richtungschalterstellung M
                              "RSV"      :     3  # Richtungschalterstellung V
                             }
        Anzeigedaten["AnzModus"] = 1 + 4 + 8 + 128 + 256 + 1024 + 0 + 0
    elif "215.rv.fzg" in Zugverbandsdaten[0]["Fahrzeugdateiname"]:
        Kombischalterwerte = {"FSAUS"    :     0, # Fahrschalterstellung Schnellaus
                              "FSAB"     :     1, # Fahrschalterstellung Ab
                              "FSFAHRT"  :     2, # Fahrschalterstellung Fahrt
                              "FSAUF"    :     3, # Fahrschalterstellung Auf
                              "FSFZMIN"  :     4, # Fahrschalterstellung kleinste Zugkraftvorgabe
                              "FSFZMAX"  :    11, # Fahrschalterstellung größte Zugkraftvorgabe
                              "Nachlauf" :  True, # Nachlaufsteuerung vorhanden
                              "SW0"      :     0, # Schaltwerksstufe 0
                              "SWMAX"    :    15, # größte Schaltwerksstufe
                              "BSSB"     :     0, # Bremssteller Schnellbremsstellung
                              "BSMAX"    :     1, # Bremssteller größte Bremskraftvorgabe
                              "BSMIN"    :     8, # Bremssteller kleinste Bremskraftvorgabe
                              "BSFahr"   :     9, # Bremssteller Fahrstellung
                              "BSFue"    :    10, # Bremssteller Füllstellung
                              "FbVSB"    :     0, # Führerbremsventil Schnellbremsstellung
                              "FbV35"    :     1, # Führerbremsventil Regelstellung 3,5 bar
                              "FbV47"    :     9, # Führerbremsventil Regelstellung 4,7 bar
                              "FbVFahr"  :    11, # Führerbremsventil Fahrstellung
                              "FbVFue"   :    12, # Führerbremsventil Füllstellung
                              "RSR"      :     0, # Richtungschalterstellung R
                              "RS0"      :     1, # Richtungschalterstellung 0
                              "RSM"      :     1, # Richtungschalterstellung M
                              "RSV"      :     2, # Richtungschalterstellung V
                             }
        Anzeigedaten["AnzModus"] = 0 + 0 + 0 + 0 + 512 + 0 + 2048 + 0
    elif "ETA150.rv.fzg" in Zugverbandsdaten[0]["Fahrzeugdateiname"] or "ESA150.rv.fzg" in Zugverbandsdaten[0]["Fahrzeugdateiname"]:
        Kombischalterwerte = {"FSAUS"    :     0, # Fahrschalterstellung Schnellaus
                              "FSAB"     :     0, # Fahrschalterstellung Ab
                              "FSFAHRT"  :     0, # Fahrschalterstellung Fahrt
                              "FSAUF"    :     0, # Fahrschalterstellung Auf
                              "FSFZMIN"  :     1, # Fahrschalterstellung kleinste Zugkraftvorgabe
                              "FSFZMAX"  :     6, # Fahrschalterstellung größte Zugkraftvorgabe
                              "Nachlauf" : False, # Nachlaufsteuerung vorhanden
                              "SW0"      :     0, # Schaltwerksstufe 0
                              "SWMAX"    :    15, # größte Schaltwerksstufe
                              "BSSB"     :     0, # Bremssteller Schnellbremsstellung
                              "BSMAX"    :     1, # Bremssteller größte Bremskraftvorgabe
                              "BSMIN"    :     2, # Bremssteller kleinste Bremskraftvorgabe
                              "BSFahr"   :     4, # Bremssteller Fahrstellung
                              "BSFue"    :     5, # Bremssteller Füllstellung
                              "FbVSB"    :     0, # Führerbremsventil Schnellbremsstellung
                              "FbV35"    :     1, # Führerbremsventil Regelstellung 3,5 bar
                              "FbV47"    :     2, # Führerbremsventil Regelstellung 4,7 bar
                              "FbVFahr"  :     4, # Führerbremsventil Fahrstellung
                              "FbVFue"   :     5, # Führerbremsventil Füllstellung
                              "RSR"      :     0, # Richtungschalterstellung R
                              "RS0"      :     1, # Richtungschalterstellung 0
                              "RSM"      :     1, # Richtungschalterstellung M
                              "RSV"      :     2, # Richtungschalterstellung V
                             }
        Anzeigedaten["AnzModus"] = 0 + 0 + 0 + 0 + 256 + 0 + 0 + 0
    elif "DBpbzfa_765.5.rv.fzg" in Zugverbandsdaten[0]["Fahrzeugdateiname"]:
        Kombischalterwerte = {"FSAUS"    :     0, # Fahrschalterstellung Schnellaus
                              "FSAB"     :     1, # Fahrschalterstellung Ab
                              "FSFAHRT"  :     2, # Fahrschalterstellung Fahrt
                              "FSAUF"    :     3, # Fahrschalterstellung Auf
                              "FSFZMIN"  :     4, # Fahrschalterstellung kleinste Zugkraftvorgabe
                              "FSFZMAX"  :    16, # Fahrschalterstellung größte Zugkraftvorgabe
                              "Nachlauf" : False, # Nachlaufsteuerung vorhanden
                              "SW0"      :     1, # Schaltwerksstufe 0
                              "SWMAX"    :    40, # größte Schaltwerksstufe
                              "BSSB"     :     0, # Bremssteller Schnellbremsstellung
                              "BSMAX"    :     1, # Bremssteller größte Bremskraftvorgabe
                              "BSMIN"    :     8, # Bremssteller kleinste Bremskraftvorgabe
                              "BSFahr"   :     9, # Bremssteller Fahrstellung
                              "BSFue"    :    10, # Bremssteller Füllstellung
                              "FbVSB"    :     0, # Führerbremsventil Schnellbremsstellung
                              "FbV35"    :     1, # Führerbremsventil Regelstellung 3,5 bar
                              "FbV47"    :     8, # Führerbremsventil Regelstellung 4,7 bar
                              "FbVFahr"  :     9, # Führerbremsventil Fahrstellung
                              "FbVFue"   :    10, # Führerbremsventil Füllstellung
                              "RSR"      :     0, # Richtungschalterstellung R
                              "RS0"      :     1, # Richtungschalterstellung 0
                              "RSM"      :     2, # Richtungschalterstellung M
                              "RSV"      :     3  # Richtungschalterstellung V
                             }
        Anzeigedaten["AnzModus"] = 1 + 2 + 16 + 64 + 0 + 0 + 0 + 4096
    else:
        print("Tfz nicht gefunden!")
    return Kombischalterwerte
