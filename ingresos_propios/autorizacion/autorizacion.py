#~ # -*- coding: utf-8 -*-
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
from datetime import datetime, date, time, timedelta
from dateutil.relativedelta import *
import time
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp





class acount_invoice(osv.osv):
    _inherit='account.invoice'

    _columns={
           
        'isautorizacion':fields.boolean('Autorizacion'),
        }
        

class autorizacion(osv.osv):
    
    _name="autorizacion"
    _inherits={'product.template':'product_id'}
    _description='Registro de Autorizacion'
    

    def get_default_autorizacion(self, cr, uid,fields,context=None):
        account_config_obj=self.pool.get('account.config.settings')
        res = account_config_obj.get_default_ut(cr, uid,fields)
        return res['unidad_tributaria']
        
    
    def function_calculo_pago(self,cr,uid,ids,field_name,arg,context=None):
        res={}
        for r in self.browse(cr,uid,ids):
            res[r.id]=r.unidad_tributaria_mensual*r.valor_unidad_tributaria
        return res

    def acount_tax_exento(self,cr,uid,context=None):
        
        tax_obj=self.pool.get('account.tax')
        tax_id=tax_obj.search(cr, uid, [('name','=','Exento')])
        return [[6,0,[tax_id[0]]]]
        
    def verificar_pago(self,cr,uid,ids,field_name,arg,context=None):
        res={}
        records=self.browse(cr,uid,ids)
        account_invoice_obj=self.pool.get('account.invoice')
        for r in records:
            if not r.state=='paid':
                if r.invoice_id:
                    for account_invoice in account_invoice_obj.browse(cr,uid,[r.invoice_id]):
                        if account_invoice.state=='paid':
                            self.write(cr, uid, ids, {'state':'paid'},context=context)
                            res[r.id]=1
        return res
    
   
    _columns={
        'product_id':fields.many2one('product.template', 'Producto', help="Generacion automatica del numero de la Autorizacion"),
        'partner_id':fields.many2one('res.partner', 'Personas/Empresa', help="Seleccione una Empresa"),
        'tipo_actividad_id':fields.many2one('tipo_actividad', 'Tipo Actividad',help="Seleccione el tipo de actividad a realizar"),
        'parque_id':fields.many2one('registro_parque', 'Parque Monumento',help="Seleccione el parque o monumento donde desea realiza la actividad"),
        'valor_unidad_tributaria':fields.float('Valor Unidad Tributaria', help="Valor de la Unidad Tributaria actual", readonly=True),
        'unidad_tributaria_mensual':fields.float('Cantidad Unidad Tributaria', help="Cantidad de unidades tributarias a cancelar"),
        'pago_mens':fields.function(function_calculo_pago ,'Total a Cancelar Mensual en BsF.', type='float', readonly=True, help='Pago Mensual....'),
        'fecha_inicio':fields.datetime('Fecha Inicial', help="Fecha de inicio de la autorizacion"),
        'fecha_fin':fields.datetime('Fecha Final', help="Fecha de final de la autorizacion"),
        'observacion':fields.text('Observacion'),
        'state':fields.selection([('draft', 'En Proceso'),('invoiced', 'Facturado'),('paid', 'Pagado')],'Estado', readonly=True),
        'active':fields.boolean('Activo'),
        'invoice_id':fields.integer('Id de la factura',readonly=True,),
        'verificar_pago':fields.function(verificar_pago,int='float',string='Verificar Pago'),
    }
    
     
        
    _defaults = {
    
        'active':True,
        'valor_unidad_tributaria':get_default_autorizacion,
        'state': 'draft',
        'taxes_id':acount_tax_exento,
        #~ 'fecha_inicio': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def validar_fecha_permiso(self,cr,uid,ids,fecha_inicio, fecha_fin):
        if  fecha_inicio:
            fecha,tiempo=fecha_inicio.split(' ')
            a,m,d=fecha.split('-')
            h,mi,seg=tiempo.split(':')
            fecha_inicio = datetime(int(a),int(m),int(d),int(h),int(mi),int(seg))
            fecha,tiempo=fecha_fin.split(' ')
            a,m,d=fecha.split('-')
         
            h,mi,seg=tiempo.split(':')
          
            fecha_fin = datetime(int(a),int(m),int(d),int(h),int(mi),int(seg))
            fecha_permiso=relativedelta(fecha_fin,fecha_inicio)
            print fecha_permiso
            print fecha_permiso
            print fecha_permiso
            print fecha_permiso.hours
            print fecha_permiso
            if (fecha_permiso.days >= 0 and fecha_permiso.days <  16 )and (fecha_permiso.hours >= 0)and (fecha_permiso.seconds >=0):
                print 'Tiempo correcto'
            else: 
                raise osv.except_osv(
                    ('Error!'),
                    (u'La Autorizacion no puede ser otorgada\
                    por un lapso mayor a 15 dias, por favor verifique La Fecha Final\
                    ingresada %s, Gracias!'% (fecha_fin)))
        return True
           

    
    def validar_fecha(self, cr, uid, ids, context=None):
        
        for r in self.browse(cr,uid,ids):
            fecha,tiempo=r.fecha_inicio.split(' ')
            a,m,d=fecha.split('-')
            h,mi,seg=tiempo.split(':')
            fecha_inicio = datetime(int(a),int(m),int(d),int(h),int(mi),int(seg))
            fecha,tiempo=r.fecha_fin.split(' ')
            a,m,d=fecha.split('-')
            h,mi,seg=tiempo.split(':')
            fecha_fin = datetime(int(a),int(m),int(d),int(h),int(mi),int(seg))
            fecha_permiso=relativedelta(fecha_fin,fecha_inicio)
            if (fecha_permiso.days >= 0 and fecha_permiso.days <  16 )and (fecha_permiso.hours >= 0)and (fecha_permiso.seconds >= 0):
                
                print 'Tiempo correcto'
            else: 
                raise osv.except_osv(
                    ('Error!'),
                    (u'Revise bien que La Fecha Final %s no puede\
                     ser mayor a la fecha Inicial\
                      %s'% (fecha_fin,fecha_inicio))) 
        
        return True

    
    _constraints = [
        (validar_fecha, ' ', ['fecha_inicio', 'fecha_fin']), 
    ]
    
    
    def calculo(self,cr,uid,ids,unidad_tributaria_mensual,valor_unidad_tributaria,context=None):
        res={}
        if unidad_tributaria_mensual > 0:
            resultado=valor_unidad_tributaria*unidad_tributaria_mensual
            res={'pago_mens':resultado}
        return {'value': res}
        
 
    def pagar_autorizacion(self, cr, uid, ids,context=None):
        hoy=date.today()
        account_config_obj=self.pool.get('account.config.settings')
        #account_config_obj se instancia un objeto de la clase account.config.settings
        unidad_tributaria = account_config_obj.get_default_ut(cr, uid,fields)
        #~ se creo una variable llamada unidad_tributaria se le asigno el valor actual de la unidad tributaria a partir del objeto instanciado anteriormente
        #~ account_config_obj.get_default_ut(cr, uid,fields) se accedio al metodo que obtiene el valor unidad tributaria
        acount_line_obj=self.pool.get('account.invoice.line')
        #~ acount_line_obj se instancia un objeto de la clase account.invoice.line
        account_invoice_obj=self.pool.get('account.invoice')
        #~ account_invoice_obj se instancia un objeto de la clase account.invoice
        account_obj=self.pool.get('account.account')
        #~ account_obj se instancia un objeto de la clase account.account
        account_ids=account_obj.search(cr, 
                                        uid, 
                                        [('code','=',1122001),
                                         ('name','=','CUENTAS POR COBRAR CLIENTES'),
                                        ])
        #~ account_ids con el account_obj.search obtengo los ids segun el rango especificado en la busqueda o search[('code','=',1122001)])
        account_data=account_obj.browse(cr,uid,account_ids, context=context)
        #~ se creo una variable llamada account_data se le asignó los ids obtenidos en account_ids
        autorizacion_data=self.browse(cr,uid,ids, context=context)
        print 'autorizacion_data'
        print autorizacion_data
        print autorizacion_data
        print 'hola mundo1'
        print 'hola mundo1'
        for t in autorizacion_data:
            
            print t.partner_id
            print t.partner_id
            print t.partner_id
            print t.partner_id
            print t.partner_id
            print 'hola mundo2'
            print 'hola mundo2'
            tax=t['taxes_id']
            #~ print tax
            #~ print t
            acount_invoice_vals=[]
            acount_line_vals=[]
            acount_invoice_vals={
                'name':t['name'],
                'reference':t['name'],
                'account_id':account_data.id,
                'partner_id':t.partner_id.id,
                'date_due':hoy,
                'user_id':uid,
                'amount_total':unidad_tributaria['unidad_tributaria']*t['unidad_tributaria_mensual'],
                'amount_untaxed':unidad_tributaria['unidad_tributaria']*t['unidad_tributaria_mensual'],
                'isautorizacion':True,
                }
            print 'hola mundo3'
            # Realizamos un search para obtener los ids con las condiciones dadas dentro del mismo
            account_line_ids=account_obj.search(cr, 
                                        uid, 
                                        [('code', '=',5111002),
                                         ('name','=','VENTAS NACIONALES AL DETAL'),
                                        ])
            # Realizamos un browse para obtener los valores del search antes realizado
            account_line_data=account_obj.browse(cr,uid,account_line_ids, context=context)
            # Aqui Adicionamos la variable que contendra los valores de account invoiced line
            acount_line_vals.append(list((0,False,{
                'uos_id': 1, 
                'account_id': account_line_data.id, 
                'price_unit': unidad_tributaria['unidad_tributaria']*t['unidad_tributaria_mensual'], 
                'invoice_line_tax_id': [[6, False, [tax.id]]], 
                'product_id': t.product_id and t.product_id.id, 
                'name': t['name'], 
                'account_analytic_id': False, 
                })))
            print 'hola mundo4'
            # Aqui actualizamos los valores que trae esta variable y le pasamos en el atributo invoice_line los valores adicionados 
            acount_invoice_vals.update({'invoice_line': acount_line_vals})
            # Mediante esta variable que inicializamos al comienzo llamamos al metodo para crear la factura
            invoice_id=account_invoice_obj.create(cr, uid, acount_invoice_vals, context=context)
            print 'hola mundo5'
            account_invoice_obj.signal_workflow(cr, uid, [invoice_id], 'invoice_open')
            print 'hola mundo5'
            print invoice_id
            print invoice_id
            print invoice_id
            print invoice_id
            
            vista_pago=account_invoice_obj.invoice_pay_customer(cr,uid,[invoice_id])
            print vista_pago
            print vista_pago
            print vista_pago
            self.write(cr, uid, ids, {'state':'invoiced','invoice_id':invoice_id},context=context)
            return vista_pago
            
    def pagar_autorizacion_facturada(self, cr, uid, ids, context=None):
        account_invoice_obj=self.pool.get('account.invoice')
        for autorizacion in self.browse(cr, uid, ids, context=context):
                for account_invoice in account_invoice_obj.browse(cr,uid,[autorizacion.invoice_id]):
                    if not account_invoice.state=='paid':
                        vista_pago=account_invoice_obj.invoice_pay_customer(cr,uid,[autorizacion.invoice_id]) 
                        return vista_pago
        return True
            
    def create(self,cr,uid,values,context=None):
        h=self.pool.get('ir.sequence').get(cr,uid,'autorizacion')
        values.update({
            'name':h,
            
            })
        return super(autorizacion,self).create(cr,uid,values,context=context)


        
