# company_hr_military — Odoo 19 Module

> **Test assignment** for the Odoo Developer (Python) position at **ENAMINE**.
> Author: **Dmytro Lutvunenko**

---

[🇺🇦 Українська](README.md) &nbsp;|&nbsp; 🇬🇧 English

---

## 📋 Overview

A custom Odoo 19 Community Edition module that extends the standard HR module with military record-keeping functionality, as required by Ukrainian legislation.

### What the module does

| Feature | Description |
|---|---|
| **TCK & SP Directory** | A new reference model (`company_hr_military.tck`) for storing military recruitment centers with name, code, and phone fields |
| **Employee Extension** | Extends `hr.employee` with 4 new fields: Reservation status, Mobilization status, TCK link (Many2one), and EDRPVR number |
| **UI Integration** | All new fields are displayed in a dedicated **"Військовий облік"** group inside the employee form's **"Private Information"** tab |
| **Menu Item** | A new "ТЦК та СП" item is added under Employees → Configuration |

---

## 🗂️ Project Structure

```
odoo-test-assignment/
├── .github/
│   └── workflows/
│       └── odoo-ci.yml             # GitHub Actions: flake8 linter (CI/CD)
├── company_hr_military/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── tck.py                  # TCK & SP reference model
│   │   └── hr_employee.py          # hr.employee extension (_inherit)
│   ├── security/
│   │   └── ir.model.access.csv     # Access rights for all users
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_hr_military.py     # Unit tests (TransactionCase)
│   ├── views/
│   │   ├── tck_views.xml           # List & Form views + menu for TCK
│   │   └── hr_employee_views.xml   # XPath injection into employee form
│   ├── __init__.py
│   └── __manifest__.py
├── .gitignore
├── odoo.conf                       # Example configuration file
├── README.md                       # 🇺🇦 Ukrainian documentation
└── README.en.md                    # 🇬🇧 This document
```

---

## ⚙️ Environment Setup

**Stack:** Ubuntu 24.04 (WSL2 on Windows 11) · Python 3.12 · PostgreSQL 18 (native, no Docker) · Odoo 19.0 CE (from source)

### Step 1 — System dependencies

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv python3-dev \
    build-essential libxml2-dev libxslt1-dev libldap2-dev libsasl2-dev \
    libtiff5-dev libjpeg8-dev libpq-dev libfreetype6-dev liblcms2-dev \
    libwebp-dev libharfbuzz-dev libfribidi-dev libxcb1-dev git
```

### Step 2 — PostgreSQL (native install, no Docker)

```bash
sudo apt install -y postgresql postgresql-client
sudo service postgresql start

# Create Odoo DB user
sudo su - postgres -c "createuser -s odoo"
sudo su - postgres -c "psql -c \"ALTER USER odoo WITH PASSWORD 'odoo';\""
```

> ⚠️ **WSL2 note:** Use `sudo service postgresql start` instead of `systemctl` — systemd is not enabled by default in WSL2.

### Step 3 — wkhtmltopdf (for PDF reports)

```bash
wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.jammy_amd64.deb
sudo apt install -y ./wkhtmltox_0.12.6.1-2.jammy_amd64.deb
```

### Step 4 — Clone Odoo 19 source

```bash
# Clone to Linux home directory (NOT to /mnt/d/ — git chmod fails on NTFS)
mkdir ~/odoo && cd ~/odoo
git clone --branch 19.0 --single-branch --depth 1 https://github.com/odoo/odoo.git .
```

> ⚠️ **Important:** Always clone Odoo to the native Linux filesystem (`~/`), not to a Windows-mounted drive (`/mnt/d/`). Git's `core.filemode` chmod operations fail on NTFS volumes.

### Step 5 — Python virtual environment

```bash
python3 -m venv ~/odoo-venv
source ~/odoo-venv/bin/activate

pip install setuptools wheel
pip install -r ~/odoo/requirements.txt
```

### Step 6 — Clone this repository & configure

```bash
git clone https://github.com/Lutvunenko-Dmutro/odoo-test-assignment.git ~/odoo-test-assignment
```

Edit `odoo.conf` and set your `addons_path`:

```ini
[options]
admin_passwd = admin_master_password
db_host = localhost
db_port = 5432
db_user = odoo
db_password = odoo
addons_path = ~/odoo/addons,~/odoo-test-assignment
http_port = 8069
```

> ⚠️ **WSL2 note:** Set `db_host = localhost` (not `False`). Without it, PostgreSQL uses peer authentication which fails for non-`postgres` system users.

### Step 7 — Run the server

```bash
source ~/odoo-venv/bin/activate
cd ~/odoo
./odoo-bin -c ~/odoo-test-assignment/odoo.conf
```

Open `http://localhost:8069` in your browser.

---

## 🚀 Module Installation

1. Create a new database at `http://localhost:8069` (enable **Demo data** for sample employees).
2. Go to **Settings** → scroll to bottom → click **Activate the developer mode**.
3. Go to **Apps** → click **Update Apps List** → confirm.
4. Search for `Military` → find **Company HR Military** → click **Activate**.

---

## 🧪 Running Tests

```bash
source ~/odoo-venv/bin/activate
cd ~/odoo
./odoo-bin -c ~/odoo-test-assignment/odoo.conf \
    --test-enable \
    --stop-after-init \
    -u company_hr_military \
    -d test_db
```

The test suite covers:
- ✅ TCK record creation and field validation
- ✅ Employee military fields persistence
- ✅ Many2one relation between employee and TCK

---

## 🔄 CI/CD

Every push to `main` triggers a **GitHub Actions** workflow (`.github/workflows/odoo-ci.yml`):
1. Spins up Ubuntu on GitHub's cloud.
2. Installs Python 3.10 + `flake8`.
3. Runs two linting passes on `company_hr_military/`:
   - **Pass 1:** Hard fail on syntax errors (`E9`, `F63`, `F7`, `F82`)
   - **Pass 2:** PEP8 style check (warnings only, max line length 120)

---

## 🐛 Challenges & Solutions

| Challenge | Solution |
|---|---|
| `git chmod` fails on `/mnt/d/` (NTFS) | Cloned Odoo to native Linux `~/` filesystem |
| `python3 -m venv` fails on `/mnt/d/` | Created venv at `~/odoo-venv` on Linux filesystem |
| PostgreSQL peer auth error | Set `db_host = localhost` in `odoo.conf` to force TCP connection |
| `odoo.conf` warns `db_host reads 'False'` | Replaced `False` placeholder with real `localhost` value |
| Odoo 19 rejects `<tree>` tag in XML views | Replaced with `<list>` — renamed in Odoo 19 (breaking change from v18) |

---

## 📦 Tech Stack

- **Odoo 19.0 CE** (Community Edition, from source)
- **Python 3.12**
- **PostgreSQL 18** (native, no Docker)
- **Ubuntu 24.04** via WSL2
- **GitHub Actions** for CI/CD (flake8 linter)
