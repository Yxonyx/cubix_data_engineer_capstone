"""Tests for customers silver transformation."""

from datetime import datetime

import pyspark.sql.types as st
import pyspark.testing as spark_testing
from cubix_data_engineer_capstone.etl.silver.customers import get_customers


def test_get_customers(spark):
    """
    Positive test that get_customers returns the expected DataFrame.
    """
    test_data = spark.createDataFrame(
        [
            ("1", "10", "John Doe", "1990-05-15", "M", "M", "50000", "2", "Pro"),
            ("1", "10", "John Doe", "1990-05-15", "M", "M", "50000", "2", "Pro"),
        ],
        schema=[
            "ck",
            "gk",
            "name",
            "bdate",
            "ms",
            "gender",
            "income",
            "childrenhome",
            "occ",
        ],
    )

    results = get_customers(test_data)

    expected_schema = st.StructType(
        [
            st.StructField("CustomerKey", st.IntegerType(), True),
            st.StructField("GeographyKey", st.IntegerType(), True),
            st.StructField("CustomerName", st.StringType(), True),
            st.StructField("BirthDate", st.DateType(), True),
            st.StructField("MaritalStatus", st.StringType(), True),
            st.StructField("Gender", st.StringType(), True),
            st.StructField("YearlyIncome", st.IntegerType(), True),
            st.StructField("TotalChildren", st.IntegerType(), True),
            st.StructField("Occupation", st.StringType(), True),
        ]
    )

    expected = spark.createDataFrame(
        [(1, 10, "John Doe", datetime(1990, 5, 15), "M", "M", 50000, 2, "Pro")],
        schema=expected_schema,
    )

    spark_testing.assertDataFrameEqual(results, expected)
