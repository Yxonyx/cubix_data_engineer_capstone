"""Product Category dimension transformation module."""

import pyspark.sql.functions as sf
from pyspark.sql import DataFrame

PRODUCT_CATEGORY_MAPPING = {
    "pck": "ProductCategoryKey",
    "pcak": "ProductCategoryAlternateKey",
    "epcn": "EnglishProductCategoryName",
    "spcn": "SpanishProductCategoryName",
    "fpcn": "FrenchProductCategoryName",
}


def get_product_category(product_category_raw: DataFrame) -> DataFrame:
    """Map and filter Product Category data.

    :param product_category_raw:    Raw Product Category data.
    :return:                        Mapped and filtered Product Category data.
    """
    return (
        product_category_raw.select(
            sf.col("pck").cast("int"),
            sf.col("pcak").cast("int"),
            sf.col("epcn"),
            sf.col("spcn"),
            sf.col("fpcn"),
        )
        .withColumnsRenamed(PRODUCT_CATEGORY_MAPPING)
        .dropDuplicates()
    )
