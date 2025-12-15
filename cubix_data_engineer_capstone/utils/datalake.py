"""Azure Data Lake integration utilities."""

from typing import Any
from pyspark.sql import DataFrame, SparkSession
from .config import Config


class DataLakeClient:
    """Client for interacting with Azure Data Lake Storage."""
    
    def __init__(self, spark: SparkSession, config: Config | None = None):
        """
        Initialize the Data Lake client.
        
        Args:
            spark: Active SparkSession.
            config: Optional configuration object. If None, loads from environment.
        """
        if config is None:
            config = Config.from_env()
        
        self.spark = spark
        self.storage_account = config.storage_account_name
        self.container = config.container_name
        self._base_path = self._build_base_path()
    
    def _build_base_path(self) -> str:
        """Build the base ABFS path for the data lake."""
        if not self.storage_account:
            raise ValueError(
                "Storage account name is required. "
                "Set STORAGE_ACCOUNT_NAME environment variable."
            )
        return f"abfss://{self.container}@{self.storage_account}.dfs.core.windows.net"
    
    def read_parquet(self, path: str) -> DataFrame:
        """
        Read a Parquet file from the data lake.
        
        Args:
            path: Relative path to the Parquet file/directory.
            
        Returns:
            Spark DataFrame containing the data.
        """
        full_path = f"{self._base_path}/{path}"
        return self.spark.read.parquet(full_path)
    
    def write_parquet(
        self, 
        df: DataFrame, 
        path: str, 
        mode: str = "overwrite",
        partition_by: list[str] | None = None
    ) -> None:
        """
        Write a DataFrame to the data lake as Parquet.
        
        Args:
            df: DataFrame to write.
            path: Relative path for the output.
            mode: Write mode ('overwrite', 'append', 'error', 'ignore').
            partition_by: Optional list of columns to partition by.
        """
        full_path = f"{self._base_path}/{path}"
        writer = df.write.mode(mode)
        
        if partition_by:
            writer = writer.partitionBy(*partition_by)
        
        writer.parquet(full_path)
    
    def read_delta(self, path: str) -> DataFrame:
        """
        Read a Delta table from the data lake.
        
        Args:
            path: Relative path to the Delta table.
            
        Returns:
            Spark DataFrame containing the data.
        """
        full_path = f"{self._base_path}/{path}"
        return self.spark.read.format("delta").load(full_path)
    
    def write_delta(
        self,
        df: DataFrame,
        path: str,
        mode: str = "overwrite",
        partition_by: list[str] | None = None
    ) -> None:
        """
        Write a DataFrame to the data lake as Delta.
        
        Args:
            df: DataFrame to write.
            path: Relative path for the output.
            mode: Write mode ('overwrite', 'append', 'error', 'ignore').
            partition_by: Optional list of columns to partition by.
        """
        full_path = f"{self._base_path}/{path}"
        writer = df.write.format("delta").mode(mode)
        
        if partition_by:
            writer = writer.partitionBy(*partition_by)
        
        writer.save(full_path)
