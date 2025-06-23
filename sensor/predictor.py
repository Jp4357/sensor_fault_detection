import os
from sensor.entity.config_entity import (
    TRANSFORMER_OBJECT_FILE_NAME,
    MODEL_FILE_NAME,
    TARGET_ENCODER_OBJECT_FILE_NAME,
)
from glob import glob
from typing import Optional


class ModelResolver:

    def __init__(self, model_registry: str = "saved_models"):
        self.model_registry = model_registry
        os.makedirs(self.model_registry, exist_ok=True)

    def get_latest_dir_path(self) -> Optional[str]:
        try:
            dir_names = os.listdir(self.model_registry)
            if len(dir_names) == 0:
                return None

            # Filter only numeric directories and convert to int
            numeric_dirs = []
            for dir_name in dir_names:
                try:
                    numeric_dirs.append(int(dir_name))
                except ValueError:
                    continue  # Skip non-numeric directories

            if len(numeric_dirs) == 0:
                return None

            latest_folder_name = max(numeric_dirs)
            return os.path.join(self.model_registry, f"{latest_folder_name}")
        except Exception as e:
            raise e

    def get_latest_model_path(self):
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                raise Exception(f"Model is not available")
            return os.path.join(latest_dir, MODEL_FILE_NAME)
        except Exception as e:
            raise e

    def get_latest_transformer_path(self):
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                raise Exception(f"Transformer is not available")
            return os.path.join(latest_dir, TRANSFORMER_OBJECT_FILE_NAME)
        except Exception as e:
            raise e

    def get_latest_target_encoder_path(self):
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                raise Exception(f"Target Encoder is not available")
            return os.path.join(latest_dir, TARGET_ENCODER_OBJECT_FILE_NAME)
        except Exception as e:
            raise e

    def get_latest_save_dir_path(self):
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                # First time - create directory "0"
                new_dir_num = 0
            else:
                # Get latest directory number and increment by 1
                latest_dir_num = int(os.path.basename(latest_dir))
                new_dir_num = latest_dir_num + 1

            new_dir = os.path.join(self.model_registry, f"{new_dir_num}")

            # Create only the main numbered directory
            os.makedirs(new_dir, exist_ok=True)

            return new_dir
        except Exception as e:
            raise e

    def get_latest_save_paths(self):
        """
        Returns all three save paths for the same directory to avoid creating multiple directories
        """
        try:
            save_dir = self.get_latest_save_dir_path()
            return {
                "transformer_path": os.path.join(
                    save_dir, TRANSFORMER_OBJECT_FILE_NAME
                ),
                "model_path": os.path.join(save_dir, MODEL_FILE_NAME),
                "target_encoder_path": os.path.join(
                    save_dir, TARGET_ENCODER_OBJECT_FILE_NAME
                ),
            }
        except Exception as e:
            raise e

    def get_latest_save_model_path(self):
        try:
            latest_dir = self.get_latest_save_dir_path()
            return os.path.join(latest_dir, MODEL_FILE_NAME)
        except Exception as e:
            raise e

    def get_latest_save_transformer_path(self):
        try:
            latest_dir = self.get_latest_save_dir_path()
            return os.path.join(latest_dir, TRANSFORMER_OBJECT_FILE_NAME)
        except Exception as e:
            raise e

    def get_latest_save_target_encoder_path(self):
        try:
            latest_dir = self.get_latest_save_dir_path()
            return os.path.join(latest_dir, TARGET_ENCODER_OBJECT_FILE_NAME)
        except Exception as e:
            raise e


class Predictor:

    def __init__(self, model_resolver: ModelResolver):
        self.model_resolver = model_resolver
