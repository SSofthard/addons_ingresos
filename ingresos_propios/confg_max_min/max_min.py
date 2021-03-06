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
# Generated by the OpenERP plugin for Dia !
from openerp.osv import fields, osv

class max_min(osv.osv):
    _name = 'max_min'

    _columns = {
        'parque_id':fields.many2one('registro_parque','Parque',help='Nombre del Parque o Monumento '),
        'product_ids':fields.one2many('objeto_product_relacion','max_min_id','Relacion',help='Productos  '),
     
    }
    _sql_constraints = [
        ('parque_id_unique','unique(parque_id)',u'El nombre del Parque para Maximos y Minimos Ya esta Registrado\
                                                debe Editar el Registro'),
        
        ]
    
    def _check_maximo_minimo_product(self, cr, uid, ids, context=None):
        productos_ids=[]
        for d in self.browse(cr, uid, ids, context=context):
            for sp in d.product_ids:
                 productos_ids.append(sp.product_id.id)
        for i in productos_ids:
            counts=productos_ids.count(i)
            if counts>1:
                return False
            
        return True
    _constraints = [(_check_maximo_minimo_product, 'El Producto seleccionado ya existe', ['product_ids'])]
            
class objeto_product_relacion(osv.osv):
    _name = 'objeto_product_relacion'
    _rec_name = 'product_id'
    
    _columns = {
        'product_id':fields.many2one('product.template','Producto',help=' Productos del Parque o Monumento '),
        'maximo':fields.char('maximo',size=80,help=' Maximo de Productos '),
        'minimo':fields.char('minimo',size=80,help=' Minimo de Productos'),
        'max_min_id':fields.many2one('max_min',help=' Relacion con la clase maximo_minimo '),
     
    }    
    
     
    
    
