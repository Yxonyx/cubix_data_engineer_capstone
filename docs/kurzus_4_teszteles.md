# Cubix Data Engineer Capstone - 4. Rész
## Unit Tesztelés PySpark-kal

**Dátum:** 2026-01-11
**Szerző:** Yxonyx (kaiserjonatan911@gmail.com)

---

## 📋 Tartalomjegyzék

1. [Honnan indultunk?](#1-honnan-indultunk)
2. [Miért tesztelünk?](#2-miért-tesztelünk)
3. [Pytest alapok](#3-pytest-alapok)
4. [PySpark tesztelés](#4-pyspark-tesztelés)
5. [Teszt struktúra](#5-teszt-struktúra)
6. [Példa: Calendar teszt](#6-példa-calendar-teszt)
7. [Futtatás](#7-futtatás)

---

## 1. Honnan indultunk?

### Korábbi részek összefoglalása

| Kurzus | Téma | Eredmény |
|--------|------|----------|
| **1. Rész** | Projekt létrehozás | Poetry projekt, .venv, függőségek |
| **2. Rész** | Wheel & Databricks | .whl build, UC Volume read/write |
| **3. Rész** | Kódminőség | pre-commit, ruff, mypy |

**Most:** Unit tesztek írása a Silver layer transzformációkhoz.

---

## 2. Miért tesztelünk?

### A probléma

```
┌────────────────────────────────────────────────────────┐
│  Kód változtatás                                        │
│       ↓                                                 │
│  "Működik lokálisan"                                    │
│       ↓                                                 │
│  Deploy Databricks-be                                   │
│       ↓                                                 │
│  ❌ HIBA! De melyik változtatás okozta?                │
└────────────────────────────────────────────────────────┘
```

### A megoldás: Unit tesztek

```
┌────────────────────────────────────────────────────────┐
│  Kód változtatás                                        │
│       ↓                                                 │
│  pytest futtatás                                        │
│       ↓                                                 │
│  ✅ PASSED → biztos, hogy működik                      │
│  ❌ FAILED → azonnal látszik a hiba                    │
└────────────────────────────────────────────────────────┘
```

### Mit tesztelünk?

| Teszt típusa | Leírás | Példa |
|--------------|--------|-------|
| **Séma validáció** | A kimenet oszlopai és típusai helyesek | `Date` oszlop `DateType()` típusú |
| **Transzformáció** | Az adatok helyesen alakulnak át | String → Integer konverzió |
| **Üzleti logika** | A deduplikáció, szűrés működik | `dropDuplicates()` tényleg eltávolít |
| **Edge case-ek** | Szélsőséges esetek kezelése | NULL értékek, üres DataFrame |

---

## 3. Pytest alapok

### Mi az a pytest?

A **pytest** a Python legnépszerűbb tesztelési keretrendszere:

- 🚀 **Egyszerű szintaxis** - függvények, nem class-ok
- 📦 **Fixture-ök** - újrafelhasználható setup
- ✅ **Automatikus felfedezés** - `test_*.py` fájlok

### Telepítés

```powershell
python -m pip install pytest
```

### Alapvető teszt

```python
# tests/test_example.py

def test_addition():
    """Teszt: 1 + 1 = 2"""
    assert 1 + 1 == 2

def test_string():
    """Teszt: string műveletek"""
    assert "hello".upper() == "HELLO"
```

### Futtatás

```powershell
pytest tests/ -v
```

**Kimenet:**
```
tests/test_example.py::test_addition PASSED
tests/test_example.py::test_string PASSED
```

---

## 4. PySpark tesztelés

### Kihívások

A PySpark tesztelés speciális, mert:

1. **SparkSession kell** - minden teszthez
2. **Java/Hadoop környezet** - winutils.exe Windows-on
3. **Lassabb** - JVM indítás időbe telik

### Megoldás: Fixture

A **fixture** egy olyan függvény, ami előkészíti a tesztkörnyezetet:

```python
# tests/conftest.py

from pyspark.sql import SparkSession
from pytest import fixture


SPARK = (
    SparkSession
    .builder
    .master("local")
    .appName("localTests")
    .getOrCreate()
)


@fixture
def spark():
    return SPARK.getActiveSession()
```

### Miért így?

| Megoldás | Probléma |
|----------|----------|
| Minden tesztben új SparkSession | 🐢 Nagyon lassú (JVM újraindítás) |
| Globális SparkSession + fixture | ✅ Gyors, egyszer indul |

### Környezeti változók (Windows)

A PySpark Windows-on igényli:

```powershell
# PowerShell - beállítás felhasználó szinten
[System.Environment]::SetEnvironmentVariable("PYSPARK_PYTHON", "C:\Users\User\spark_env\Python311\python.exe", "User")
[System.Environment]::SetEnvironmentVariable("PYSPARK_DRIVER_PYTHON", "C:\Users\User\spark_env\Python311\python.exe", "User")
[System.Environment]::SetEnvironmentVariable("HADOOP_HOME", "C:\Users\User\spark_env\hadoop-3.3.1", "User")
```

---

## 5. Teszt struktúra

### Könyvtárstruktúra

```
cubix_data_engineer_capstone/
├── cubix_data_engineer_capstone/
│   └── etl/
│       └── silver/
│           ├── __init__.py
│           └── calendar.py          ← Tesztelendő kód
│
└── tests/
    ├── __init__.py
    ├── conftest.py                   ← Spark fixture
    └── etl/
        ├── __init__.py
        └── silver/
            ├── __init__.py
            └── test_calendar.py      ← Teszt fájl
```

### Elnevezési konvenció

| Elem | Szabály | Példa |
|------|---------|-------|
| Teszt fájl | `test_*.py` | `test_calendar.py` |
| Teszt függvény | `test_*` | `test_get_calendar()` |
| Fixture | PEP8 | `spark`, `sample_data` |

---

## 6. Példa: Calendar teszt

### A tesztelendő függvény

```python
# cubix_data_engineer_capstone/etl/silver/calendar.py

import pyspark.sql.functions as sf
from pyspark.sql import DataFrame


def get_calendar(calendar_raw: DataFrame) -> DataFrame:
    """Clean and transform data type for Calendar data.

    1. Select required columns.
    2. Cast them explicitly.
    3. Drop duplicates.

    :param calendar_raw:    Raw Calendar DataFrame.
    :return:                Transformed Calendar DataFrame.
    """
    return (
        calendar_raw
        .select(
            sf.col("Date").cast("date"),
            sf.col("DayNumberOfWeek").cast("int"),
            sf.col("DayName"),
            sf.col("MonthName"),
            sf.col("MonthNumberOfYear").cast("int"),
            # ... további oszlopok
        )
        .dropDuplicates()
    )
```

### A teszt

```python
# tests/etl/silver/test_calendar.py

from datetime import datetime
import pyspark.sql.types as st
import pyspark.testing as spark_testing
from cubix_data_engineer_capstone.etl.silver.calendar import get_calendar


def test_get_calendar(spark):
    """
    Positive test that the function get_calendar returns the expected DataFrame.
    """
    # ARRANGE - Teszt adat előkészítése
    test_data = spark.createDataFrame(
        [
            ("2017-01-01", "7", "Sunday", "January", "1", "1", ...),
            ("2017-01-01", "7", "Sunday", "January", "1", "1", ...),  # Duplikátum!
        ],
        schema=["Date", "DayNumberOfWeek", "DayName", "MonthName", ...]
    )

    # ACT - Függvény meghívása
    results = get_calendar(test_data)

    # ASSERT - Eredmény ellenőrzése
    expected_schema = st.StructType([
        st.StructField("Date", st.DateType(), True),
        st.StructField("DayNumberOfWeek", st.IntegerType(), True),
        st.StructField("DayName", st.StringType(), True),
        # ...
    ])

    expected = spark.createDataFrame(
        [(datetime(2017, 1, 1), 7, "Sunday", "January", ...)],  # Csak 1 sor!
        schema=expected_schema
    )

    spark_testing.assertDataFrameEqual(results, expected)
```

### A teszt elemei

| Elem | Leírás |
|------|--------|
| **ARRANGE** | Teszt adatok előkészítése (input DataFrame) |
| **ACT** | A tesztelendő függvény meghívása |
| **ASSERT** | Eredmény összehasonlítása az elvárttal |

### Mit ellenőrzünk?

1. ✅ **Séma** - `assertDataFrameEqual` összehasonlítja a sémákat
2. ✅ **Típuskonverzió** - String "7" → Integer 7
3. ✅ **Dátumkonverzió** - String "2017-01-01" → DateType
4. ✅ **Deduplikáció** - 2 azonos sor → 1 sor marad

---

## 7. Futtatás

### Egyetlen teszt fájl

```powershell
python -m pytest .\tests\etl\silver\test_calendar.py -v
```

**Kimenet:**
```
tests/etl/silver/test_calendar.py::test_get_calendar PASSED [100%]

=============== 1 passed in 6.91s ================
```

### Összes teszt

```powershell
python -m pytest tests/ -v
```

### Részletes output hibánál

```powershell
python -m pytest tests/ -v --tb=long
```

### pyproject.toml konfiguráció

```toml
[tool.pytest.ini_options]
testpaths = ["./tests"]
filterwarnings = ["ignore:DeprecationWarning"]
addopts = "--disable-warnings -p no:warnings"
```

---

## 📊 Összefoglaló: Hová jutottunk?

| Kurzus | Téma | Eredmény |
|--------|------|----------|
| **1. Rész** | Projekt létrehozás | Poetry projekt, .venv, függőségek |
| **2. Rész** | Wheel & Databricks | .whl build, UC Volume read/write |
| **3. Rész** | Kódminőség | pre-commit, ruff, mypy |
| **4. Rész** | Tesztelés | pytest, PySpark fixtures, assertDataFrameEqual |

### Teljes workflow

```
┌──────────────────────────────────────────────────────────────────┐
│                        FEJLESZTÉS                                │
│                                                                  │
│  1. Transzformáció írása (pl. get_calendar)                      │
│  2. Unit teszt írása (test_get_calendar)                         │
│  3. pytest futtatás → ✅ PASSED                                  │
│  4. git commit → pre-commit ellenőrzések                         │
│  5. git push → GitHub-ra                                         │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│                        DEPLOYMENT                                │
│                                                                  │
│  1. poetry build -f wheel → .whl csomag                         │
│  2. Feltöltés Databricks-be                                      │
│  3. !pip install *.whl                                           │
│  4. Biztos, hogy működik - mert tesztelve van! ✅               │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## ✅ Ellenőrző lista

- [x] pytest telepítve
- [x] tests/ könyvtárstruktúra létrehozva
- [x] conftest.py SparkSession fixture-rel
- [x] test_calendar.py megírva
- [x] Környezeti változók beállítva (PYSPARK_PYTHON, HADOOP_HOME)
- [x] Teszt sikeresen lefut

---

## 🔗 Hasznos linkek

- [pytest dokumentáció](https://docs.pytest.org/)
- [PySpark Testing dokumentáció](https://spark.apache.org/docs/latest/api/python/reference/pyspark.testing.html)
- [assertDataFrameEqual](https://spark.apache.org/docs/latest/api/python/reference/pyspark.testing.html#pyspark.testing.assertDataFrameEqual)

---

**Előző rész:** [3. Kódminőség és Automatizálás](kurzus_3_kodminoseg.md)
**Következő rész:** ETL Pipeline - Gold réteg
