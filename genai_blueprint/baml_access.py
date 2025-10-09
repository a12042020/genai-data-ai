from dotenv import load_dotenv
from genai_tk.utils.config_mngr import global_config
from rich import print  # noqa: F401

from genai_blueprint.hackathon.baml_client import b

load_dotenv()


def extract_legal_information(md_file: str) -> str:
    """Takes a Markdown file, use an LLM to extract information related to risks ,and
    return a ExtractedContractInformation object as JSON"""
    synt_contract = b.ExtractLegalContract(md_file)
    result = synt_contract.model_dump_json(indent=2)
    return result


def resume_contract(json_content: str) -> str:
    result = b.ResumeRisk(json_content)
    return result


def analyse_contract_kcp(json_content: str, kcp: str) -> str:
    result = b.KcpAnalysis(json_content, kcp)
    return result


def test():
    from genai_tk.utils.pydantic.kv_store import PydanticStore

    root_path = global_config().get_dir_path("paths.team_sp")
    assert root_path.exists()
    test_file_path = (
        root_path / "data/generated" / "EXEMPLE DE CONTRAT 3 - 102024-UBIKA-Conditions-Generales-de-Licence.md"
    )
    assert test_file_path.exists()
    test_file = test_file_path.read_text()
    extracted = extract_legal_information(test_file)

    print(extracted)

    resumed = resume_contract(extracted)
    print(resumed)

    global_config().set(
        "paths.team_sp", "${oc.env:ONEDRIVE, undefined_path}/Team Hackathon DATA&AI - Team Data AI Kackathon"
    )

    contract_store = PydanticStore(kvstore_id="file", model=ExtractedContractInformation)

    list_contracts = list(contract_store.get_kv_store().yield_keys())
    print(list_contracts)

    # Remove .json extension from the key (it's already encoded)
    first_key = list_contracts[0]
    if first_key.endswith(".json"):
        contract0_key = first_key[:-5]  # Remove .json extension
    else:
        contract0_key = first_key

    root_path = global_config().get_dir_path("paths.team_sp")
    assert root_path.exists()
    kcp_file_path = root_path / "data/kcp_example.md"
    assert kcp_file_path.exists()

    contract = contract_store.load_object(contract0_key)
    assert contract

    print("Analyse KCP:.....")

    analyse_contract_kcp(contract.model_dump_json(indent=2), kcp_file_path.read_text())


if __name__ == "__main__":
    test()
