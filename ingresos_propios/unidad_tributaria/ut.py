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
from openerp import tools, api
from openerp.osv import fields, osv
class ut(osv.osv):
    """Unidad Tributaria"""
    _name = 'ut'
    _rec_name = 'nombre'
    def calcula_monto(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for o in self.browse(cr, uid, ids, context=context):
            res[o.id] = o.nombre * o.cantidad
        return res
        
    
    _columns = {
    'nombre': fields.float('Valor de la Unidad Tributaria', digits=(3,2), required=True, help='Valor de la Unidad Tributaria'),
    'cantidad': fields.integer('Cantidad', size=10,  help='Valor de la Unidad Tributaria'),
    'monto': fields.function(calcula_monto, string='Monto Equivalente en Bsf', type="char"),
    'campo_activo': fields.boolean('Activo'),
    
    }
    _defaults = {
        'campo_activo':True, 
    }
    def create(self, cr, uid, vals, context=None):
        cr.execute('update ut set campo_activo = False')
        return super(ut, self).create(cr, uid, vals, context=context)
