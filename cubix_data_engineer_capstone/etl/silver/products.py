"""Products dimension transformation module."""

import pyspark.sql.functions as sf
from pyspark.sql import DataFrame

PRODUCTS_MAPPING = {
    "pk": "ProductKey",
    "psck": "ProductSubcategoryKey",
    "name": "ProductName",
    "stancost": "StandardCost",
    "color": "Color",
    "ssl": "SafetyStockLevel",
    "listprice": "ListPrice",
    "size": "Size",
    "rang": "Range"
}


def get_products(products_raw: DataFrame) -> DataFrame:
    """Map and filter Products data.

    :param products_raw:    Raw Products data.
    :return:                Mapped and filtered Products data.
    """
    return (
        products_raw
        .select(
            sf.col("pk").cast("int"),
            sf.col("psck").cast("int"),
            sf.col("name"),
            sf.col("stancost").cast("double"),
            sf.col("color"),
            sf.col("ssl").cast("int"),
            sf.col("listprice").cast("double"),
            sf.col("size"),
            sf.col("rang"),
        )
        .withColumnsRenamed(PRODUCTS_MAPPING)
        .dropDuplicates()
    )
