from pyspark.sql import SparkSession
from pytest import fixture


SPARK = SparkSession.builder.master("local").appName("localTests").getOrCreate()


@fixture
def spark():
    return SPARK.getActiveSession()
