from pyspark.sql import DataFrame, SparkSession


def read_file_from_volume(full_path: str, format: str) -> DataFrame:
    """Reads a file from UC Volume and returns it as a Spark DataFrame.

    :param full_path:   The path to the file on the volume.
    :param format:      The format of the file. Can be "csv", "parquet", "delta".
    :return:            DataFrame with the data.
    """
    if format not in ["csv", "parquet", "delta"]:
        raise ValueError(f"Invalid format: {format}. Supported formates are: csv, parquet, delta.")

    spark = SparkSession.getActiveSession()

    reader = spark.read.format(format)
    if format == "csv":
        reader = reader.option("header", "true")

    return reader.load(full_path)
