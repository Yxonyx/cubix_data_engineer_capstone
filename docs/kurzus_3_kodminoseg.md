# Cubix Data Engineer Capstone - 3. Rész
## Kódminőség és Automatizálás

**Dátum:** 2024-12-30
**Szerző:** Yxonyx (kaiserjonatan911@gmail.com)

---

## 📋 Tartalomjegyzék

1. [Honnan indultunk?](#1-honnan-indultunk)
2. [Mi a probléma?](#2-mi-a-probléma)
3. [Pre-commit](#3-pre-commit)
4. [Ruff - Linting és Formatting](#4-ruff---linting-és-formatting)
5. [Mypy - Típusellenőrzés](#5-mypy---típusellenőrzés)
6. [Telepítés és Használat](#6-telepítés-és-használat)

---

## 1. Honnan indultunk?

### 1. Rész - Projekt létrehozás

Az első részben létrehoztuk a Poetry projektet:

- ✅ Poetry konfiguráció (`virtualenvs.in-project = true`)
- ✅ Projekt struktúra (`cubix_data_engineer_capstone/`)
- ✅ Virtuális környezet (`.venv/`)
- ✅ Függőségek (`pyspark`, `numpy`, `pytest`, `pandas`, stb.)
- ✅ pyproject.toml konfiguráció

**Eredmény:** Működő Python projekt fejlesztési környezettel.

### 2. Rész - Wheel és Databricks

A második részben megtanultuk a kód megosztását:

- ✅ Python Wheel (`.whl`) csomag építése
- ✅ `read_file_from_volume()` - UC Volume olvasás
- ✅ `write_file_to_volume()` - UC Volume írás
- ✅ Databricks telepítés és használat
- ✅ Verziókezelés (`poetry version patch`)

**Eredmény:** Lokálisan fejlesztett kód futtatható Databricks-ben.

---

## 2. Mi a probléma?

Eddig **működő** kódunk van, de:

| Probléma | Következmény |
|----------|--------------|
| ❌ Nincs kódstílus ellenőrzés | Vegyes formázás, nehezen olvasható |
| ❌ Nincs automatikus hibadetektálás | Bugok csak futáskor derülnek ki |
| ❌ Nincs típusellenőrzés | Type error-ok rejtve maradnak |
| ❌ Nincs automatizálás | Minden commit előtt manuális ellenőrzés |

### A megoldás: Pre-commit + Ruff + Mypy

```
┌─────────────────────────────────────────────────────────┐
│                    git commit                           │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                    PRE-COMMIT                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │ Ruff Lint   │  │ Ruff Format │  │    Mypy     │     │
│  │  (hibák)    │  │  (stílus)   │  │  (típusok)  │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
                 ✅ Commit sikeres
                   VAGY
                 ❌ Commit blokkolva
```

---

## 3. Pre-commit

### Mi az a pre-commit?

A **pre-commit** egy git hook kezelő, ami automatikusan futtat ellenőrzéseket **minden commit előtt**.

### Konfiguráció: `.pre-commit-config.yaml`

```yaml
repos:
  # Általános ellenőrzések
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace      # Sorok végéről felesleges szóközök
      - id: end-of-file-fixer        # Fájlok üres sorral végződjenek
      - id: check-yaml               # YAML szintaxis ellenőrzés
      - id: check-added-large-files  # Nagy fájlok blokkolása
      - id: check-merge-conflict     # Merge conflict markerek detektálása

  # Ruff linter és formatter
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.9
    hooks:
      - id: ruff                     # Linting + auto-fix
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format              # Kód formázás

  # Mypy típusellenőrzés
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies:
          - pyspark-stubs            # PySpark típusok
        args: [--ignore-missing-imports]
```

### Hook-ok magyarázata

| Hook | Leírás | Automatikus javítás |
|------|--------|:-------------------:|
| `trailing-whitespace` | Sorvégi szóközök eltávolítása | ✅ |
| `end-of-file-fixer` | Üres sor a fájl végére | ✅ |
| `check-yaml` | YAML szintaxis | ❌ |
| `check-added-large-files` | >500KB fájlok blokkolása | ❌ |
| `check-merge-conflict` | `<<<<<<<` markerek keresése | ❌ |
| `ruff` | Python linting | ✅ |
| `ruff-format` | Kód formázás | ✅ |
| `mypy` | Típusellenőrzés | ❌ |

---

## 4. Ruff - Linting és Formatting

### Mi az a Ruff?

A **Ruff** egy rendkívül gyors Python linter és formatter, ami Rust-ban íródott.

- 🚀 **10-100x gyorsabb** mint flake8, black, isort
- 📦 **All-in-one** - linting + formatting + import sorting
- 🔧 **Auto-fix** - automatikusan javít

### Ruff vs. korábbi eszközök

| Funkció | Régi eszköz | Ruff |
|---------|-------------|------|
| Linting | flake8, pylint | ✅ `ruff check` |
| Formatting | black | ✅ `ruff format` |
| Import sorting | isort | ✅ Beépített |
| Sebesség | Lassú | 🚀 10-100x gyorsabb |

### Példa: hibák keresése

```powershell
ruff check .
```

Kimenet:
```
cubix_data_engineer_capstone/utils/databricks.py:28:9: B006 Do not use mutable data structures for argument defaults
Found 1 error.
```

### Példa: automatikus javítás

```powershell
ruff check --fix .
```

### Példa: formázás

```powershell
ruff format .
```

---

## 5. Mypy - Típusellenőrzés

### Mi az a Mypy?

A **Mypy** statikus típusellenőrző, ami ellenőrzi a type hint-eket futtatás nélkül.

### Miért fontos?

```python
# Type hints nélkül - hiba csak futáskor derül ki
def add_numbers(a, b):
    return a + b

result = add_numbers("hello", 5)  # TypeError futáskor!

# Type hints-szel - mypy előre jelzi
def add_numbers(a: int, b: int) -> int:
    return a + b

result = add_numbers("hello", 5)  # Mypy error: "str" != "int"
```

### PySpark támogatás

A `pyspark-stubs` csomag biztosítja a típusdefiníciókat:

```yaml
- id: mypy
  additional_dependencies:
    - pyspark-stubs
```

### Futtatás

```powershell
mypy cubix_data_engineer_capstone/
```

---

## 6. Telepítés és Használat

### 1. Függőségek telepítése

```powershell
# A virtuális környezetbe
.\.venv\Scripts\python.exe -m pip install pre-commit ruff mypy pyspark-stubs
```

Vagy Poetry-vel (ha működik):
```powershell
poetry add --group dev pre-commit ruff mypy pyspark-stubs
```

### 2. Pre-commit hook-ok telepítése

```powershell
.\.venv\Scripts\pre-commit.exe install
```

**Kimenet:**
```
pre-commit installed at .git/hooks/pre-commit
```

### 3. Manuális futtatás (összes fájl)

```powershell
.\.venv\Scripts\pre-commit.exe run --all-files
```

**Példa kimenet:**
```
Trim Trailing Whitespace.................................................Passed
Fix End of Files.........................................................Passed
Check Yaml...............................................................Passed
Check for added large files..............................................Passed
Check for merge conflicts................................................Passed
ruff.....................................................................Passed
ruff-format..............................................................Passed
mypy.....................................................................Passed
```

### 4. Git commit (automatikus futás)

```powershell
git add -A
git commit -m "Add code quality tools"
```

Ha van hiba, a commit **blokkolódik** amíg nem javítod ki!

---

## 📊 Összefoglaló: Hová jutottunk?

| Kurzus | Téma | Eredmény |
|--------|------|----------|
| **1. Rész** | Projekt létrehozás | Poetry projekt, .venv, függőségek |
| **2. Rész** | Wheel & Databricks | .whl build, UC Volume read/write |
| **3. Rész** | Kódminőség | pre-commit, ruff, mypy |

### Teljes workflow

```
┌──────────────────────────────────────────────────────────────────┐
│                        FEJLESZTÉS                                │
│                                                                  │
│  1. VS Code-ban kód írása                                        │
│  2. git add → git commit                                         │
│  3. Pre-commit automatikusan fut:                                │
│     ├─ ruff check → hibák javítása                              │
│     ├─ ruff format → egységes formázás                          │
│     └─ mypy → típushibák detektálása                            │
│  4. Ha minden OK → commit sikeres                                │
│  5. git push → GitHub-ra                                         │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│                        DEPLOYMENT                                │
│                                                                  │
│  1. poetry version patch → verzió növelés                        │
│  2. poetry build -f wheel → .whl csomag                         │
│  3. Feltöltés Databricks-be                                      │
│  4. !pip install *.whl                                           │
│  5. from cubix_data_engineer_capstone import ...                 │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## ✅ Ellenőrző lista

- [x] Pre-commit konfiguráció (`.pre-commit-config.yaml`)
- [x] Ruff telepítés és konfiguráció
- [x] Mypy telepítés PySpark támogatással
- [x] Pre-commit hook-ok telepítése
- [x] Manuális futtatás tesztelése
- [x] Git commit workflow tesztelése

---

## 🔗 Hasznos linkek

- [Pre-commit dokumentáció](https://pre-commit.com/)
- [Ruff dokumentáció](https://docs.astral.sh/ruff/)
- [Mypy dokumentáció](https://mypy.readthedocs.io/)
- [Ruff rules](https://docs.astral.sh/ruff/rules/)

---

**Előző rész:** [2. Wheel és Databricks](kurzus_2_wheel_databricks.md)
**Következő rész:** ETL Pipeline fejlesztés
