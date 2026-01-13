# Cubix Data Engineer Capstone - 1. Rész
## Python Projekt Létrehozása Poetry-vel

**Dátum:** 2024-12-15
**Szerző:** Yxonyx (kaiserjonatan911@gmail.com)

---

## 📋 Tartalomjegyzék

1. [Projekt inicializálás](#1-projekt-inicializálás)
2. [Virtuális környezet](#2-virtuális-környezet)
3. [Függőségek telepítése](#3-függőségek-telepítése)
4. [Projekt struktúra](#4-projekt-struktúra)
5. [Wheel Build és Databricks](#5-wheel-build-és-databricks)
6. [Verziókezelés (Git)](#6-verziókezelés-git)

---

## 1. Projekt inicializálás

### Poetry konfigurálása

```powershell
# Virtuális környezet a projekt mappában legyen
poetry config virtualenvs.in-project true
```

### Új projekt létrehozása

```powershell
poetry new cubix_data_engineer_capstone
cd cubix_data_engineer_capstone
```

---

## 2. Virtuális környezet

### pyproject.toml

```toml
[project]
name = "cubix-data-engineer-capstone"
version = "0.2.24"
description = ""
authors = [
    {name = "Yxonyx", email="kaiserjonatan911@gmail.com"}
]
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "pyspark (>=3.5.4)",
    "numpy (>=1)"
]

[project.optional-dependencies]
delta = ["delta-spark>=3.3.0"]

[tool.poetry.group.dev.dependencies]
pytest = "^8.3.4"
pyarrow = "^19.0.0"
pre-commit = "^4.0.1"
pandas = "^2.2.3"

[tool.pytest.ini_options]
testpaths = ["./tests"]
filterwarnings = ["ignore:DeprecationWarning"]
addopts = "--disable-warnings -p no:warnings"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

### Virtuális környezet létrehozása

```powershell
python -m poetry install
```

---

## 3. Függőségek telepítése

### Fő függőségek

```powershell
python -m poetry add pyspark
python -m poetry add "numpy=^1"
```

### Dev függőségek

```powershell
python -m poetry add --group dev pytest pyarrow pre-commit pandas
```

### Csomagok összefoglalója

| Csomag | Verzió | Típus | Leírás |
|--------|--------|-------|--------|
| pyspark | >=3.5.4 | dependency | Apache Spark Python API |
| numpy | >=1 | dependency | Numerikus számítások |
| pytest | ^8.3.4 | dev | Tesztelési keretrendszer |
| pyarrow | ^19.0.0 | dev | Apache Arrow, Parquet |
| pre-commit | ^4.0.1 | dev | Git hook kezelés |
| pandas | ^2.2.3 | dev | DataFrame műveletek |
| delta-spark | >=3.3.0 | optional | Delta Lake támogatás |

---

## 4. Projekt struktúra

```
cubix_data_engineer_capstone/
├── .github/
│   └── workflows/
│       └── deploy.yml           # CI/CD pipeline
├── .venv/                       # Virtuális környezet
├── cubix_data_engineer_capstone/
│   ├── etl/
│   │   └── __init__.py          # ETL modulok
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── authentication.py    # Spark session
│   │   ├── config.py            # Konfiguráció
│   │   ├── databricks.py        # UC Volume olvasás
│   │   └── datalake.py          # Data Lake műveletek
│   ├── __init__.py
│   └── upload_latest_whl.ps1    # Wheel feltöltés script
├── dist/                        # Build kimenet
├── docs/
│   └── kurzus_1_projekt_letrehozas.md
├── tests/
│   └── __init__.py
├── .gitignore
├── .pre-commit-config.yaml
├── poetry.lock
├── pyproject.toml
└── README.md
```

---

## 5. Wheel Build és Databricks

### Verzió frissítése

```powershell
python -m poetry version patch
# Bumping version from 0.2.23 to 0.2.24
```

### Wheel építése

```powershell
python -m poetry build -f wheel
# Built cubix_data_engineer_capstone-0.2.24-py3-none-any.whl
```

A wheel fájl a `dist/` mappában jön létre.

### Databricks telepítés

1. Töltsd fel a `.whl` fájlt Databricks Workspace-be
2. Notebook-ban:

```python
!pip install /Workspace/Users/majomkaiser@icloud.com/cubix_data_engineer_capstone-0.2.24-py3-none-any.whl
```

3. Kernel újraindítás (ha szükséges):

```python
%restart_python
```

4. Import és használat:

```python
from cubix_data_engineer_capstone.utils.databricks import read_file_from_volume

full_path = "/Volumes/source_system/source_system/source_files/calendar/calendar.csv"
df = read_file_from_volume(full_path, "csv")
display(df)
```

### A `read_file_from_volume` függvény

```python
from pyspark.sql import DataFrame, SparkSession


def read_file_from_volume(full_path: str, format: str) -> DataFrame:
    """Reads a file from UC Volume and returns it as a Spark DataFrame.

    :param full_path:   The path to the file on the volume.
    :param format:      The format of the file. Can be "csv", "parquet", "delta".
    :return:            DataFrame with the data.
    """
    if format not in ["csv", "parquet", "delta"]:
        raise ValueError(f"Invalid format: {format}. Supported formates are: csv, parquet, delta.")

    spark = SparkSession.getActiveSession()

    reader = spark.read.format(format)
    if format == "csv":
        reader = reader.option("header", "true")

    return reader.load(full_path)
```

---

## 6. Verziókezelés (Git)

### .gitignore (kivonatok)

```gitignore
__pycache__/
*.py[cod]
.venv/
dist/
*.egg-info/
.idea/
.vscode/
derby.log
metastore_db/
```

### Git parancsok

```powershell
git add -A
git commit -m "Add wheel build and Databricks integration"
git push origin main
```

---

## ✅ Ellenőrző lista

- [x] Poetry konfiguráció
- [x] Projekt létrehozás
- [x] Virtuális környezet (.venv)
- [x] Függőségek telepítése
- [x] Projekt struktúra kialakítása
- [x] Utils modulok (databricks.py, datalake.py, stb.)
- [x] Wheel build (`poetry build -f wheel`)
- [x] Databricks telepítés és tesztelés
- [x] GitHub push

---

## 🔗 Hasznos linkek

- [Poetry dokumentáció](https://python-poetry.org/docs/)
- [PySpark dokumentáció](https://spark.apache.org/docs/latest/api/python/)
- [GitHub repo](https://github.com/Yxonyx/cubix_data_engineer_capstone)

---

**Következő rész:** ETL pipeline fejlesztés
