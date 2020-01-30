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
from openerp.osv import fields, osv

class punto_cuenta(osv.osv):
    _name = 'punto.cuenta'
    _inherit = ['mail.thread']
    _rec_name = 'nro_control'
    
    def _get_attachment_number(self, cr, uid, ids, fields, args, context=None):
        res = dict.fromkeys(ids, 0)
        for app_id in ids:
            res[app_id] = self.pool['ir.attachment'].search_count(cr, uid, [('res_model', '=', 'punto.cuenta'), ('res_id', '=', app_id)], context=context)
        return res
    
    _columns = {
        'nro_control': fields.char('Numero de Control', size=100, readonly=True),
        'fecha': fields.date('Fecha de Emision',required=True),
        'proposicion_tipo_id':fields.many2one('proposicion_tipo','Categoria'),
        'porciento': fields.integer('Multas equivalente al',required=False),
        'categoria_ids': fields.one2many('relacion.proposicion', 'punto_cuenta_id', 'Campo relacionado'),
        'unidad_origen': fields.char('Unidad de Origen', size=100),
        'proyecto': fields.char('Proyecto', size=300, required=True),
        'objeto': fields.text('Objeto', size=100),
        'monto_numero': fields.integer('Monto en Numero'),
        'monto_letras': fields.char('Monto en letras', size=150),
        'partner_id': fields.many2one('res.partner','Beneficiario'),
        'lapso_ejecucion': fields.char('Lapso de Ejecucion', size=300),
        'nro_contrato': fields.char('Numero de Contrato'),
        'state':fields.selection(
                [('generado','Generado'),
                ('aprobado','Aprobado'),
                ('negado','Negado'),
                ('cancelado','Cancelado'),],'Estatus',
                required=True),
        'active': fields.boolean('Active'),
        'para_dpto_id': fields.many2one('departamento','Para', required=True),
        'de_dpto_id': fields.many2one('departamento','De', required=True),
        'descripcion_objeto': fields.text('Descripcion del Objeto', required=True),
        'justificacion_objeto': fields.text('Justificacion del Objeto', required=True),
        'proposicion': fields.text('Proposicion', required=True),
        'tipo_tramite_id': fields.many2one('tipo_tramite','Tipo de Tramite',  required=True),
        'imputacion_presupuestaria_ids':fields.one2many('imputacion.presupuestaria','partidas_id','Imputacion Presupuestaria'),
        'punto': fields.boolean('punto'),
        #~ 'canon_id':fields.many2one('ip.canon.concesiones', 'Canon'),
        'attachment_number': fields.function(_get_attachment_number, string='Number of Attachments', type="integer"),
    }
 
    _defaults={
    'punto':True,
    'active' :True,
    'monto_letras': 'N/A',
    'lapso_ejecucion': 'N/A',
    'nro_contrato': 'N/A',
    'state':lambda *a:'generado',
    }
    
    def action_get_attachment_tree_view(self, cr, uid, ids, context=None):
        model, action_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'base', 'action_attachment')
        action = self.pool.get(model).read(cr, uid, action_id, context=context)
        action['context'] = {'default_res_model': self._name, 'default_res_id': ids[0]}
        action['domain'] = str(['&', ('res_model', '=', self._name), ('res_id', 'in', ids)])
        return action
    
    def pc_aprobado(self, cr, uid, ids, context=None):
         #~ for i in self.browse(cr,uid,ids,context=context):
            #~ canon_conceciones_obj=self.pool.get('ip.canon.concesiones')
            #~ canon_conceciones_ids=canon_conceciones_obj.search(cr,uid,[('id','=',int(i.canon_id))],context=context)
            #~ canon_conceciones_obj.write(cr, uid, canon_conceciones_ids, {'state': 'aprobado_pc',})
        self.write(cr, uid, ids, {'state': 'aprobado',})
        return True
        
    def pc_negado(self, cr, uid, ids, context=None):
        for i in self.browse(cr,uid,ids,context=context):
            #~ canon_conceciones_obj=self.pool.get('ip.canon.concesiones')
            #~ canon_conceciones_ids=canon_conceciones_obj.search(cr,uid,[('id','=',int(i.canon_id))],context=context)
            #~ canon_conceciones_obj.write(cr, uid, canon_conceciones_ids, {'state': 'aprobado_pc',})
            self.write(cr, uid, ids, {'state': 'negado',})
            return True
        
    def pc_cancelado(self, cr, uid, ids, context=None):
        for i in self.browse(cr,uid,ids,context=context):
            #~ canon_conceciones_obj=self.pool.get('ip.canon.concesiones')
            #~ canon_conceciones_ids=canon_conceciones_obj.search(cr,uid,[('id','=',int(i.canon_id))],context=context)
            #~ canon_conceciones_obj.write(cr, uid, canon_conceciones_ids, {'state': 'aprobado_pc',})
            self.write(cr, uid, ids, {'state': 'cancelado',})
            return True
    
    def generar_contrato_concesiones(self,cr,uid,ids,context=None):
        for i in self.browse(cr,uid,ids,context=context):
            partner_id=i.partner_id
            total=i.monto_numero
            punto_cuenta_id=i.id
        return {
            'name': ('concesiones'),
            'res_model': 'concesiones',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'form,tree',
            'view_type': 'form',
            'limit': 80,
            'context': "{   'default_punto_cuenta_id':%d,\
                            'default_partner_id':%d,\
                            'default_pago_mensual':%f,\
                            'default_control_conc':False,\
                            }" % (punto_cuenta_id,partner_id,total),
        }
    
    def create(self,cr,uid,values,context=None):
        print str(values)
        values.update({
            'nro_control':self.pool.get('ir.sequence').get(cr,uid,'seq.puntocuenta')})
        print str(values)
        return super(punto_cuenta,self).create(cr,uid,values,context=context)
    
class tipo_tramite(osv.osv):
    _name = 'tipo_tramite'
    _rec_name = 'nombre'
    
    _columns = {
        'nombre': fields.char('Tipo de Tramite',size=100, required=True),
    }

class concesiones(osv.osv):
    _inherit = 'concesiones'
   
    _columns = {
        'punto_cuenta_id': fields.many2one('punto.cuenta','Punto de Cuenta'),
        #~ 'canon_id': fields.many2one('ip.canon.concesiones', 'Canon' ),
        'control_conc': fields.boolean('control_concesiones'),
    }
    
    _defaults={
        'control_conc':True
    }
    
class departamento(osv.osv):
    _name = 'departamento'
    _rec_name = 'nombre'
    
    _columns = {
        'nombre': fields.char('Nombre del Departamento', size=100, required=True),
    }
    
    
class imputacion_presupuestaria(osv.osv):
    _name = 'imputacion.presupuestaria'
    _rec_name = 'partidas'
    
    _columns = {
        'partidas_id': fields.many2one('punto.cuenta','Partidas', required=True),
        'denominacion': fields.char('Denominacion',required=True),
        'partidas': fields.char('Partidas',required=True),
        'disponibilidad_anterior': fields.integer('Disponibilidad Anterior BsF', required=True),
        'monto_imputar': fields.integer('Monto Imputar', required=True),
        'disponibilidad_actual': fields.integer('Disponibilidad Actual BsF', required=True),
    }
    
    _defaults={
        'partidas': 'N/A',
        'denominacion': 'N/A',
        'disponibilidad_anterior': '0',
        'monto_imputar': '0',
        'disponibilidad_actual': '0',
    }

class relacion_proposicion(osv.osv):
    _name = 'relacion.proposicion'
    _rec_name = 'punto_cuenta_id'
    
    def funcion_monto_multa(self, cr, uid, ids, field_name, arg, contex=None):
        res={}
        for r in self.browse(cr, uid, ids):
            resultado= float(r.porciento)/100
            resultado2=float(r.monto)*float(resultado)
            res[r.id]=resultado2
        return res
            
    _columns = {
        'punto_cuenta_id':fields.many2one('punto.cuenta','Padre de Categoria'),
        'proposicion_tipo_id':fields.many2one('proposicion_tipo','Categoria'),
        'proposicion_sub_tipo_id':fields.many2one('proposicion_sub_tipo','Sub Categoria'),
        'monto': fields.integer('Monto UT',required=True),
        'porciento': fields.integer('Multas equivalente al',required=False),
        'embarcacion': fields.function(funcion_monto_multa,'Multa de Dueños de Embarcacion', type='float', readonly=True),
        'marinas_estacionamiento': fields.function(funcion_monto_multa,'Multa de Marinas y Estacionamientos', type='float', readonly=True),
    }
    def monto_multa(self, cr, uid, ids, monto, porciento, context=None):
        res={}
        if (porciento>0):
            resultado= float(porciento) /100
            resultado2= float(monto) *float(resultado)
            res['embarcacion'] = resultado2
            res['marinas_estacionamiento'] = resultado2
            return {'value': res}
           
            
    
    
class proposicion_tipo(osv.osv):
    _name='proposicion_tipo'
    _rec_name = 'nombre'
    
    _columns = {
        'nombre': fields.char('Categoria del Padre', size=100, required=True),
    }
    
    
class proposicion_sub_tipo(osv.osv):
    _name='proposicion_sub_tipo'
    _rec_name = 'nombre'
    
    _columns = {
        'nombre': fields.char('Sub Categoria',  size=100, required=True),
        'proposicion_tipo_id':fields.many2one('proposicion_tipo','Padre de Categoria'),
    }
    
    
