"""Configuration management for the project."""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    """Project configuration settings."""

    # Databricks settings
    databricks_host: Optional[str] = None
    databricks_token: Optional[str] = None

    # Data Lake settings
    storage_account_name: Optional[str] = None
    storage_account_key: Optional[str] = None
    container_name: str = "data"

    # Spark settings
    app_name: str = "CubixDataEngineerCapstone"

    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables."""
        return cls(
            databricks_host=os.getenv("DATABRICKS_HOST"),
            databricks_token=os.getenv("DATABRICKS_TOKEN"),
            storage_account_name=os.getenv("STORAGE_ACCOUNT_NAME"),
            storage_account_key=os.getenv("STORAGE_ACCOUNT_KEY"),
            container_name=os.getenv("CONTAINER_NAME", "data"),
            app_name=os.getenv("SPARK_APP_NAME", "CubixDataEngineerCapstone"),
        )
