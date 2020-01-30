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
from datetime import datetime, date, time, timedelta
from dateutil.relativedelta import *

class product_product(osv.Model):
    _inherit = "product.product"
    _columns = {
        'isetiqueta':fields.boolean('Is Etiquela'),
    }
    
class etiqueta(osv.osv):
    _name="etiquetas"
    _inherits = {'product.product': 'product_id'}
    
    #~ Calcular la cantidad de correlativos por Etiquetas
    def cantidad_etiquetas(self, cr, uid, ids, name, arg, context=None):
        res = dict(map(lambda x: (x,0), ids))
        
        correlativo_generar_obj=self.pool.get('ip.correlativo.generar')
        correlativo_boleto_obj=self.pool.get('ip.correlativo.etiquetas')
    
        
        for etiqueta in self.browse(cr, uid, ids, context=context):
            etiquetas_ids=correlativo_boleto_obj.search(cr, uid,[('etiqueta_id', '=', etiqueta.id)],context=context)
            for correlativo_boleto in correlativo_boleto_obj.browse(cr, uid, etiquetas_ids, context=context):
                res[etiqueta.id]=res[etiqueta.id]+len(correlativo_generar_obj.search(cr, uid,[('state', '=', 'generado'),('etiqueta_id','=',correlativo_boleto.id)],context=context))
        return res
    
    #~ Calcular el precio de venta de la Etiqueta
    def funcion_cal_precio_venta(self,cr,uid,ids,field_name,arg,context=None):
            res={}
            for r in self.browse(cr,uid,ids):
                res[r.id]=r.unidad_tributaria*r.cant_unid_tribut
            return res
        
        
    #~ Metodo para mostrar la Unidad Tributaria por defecto en la Vista
    def unidad_tributaria(self,cr,uid,ids,context=None):
        account_config_obj=self.pool.get('account.config.settings')
        res=account_config_obj.get_default_ut(cr,uid,fields)
        return res['unidad_tributaria']
        
    #~ Establecer por defecto el Año actual, al año anterior y el año posterior
    def _get_selection(self, cursor, user_id, context=None):
        format="%Y"
        hoy=date.today()
        ant=hoy+relativedelta(years=-1)
        prox=hoy+relativedelta(years=+1)
        ant=ant.strftime(format)
        hoy=hoy.strftime(format)
        prox=prox.strftime(format)
        return (
            (ant,ant),
            (hoy,hoy),
            (prox,prox))
            
      
    _columns = {
        'color': fields.integer('Color Index'),
        'product_id': fields.many2one(
                'product.product',
                'Product_id',
                required=True,
                ondelete='cascade'),
        'cant_unid_tribut':fields.float(
                'Cantidad Unidad Tributaria',
                required=True,),
        'unidad_tributaria':fields.float('Unidad Tributaria',required=True,readonly=True,help='Ingreso de la Cantidad de Unidad Tributaria'),
        
        'ano':fields.selection(_get_selection,'Año', required = True),
        'precio_venta': fields.function(
                            funcion_cal_precio_venta, 
                            'Precio Venta', store=True,
                            type='float'), 
        'tipo_embarcacion_id':fields.many2one(
                'conc.tipo_embarcacion',
                'Tipo de Embarcacion'),
        'cant_generados':fields.function(cantidad_etiquetas, 'Correlativos Generados',type='integer',)
    }
    
    _defaults = {
        'isetiqueta': True,
        'unidad_tributaria':unidad_tributaria
    }
    
    
    #~ Establecer el nombre y año de la etiqueta únicos.
    def buscar_datos(self, cr, uid, ids, context=None):
        for d in self.browse(cr,uid,ids):
            product_ids = self.search(cr, uid, [('name_template', '=', d.name_template), ('ano', '=', d.ano)], context=context)
            if len(product_ids)==1:
                return True
    _constraints = [
        (buscar_datos, 'Error! No puedes crear etiquetas con el mismo nombre y el mismo año ', ['ano'])
    ]
    
    
    
    #~ Calcular el precio de venta de la Etiqueta
    def cal_precio_venta(self,cr,uid,ids,unidad_tributaria,cant_unid_tribut,context=None):
        dic={}
        if (cant_unid_tribut>0):
            res = float(unidad_tributaria)*float(cant_unid_tribut)
            dic['precio_venta']=res
            dic['lst_price']=res
            return {
                'value':dic,
                }
            
    def create(self,cr,uid,vals,context=None):
        vals.update({
                'name':vals['name'].upper()
                })
        return super(etiqueta, self).create(cr, uid, vals, context=context)


class etiqueta_color(osv.osv):
    _name="etiqueta.color"
    
    _columns = {
        'color': fields.char('Color de la Etiqueta',size=80,required=True,help='Este es el Color de la Etiqueta'),
        'num_hexa':fields.integer('Numero en Exadecimal',
        size=20,required=True,help='Numero en Exadecimal'),
    }
    
    _defaults = {
        'name': 1,
    }    


    
    
    
 
