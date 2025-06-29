from sensor.predictor import ModelResolver
from sensor.entity.config_entity import ModelPusherConfig
from sensor.exception import SensorException
import os, sys
from sensor.utils import load_object, save_object
from sensor.logger import logging
from sensor.entity.artifact_entity import (
    DataTransformationArtifact,
    ModelTrainerArtifact,
    ModelPusherArtifact,
)


class ModelPusher:

    def __init__(
        self,
        model_pusher_config: ModelPusherConfig,
        data_transformation_artifact: DataTransformationArtifact,
        model_trainer_artifact: ModelTrainerArtifact,
    ):
        try:
            logging.info(f"{'>>'*20} Model Pusher {'<<'*20}")
            self.model_pusher_config = model_pusher_config
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_artifact = model_trainer_artifact
            self.model_resolver = ModelResolver(
                model_registry=self.model_pusher_config.saved_model_dir
            )
        except Exception as e:
            raise SensorException(e, sys)

    def initiate_model_pusher(self) -> ModelPusherArtifact:
        try:
            # Load objects
            logging.info(f"Loading transformer, model and target encoder")
            transformer = load_object(
                file_path=self.data_transformation_artifact.transform_object_path
            )
            model = load_object(file_path=self.model_trainer_artifact.model_path)
            target_encoder = load_object(
                file_path=self.data_transformation_artifact.target_encoder_path
            )

            # Save to model pusher directory (artifact directory)
            logging.info(f"Saving model into model pusher directory")

            # Ensure pusher directories exist
            os.makedirs(
                os.path.dirname(self.model_pusher_config.pusher_transformer_path),
                exist_ok=True,
            )
            os.makedirs(
                os.path.dirname(self.model_pusher_config.pusher_model_path),
                exist_ok=True,
            )
            os.makedirs(
                os.path.dirname(self.model_pusher_config.pusher_target_encoder_path),
                exist_ok=True,
            )

            save_object(
                file_path=self.model_pusher_config.pusher_transformer_path,
                obj=transformer,
            )
            save_object(file_path=self.model_pusher_config.pusher_model_path, obj=model)
            save_object(
                file_path=self.model_pusher_config.pusher_target_encoder_path,
                obj=target_encoder,
            )

            # Save to saved_models directory with incremental numbering
            logging.info(
                f"Saving model in saved_models directory with incremental numbering"
            )

            # Get all paths for the same directory (prevents creating multiple directories)
            save_paths = self.model_resolver.get_latest_save_paths()

            transformer_path = save_paths["transformer_path"]
            model_path = save_paths["model_path"]
            target_encoder_path = save_paths["target_encoder_path"]

            # Save the objects to the incremental directory
            save_object(file_path=transformer_path, obj=transformer)
            save_object(file_path=model_path, obj=model)
            save_object(file_path=target_encoder_path, obj=target_encoder)

            # Log the directory where models were saved
            saved_dir = os.path.dirname(model_path)
            logging.info(f"Models successfully saved to: {saved_dir}")
            logging.info(f"Directory number: {os.path.basename(saved_dir)}")

            model_pusher_artifact = ModelPusherArtifact(
                pusher_model_dir=self.model_pusher_config.pusher_model_dir,
                saved_model_dir=self.model_pusher_config.saved_model_dir,
            )
            logging.info(f"Model pusher artifact: {model_pusher_artifact}")
            return model_pusher_artifact

        except Exception as e:
            raise SensorException(e, sys)
