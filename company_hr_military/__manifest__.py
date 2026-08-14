{
    'name': 'Company HR Military',
    'version': '1.0',
    'category': 'Human Resources',
    'summary': 'Військовий облік співробітників (ТЦК та мобілізація)',
    'description': """
        Модуль розширює стандартний функціонал співробітників (hr)
        для додавання інформації про військовий облік:
        - Довідник ТЦК та СП
        - Бронювання співробітника
        - Мобілізація співробітника
        - Номер в ЄДРПВР
    """,
    'author': 'Dmytro Lutvunenko',
    'depends': ['hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/tck_views.xml',
        'views/hr_employee_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
