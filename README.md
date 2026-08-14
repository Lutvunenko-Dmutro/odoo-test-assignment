# Тестове завдання для розробника Odoo

## 1. Налаштування робочого оточення

Цей гайд описує розгортання Odoo 19 Community Edition на базі Ubuntu (може бути використано як для нативної Ubuntu, так і для WSL2 на Windows 10/11).

### Крок 1. Оновлення системи та встановлення системних залежностей
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv python3-dev \
    build-essential libxml2-dev libxslt1-dev libldap2-dev libsasl2-dev \
    libtiff5-dev libjpeg8-dev libpq-dev libfreetype6-dev liblcms2-dev \
    libwebp-dev libharfbuzz-dev libfribidi-dev libxcb1-dev git
```

### Крок 2. Встановлення та налаштування PostgreSQL
```bash
sudo apt install -y postgresql postgresql-client
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Створення користувача PostgreSQL для Odoo
sudo su - postgres -c "createuser -s odoo"
# Задамо пароль користувачу (введіть 'odoo' при запиті)
sudo su - postgres -c "psql -c \"ALTER USER odoo WITH PASSWORD 'odoo';\""
```

### Крок 3. Встановлення wkhtmltopdf
Для коректної генерації PDF-звітів (з підтримкою хедерів/футерів) необхідна версія wkhtmltopdf 0.12.6:
```bash
wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.jammy_amd64.deb
sudo apt install ./wkhtmltox_0.12.6.1-2.jammy_amd64.deb
```

### Крок 4. Клонування репозиторію Odoo 19 CE
Оберіть директорію (наприклад, `~/odoo19`) та зклонуйте вихідний код Odoo:
```bash
mkdir ~/odoo_dev
cd ~/odoo_dev
git clone --branch 19.0 --single-branch https://github.com/odoo/odoo.git
```

### Крок 5. Створення virtualenv та встановлення Python-залежностей
```bash
cd ~/odoo_dev/odoo
python3 -m venv venv
source venv/bin/activate

# Встановлення залежностей з requirements.txt
pip install setuptools wheel
pip install -r requirements.txt
```

### Крок 6. Запуск Odoo
Для запуску Odoo відредагуйте конфігураційний файл `odoo.conf` (його приклад знаходиться у цьому репозиторії). Переконайтеся, що шлях `addons_path` у файлі конфігурації вказує на стандартні аддони Odoo та на папку з вашими кастомними модулями (куди ви покладете `company_hr_military`).

```bash
# Переконайтесь, що virtualenv активовано
./odoo-bin -c /шлях/до/вашого/odoo.conf
```
Після того, як сервер запуститься, відкрийте браузер і перейдіть за адресою `http://localhost:8069`.

---

## 2. Створення бази даних та робота з модулями

1. При першому запуску перейдіть на `http://localhost:8069`.
2. Odoo запропонує створити нову базу даних.
3. Заповніть поля:
   - **Master Password**: вкажіть пароль з `odoo.conf` (за замовчуванням у прикладі `admin_master_password`).
   - **Database Name**: наприклад, `test_db`.
   - **Email / Password**: admin / admin (для входу).
   - **Language**: English або Ukrainian.
   - **Demo data**: увімкніть галочку (щоб були тестові дані для перевірки).
4. Після створення БД увійдіть у систему, перейдіть у меню **Apps** (Додатки).
5. Приберіть фільтр "Apps" (у стрічці пошуку) і знайдіть модуль "Співробітники" (Employees / `hr`). Встановіть його.
6. Для встановлення власного модуля `company_hr_military`:
   - Увімкніть режим розробника (Developer Mode) у налаштуваннях (Settings).
   - Перейдіть у меню **Apps** -> **Update Apps List** (Оновити список додатків).
   - Знайдіть `Company HR Military` та натисніть "Activate/Install".

---

## 3. Опис модуля `company_hr_military`

Модуль `company_hr_military` розширює стандартний модуль `hr` (Співробітники) для ведення військового обліку на підприємстві.

### Реалізований функціонал:
1. **Модель (довідник) ТЦК та СП (`company_hr_military.tck`)**:
   - Містить поля: Назва (char), Код (char), Телефон (char).
   - Додано відображення (List та Form view).
   - Додано пункт меню в "Співробітники" -> "Налаштування" -> "ТЦК та СП".
2. **Розширення моделі `hr.employee`**:
   - Додано нові поля: `is_reserved` (Бронювання), `is_mobilized` (Мобілізований), `tck_id` (зв'язок Many2one з ТЦК), `edrpvr_number` (Номер в ЄДРПВР).
   - Додано відображення цих полів на формі співробітника у вкладці "Приватна інформація" (Private Information) у новому блоці "Військовий облік".

### Проблеми, з якими зіткнувся (для звіту):
- _(Тут ви можете описати будь-які проблеми, з якими зіткнулися під час налаштування WSL2, наприклад, помилки з портами, встановлення wkhtmltopdf або труднощі з PostgreSQL, якщо вони виникнуть)_
