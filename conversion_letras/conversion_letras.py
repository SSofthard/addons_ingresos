#!/usr/bin/python
# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Business Applications
#    Copyright (C) 2004-2012 OpenERP S.A. (<http://openerp.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv
"""
    Módulo numerals para convertir un número en una cadena literal del número.
    Autor: Chema Cortés - Agosto 1995 (Convertido de clipper a python en
    Septiembre 2001)
    Modificaciones: Infoprimo - Marcelo Zunino (marcelo@infoprimo.com)

    A sugerencia de su autor original, este código está bajo dominio público.
"""

# las constantes permanecen globales para reducir el costo de la recursión.
_n1 = ( "un","dos","tres","cuatro","cinco","seis","siete","ocho",
        "nueve","diez","once","doce","trece","catorce","quince",
        "dieciséis","diecisiete","dieciocho","diecinueve","veinte")

_n11 =( "un","dós","trés","cuatro","cinco","séis","siete","ocho","nueve")

_n2 = ( "dieci","veinti","treinta","cuarenta","cincuenta","sesenta",
        "setenta","ochenta","noventa")

_n3 = ( "ciento","dosc","tresc","cuatroc","quin","seisc",
        "setec","ochoc","novec")


class EnLetras(osv.osv):
    
    _name="numerosletras"

    '''
    Ejemplo de uso:

        >>> execfile('/path/al/archivo/num2cad.py')      - [ó import num2cad]
        >>> cadena = num2cad.EnLetras('3761.09')
        >>> cadena.largo
        46
        >>> cadena.numero
        '7361.09'
        >>> cadena.escribir
        'SIETE MIL TRESCIENTOS SESENTA Y UNO CON NUEVE.'


    -----------------------------------------------------------


    Demo:
            descomentar "def __main__()" al final de este archivo
            y ejecutar "$ python num2cad.py  <Número a convertir>"


    '''

    def convertir(self,num):


        try:
            tmp = '%.2f' % float(num)
            ent = tmp.split(".")[0]
            fra = tmp.split(".")[1]

            enteros = self.numerals(int(ent))
            decimas = self.numerals(int(fra))

            # print "enteros: ", enteros, "decimas :", decimas

            if enteros == 'cero' and decimas != 'cero' :
                letras = " son centavillos, no merece un pagaré "
            else:
                if decimas == 'cero':
                    letras = enteros.upper() + "."
                else:
                    letras = enteros.upper() + " CON "+ decimas.upper() + "."
        except:
            letras = "acá hay algo que no me gusta..."

        self.numero = str(num)
        self.largo  = len(letras)
        self.escribir = letras
        return self.escribir


    def numerals(self, nNumero):
        """
        numerals(nNumero) --> cLiteral

        Convierte el número a una cadena literal de caracteres
        P.e.:       201     -->   "doscientos uno"
                   1111     -->   "mil ciento once"

        """


        # función recursiva auxiliar esta es "la" rutina ;)
        def _numerals(n):

            # Localizar los billones
            prim,resto = divmod(n,10L**12)
            if prim!=0:
                if prim==1:
                    cRes = "un billón"
                else:
                    cRes = _numerals(prim)+" billones" # Billones es masculino
                if resto!=0:
                    cRes += " "+_numerals(resto)
            else:
            # Localizar millones
                prim,resto = divmod(n,10**6)
                if prim!=0:
                    if prim==1:
                        cRes = "un millón"
                    else:
                        cRes = _numerals(prim)+" millones" # Millones es masculino
                    if resto!=0:
                        cRes += " " + _numerals(resto)
                else:
            # Localizar los miles
                    prim,resto = divmod(n,10**3)
                    if prim!=0:
                        if prim==1:
                            cRes="mil"
                        else:
                            cRes=_numerals(prim)+" mil"
                        if resto!=0:
                            cRes += " " + _numerals(resto)
                    else:
            # Localizar los cientos
                        prim,resto=divmod(n,100)
                        if prim!=0:
                            if prim==1:
                                if resto==0:
                                    cRes="cien"
                                else:
                                    cRes="ciento"
                            else:
                                cRes=_n3[prim-1]
                                cRes+="ientos"
                            if resto!=0:
                                cRes+=" "+_numerals(resto)
                        else:
            # Localizar las decenas
                            if n<=20:
                                cRes=_n1[n-1]
                            else:
                                prim,resto=divmod(n,10)
                                cRes=_n2[prim-1]
                                if resto!=0:
                                    if prim==2:
                                        cRes+=_n11[resto-1]
                                    else:
                                        cRes+=" y "+_n1[resto-1]
            return cRes

        # Nos aseguramos del tipo de <nNumero>
        # se podría adaptar para usar otros tipos (pe: float)
        nNumero = long(nNumero)
        if nNumero < 0:
            # negativos
            cRes = "menos "+_numerals(-nNumero)
        elif nNumero == 0:
            # cero
            cRes = "cero"
        else:
            # positivo
            cRes = _numerals(nNumero)

        # Excepciones a considerar
        if nNumero % 10 == 1 and nNumero % 100 != 11:
            cRes += "o"
        return cRes

# ----------------------------------------
# Lo que sigue se puede eliminar.
# Para usar como módulo "import num2cad"


#~ def __main__():
    #~ import sys
#~ 
    #~ valor =22555379
    #~ if len(sys.argv) == 2:
        #~ valor = sys.argv[1]
#~ 
    #~ cadena = EnLetras(valor)
    #~ print "Largo: ", cadena.largo
    #~ print "Numero a escribir: ", cadena.numero
    #~ print "Son : ", cadena.escribir
#~ 
#~ if __name__ == "__main__" :
    #~ __main__()
