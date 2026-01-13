"""Customers dimension transformation module."""

import pyspark.sql.functions as sf
from pyspark.sql import DataFrame

CUSTOMERS_MAPPING = {
    "ck": "CustomerKey",
    "gk": "GeographyKey",
    "name": "CustomerName",
    "bdate": "BirthDate",
    "ms": "MaritalStatus",
    "gender": "Gender",
    "income": "YearlyIncome",
    "childrenhome": "TotalChildren",
    "occ": "Occupation"
}


def get_customers(customers_raw: DataFrame) -> DataFrame:
    """Map and filter Customers data.

    :param customers_raw:   Raw Customers data.
    :return:                Mapped and filtered Customers data.
    """
    return (
        customers_raw
        .select(
            sf.col("ck").cast("int"),
            sf.col("gk").cast("int"),
            sf.col("name"),
            sf.col("bdate").cast("date"),
            sf.col("ms"),
            sf.col("gender"),
            sf.col("income").cast("int"),
            sf.col("childrenhome").cast("int"),
            sf.col("occ"),
        )
        .withColumnsRenamed(CUSTOMERS_MAPPING)
        .dropDuplicates()
    )
