from odoo.tests.common import TransactionCase

class TestHrMilitary(TransactionCase):
    
    @classmethod
    def setUpClass(cls):
        super(TestHrMilitary, cls).setUpClass()
        # Ініціалізація моделей
        cls.tck_model = cls.env['company_hr_military.tck']
        cls.employee_model = cls.env['hr.employee']
        
        # Створюємо тестовий ТЦК
        cls.test_tck = cls.tck_model.create({
            'name': 'Київський міський ТЦК',
            'code': '12345678',
            'phone': '+380441234567'
        })
        
        # Створюємо тестового співробітника та прив'язуємо до ТЦК
        cls.test_employee = cls.employee_model.create({
            'name': 'Іван Іваненко',
            'is_reserved': True,
            'is_mobilized': False,
            'tck_id': cls.test_tck.id,
            'edrpvr_number': '1122334455'
        })

    def test_01_tck_creation(self):
        """ Перевірка створення ТЦК та правильності збереження полів """
        self.assertEqual(self.test_tck.name, 'Київський міський ТЦК')
        self.assertEqual(self.test_tck.code, '12345678')
        self.assertEqual(self.test_tck.phone, '+380441234567')

    def test_02_employee_military_fields(self):
        """ Перевірка збереження військових полів у картці співробітника """
        self.assertTrue(self.test_employee.is_reserved, "Співробітник має бути заброньований")
        self.assertFalse(self.test_employee.is_mobilized, "Співробітник не має бути мобілізований")
        self.assertEqual(self.test_employee.edrpvr_number, '1122334455', "Номер ЄДРПВР не збігається")
        
    def test_03_tck_employee_relation(self):
        """ Перевірка зв'язку Many2one між Співробітником та ТЦК """
        self.assertTrue(self.test_employee.tck_id, "ТЦК не прив'язаний до співробітника")
        self.assertEqual(self.test_employee.tck_id.id, self.test_tck.id, "ID ТЦК не збігається")
        self.assertEqual(self.test_employee.tck_id.name, 'Київський міський ТЦК', "Назва прив'язаного ТЦК не збігається")
