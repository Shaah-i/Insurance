import os, sys
from typing import Optional
import xgboost as xg
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, f1_score
import pandas as pd
import numpy as np

from Insurance import utils
from Insurance.logger import lg
from Insurance.exception import InsuranceException
from Insurance.entity import artifact_entity, config_entity
from Insurance.config import TARGET_COLUMN
from Insurance.predictor import ModelResolver

class ModelEvaluation:

    def __init__(self, model_evaluation_config: config_entity.ModelEvaluationConfig, data_ingestion_artifact: artifact_entity.DataIngestionArtifact, data_transformation_artifact: artifact_entity.DataTransformationArtifact, model_trainer_artifact: artifact_entity.ModelTrainerArtifact):
        try:
            lg.info(f"{'**'*10} | ** -- Model Evaluation -- ** | {'**'*10}")
            self.model_evaluation_config = model_evaluation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_artifact= data_transformation_artifact
            self.model_trainer_artifact = model_trainer_artifact
            self.model_resolver = ModelResolver()

        except Exception as e:
            raise InsuranceException(e, sys)
        
    def initiate_model_evaluation(self)-> artifact_entity.ModelEvaluationArtifact:
        try:
            latest_dir_path = self.model_resolver.get_latest_dir_path()

            if latest_dir_path == None:
                model_eval_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted= True, improved_accuracy= None)
                lg.info(f"Model evaluation artifact: {model_eval_artifact}")

                return model_eval_artifact
            
        except Exception as e:
            raise InsuranceException(e, sys)