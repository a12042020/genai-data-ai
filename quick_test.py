from dotenv import load_dotenv
from genai_tk.core.embeddings_factory import EmbeddingsFactory
from genai_tk.utils.config_mngr import global_config

assert load_dotenv(verbose=True)

model = global_config().get("llm.models")
print(model)

print(EmbeddingsFactory.known_list())
