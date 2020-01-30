# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
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

import datetime
from lxml import etree
import math
import pytz
import urlparse

import openerp
from openerp import tools, api
from openerp.osv import osv, fields
from openerp.osv.expression import get_unaccent_wrapper
from openerp.tools.translate import _



class partner(osv.osv):
    """Registro de laas Personas y Empresas"""
    _name = 'res.partner'
    _inherit="res.partner"
    
    _columns = {
        'marina': fields.boolean('Activo'),
    }
    

class registro_marinas(osv.osv):
    _name = 'conc.registro_marinas'
    _inherits = {'res.partner': 'partner_id'}
    
    
    @api.multi
    def _get_image(self, name, args):
        return dict((p.id, tools.image_get_resized_images(p.image1)) for p in self)

    @api.one
    def _set_image(self, name, value, args):
        return self.write({'image1': tools.image_resize_image_big(value)})

    @api.multi
    def _has_image(self, name, args):
        return dict((p.id, bool(p.image1)) for p in self)
    
    
    _columns = {
        'partner_id':fields.many2one('res.partner', 
                'Registro de la Embarcacion', 
                required=True, 
                ondelete='cascade'
                ),
        'capacidad': fields.char('Capacidad ',
                size=20, 
                required=False, 
                help='Numero de la Embarcación que se va a Registrar'
                ),
        'image1': fields.binary("Image",
            help="This field holds the image used as avatar for this contact, limited to 1024x1024px"),
        'image_medium': fields.function(_get_image, fnct_inv=_set_image,
            string="Medium-sized image", type="binary", multi="_get_image",
            store={
               
                'conc.registro_marinas': (lambda self, cr, uid, ids, c={}: ids, ['image1'], 10),
            },
            help="Medium-sized image of this contact. It is automatically "\
                 "resized as a 128x128px image, with aspect ratio preserved. "\
                 "Use this field in form views or some kanban views."),
        'image_small': fields.function(_get_image, fnct_inv=_set_image,
            string="Small-sized image", type="binary", multi="_get_image",
            store={
                'conc.registro_marinas': (lambda self, cr, uid, ids, c={}: ids, ['image1'], 10),
            },
            help="Small-sized image of this contact. It is automatically "\
                 "resized as a 64x64px image, with aspect ratio preserved. "\
                 "Use this field anywhere a small image is required."),
        'has_image': fields.function(_has_image, type="boolean"),
        'documentos_ids': fields.one2many(
            'documentos_marinas',
            'documentos_marinas_id',
            'Documentos',
            help='Relacion de la Persona Natura o Juridica con los Documentos'
            ),
    }
    _defaults = {
        'marina':True,
        'is_company': True,
    }
    
    
    
    @api.multi
    def onchange_type(self, is_company):
        value = {'title': False}
        print value
        if is_company:
            value['use_parent_address'] = False
            domain = {'title': [('domain', '=', 'partner')]}
        else:
            domain = {'title': [('domain', '=', 'contact')]}
        return {'value': value, 'domain': domain}


    def create(self,cr,uid,values,context=None):
        print str(values)
        values.update({
            'image':values['image1']})
        return super(registro_marinas,self).create(cr,uid,values,context=context)
        


class documentos_marinas(osv.osv):
    """Registro de Documentos"""
    _name = 'documentos_marinas'
    _rec_name = 'nombre'
    
    _columns = {
        'documentos_marinas_id': fields.many2one(
                'conc.registro_marinas',
                'Marinas',
                help='Documentos de la Marinas'
                 ),
        'nombre': fields.char(
                'Nombre del Documento',
                size=100,
                required=True,
                help='Nombre que posee el Documento'
                ),
        'descripcion': fields.text(
                'Descripcion',
                help='Descripcion del Documento'
                ),
        'fecha_exp': fields.date(
                'Fecha de Expedicion',
                required=True,
                help='Fecha de Expedicion que posee el Documento'
                ),
        'fecha_venc': fields.date(
                'Fecha de Venciemiento',
                help='Fecha de Vencimiento del Documento '
                ),
    }

