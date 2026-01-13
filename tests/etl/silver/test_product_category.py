"""Tests for product category silver transformation."""

import pyspark.sql.types as st
import pyspark.testing as spark_testing
from cubix_data_engineer_capstone.etl.silver.product_category import (
    get_product_category,
)


def test_get_product_category(spark):
    """
    Positive test that get_product_category returns expected DataFrame.
    """
    test_data = spark.createDataFrame(
        [
            ("1", "1", "Bikes", "Bicicleta", "Vélo"),
            ("1", "1", "Bikes", "Bicicleta", "Vélo"),
        ],
        schema=["pck", "pcak", "epcn", "spcn", "fpcn"],
    )

    results = get_product_category(test_data)

    expected_schema = st.StructType(
        [
            st.StructField("ProductCategoryKey", st.IntegerType(), True),
            st.StructField("ProductCategoryAlternateKey", st.IntegerType(), True),
            st.StructField("EnglishProductCategoryName", st.StringType(), True),
            st.StructField("SpanishProductCategoryName", st.StringType(), True),
            st.StructField("FrenchProductCategoryName", st.StringType(), True),
        ]
    )

    expected = spark.createDataFrame(
        [(1, 1, "Bikes", "Bicicleta", "Vélo")], schema=expected_schema
    )

    spark_testing.assertDataFrameEqual(results, expected)
