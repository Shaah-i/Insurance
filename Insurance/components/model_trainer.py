"""
- Model definition and training
- Current accuracy 80, say new model has 65, 68, 60 etc.
- threshold of 70, so accuracy equal to or above 70  can be accepted or else rejected
- Overfitting and underfitting
"""

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

class ModelTrainer:

    def __init__(self, model_trainer_config: config_entity.ModelTrainerConfig, data_transformation_artifact: artifact_entity.DataTransformationArtifact):
        try:
            lg.info(f"{'**'*10} | ** -- Model Trainer -- ** | {'**'*10}")
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact= data_transformation_artifact

        except Exception as e:
            raise InsuranceException(e, sys)
        
    def fine_tune(self):
        """
        GridSearch CV
        """
        try:
            pass
        except Exception as e:
            raise InsuranceException(e, sys)
        
    def train_model(self, X, y):
        try:
            lr = LinearRegression()
            lr.fit(X, y)
            return lr
        except Exception as e:
            raise InsuranceException(e, sys)
        
    def initiate_model_trainer(self)-> artifact_entity.ModelTrainerArtifact:
        try:
            lg.info(f"Loading train and test array")
            train_arr = utils.load_numpy_array_data(file_path= self.data_transformation_artifact.transform_train_path)
            test_arr = utils.load_numpy_array_data(file_path= self.data_transformation_artifact.transform_test_path)

            lg.info(f"Splitting input and target features from both train and test array")
            # X_train, y_train = pd.DataFrame(train_arr).drop(TARGET_COLUMN, axis=1), pd.DataFrame(train_arr)[TARGET_COLUMN]
            # X_test, y_test = pd.DataFrame(test_arr).drop(TARGET_COLUMN, axis=1), pd.DataFrame(test_arr)[TARGET_COLUMN]
            X_train, y_train = train_arr[:,:-1],train_arr[:,-1]
            X_test, y_test = test_arr[:,:-1],test_arr[:,-1]

            lg.info(f"Train the model")
            model = self.train_model(X= X_train, y= y_train)

            lg.info(f"Calculating R2 and f1 train score")
            yhat_train = model.predict(X_train)
            r2_train_score = r2_score(y_true= y_train, y_pred= yhat_train)
            # f1_train_score = f1_score(y_true= y_train, y_pred= yhat_train)

            lg.info(f"Calculating R2 and f1 test score")
            yhat_test = model.predict(X_test)
            r2_test_score = r2_score(y_true= y_test, y_pred= yhat_test)
            # f1_test_score = f1_score(y_true= y_test, y_pred= yhat_test)

            lg.info(f"Train R2 score: {r2_train_score} and Test R2 score: {r2_test_score}")
            # lg.info(f"Train f1 score: {f1_train_score} and Test f1 score: {f1_test_score}")

            # Check for overfitting or underfitting or expected score
            lg.info("Checking if our model is underfitting or not")
            if r2_test_score < self.model_trainer_config.expected_accuracy:
                raise Exception(f"Model is not good as it is not able to give expected accuracy: {self.model_trainer_config.expected_accuracy}, model actual score: {r2_test_score}")
            
            lg.info("Checking if our model is overfitting or not")
            diff = abs(r2_train_score - r2_test_score)

            if diff > self.model_trainer_config.overfitting_threshold:
                raise Exception(f"Train and test score difference: {diff} is more than overfitting threshold: {self.model_trainer_config.overfitting_threshold}")
            
            # Save the trained model
            lg.info("Saving the model object")
            utils.save_object(file_path= self.model_trainer_config.model_path, obj= model)

            # Prepare artifact
            lg.info("Prepareing the artifact")
            model_trainer_artifact = artifact_entity.ModelTrainerArtifact(model_path= self.model_trainer_config.model_path, r2_train_score= r2_train_score, r2_test_score= r2_test_score)

            lg.info(f"Model trainer artifact: {model_trainer_artifact}")

            return model_trainer_artifact


        except Exception as e:
            raise InsuranceException(e, sys)
        
    