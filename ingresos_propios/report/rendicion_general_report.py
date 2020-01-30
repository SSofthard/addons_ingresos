# -*- encoding: utf-8 -*-

from openerp.osv import osv
import time
from openerp.report import report_sxw
from datetime import datetime

class datos_rendicion_general(report_sxw.rml_parse):
    total=0.0
    def __init__(self, cr, uid, name, context):
        super(datos_rendicion_general,self).__init__(cr,uid,name,context)
        self.localcontext.update({
            'time': time,
            'get_data1': self.get_data1,
            'get_total':self.get_total
           
        
        })
        self.context = context
        
        
    def get_data1(self,date_start,date_end,parque_id):
        account_voucher_obj=self.pool.get('account.voucher')
        tids = account_voucher_obj.search(self.cr,self.uid,[('create_date', '>=', date_start),('create_date', '<=', date_end),('parque_id', '=', parque_id[0])])
        res = account_voucher_obj.browse(self.cr,self.uid,tids)
        for t in res:
            self.total+=t.amount
        return res
        
    def get_total(self):
        
        return self.total
        
     

    
        
class report_rendicion_general(osv.AbstractModel):
    _name = "report.ingresos_propios.id_rendicion_general1_report_qweb"
    _inherit = "report.abstract_report"
    _template = "ingresos_propios.id_rendicion_general1_report_qweb"
    _wrapped_report_class = datos_rendicion_general
        

# report_sxw.report_sxw('report.ingresos_propios.account_voucher', 'account_invoice', 'local_addons8/ingresos_propios/report/id_rendicion_general_report_qweb.rml',parser=datos_rendicion_general)


