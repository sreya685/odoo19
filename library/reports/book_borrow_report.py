from odoo import models,api



class ReportlibraryForm_Library_Report(models.AbstractModel):
    _name = 'report.library.form_library_report'

    @api.model
    def _get_report_values(self, docids, data=None):
        # docs = self.env['checkouts'].browse(docids)
        # print(docids)
        # print(docs)
        print('data :',data)
        # print(data)
        return {
            # 'doc_ids': docids,
            # 'doc_model': 'checkouts',
            # 'docs': docs,
            'data': data,
        }
