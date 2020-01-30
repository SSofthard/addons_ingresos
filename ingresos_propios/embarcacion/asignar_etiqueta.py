# -*- coding: utf-8 -*-
from openerp.osv import fields, osv


class asignar_etiqueta(osv.osv):
    _name = 'etiqueta.asignar'
    _rec_name="etiqueta_id"
    
    
    def mostrar_anno(self,cr,uid,ids,field_name,arg, context=None):
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
    
    def mostrar_cantidad(self,cr,uid,ids,field_name,arg, context=None):
        res={}
        for i in self.browse(cr,uid,ids):
            if i.etiqueta_id:
                icg_obj=self.pool.get('ip.correlativo.etiquetas')
                icg_ids=icg_obj.search(cr,uid,[('id','=',int(i.etiqueta_id))],context=context)
                icg_datos=icg_obj.browse(cr,uid,icg_ids,context=context)
                res[i.id]=icg_datos['cantidad'],
                for a in res[i.id]:
                    res[i.id]=a
        return res
        

    
    _columns = {
        'parque_id':fields.many2one(
                    'registro_parque',
                    'Parque',
                    required=True,
                    help='Esta es el parque a asignar el boleto'),
        'desde':fields.char('Primera etiqueta asignada',
                help='Primera etiqueta asignada'),
        'hasta':fields.char('Ultima etiqueta asignada',
                help='Ultima etiqueta asignada'),
        'cantidad': fields.integer('Cantidad',size=10,
                required=True,
                type='char',
                help='Cantidad de Etiquetas a Asignar'),
        'etiqueta_id':fields.many2one('etiquetas',
                'Tipo de Etiqueta'),
        'ano':fields.function(
                        mostrar_anno,
                        'Año',
                        type='char',
                        help='Este es el año de la etiqueta seleccionada'),
        'etiq_disp':fields.function(
                        mostrar_cantidad,
                        'Etiquetas disponibles',
                        type='char',
                        help='Cantidad de etiquetas disponibles que puede asignar!.'),
    }
    
    
    def mostrar_disponible(self,cr,uid,ids,etiqueta_id,context=None):
        res={}
        etiquetas_obj=self.pool.get('etiquetas')
        etiquetas_ids=etiquetas_obj.search(cr,uid,[('id','=',int(etiqueta_id))],context=context)
        etiquetas_datos=etiquetas_obj.browse(cr,uid,etiquetas_ids,context=context)
        if etiqueta_id:
            if len(etiquetas_ids)==1:
                cr.execute("select COUNT(ipg.state) as state from ip_correlativo_etiquetas as ice\
                inner join ip_correlativo_generar as ipg on ipg.etiqueta_id=ice.id\
                where ice.etiqueta_id=%s and ice.active=TRUE and ipg.state='generado';",(str(etiqueta_id),))
                
                for i in cr.fetchall():
                    disponible=i[0]
                    
                        
                    res={
                        'ano':etiquetas_datos['ano'],
                        'etiq_disp':disponible,
                        'parque_id':'',
                        'cantidad':'',
                        'desde':'',
                        'hasta':'',
                    }
        
        return {'value':res}
    
    
    def mostrar_desde(self,cr,uid,ids,etiqueta_id,parque_id,cantidad,context=None):
        res={}
        if etiqueta_id and parque_id and int(cantidad):
            cr.execute("select (ipg.correlativo) as correlativo from ip_correlativo_etiquetas as ice\
            inner join ip_correlativo_generar as ipg on ipg.etiqueta_id=ice.id\
            where ice.etiqueta_id=%s and ice.active=TRUE and ipg.state='generado' order by correlativo asc LIMIT 1 ;",(str(etiqueta_id),))
            for i in cr.fetchall():
                disponible=i[0]
                p,d=disponible.split('-')
                digitos=len(d)
                if int(cantidad)==1:
                    etiq_desde=disponible
                    ult_etiq=disponible
                elif int(d)==1:
                    etiq_desde=int(cantidad)
                    ult_etiq=str(p.upper())+'-'+str(etiq_desde).rjust(digitos,'0')
                else:
                    etiq_desde=int(d)+int(cantidad)-1
                    ult_etiq=str(p.upper())+'-'+str(etiq_desde).rjust(digitos,'0')
                
                res={
                'desde':disponible,
                'hasta':ult_etiq,
                }
                
                

        return {'value':res}
    
    def create(self,cr,uid,vals,context=None):
        #~ vals.update({
                #~ 'parque_id':vals['parque_id'].upper()
                #~ })
        
        cr.execute("select COUNT(ipg.state) as state from ip_correlativo_etiquetas as ice\
            inner join ip_correlativo_generar as ipg on ipg.etiqueta_id=ice.id\
            where ice.etiqueta_id=%s and ice.active=TRUE and ipg.state='generado';",(str(vals['etiqueta_id']),))
            
        for i in cr.fetchall():
            disponible=i[0]
            if disponible<=0:
                raise osv.except_osv(
                                    ('¡¡¡Error!!!'),
                                    ('La ETIQUETA seleccionada no posee registros generados.'))
            if int(vals['cantidad'])==0:
                raise osv.except_osv(
                                    ('¡¡¡Error de Cantidad!!!'),
                                    ('La cantidad '+str(vals['cantidad'])+' no puede ser asignada.'))
            if int(vals['cantidad']) > disponible:
                raise osv.except_osv(
                                    ('!!!Error de Cantidad¡¡¡'),
                                    ('La Cantidad Asignar '+str(vals['cantidad'])+' no puede ser mayor a la cantidad de Etiquetas Disponible '+str(disponible)))
                                    
        if vals['etiqueta_id'] and vals['parque_id'] and vals['cantidad']:
            
            cr.execute("select (ipg.id) as id from ip_correlativo_etiquetas as ice\
            inner join ip_correlativo_generar as ipg on ipg.etiqueta_id=ice.id\
            where ice.etiqueta_id=%s and ice.active=TRUE and ipg.state='generado' LIMIT 1;",(str(vals['etiqueta_id']),))
                
            for i in cr.fetchall():
                id_gen=i[0]
                if int(vals['cantidad'])==1:
                    correlativo_generar_obj=self.pool.get('ip.correlativo.generar')
                    correlativo_generar_obj.write(cr, uid, id_gen, {'state': 'asignado','parque_id':vals['parque_id']},context=context)
                elif id_gen==1:
                    h=int(vals['cantidad'])
                    correlativo_generar_obj=self.pool.get('ip.correlativo.generar')
                    while id_gen <= h :
                        correlativo_generar_obj.write(cr, uid, id_gen, {'state': 'asignado','parque_id':vals['parque_id']},context=context)
                        id_gen+=1
                else:
                    h=int(vals['cantidad'])+int(id_gen)-1
                    correlativo_generar_obj=self.pool.get('ip.correlativo.generar')
                    while id_gen <= h :
                        correlativo_generar_obj.write(cr, uid, id_gen, {'state': 'asignado','parque_id':vals['parque_id']},context=context)
                        id_gen+=1
        
        
        
        return super(asignar_etiqueta, self).create(cr, uid, vals, context=context)
        
        
