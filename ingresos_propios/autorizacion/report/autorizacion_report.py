 # -*- encoding: utf-8 -*-

from openerp.osv import osv
import time
from openerp.report import report_sxw

class autorizacion_report(report_sxw.rml_parse):
   
    def __init__(self , cr, uid, name, context):
        super(autorizacion_report,self).__init__(cr,uid,name,context)
        self.localcontext.update({
            'time':time,
        })
        self.context = context
    
        
class report_autorizacion(osv.AbstractModel):
    _name = "report.autorizacion.id_template_autorizacion_qweb"
    _inherit = "report.abstract_report"
    _template = "autorizacion.id_template_autorizacion_qweb"
    _wrapped_report_class = autorizacion_report
# report_sxw.report_sxw('report.autorizacion', 'autorizacion', 'local_addons/autorizacion/report/autorizacion.rml', parser=autorizacion_report)
