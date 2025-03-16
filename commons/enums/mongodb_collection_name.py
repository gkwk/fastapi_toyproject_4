from enum import Enum


class MongoDBCollectionName(str, Enum):
    LLM_PROMPTS = "llm_prompts"
    TEXT_TO_IMAGE_MODEL_PROMPTS = "text_to_image_model_prompts"


print(isinstance("dd", MongoDBCollectionName))
print(isinstance(MongoDBCollectionName.LLM_PROMPTS, MongoDBCollectionName))
