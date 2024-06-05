# -*- coding: utf-8 -*-
{
    'name': "mohsin_school",

    'summary': "I am Muhammad Mohsin Mushtaq I have created this school management system in odoo",

    'description': """
Long I am Muhammad Mohsin Mushtaq I have created this school management system in odoo
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr'],

    # always loaded
    'data': [
        'security/school_security.xml',
        'security/ir.model.access.csv',
        'wizard/mark_attendance_wizard_view.xml',
        'views/school_menu.xml',
        'views/templates.xml',
        'views/res_company_view.xml',
        'views/res_config_settings_view.xml',
        'views/academic_year_view.xml',
        'views/resource_calendar_view.xml',
        'views/classroom_view.xml',
        'views/subject_view.xml',
        'views/course_view.xml',
        'views/batch_view.xml',
        'views/section_view.xml',
        'views/res_partner_view.xml',
        'views/student_medical_view.xml',
        'views/medical_type_view.xml',
        'views/student_view.xml',
        'views/teacher_view.xml',
        'views/teacher_subjects_view.xml',
        'views/attendance_register_view.xml',
        'views/attendance_sheet_view.xml',
        'views/attendance_view.xml',
        'report/report.xml',
        'report/student_detail_report.xml',
        'report/attendance_excel_report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',

    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}
