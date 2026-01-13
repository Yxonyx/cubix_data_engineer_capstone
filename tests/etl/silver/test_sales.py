"""Tests for sales silver transformation."""

from datetime import datetime

import pyspark.sql.types as st
import pyspark.testing as spark_testing
from cubix_data_engineer_capstone.etl.silver.sales import get_sales


def test_get_sales(spark):
    """
    Positive test that the function get_sales returns the expected DataFrame.
    """
    test_data = spark.createDataFrame(
        [
            ("SO001", "2017-01-01", "101", "201", "2017-01-05", "5", "extra"),
            ("SO001", "2017-01-01", "101", "201", "2017-01-05", "5", "extra"),
        ],
        schema=[
            "son",
            "orderdate",
            "pk",
            "ck",
            "dateofshipping",
            "oquantity",
            "extra_col"
        ]
    )

    results = get_sales(test_data)

    expected_schema = st.StructType(
        [
            st.StructField("SalesOrderNumber", st.StringType(), True),
            st.StructField("OrderDate", st.DateType(), True),
            st.StructField("ProductKey", st.IntegerType(), True),
            st.StructField("CustomerKey", st.IntegerType(), True),
            st.StructField("ShipDate", st.DateType(), True),
            st.StructField("OrderQuantity", st.IntegerType(), True),
        ]
    )

    expected = spark.createDataFrame(
        [
            (
                "SO001",
                datetime(2017, 1, 1),
                101,
                201,
                datetime(2017, 1, 5),
                5
            )
        ],
        schema=expected_schema
    )

    spark_testing.assertDataFrameEqual(results, expected)
