# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

from openerp.osv import fields,osv

class product_product(osv.osv):
    _inherit = "product.product"
    _columns = {
        'isetiqueta':fields.boolean('Is Etiquela'),
    }
    
class etiqueta(osv.osv):
    _name="etiquetas"
    _inherits = {'product.product': 'product_id'}
  
    
    _columns = {
        'product_id': fields.many2one('product.product', 'Product_id', required=True, ondelete='cascade'),
        'cant_unid_tribut':fields.float('Cantidad Unidad Tributaria',required=True,help='Ingreso de la Cantidad de Unidad Tributaria'),
        'anio':fields.date('Año',size=6,required=True,help='Ingreso del Año'),
        'precio_venta':fields.float('Precio Venta', help='Total a Pagar'),
    }
    
    _defaults = {
        'isetiqueta': 1,
    }

    


