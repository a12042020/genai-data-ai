from json import tool
from hackathon.baml_client.types import ExtractedContractInformation


store = PydanticStore()

store.get("")
c = AnalyseLegalContract

@tool
def analyse_legal_contract(doc: str) 

