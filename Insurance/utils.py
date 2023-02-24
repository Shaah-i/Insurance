import pandas as pd
import numpy as np
import os, sys

from Insurance.exception import InsuranceException
from Insurance.config import mongo_client
from Insurance.logger import lg


def get_collection_as_dataframe(database_name:str,collection_name:str)->pd.DataFrame:
    """
    Description: This function return collection as dataframe
    =========================================================
    Params:
    database_name: database name
    collection_name: collection name
    =========================================================
    return Pandas dataframe of a collection
    """
    try:
        lg.info(f"Reading data from database: {database_name} and collection: {collection_name}")
        df = pd.DataFrame(list(mongo_client[database_name][collection_name].find()))
        lg.info(f"Found columns: {df.columns}")
        if "_id" in df.columns:
            lg.info(f"Dropping column: _id ")
            df = df.drop("_id",axis=1)
        lg.info(f"Row and columns in df: {df.shape}")
        return df
    except Exception as e:
        raise InsuranceException(e, sys)
    