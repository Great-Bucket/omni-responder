import os
from dataclasses import dataclass

@dataclass
class SystemSettings:
    app_name: str = "Omni-Responder DGX Spark"
    target_hardware: str = "NVIDIA DGX Spark (Grace Blackwell 128GB Unified Memory)"
    vlm_model: str = "nvidia/cosmos-reason2-8b"
    # The LLM NIM deployed alongside the VLM on the Spark. It is NOT called by
    # this pipeline — orchestration is deterministic Python. Kept because the
    # deployment config in config/nim/ still launches it.
    orchestrator_llm: str = "nvidia/NVIDIA-Nemotron-Nano-9B-v2-FP8"
    # Set SPARK_HOST / NIM_ENDPOINT_URL / VSS_ENDPOINT_URL to your own Spark's
    # address. The defaults are placeholders and will not resolve.
    spark_host: str = os.getenv("SPARK_HOST", "http://<DGX_IP_ADDRESS>:3000")
    nim_endpoint_url: str = os.getenv("NIM_ENDPOINT_URL", "http://<DGX_IP_ADDRESS>:3000/v1")
    vss_endpoint_url: str = os.getenv("VSS_ENDPOINT_URL", "http://<DGX_IP_ADDRESS>:3000")
    hazmat_db_path: str = "data/hazmat_db.json"
    mock_traffic_api_url: str = "http://localhost:9000/api/v1/traffic"

settings = SystemSettings()
