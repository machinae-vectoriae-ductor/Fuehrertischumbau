#!/usr/bin/python3
# -*- coding] = utf-8 -*-

"""
Dieser Quellcode ist in Python 3 geschrieben und enthält Textfunktionen für
die Führertischhardware.

This source code is written in Python 3 and contains test functions
for the drivers desk hardware.

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
(a software for communication with the simulation
Zusi2).

Wolfgang Evers
Versionsdatum 05.12.2021

"""

def AusgabeReset(Anzeigedaten):
    Anzeigedaten["Vist"] = 0.0
    Anzeigedaten["Fzb"] = 0.0
    Anzeigedaten["Fzba"] = 0.0
    Anzeigedaten["Fzbsoll"] = 0.0
    Anzeigedaten["Fzbasoll"] = 0.0
    Anzeigedaten["LMSchleudern"] = False
    Anzeigedaten["LMGleiten"] = False
    Anzeigedaten["LMHS"] = False
    Anzeigedaten["LMZS"] = False
    Anzeigedaten["LMEB"] = False
    Anzeigedaten["LMHAB"] = False
    Anzeigedaten["LMNBrems"] = False
    Anzeigedaten["LMSifa"] = False
    Anzeigedaten["LMTuer"] = 0
    Anzeigedaten["FSt"] = 0
    Anzeigedaten["LM85"] = 0
    Anzeigedaten["LM70"] = 0
    Anzeigedaten["LM55"] = 0
    Anzeigedaten["LM1000Hz"] = 0
    Anzeigedaten["LM500Hz"] = 0
    Anzeigedaten["LMB40"] = 0
    Anzeigedaten["LMH"] = 0
    Anzeigedaten["LMG"] = 0
    Anzeigedaten["LME40"] = 0
    Anzeigedaten["LMEL"] = 0
    Anzeigedaten["LMEnde"] = 0
    Anzeigedaten["LMV40"] = 0
    Anzeigedaten["LMB"] = 0
    Anzeigedaten["LMS"] = 0
    Anzeigedaten["LMUe"] = 0
    Anzeigedaten["LMStoer"] = 0
    Anzeigedaten["HupePZB"] = 0
    Anzeigedaten["SchnarreLZB"] = 0
    Anzeigedaten["HupeSifa"] = 0
    Anzeigedaten["AFBVsoll"] = 0.0
    Anzeigedaten["LZBVsoll"] = 0.0
    Anzeigedaten["LZBVziel"] = 0.0
    Anzeigedaten["LZBSziel"] = 0.0
    Anzeigedaten["LZBZeig"] = False
    Anzeigedaten["ZDK"] = False
    Anzeigedaten["Uol"] = 0.0
    Anzeigedaten["Iol"] = 0.0
    Anzeigedaten["DruckHB"] = 0.0
    Anzeigedaten["DruckHL"] = 0.0
    Anzeigedaten["DruckZ"] = 0.0
    Anzeigedaten["DruckC"] = 0.0
    return None

