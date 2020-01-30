# -*- coding: utf-8 -*-

from openerp.osv import fields,osv
from datetime import datetime, date, time, timedelta
import json 


class correlativo(osv.osv):
    _name="ip.correlativo.etiquetas"
    _rec_name="etiqueta_id"
    _inherit = ['mail.thread']
    
    def mostrar_ano(self,cr,uid,ids,field_name,arg, context=None):
        res={}
        
        for i in self.browse(cr,uid,ids):
            
            if i.etiqueta_id:
                etiquetas_obj=self.pool.get('etiquetas')
                etiquetas_ids=etiquetas_obj.search(cr,uid,[('id','=',int(i.etiqueta_id))],context=context)
                etiquetas_datos=etiquetas_obj.browse(cr,uid,etiquetas_ids,context=context)
                res[i.id]=etiquetas_datos['ano'],
                for a in res[i.id]:
                    res[i.id]=a
        return res
    
    
        
    _columns = {
        'etiqueta_id':fields.many2one('etiquetas','Tipo de Etiquetas'),
        'cantidad':fields.integer('Cantidad',size=10,required=True,help='Cantidad de boletos a generar'),
        'cantidad_digitos':fields.integer('Cantidad de digitos',size=10,required=True,help='Cantidad de digitos del correlativo'),
        'prefijo':fields.char('Prefijo',size=10,required=True,help='Letra a utilizar como Prefijo'),
        'etiquetas_ids':fields.one2many('ip.correlativo.generar','etiqueta_id','Correlativo'),
        'ano':fields.integer('Año', required = True),
        'ano_2':fields.function(
                        mostrar_ano,
                        'Año',
                        type='char',
                        help='Año de la etiqueta seleccionada'),
        'active': fields.boolean('Activo'),
        'state': fields.selection([
            ('borrador', 'Borrador'),
            ('generados', 'Generados'),
            ('asignado', 'Asignado'),
            ('eliminado', 'Eliminado'),
            ('rendido', 'Rendido'),
            ], 'state', help="Este es es estado actual del boleto."),
        
        }
    _order ='create_date desc, id desc'
    
    _defaults = {
        'cantidad': '',
        'active':True,
        'state':'borrador'
        }
        
        
    def buscar_valores(self,cr,uid,ids,etiqueta_id,context=None):
        res={}
        if etiqueta_id:
            etiquetas_obj=self.pool.get('etiquetas')
            etiquetas_ids=etiquetas_obj.search(cr,uid,[('id','=',int(etiqueta_id))],context=context)
            etiquetas_datos=etiquetas_obj.browse(cr,uid,etiquetas_ids,context=context)
            correlativo_ids=self.search(cr,uid,[('etiqueta_id','=',etiqueta_id)],limit=1,order='id desc',context=context)
            correlativo_datos=self.browse(cr,uid,correlativo_ids,context=context)
            if len(correlativo_ids)==1:
                for i in correlativo_datos:
                    res={
                        'prefijo': i.prefijo,
                        'cantidad_digitos': i.cantidad_digitos,
                        'ano':etiquetas_datos['ano'],
                        'ano_2':etiquetas_datos['ano'],
                    }
            else:
                 res={
                        'prefijo':'',
                        'cantidad_digitos': '',
                        'ano':etiquetas_datos['ano'],
                        'ano_2':etiquetas_datos['ano'],
                    }
        else:
                 res={
                        'prefijo':'',
                        'cantidad_digitos': '',
                        'cantidad': '',
                    }
        return {'value':res}
        
        
    def generar_correlativo(self,cr,uid,ids,etiqueta_id,prefijo,cantidad_digitos,cantidad,context=None):
        now=date.today()
        res={}
        etiqueta=[]
        if etiqueta_id and prefijo and cantidad_digitos:
            correlativo_ids=self.search(cr,uid,[('etiqueta_id','=',etiqueta_id)],limit=1,order='id desc',context=context)
            correlativo_datos=self.browse(cr,uid,correlativo_ids,context=context)
            int (etiqueta_id)
            if len(correlativo_ids)==1:
                cr.execute("select MAX(ipg.correlativo) as correlativo from ip_correlativo_etiquetas as ice inner join ip_correlativo_generar as ipg on ipg.etiqueta_id=ice.id where ice.etiqueta_id=%s and ice.active=TRUE;",(str(etiqueta_id),))
                for i in cr.fetchall():
                    correlativo=i[0]
                if prefijo.upper()==correlativo_datos['prefijo']:
                    p,c=correlativo.split('-')
                    n=int(c)+1
                    while  n <= int(c)+cantidad:
                        etiqueta.append([0,False,{'correlativo' : str(prefijo.upper())+'-'+str(n).rjust(cantidad_digitos,'0'), 'state': 'generado','fecha':now,'etiqueta_id': False,}])
                        n+=1 
                        res={
                            'etiquetas_ids':etiqueta,
                            }
                else:
                     n=1
                while  n <= cantidad:
                    etiqueta.append([0,False,{'correlativo' : str(prefijo.upper())+'-'+str(n).rjust(cantidad_digitos,'0'), 'state': 'generado','fecha':now,'etiqueta_id': False,'etiquetas_id':int(etiqueta_id)}])
                    n+=1 
                res={
                    'etiquetas_ids':etiqueta,
                    }
            else:
                n=1
                while  n <= cantidad:
                    etiqueta.append([0,False,{'correlativo' : str(prefijo.upper())+'-'+str(n).rjust(cantidad_digitos,'0'), 'state': 'generado','fecha':now,'etiqueta_id': False,'etiquetas_id':int(etiqueta_id)}])
                    n+=1 
                res={
                    'etiquetas_ids':etiqueta,
                    }
        else:
            res={
               'prefijo':'',
               'cantidad_digitos':'',
               'cantidad':'',
            }
        return {'value':res}
    
    
    def eliminar_etiqueta(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'active': False,'state':'eliminado'},context=context)
        for i in self.browse(cr,uid,ids):
            correlativos_obj=self.pool.get('ip.correlativo.generar')
            correlativos_ids=correlativos_obj.search(cr,uid,[('etiqueta_id','=',i.id)],context=context)
            correlativos_datos=correlativos_obj.browse(cr,uid,correlativos_ids,context=context)
            correlativos_obj.write(cr, uid, correlativos_ids, {'state': 'eliminado'},context=context)
        return True
    
    
    def create(self,cr,uid,vals,context=None):
        generado_id=self.search(cr,uid,[('etiqueta_id','=',vals['etiqueta_id']),('state','=','borrador')],context=context)
        generado_data=self.browse(cr,uid,generado_id,context=context)
        for dato in generado_data:
            self.write(cr, uid, dato.id, {'state': 'generados'},context=context)
        vals.update({
                'prefijo':vals['prefijo'].upper()
                })
        prefijos_id=self.search(cr,uid,[('etiqueta_id','=',vals['etiqueta_id'])],context=context)
        prefijos=self.browse(cr,uid,prefijos_id,context=context)
        
        prefijo_id=self.search(cr,uid,[('etiqueta_id','=',vals['etiqueta_id'])],limit=1,order='id desc',context=context)
        prefijo=self.browse(cr,uid,prefijo_id,context=context)
        prefijo_list=[]
        if prefijo['prefijo']!=vals['prefijo']:
            for p in prefijos:
                prefijo_list.append(str(p.prefijo))
            prefijos_disp={x:1 for x in prefijo_list}.keys()
            for r in prefijos_disp:
                if r==vals['prefijo'].upper():
                    raise osv.except_osv(
                                ('Error de prefijo'),
                                ('El prefijo ya fue utilizado.'))
        for i in vals['etiquetas_ids']:
            
            for r in i[2]:
                correlativo1 = i[2].values()
            numero=correlativo1[0] 
            p,c=numero.split('-')
            if p != vals['prefijo']:
                raise osv.except_osv(
                                ('Error!'),
                                ('El prefijo no puede ser modificado.'))
            
            if len(c) != vals['cantidad_digitos']:
                raise osv.except_osv(
                                ('Error!'),
                                ('La cantidad de digitos no puede ser modificada.'))
            
            if len(vals['etiquetas_ids']) != vals['cantidad']:
                raise osv.except_osv(
                                ('Error!'),
                                ('La cantidad a generar no puede ser modificada. Verifique la cantidad que desea generar.'))
            
        if vals['cantidad'] <=0:
            raise osv.except_osv(
                                ('Error de Cantidad'),
                                ('La cantidad '+str(vals['cantidad'])+' no puede ser generada.'))
        return super(correlativo, self).create(cr, uid, vals, context=context)
    
    
class generar_correlativo(osv.osv):
    _name="ip.correlativo.generar"
    _rec_name="correlativo"
    _inherit = ['mail.thread']
    
    def verificar_pago(self,cr,uid,ids,field_name,arg,context=None):
        res={}
        records=self.browse(cr,uid,ids)
        account_invoice_obj=self.pool.get('account.invoice')
        for r in records:
            if not r.state=='rendido':
                if r.acccount_invoice_id:
                    for account_invoice in account_invoice_obj.browse(cr,uid,[r.acccount_invoice_id]):
                        if account_invoice.state=='paid':
                            self.write(cr, uid, ids, {'state':'pagado'},context=context)
                            res[r.id]=1
        return res
    
    def embarcacion_mostrar(self,cr,uid,ids,field_name,arg,context=None):
        res={}
        for i in self.browse(cr,uid,ids):
            reg_embarcacion_obj=self.pool.get('conc.registro_embarcaciones')
            reg_embarcacion_ids=reg_embarcacion_obj.search(cr,uid,[('id','=',int(i.matricula_id))],context=context)
            reg_embarcacion_datos=reg_embarcacion_obj.browse(cr,uid,reg_embarcacion_ids,context=context)
            res[i.id]=reg_embarcacion_datos['name'],
            for a in res[i.id]:
                res[i.id]=a    
        return res
        
    _columns = {
        'correlativo':fields.char('Etiqueta',size=100,required=True,help='Numero de Etiqueta'),
        'etiqueta_id':fields.many2one('ip.correlativo.etiquetas','Boletos'),
        'state': fields.selection([
            ('generado', 'Generado'),
            ('asignado', 'Asignado'),
            ('facturado', 'Facturado'),
            ('eliminado', 'Eliminado'),
            ('incidencia', 'Incidencia'),
            ('pagado', 'Pagado'),
            ('val_incidencia', 'Incidencia Validada'),
            ('rendido', 'Rendido'),
            ], 'state', readonly=True, copy=False, help="Este es el estado actual del boleto.", select=True),
        'fecha':fields.date('Fecha de generacion'),
        'parque_id':fields.many2one('registro_parque','Parque'),
        'descripcion':fields.text('Descripcion'),
        'matricula_id':fields.many2one('conc.registro_embarcaciones','Matrícula'),
        'fecha_venta': fields.datetime('Fecha de Venta', required=True, readonly=True, select=True),
        'acccount_invoice_id':fields.integer('Id de la factura',readonly=True,),
        'verificar_pago':fields.function(verificar_pago,int='float',string='Verificar Pago',readonly=True),
        'embarcacion':fields.function(embarcacion_mostrar,
                        'Embarcación',
                        store=True,
                        type='char',
                        help='Embarcación a la que se le vende la Etiqueta'),
    }
    
    _defaults = {
        'state':'generado',
        'fecha_venta': fields.datetime.now,
        }
    
    #~ def buscar_etiqueta(self, cr, uid, ids, context=None):
        #~ for i in self.browse(cr,uid,ids):
           #~ 
            #~ 
            #~ etiquetas_obj=self.pool.get('ip.etiquetas')
            #~ etiquetas_ids=etiquetas_obj.search(cr,uid,[('id','=',int(i.etiqueta_id))],context=context)
            #~ etiquetas_datos=etiquetas_obj.browse(cr,uid,etiquetas_ids,context=context)
            #~ print 'Bolívar'
            #~ print etiquetas_datos
            #~ print etiquetas_datos
            #~ annio_vista=i.etiqueta_id.ano
            #~ print annio_vista
            #~ print 'jj'
            #~ annio_bdatos=etiquetas_datos['ano']
            #~ print annio_bdatos
            #~ correlativo_generar_ids=self.search(cr,uid,[('matricula_id','=',int(i.matricula_id))],context=context)
            #~ if len(correlativo_generar_ids)==1 and annio_bdatos != annio_vista:
                #~ return True
            #~ 
    #~ _constraints = [
        #~ (buscar_etiqueta, 'La Embarcación ya posee etiqueta asiganada por éste año ', ['matricula_id'])
    #~ ]
    
    def mostrar_embarcacion(self, cr, uid, ids, matricula_id, context=None):
        reg_embarcacion_obj=self.pool.get('conc.registro_embarcaciones')
        reg_embarcacion_ids=reg_embarcacion_obj.search(cr,uid,[('id','=',int(matricula_id))],context=context)
        reg_embarcacion_datos=reg_embarcacion_obj.browse(cr,uid,reg_embarcacion_ids,context=context)
        if matricula_id:
            for i in reg_embarcacion_datos:
                res={
                'embarcacion':i.name,
                }
        else:
            res={
            'embarcacion':'',
            }
        return {'value':res}
        
    def incidencia_etiqueta(self, cr, uid, ids, context=None):
        for d in self.browse(cr,uid,ids):
            if d.descripcion:
                self.write(cr, uid, ids,{'state':'incidencia'})
            else:
                raise osv.except_osv(
                                ('Error!'),
                                ('Click en Editar y agregar una descripción para generar una INCIDENCIA.'))
            if d.embarcacion:
                raise osv.except_osv(
                                ('Error!'),
                                ('El campo Embarcación debe estar vacío para generar una INCIDENCIA.'))
        return True
        
    def pagar_etiqueta_facturada(self, cr, uid, ids, context=None):
        account_invoice_obj=self.pool.get('account.invoice')
        for etiqueta in self.browse(cr, uid, ids, context=context):
                for account_invoice in account_invoice_obj.browse(cr,uid,[etiqueta.acccount_invoice_id]):
                    if not account_invoice.state=='paid':
                        vista_pago=account_invoice_obj.invoice_pay_customer(cr,uid,[etiqueta.acccount_invoice_id]) 
                        return vista_pago
        return True
    
    def pagar_etiqueta(self, cr, uid, ids, context=None):
        for e in self.browse(cr, uid, ids):
            if not e.embarcacion:
                raise osv.except_osv(
                                ('Error!'),
                                ('Click en Editar y agregar una Embarcación.'))
        account_invoice_obj=self.pool.get('account.invoice')
        account_line_obj=self.pool.get('account.invoice.line')
        account_obj=self.pool.get('account.account')
        #~ Realizamos un search para obtener los ids con las condiciones dadas dentro del mismo
        account_ids=account_obj.search(cr, 
                                        uid, 
                                        [('code', '=',1122001),
                                         ('name','=','CUENTAS POR COBRAR CLIENTES'),
                                        ])
        #~ a los ids del search le hacemos un browse para obtener los datos especificos de esa busqueda
        account_data=account_obj.browse(cr,uid,account_ids, context=context)
        # Realizamos un search para obtener los ids con las condiciones dadas dentro del mismo
        account_line_ids=account_obj.search(cr, 
                                        uid, 
                                        [('code', '=',5111002),
                                         ('name','=','VENTAS NACIONALES AL DETAL'),
                                        ])
        # Realizamos un browse para obtener los valores del search antes realizado
        account_line_data=account_obj.browse(cr,uid,account_line_ids, context=context)
        
        for r in self.browse(cr, uid, ids, context=context):
            account_invoice_vals=[]
            account_line_vals=[]
            propietario=r.matricula_id.partner_id.child_ids[0].id
            name=r.etiqueta_id.etiqueta_id.product_id.name +'/'+ r.correlativo
            tax= [t.id for t in r.etiqueta_id.etiqueta_id.product_id.taxes_id]
            #~ Aqui Adicionamos la variable que contendra los valores de account invoiced line por cada servicio
            account_line_vals.append(list((0,False,{
                'uos_id':1, 
                'account_id': account_line_data.id, 
                'price_unit': r.etiqueta_id.etiqueta_id.precio_venta, 
                'quantity': 1,
                'invoice_line_tax_id': [[6, False, [tax[0]]]], 
                'product_id': r.etiqueta_id.etiqueta_id.product_id.id, 
                'name': name, 
                'account_analytic_id': False, 
                })))
            #~ Aqui llenamos una variable que contendra los valores de account invoiced
            account_invoice_vals={
            'account_id': account_data.id,
            'parque_id': r.parque_id.id ,
            'partner_id': propietario,
            'date_due': date.today(),
            'user_id': uid,
            'amount_total': r.etiqueta_id.etiqueta_id.precio_venta,
            'amount_untaxed': r.etiqueta_id.etiqueta_id.precio_venta,
            }
        #~ Aqui actualizamos los valores que trae esta variable y le pasamos en el atributo invoice_line los valores adicionados 
        account_invoice_vals.update({'invoice_line': account_line_vals})
        #~ Mediante esta variable que inicializamos al comienzo llamos al metodo para crear la factura
        acccount_invoice_id=account_invoice_obj.create(cr, uid, account_invoice_vals, context=context)
        #~ con esto manipulo el workflow de account invoice para validar la factura 
        account_invoice_obj.signal_workflow(cr, uid, [acccount_invoice_id], 'invoice_open')
        #~ con esto pulso el boton de registrar pago y el por defecto me devuelve la vista de cancelar la 
        #~ factura
        vista_pago=account_invoice_obj.invoice_pay_customer(cr,uid,[acccount_invoice_id])
        self.write(cr, uid, ids, {'state':'facturado','acccount_invoice_id':acccount_invoice_id},context=context)
        return vista_pago
        
    def rendicion_etiqueta(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids,{'state':'rendido'},context=context)
        return True
        
    def validacion_incidencia(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids,{'state':'val_incidencia'},context=context)
        return True
   
    
    
    
    
