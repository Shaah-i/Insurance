"""
- if accuracy > previous then model accepted
- save model
"""

import sys
from sklearn.metrics import r2_score
import pandas as pd
import numpy as np

from Insurance.logger import lg
from Insurance.exception import InsuranceException
from Insurance.entity import artifact_entity, config_entity
from Insurance.config import TARGET_COLUMN
from Insurance.predictor import ModelResolver
from Insurance.utils import load_object

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
            
            # Find location of previous model
            transformer_path = self.model_resolver.get_latest_transformer_path()
            model_path = self.model_resolver.get_latest_model_path()
            target_encoder_path = self.model_resolver.get_latest_target_encoder_path()

            # for previous model
            model = load_object(file_path= model_path)
            transformer = load_object(file_path= transformer_path)
            
            # model = load_object(file_path= model_path)
            target_encoder= load_object(file_path= target_encoder_path)

            print(transformer_path, transformer)
            print(model_path, model)
            print(target_encoder_path, target_encoder)

            # for new model
            current_transformer = load_object(file_path= self.data_transformation_artifact.transform_object_path)
            current_model = load_object(file_path= self.model_trainer_artifact.model_path)
            current_target_encoder= load_object(file_path= self.data_transformation_artifact.target_encoder_path)

            # print(self.data_transformation_artifact.transform_object_path, current_transformer)
            # print(self.model_trainer_artifact.model_path,current_model)
            # print(self.data_transformation_artifact.target_encoder_path, current_target_encoder)

            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            target_df = test_df[TARGET_COLUMN]
            y_true = target_df
            
            # Accuracy previous model
            input_feature_name = list(transformer.feature_names_in_)
            for i in input_feature_name:
                if test_df[i].dtypes == "object":
                    test_df[i] = target_encoder.fit_transform(test_df[i])
            input_arr = transformer.transform(test_df[input_feature_name])
            y_pred = model.predict(input_arr)
            
            
            previous_model_score = r2_score(y_true= y_true, y_pred= y_pred)

            # Accuracy current model
            input_feature_name = list(current_transformer.feature_names_in_)
            input_arr = current_transformer.transform(test_df[input_feature_name])
            y_pred = current_model.predict(input_arr)
            y_true = target_df

            current_model_score = r2_score(y_true= y_true, y_pred=y_pred)

            # Comparison b/w new model and old model
            if current_model_score <= previous_model_score:
                lg.info("Current model is not better than previous model")
                raise Exception("Current model is not better than previous model")
            
            model_eval_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted= True, improved_accuracy= current_model_score - previous_model_score)

            return model_eval_artifact

        except Exception as e:
            raise InsuranceException(e, sys)