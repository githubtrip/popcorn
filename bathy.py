#!/usr/bin/python
# -*- coding: utf8 -*-
# 11 mars 2015 - Tristan Le Toullec  
#
#This file is part of AP2V.
#
#    AP2V is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    AP2V is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with AP2V.  If not, see <http://www.gnu.org/licenses/>.
#
# Ce fichier gere la lecture de fichier de bathymetrie

from Scientific.IO.NetCDF import *

class etopo2(object):
    """Class pour la creation d'un objet bathymetrique avec les donnees ETOPO2 V2G"""

    def __init__(self, filename):
        """Method docstring."""
        # Ouverture du fichier en read-only
        self.file = filename
        self.nc = NetCDFFile(filename,'r')
        # Recuperation des valeurs x>long y>lat et z>level dans des tableaux
        longitude = self.nc.variables['x']
        latitude = self.nc.variables['y']
        level = self.nc.variables['z']
        self.longitudeVar = longitude[:]
        self.latitudeVar = latitude[:]
        self.levelVar = level[:]

        # Calcul du nombre de point par latitude et par longitude
        self.defLatitude = len(self.latitudeVar) / 180
        self.defLongitude = len(self.longitudeVar) / 360

    def about(self):
        """Informations sur la bathymetrie"""
        print("Variables presentes dans le fichier : ", self.nc.variables)
        print("etopo2 - Def en latitude (par deg)", self.defLatitude)
        print("etopo2 - Def en longitude", self.defLongitude)

        
    def getLevel(self, lat, long):
        """Recupere le level selon latitude et longitude"""
        # Verification parametres
        if not ( -90 <= lat <= 90 ) or not ( -180 <= long <= 180 ):
            print('\n!!! Parameters error - lat must be -90>90 and long must be -180>180')
            return 0
        # Le premier indice d'ETOPO 2 commence a -90,-180, donc l'indice 0,0 corresponde au level de -90,-180
        # Il faut donc relever les donnees vers une echelle 0->180 (pour la lat) et multiplier par la definition en lat
        indicelat = int( (lat + 90) * self.defLatitude )
        indicelong = int ( (long + 180) * self.defLongitude )
        # Puis lire le level correspondant aux indices 
        return self.levelVar[indicelat,indicelong]
 
class fake(object):
    """Class pour la creation d'un objet bathymetrique de test"""

    def __init__(self):
        """Method docstring."""
        print("!!! Warning Using fake bathymetrics data")
               
    def getLevel(self, lat, long):
        if -5 < lat < 5 and -5 < long < 5:
            return 16000
        else:
            return 0
        
#Test du script
if __name__ == '__main__':
    print("Test Module Bathy")
    bathymetrie = etopo2("etopo2.nc")
    bathymetrie.about()
    lat,long = 48.2301, -4.3015
    print("Brest - lat->",lat," long->",long," level->",bathymetrie.getLevel(lat, long))
    lat,long = 46.1544, -2.5523
    print("Plateau GDC - lat->",lat," long->",long," level->",bathymetrie.getLevel(lat, long))
    lat,long = -35.2609, 20.0045
    print("Plateau Cap Town - lat->",lat," long->",long," level->",bathymetrie.getLevel(lat, long))
    lat,long = -8.4044, -165.1133
    print("Milieux pacifique - lat->",lat," long->",long," level->",bathymetrie.getLevel(lat, long))
    lat,long = 94, 0
    print("Bad parameters - lat->",lat," long->",long," level->",bathymetrie.getLevel(lat, long))