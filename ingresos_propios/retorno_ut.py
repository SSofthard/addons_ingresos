def get_default_autorizacion(self, cr, uid,fields,context=None):
        account_config_obj=self.pool.get('account.config.settings')
        res = account_config_obj.get_default_ut(cr, uid,fields)
        return res['unidad_tributaria']
        
