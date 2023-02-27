"""
- data type check, 
- finding unwanted data, 
- cleaning the data

We will build a pipline anticipating some cases
"""
import pandas as pd
import numpy as np
import os, sys
from typing import Optional
from scipy.stats import ks_2samp

from Insurance.entity import artifact_entity, config_entity
from Insurance.exception import InsuranceException
from Insurance.logger import lg
from Insurance.config import TARGET_COLUMN
from Insurance import utils

class DataValidation:
    def __init__(
            self, 
            data_validation_config: config_entity.DataValidationConfig,
            data_ingestion_artifact: artifact_entity.DataIngestionArtifact):
        try:
            lg.info(f"{'**'*10} | ** -- Data Validation -- ** | {'**'*10}")
            self.data_validation_config= data_validation_config
            self.data_ingestion_artifact= data_ingestion_artifact
            self.validation_error = dict()

        except Exception as e:
            raise InsuranceException(e, sys)
        
    def drop_missing_values_columns(self, df: pd.DataFrame, report_key_name: str)->Optional[pd.DataFrame]:
        try:
            threshold = self.data_validation_config.missing_threshold
            null_report= df.isna().sum() / df.shape[0]
            drop_columns_names = null_report[null_report > threshold].index
            
            self.validation_error[report_key_name] = list(drop_columns_names)
            df.drop(list(drop_columns_names), axis= 1, inplace= True)

            if len(df.columns) == 0:
                return None
            return df
        except Exception as e:
            raise InsuranceException(e, sys)

    def do_required_columns_exist(self, base_df: pd.DataFrame, current_df: pd.DataFrame, report_key_name: str)->bool:
        try:
            base_columns = base_df.columns
            current_columns= current_df.columns

            missing_columns = []
            for base_col in base_columns:
                if base_col not in current_columns:
                    lg.info(f"Column: [{base_col} is not available ]")
                    missing_columns.append(base_col)

            if len(missing_columns)> 0:
                self.validation_error[report_key_name] = missing_columns
                return False
            return True
            
        except Exception as e:
            raise InsuranceException(e, sys)


    def data_drift(self, base_df: pd.DataFrame, current_df: pd.DataFrame, report_key_name: str):
        try:
            drift_report = dict()

            base_columns = base_df.columns
            current_columns = current_df.columns

            for base_col in base_columns:
                base_data, current_data = base_df[base_col], current_df[base_col]

                same_distribution = ks_2samp(base_data, current_data)

                if same_distribution.pvalue > 0.05:
                    # Null hypothesis accept
                    drift_report[base_col] = {"pvalues": float(same_distribution.pvalue), "same_distribution": True}
                else:
                    # alternate hypothesis accept
                    drift_report[base_col] = {"pvalues": float(same_distribution.pvalue), "same_distribution": False}

            self.validation_error[report_key_name]= drift_report

        except Exception as e:
            raise InsuranceException(e, sys)


    def initiate_data_validation(self)-> artifact_entity.DataValidationArtifact:
        try:
            lg.info(f"Reading base dataframe")
            base_df = pd.read_csv(self.data_validation_config.base_file_path)
            base_df.replace({"na": np.NAN}, inplace=True)
            lg.info(f"Replace na value in base df")
            #base_df has na as null
            lg.info(f"Drop null values colums from base df")
            base_df=self.drop_missing_values_columns(df=base_df,report_key_name="missing_values_within_base_dataset")

            lg.info(f"Reading train dataframe")
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            lg.info(f"Reading test dataframe")
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            lg.info(f"Drop null values colums from train df")
            train_df = self.drop_missing_values_columns(df=train_df,report_key_name="missing_values_within_train_dataset")
            lg.info(f"Drop null values colums from test df")
            test_df = self.drop_missing_values_columns(df=test_df,report_key_name="missing_values_within_test_dataset")
            
            exclude_columns = [TARGET_COLUMN]
            base_df = utils.convert_columns_float(df=base_df, exclude_columns=exclude_columns)
            train_df = utils.convert_columns_float(df=train_df, exclude_columns=exclude_columns)
            test_df = utils.convert_columns_float(df=test_df, exclude_columns=exclude_columns)


            lg.info(f"Are all required columns present in train df")
            train_df_columns_status = self.do_required_columns_exist(base_df=base_df, current_df=train_df,report_key_name="missing_columns_within_train_dataset")
            lg.info(f"Are all required columns present in test df")
            test_df_columns_status = self.do_required_columns_exist(base_df=base_df, current_df=test_df,report_key_name="missing_columns_within_test_dataset")

            if train_df_columns_status:
                lg.info(f"As all column are available in train df hence detecting data drift")
                self.data_drift(base_df=base_df, current_df=train_df, report_key_name="data_drift_within_train_dataset")
            if test_df_columns_status:
                lg.info(f"As all column are available in test df hence detecting data drift")
                self.data_drift(base_df=base_df, current_df=test_df, report_key_name="data_drift_within_test_dataset")
          
            #write the report
            lg.info("Write report in yaml file")
            utils.write_yaml_file(file_path=self.data_validation_config.report_file_path, data=self.validation_error)

            data_validation_artifact = artifact_entity.DataValidationArtifact(report_file_path=self.data_validation_config.report_file_path,)
            lg.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact
        
        except Exception as e:
            raise InsuranceException(e, sys)
