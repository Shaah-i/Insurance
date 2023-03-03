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
# from Insurance.entity import artifact_entity, config_entity
from Insurance.config import TARGET_COLUMN
from Insurance.predictor import ModelResolver
from Insurance.utils import load_object, save_object
from Insurance.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact, ModelPusherArtifact
from Insurance.entity.config_entity import ModelPusherConfig
from Insurance.predictor import ModelResolver

class ModelPusher:
    def __init__(self, model_pusher_config: ModelPusherConfig, data_transformation_artifact: DataTransformationArtifact, model_trainer_artifact: ModelTrainerArtifact):
        try:
            lg.info(f"{'**'*10} | ** -- Model Pusher -- ** | {'**'*10}")
            self.model_pusher_config= model_pusher_config
            self.data_transformation_artifact= data_transformation_artifact
            self.model_trainer_artifact = model_trainer_artifact
            self.model_resolver= ModelResolver(model_registry= self.model_pusher_config.saved_model_dir)

        except Exception as e:
            raise InsuranceException(e, sys)
        
    def initiate_model_pusher(self)->ModelPusherArtifact:
        try:
            # Model and target encoder data
            transformer= load_object(file_path= self.data_transformation_artifact.transform_object_path)
            model= load_object(file_path= self.model_trainer_artifact.model_path)
            target_encoder= load_object(file_path= self.data_transformation_artifact.target_encoder_path)

            # model pusher dir
            save_object(file_path= self.model_pusher_config.pusher_transformer_path, obj= transformer)
            save_object(file_path= self.model_pusher_config.pusher_model_path, obj= model)
            save_object(file_path= self.model_pusher_config.pusher_target_encoder_path, obj= target_encoder)

            # save model
            transform_path = self.model_resolver.get_latest_save_transformer_path()
            model_path = self.model_resolver.get_latest_save_model_path()
            target_encoder_path = self.model_resolver.get_latest_save_target_encoder_path()

            save_object(file_path= transform_path, obj= transformer)
            save_object(file_path= model_path, obj= model)
            save_object(file_path= target_encoder_path, obj= target_encoder)

            model_pusher_artifact= ModelPusherArtifact(pusher_model_dir= self.model_pusher_config.pusher_model_dir, saved_model_dir= self.model_pusher_config.saved_model_dir)

            lg.info(f"Model pusher artifact: {model_pusher_artifact}")

            return model_pusher_artifact

        except Exception as e:
            raise InsuranceException(e, sys)