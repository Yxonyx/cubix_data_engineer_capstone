"""Tests for products silver transformation."""

import pyspark.sql.types as st
import pyspark.testing as spark_testing
from cubix_data_engineer_capstone.etl.silver.products import get_products


def test_get_products(spark):
    """
    Positive test that get_products returns the expected DataFrame.
    """
    test_data = spark.createDataFrame(
        [
            ("101", "5", "Road Bike", "500.50", "Red", "10", "999.99", "L", "High"),
            ("101", "5", "Road Bike", "500.50", "Red", "10", "999.99", "L", "High"),
        ],
        schema=[
            "pk", "psck", "name", "stancost", "color",
            "ssl", "listprice", "size", "rang"
        ]
    )

    results = get_products(test_data)

    expected_schema = st.StructType([
        st.StructField("ProductKey", st.IntegerType(), True),
        st.StructField("ProductSubcategoryKey", st.IntegerType(), True),
        st.StructField("ProductName", st.StringType(), True),
        st.StructField("StandardCost", st.DoubleType(), True),
        st.StructField("Color", st.StringType(), True),
        st.StructField("SafetyStockLevel", st.IntegerType(), True),
        st.StructField("ListPrice", st.DoubleType(), True),
        st.StructField("Size", st.StringType(), True),
        st.StructField("Range", st.StringType(), True),
    ])

    expected = spark.createDataFrame(
        [(101, 5, "Road Bike", 500.50, "Red", 10, 999.99, "L", "High")],
        schema=expected_schema
    )

    spark_testing.assertDataFrameEqual(results, expected)
