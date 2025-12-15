"""Authentication and Spark session management."""

from pyspark.sql import SparkSession
from .config import Config


def get_spark_session(config: Config | None = None) -> SparkSession:
    """
    Create and return a configured Spark session.
    
    Args:
        config: Optional configuration object. If None, loads from environment.
        
    Returns:
        Configured SparkSession instance.
    """
    if config is None:
        config = Config.from_env()
    
    builder = SparkSession.builder.appName(config.app_name)
    
    # Configure for Azure Data Lake if credentials are provided
    if config.storage_account_name and config.storage_account_key:
        builder = builder.config(
            f"fs.azure.account.key.{config.storage_account_name}.dfs.core.windows.net",
            config.storage_account_key
        )
    
    return builder.getOrCreate()


def stop_spark_session(spark: SparkSession) -> None:
    """Stop the Spark session gracefully."""
    if spark is not None:
        spark.stop()
