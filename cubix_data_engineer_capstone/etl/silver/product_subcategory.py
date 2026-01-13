"""Product Subcategory dimension transformation module."""

import pyspark.sql.functions as sf
from pyspark.sql import DataFrame

PRODUCT_SUBCATEGORY_MAPPING = {
    "psk": "ProductSubcategoryKey",
    "psak": "ProductSubcategoryAlternateKey",
    "epsn": "EnglishProductSubcategoryName",
    "spsn": "SpanishProductSubcategoryName",
    "fpsn": "FrenchProductSubcategoryName",
    "pck": "ProductCategoryKey",
}


def get_product_subcategory(product_subcategory_raw: DataFrame) -> DataFrame:
    """Map and filter Product Subcategory data.

    :param product_subcategory_raw: Raw Product Subcategory data.
    :return:                        Mapped and filtered Product Subcategory data.
    """
    return (
        product_subcategory_raw.select(
            sf.col("psk").cast("int"),
            sf.col("psak").cast("int"),
            sf.col("epsn"),
            sf.col("spsn"),
            sf.col("fpsn"),
            sf.col("pck").cast("int"),
        )
        .withColumnsRenamed(PRODUCT_SUBCATEGORY_MAPPING)
        .dropDuplicates()
    )
