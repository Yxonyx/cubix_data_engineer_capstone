"""Tests for product subcategory silver transformation."""

import pyspark.sql.types as st
import pyspark.testing as spark_testing
from cubix_data_engineer_capstone.etl.silver.product_subcategory import (
    get_product_subcategory,
)


def test_get_product_subcategory(spark):
    """
    Positive test that get_product_subcategory returns expected DataFrame.
    """
    test_data = spark.createDataFrame(
        [
            ("1", "1", "Mountain Bikes", "Bicicleta", "VTT", "1"),
            ("1", "1", "Mountain Bikes", "Bicicleta", "VTT", "1"),
        ],
        schema=["psk", "psak", "epsn", "spsn", "fpsn", "pck"],
    )

    results = get_product_subcategory(test_data)

    expected_schema = st.StructType(
        [
            st.StructField("ProductSubcategoryKey", st.IntegerType(), True),
            st.StructField("ProductSubcategoryAlternateKey", st.IntegerType(), True),
            st.StructField("EnglishProductSubcategoryName", st.StringType(), True),
            st.StructField("SpanishProductSubcategoryName", st.StringType(), True),
            st.StructField("FrenchProductSubcategoryName", st.StringType(), True),
            st.StructField("ProductCategoryKey", st.IntegerType(), True),
        ]
    )

    expected = spark.createDataFrame(
        [(1, 1, "Mountain Bikes", "Bicicleta", "VTT", 1)], schema=expected_schema
    )

    spark_testing.assertDataFrameEqual(results, expected)
