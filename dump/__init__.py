# -*- coding: utf-8 -*-
import os, csv
import datetime as dt

dumpdir = os.path.dirname(os.path.realpath(__file__))


def to_bool(data):
    if isinstance(data, str):
        data = data.lower()
        if data == "0" or data == "false":
            return False
        elif data == "1" or data == "true":
            return True

    return NotImplemented


def to_date_format(string):
    # remove time element
    string = string.split(' ')[0]
    try:
        return dt.datetime.strptime(string, '%d/%m/%Y')
    except ValueError:
        return None


def to_dec(data):
    try:
        return float(data)
    except:
        return 0


def dump_unit_price(env=None, file='UnitPrice.csv'):
    if env is None:
        raise ValueError

    csvpath = os.path.join(dumpdir, file)

    with open(csvpath) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:

            unit_price = env['outsource.unit.rate'].search([('access_db_id', '=', row["id"])], limit=1)

            if unit_price:
                print('Resource ID# %s Exist' % row["id"])
                continue
            else:
                data = {
                    'access_db_id': row["id"],
                    'po_level': row['po_level'],
                    'po_position': row['po_position'],
                    'contractor': row['contractor'],
                    'amount': to_dec(row['amount']),
                    'percent': row['percent'],

                }
                env['outsource.unit.rate'].create(data)
                env.cr.commit()


def dump_purchase_order(env=None, file='TechPO.csv'):
    if env is None:
        raise ValueError

    csvpath = os.path.join(dumpdir, file)
    with open(csvpath) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            po = env['outsource.purchase.order'].search([('access_db_id', '=', row["POID"])])

            if len(po) != 0:
                print('Purchase Order ID# %s Exist' % row["POID"])
                continue
            else:
                data = {
                    'access_db_id': row["POID"],
                    'po_num': row["PONum"],
                    #                'po_date': to_date_format(row["PODate"]),
                    'po_value': to_dec(row["POValue"]),
                    'contractor': row["Contractor"],
                    'budget': row["Budget"],
                    'capex_commitment_value': to_dec(row["CPXComValue"]),
                    'capex_expenditure_value': to_dec(row["CPXExpValue"]),
                    'opex_value': to_dec(row["OPXValue"]),
                    'revenue_value': to_dec(row["REVValue"]),
                    'task_num': row["TaskNum"],
                    'renew_status': row["RenewStatus"],
                    'renew_po_no': row["RenewPONum"],
                    'po_status': row["POStatus"],
                    'po_remarks': row["PORemarks"],
                    'po_type': row["POType"],
                }

                env['outsource.purchase.order'].create(data)
                env.cr.commit()


def dump_purchase_order_line(env=None, file='TechPOLine.csv'):
    if env is None:
        raise ValueError
    csvpath = os.path.join(dumpdir, file)

    with open(csvpath) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            po_line = env['outsource.purchase.order.line'].search([('access_db_id', '=', row["POLineID"])])
            if len(po_line) != 0:
                print('Purchase Order Line ID# %s Exist' % row["POID"])
                continue
            else:
                po = env['outsource.purchase.order'].search([('access_db_id', '=', row["POID"])])

                if len(po) == 0:
                    print("Purchase Order ID# %s Does't Exist" % row["POID"])
                    continue
                elif len(po) > 1:
                    print("Purchase Order ID# %s Multiple Record" % row["POID"])
                    continue
                else:
                    data = {
                        'po_id': po[0].id,
                        'access_db_id': row["POLineID"],
                        'line_num': row["POLineNum"],
                        'line_duration': row["POLineDuration"],
                        'line_value': to_dec(row["POLineValue"]),
                        'line_revise_rate': to_dec(row["POLineRValue"]),
                        'line_rate': to_dec(row["POLineRate"]),
                        'line_status': row["POLineStatus"],
                        'line_actuals': row["POLineActuals"],
                        'capex_percent': row["CPXPercent"],
                        'opex_percent': row["OPXPercent"],
                        'revenue_percent': row["REVPercent"],
                    }
                    env['outsource.purchase.order.line'].create(data)
                    env.cr.commit()


def dump_purchase_order_line_details(env=None, file='TechPOLineDetail.csv'):
    if env is None:
        raise ValueError

    csvpath = os.path.join(dumpdir, file)
    with open(csvpath) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            po_line_detail = env['outsource.purchase.order.line.detail'].search([('access_db_id', '=', row["PODetID"])])
            if len(po_line_detail) != 0:
                print('Purchase Order Line Detail ID# %s Exist' % row["PODetID"])
                continue
            else:

                po_line = env['outsource.purchase.order.line'].search([('access_db_id', '=', row["POLineID"])])
                if len(po_line) == 0:
                    print("Purchase Order Line ID# %s Does't Exist" % row["POLineID"])
                    continue
                else:
                    data = {
                        'po_line_id': po_line[0].id,
                        'access_db_id': row["PODetID"],
                        'po_os_ref': row["POOSRef"],
                        'po_position': row["POPosition"],
                        'po_level': row["POLevel"],
                        'po_rate': to_dec(row["PORate"]),
                        'po_revise_rate': to_dec(row["PORRate"]),
                        'division': row["Division"],
                        'section': row["Section"],
                        'sub_section': row["SubSection"],
                        'director_name': row["DirName"],
                        'frozen_status': row["FrozenStatus"],
                        'approval_ref_num': row["ApprovalRefNum"],
                        'approval_reason': row["ApprovalReason"],
                        'kpi_2016': row["2016KPI"],
                        'capex_percent': row["CPX%Age"],
                        'opex_percent': row["OPX%Age"],
                        'revenue_percent': row["REV%Age"],
                        'rate_diff_percent': to_dec(row['PORate%Incr'])

                    }
                    env['outsource.purchase.order.line.detail'].create(data)
                    env.cr.commit()


def dump_invoice(env=None, file='TechInvoiceMgmt.csv'):
    if env is None:
        raise ValueError

    csvpath = os.path.join(dumpdir, file)
    with open(csvpath) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            invoice = env['outsource.invoice'].search([('access_db_id', '=', row['InvID'])], limit=1)
            resource_id = env['outsource.resource'].search([('access_db_id', '=', row['ResID'])], limit=1)
            po_line_detail_id = env['outsource.purchase.order.line.detail'].search([('access_db_id', '=', row['PODetID'])],
                                                                                limit=1)
            if not resource_id or not po_line_detail_id:
                continue
            if invoice:
                print('Invoice ID# %s Exist' % row["InvID"])
                continue
            else:
                data = {
                    'access_db_id': row['InvID'],
                    'resource_id': resource_id.id,
                    'po_line_detail_id': po_line_detail_id.id,
                    'invoice_date': to_date_format(row['InvMonth']),
                    'invoice_hour': row['InvMonthHrs'],
                    'invoice_claim': row['InvClaimHrs'],
                    'invoice_cert_amount': row['InvCertAmt'],
                    'remarks': row['Remarks']
                }

                env['outsource.invoice'].create(data)
                env.cr.commit()


def dump_resource(env=None, file='RPT01_ Monthly Accruals - Mobillized.csv'):
    if env is None:
        raise ValueError

    csvpath = os.path.join(dumpdir, file)
    with open(csvpath) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            resource = env['outsource.resource'].search([('access_db_id', '=', row["ResID"])], limit=1)
            po_id = env['outsource.purchase.order'].search([('access_db_id', '=', row["POID"])], limit=1)
            po_line_detail_id = env['outsource.purchase.order.line.detail'].search(
                [('access_db_id', '=', row["PODetID"])], limit=1)

            if resource:
                print('Resource ID# %s Exist' % row["ResID"])
                continue
            else:
                data = {
                    'po_id': po_id.id,
                    'po_line_detail_id': po_line_detail_id.id,
                    'access_db_id': row["ResID"],
                    'res_type': row['ResType'],
                    'res_type_class': row['ResTypeClass'],
                    'agency_ref_num': row['AgencyRefNum'],
                    'res_emp_num': row['ResEmpNum'],
                    'res_full_name': row['ResFullName'],
                    # TODO FIX EMPTY
                    'date_of_join': to_date_format(row['DoJ']),
                    'res_job_title': row['ResJobTitle'],
                    'grade_level': row['GradeLevel'],
                    'po_position': row['POPosition'],
                    'po_level': row['POLevel'],
                    'division': row['Division'],
                    'section': row['Section'],
                    'manager': row['Manager'],
                    'rate': row['Rate'],
                    'po_rate_percent_increase': to_dec(row['PORate%Incr']),
                    'capex_percent': row['CPX%Age'],
                    'capex_rate': row['CAPEXRate'],
                    'opex_percent': row['OPX%Age'],
                    'opex_rate': row['OPEXRate'],
                    'revenue_percent': row['REV%Age'],
                    'revenue_rate': row['REVENUERate'],
                    'remarks': row['Remarks'],
                    'po_num': row['PONum'],
                    'po_value': row['POValue'],
                    'capex_commitment_value': row['CPXComValue'],
                    'opex_value': row['OPXValue'],
                    'revenue_value': row['REVValue'],
                    'contractor': row['Contractor'],
                    'po_os_ref': row['POOSRef'],
                    'has_tool_or_uniform': to_bool(row['ToolsProvided']),
                }
                env['outsource.resource'].create(data)
                env.cr.commit()


def clear_all(env):
    env['outsource.purchase.order'].search([]).unlink()
    print('CLEARED PURCHASE ORDER')
    env['outsource.purchase.order.line'].search([]).unlink()
    print('CLEARED PURCHASE ORDER LINE')
    env['outsource.purchase.order.line.detail'].search([]).unlink()
    print('CLEARED PURCHASE ORDER LINE DETAIL')
    env['outsource.resource'].search([]).unlink()
    print('CLEARED RESOURCE')
    env['outsource.invoice'].search([]).unlink()
    print('CLEARED INVOICE')
    env['outsource.unit.rate'].search([]).unlink()
    print('CLEARED UNIT PRICE')


def start(env):
    dump_purchase_order(env)
    print('DONE PURCHASE ORDER')
    dump_purchase_order_line(env)
    print('DONE PURCHASE ORDER LINE')
    dump_purchase_order_line_details(env)
    print('DONE PURCHASE ORDER LINE DETAILS')
    dump_resource(env)
    print('DONE RESOURCE')
    dump_unit_price(env)
    print('DONE UNIT PRICE')
    dump_invoice(env)
    print('DONE INVOICE')


if __name__ == '__main__':
    pass
