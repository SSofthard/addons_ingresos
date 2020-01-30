# -*- coding: utf-8 -*-
##############################################################################
#

#
##############################################################################

from openerp.osv import fields,osv


class product_product(osv.Model):
    _inherit = "product.template"
    
    _columns = {
        'isticket':fields.boolean('Is Ticket'),
    }

    
    
    
class boletos(osv.osv):
    _name="ip.boletos"
    _rec_name="product_id"
    _inherits = {'product.template': 'product_id'}
    _description="Registro de los Boletos"
    
    def cantidad_boleto(self, cr, uid, ids, name, arg, context=None):
        res = dict(map(lambda x: (x,0), ids))
        inventario_boletos_obj=self.pool.get('ip.inventario.boletos')
        for boleto in self.browse(cr, uid, ids, context=context):
            inventario_id=inventario_boletos_obj.search(cr, uid,[('producto_id', '=', boleto.id)],context=context)
            for inventario_boleto in inventario_boletos_obj.browse(cr,uid,inventario_id,context=context):
                res[boleto.id]=res[boleto.id]+inventario_boleto.existente
        return res
           
    _columns = {
        'product_id': fields.many2one('product.template', 'Product_id', required=True, ondelete='cascade'),
        'cant_stock':fields.function(cantidad_boleto,'Boletos Generados', type='integer',)        
    }
    
    _defaults = {
        #~ 'list_price':0,
        'isticket': True,
    }

    
