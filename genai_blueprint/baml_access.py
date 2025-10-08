from genai_tk.utils.pydantic.kv_store import PydanticStore

from genai_blueprint.hackathon.baml_client.types import ExtractedContractInformation
from genai_blueprint.hackathon.baml_client import b
from dotenv import load_dotenv
from rich import print  # noqa: F401
load_dotenv()
from genai_tk.utils.config_mngr import global_config

def extract_legal_information (md_file: str) -> str: 
    """ Takes a Markdown file, use an LLM to extract information related to risks ,and 
    return a ExtractedContractInformation object as JSON"""
    synt_contract = b.ExtractLegalContract(md_file)
    result = synt_contract.model_dump_json(indent=2)
    return result


def resume_contract (json_content: str) -> str: 
    result = b.ResumeRisk(json_content)
    return result


def test():
    # contract_store = PydanticStore(kvstore_id="file", model=ExtractedContractInformation)

    # list_contracts = list(contract_store.get_kv_store().yield_keys())
    # print(list_contracts)

    # # Remove .json extension from the key (it's already encoded)
    # first_key = list_contracts[0]
    # if first_key.endswith(".json"):
    #     contract0_key = first_key[:-5]  # Remove .json extension
    # else:
    #     contract0_key = first_key


    root_path = global_config().get_dir_path("paths.team_sp")
    assert root_path.exists()
    test_file_path = root_path / "data/generated" / "EXEMPLE DE CONTRAT 3 - 102024-UBIKA-Conditions-Generales-de-Licence.md"
    assert test_file_path.exists()
    test_file = test_file_path.read_text()
    extracted = extract_legal_information(test_file)

    print(extracted)

    resumed =resume_contract(extracted)
    print(resumed)



if __name__ == "__main__": 
    test()