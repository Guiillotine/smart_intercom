from src.client.storages.postgres.utils import load_all_models
from src.common.models import CoreModel

load_all_models()

target_metadata = CoreModel.metadata
