# Cubix Data Engineer Capstone - 2. Rész
## Python Wheel és Databricks Integráció

**Dátum:** 2024-12-16
**Szerző:** Yxonyx (kaiserjonatan911@gmail.com)

---

## 📋 Tartalomjegyzék

1. [Mi a probléma amit megoldunk?](#1-mi-a-probléma-amit-megoldunk)
2. [A megoldás: Python Wheel](#2-a-megoldás-python-wheel)
3. [Projekt struktúra](#3-projekt-struktúra)
4. [A databricks.py modul](#4-a-databrickspy-modul)
5. [Build és Deploy folyamat](#5-build-és-deploy-folyamat)
6. [Használat Databricks-ben](#6-használat-databricks-ben)

---

## 1. Mi a probléma amit megoldunk?

### A klasszikus probléma

Databricks notebook-okban gyakran **ugyanazt a kódot másolgatjuk** notebook-ról notebook-ra:
- Spark session kezelés
- Fájl olvasás/írás Volume-okról
- Konfigurációk
- Segédfüggvények

**Problémák:**
- ❌ Kód duplikáció
- ❌ Nehéz karbantartás
- ❌ Nincs verziókezelés
- ❌ Tesztelhetőség hiánya

### A megoldás

**Python wheel csomag** készítése, amit:
- ✅ Lokálisan fejlesztünk (VS Code, PyCharm)
- ✅ Verziókezeljük (Git/GitHub)
- ✅ Tesztelünk (pytest)
- ✅ Telepítünk Databricks-be

---

## 2. A megoldás: Python Wheel

### Mi az a Wheel?

A **wheel** (`.whl`) a Python szabványos csomag formátuma:
- Tömörített fájl (valójában ZIP)
- Tartalmazza a Python kódot
- Telepíthető `pip install` paranccsal

### Miért jó ez?

```
┌─────────────────┐     wheel      ┌─────────────────┐
│   VS Code       │ ───────────►   │   Databricks    │
│   (fejlesztés)  │    .whl        │   (futtatás)    │
└─────────────────┘                └─────────────────┘
```

1. **Lokálisan fejlesztesz** → IntelliSense, debugging, git
2. **Buildelsz** → `poetry build -f wheel`
3. **Feltöltöd** → Databricks Workspace
4. **Telepíted** → `!pip install *.whl`
5. **Használod** → `from mypackage import ...`

---

## 3. Projekt struktúra

```
cubix_data_engineer_capstone/
├── cubix_data_engineer_capstone/     # Fő csomag
│   ├── __init__.py
│   ├── etl/                          # ETL logika
│   │   └── __init__.py
│   └── utils/                        # Segédfüggvények
│       ├── __init__.py
│       ├── authentication.py         # Spark session
│       ├── config.py                 # Konfiguráció
│       ├── databricks.py             # UC Volume műveletek
│       └── datalake.py               # Data Lake műveletek
├── dist/                             # Build kimenet
│   └── *.whl                         # Wheel fájlok
├── docs/                             # Dokumentáció
├── tests/                            # Tesztek
├── .gitignore
├── pyproject.toml                    # Projekt konfig
└── poetry.lock                       # Függőségek
```

---

## 4. A databricks.py modul

Ez a modul Unity Catalog Volume-okkal dolgozik.

### read_file_from_volume

Fájl beolvasása Volume-ról DataFrame-be:

```python
from pyspark.sql import DataFrame, SparkSession


def read_file_from_volume(full_path: str, format: str) -> DataFrame:
    """Reads a file from UC Volume and returns it as a Spark DataFrame.

    :param full_path:   The path to the file on the volume.
    :param format:      The format of the file. Can be "csv", "parquet", "delta".
    :return:            DataFrame with the data.
    """
    if format not in ["csv", "parquet", "delta"]:
        raise ValueError(f"Invalid format: {format}")

    spark = SparkSession.getActiveSession()

    reader = spark.read.format(format)
    if format == "csv":
        reader = reader.option("header", "true")

    return reader.load(full_path)
```

### write_file_to_volume

DataFrame mentése Volume-ra:

```python
def write_file_to_volume(
        df: DataFrame,
        full_path: str,
        format: str,
        mode: str = "overwrite",
        partition_by: list[str] = None
) -> None:
    """Writes a DataFrame to UC Volume as parquet / csv / delta format.

    :param df:              DataFrame to be written.
    :param full_path:       The path to the file on the volume.
    :param format:          The format of the file.
    :param mode:            Write mode (default: "overwrite").
    :param partition_by:    List of columns to partition by.
    """
    if format not in ["csv", "parquet", "delta"]:
        raise ValueError(f"Invalid format: {format}")

    writer = df.write.mode(mode).format(format)
    if format == "csv":
        writer = writer.option("header", True)

    if partition_by:
        writer = writer.partitionBy(*partition_by)

    writer.save(full_path)
```

---

## 5. Build és Deploy folyamat

### 1. Verzió növelése

```powershell
python -m poetry version patch
# Bumping version from 0.2.24 to 0.2.25
```

Verzió típusok:
- `patch` → 0.2.24 → 0.2.25 (bug fix)
- `minor` → 0.2.24 → 0.3.0 (új funkció)
- `major` → 0.2.24 → 1.0.0 (breaking change)

### 2. Wheel építése

```powershell
python -m poetry build -f wheel
# Built cubix_data_engineer_capstone-0.2.25-py3-none-any.whl
```

A `.whl` fájl a `dist/` mappában jön létre.

### 3. Feltöltés Databricks-be

1. Databricks Workspace megnyitása
2. Jobb klikk → Import → File
3. Válaszd ki a `.whl` fájlt
4. Import

### 4. Telepítés notebook-ban

```python
!pip install /Workspace/Users/email@example.com/cubix_data_engineer_capstone-0.2.25-py3-none-any.whl
```

Ha frissítesz:
```python
!pip install --force-reinstall /Workspace/Users/.../cubix_data_engineer_capstone-0.2.25-py3-none-any.whl
%restart_python
```

---

## 6. Használat Databricks-ben

### Import

```python
from cubix_data_engineer_capstone.utils.databricks import read_file_from_volume, write_file_to_volume
```

### Olvasás

```python
full_path = "/Volumes/capstone/bronze/bronze/calendar/"
calendar_df = read_file_from_volume(full_path, "csv")
display(calendar_df)
```

### Írás

```python
output_path = "/Volumes/capstone/silver/silver/calendar/"
write_file_to_volume(calendar_df, output_path, "parquet")
```

### Ctrl+Click

Ha a függvényre **Ctrl+Click**-elsz, Databricks megmutatja a forráskódot - ez bizonyítja, hogy a csomag telepítve van!

---

## 📊 Összefoglaló

| Lépés | Parancs | Eredmény |
|-------|---------|----------|
| Verzió növelés | `poetry version patch` | 0.2.24 → 0.2.25 |
| Build | `poetry build -f wheel` | `.whl` fájl |
| Feltöltés | Databricks Import | Workspace-be |
| Telepítés | `!pip install *.whl` | Cluster-re |
| Használat | `from ... import ...` | Notebook-ban |

---

## ✅ Ellenőrző lista

- [x] Projekt struktúra kialakítása
- [x] `databricks.py` - read/write függvények
- [x] `poetry version patch` - verzió növelés
- [x] `poetry build -f wheel` - wheel építése
- [x] Feltöltés Databricks Workspace-be
- [x] `!pip install` - telepítés cluster-re
- [x] Tesztelés notebook-ban

---

## 🔗 Hasznos linkek

- [Poetry Build dokumentáció](https://python-poetry.org/docs/cli/#build)
- [Databricks Libraries](https://docs.databricks.com/libraries/index.html)
- [Unity Catalog Volumes](https://docs.databricks.com/data-governance/unity-catalog/volumes.html)

---

**Előző rész:** [1. Projekt létrehozás](kurzus_1_projekt_letrehozas.md)
**Következő rész:** ETL Pipeline fejlesztés
