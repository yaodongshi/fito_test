from odoo import http
from odoo.http import request


class QueryEditor(http.Controller):

    @http.route('/report/<int:id>', type='http', auth="user", website=True, csrf=False)
    def show_saved_report(self, **kw):
        report_id = kw.get('id')
        reports = request.env['mini.tableau'].sudo().search([('id', '=', report_id)])

        request.cr.execute(reports.user_query)
        table_column_names = request.cr.description
        table_column_names = [
            column_name[0] for column_name in table_column_names
        ]

        table_result = request.cr.fetchall()

        data = {
            'table_column_names': sorted(table_column_names),
            'table_result': table_result,
            'sql_query': reports.user_query,
            'user_query': reports.user_query,
            'report_name': reports.report_name or '',
            'report_rows': reports.report_rows or '',
            'report_columns': reports.report_columns or '',
            'chart_type': reports.chart_type or ''
        }

        return request.render('mini_tableau.saved_report_dashboard_template', data)


    @http.route('/delete-report/<int:id>', type='http', auth="user", website=True, csrf=False)
    def query_delete(self, **kw):
        report_id = kw.get('id')
        reports = request.env['mini.tableau'].sudo().search([('id', '=', report_id)])
        reports.unlink()

        return request.redirect('/query-dashboard')


    @http.route('/save-report/', type='http', auth="user", website=True, csrf=False)
    def save_report(self, **kw):
        report_object = request.env['mini.tableau'].sudo()
        report_name = kw.get('report_name')
        rows = kw.get('rows')
        columns = kw.get('columns')
        sql_query = kw.get('sql_query')
        chart_type = kw.get('chart_type')

        report_object.create({
            "user_query": sql_query,
            'report_name': report_name,
            'report_rows': rows,
            'report_columns': columns,
            'chart_type': chart_type
        })

        # self.chart_type = chart_type
        return request.redirect('/query-dashboard')


    @http.route('/query-dashboard', type='http', auth="user", website=True, csrf=False)
    def query_dashboard(self, **kw):
        request.cr.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE' ORDER BY TABLE_NAME ASC;")

        tables = request.cr.fetchall()
        reports = request.env['mini.tableau'].sudo().search([])

        data = {
            'tables': tables,
            'reports': reports
        }

        return request.render('mini_tableau.dashboard_template', data)


    @http.route('/table-result', type='json', auth='user', methods=['POST'], website=True)
    def table_result(self, **kw):
        table_name = kw.get('table_name')
        total_rows = kw.get('total_rows')
        sql_query = kw.get('sql_query')

        request.cr.execute(f'SELECT * FROM {table_name} LIMIT {total_rows};')

        table_column_names = request.cr.description
        table_column_names = [
            column_name[0] for column_name in table_column_names
        ]

        table_result = request.cr.fetchall()

        data = {
            'table_name': table_name,
            'table_column_names': table_column_names,
            'table_result': table_result
        }

        return data


    @http.route('/query-result', type='json', auth='user', methods=['POST'], website=True)
    def query_result(self, **kw):

        sql_query = kw.get('sql_query')
        message = None

        try:
            request.cr.execute(sql_query)

            table_column_names = request.cr.description
            table_column_names = [
                column_name[0] for column_name in table_column_names
            ]

            table_result = request.cr.fetchall()

            data = {
                'table_name': 'Custom query executed',
                'table_column_names': table_column_names,
                'table_result': table_result
            }

            return data

        except Exception as e:
            request.cr.rollback()
            return {'message': f'ERROR: {e}'}


    # Report Controllers
    @http.route('/report-dashboard', methods=['GET', 'POST'], type='http', auth="user", website=True, csrf=False)
    def report_dashboard(self, **kw):

        sql_query = kw.get('sql_query')
        message = None

        # sending data to the template
        request.cr.execute(sql_query)

        table_column_names = request.cr.description
        table_column_names = [
            column_name[0] for column_name in table_column_names
        ]

        data = {
            'table_column_names': sorted(table_column_names),
            'sql_query': sql_query,
        }

        return request.render('mini_tableau.report_dashboard_template', data)


    @http.route('/query-report-result', type='json', auth='user', methods=['POST'], website=True)
    def query_result_dict(self, **kw):

        sql_query = kw.get('sql_query')
        message = None

        try:
            request.cr.execute(sql_query)

            column_names = request.cr.description
            column_names = [column_name[0] for column_name in column_names]

            rows = request.cr.fetchall()

            result_dict = {}

            for column_name in column_names:
                result_dict[column_name] = []

            for row in rows:
                for key, value in zip(column_names, row):
                    result_dict[key].append(value)

            return {'result_data': result_dict}

        except Exception as e:
            request.cr.rollback()
            return {'message': f'ERROR: {e}'}
