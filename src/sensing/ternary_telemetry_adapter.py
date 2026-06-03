# path: crispy-mouse/src/sensing/ternary_telemetry_adapter.py
#!/usr/bin/env python3
"""
Ternary Telemetry Adapter for crispy-mouse

Routes kinematic and sensor telemetry through the BitNet-mlx
ternary projection layer before deterministic macro execution.
"""

import logging
from typing import Any, Dict, Optional

try:
    from bitnet_mlx.inference.ternary_pipeline import TernaryPipeline
    HAS_BITNET = True
except ImportError:
    HAS_BITNET = False

logging.basicConfig(level=logging.INFO, format="[*] %(asctime)s - %(message)s")


class TernaryTelemetryAdapter:
    """
    Projects kinematic/sensor data into ternary space before execution.
    """

    def __init__(self, output_dim: int = 64):
        if HAS_BITNET:
            self.pipeline = TernaryPipeline(output_dim=output_dim)
            logging.info("TernaryTelemetryAdapter initialized")
        else:
            self.pipeline = None
            logging.warning("BitNet-mlx not available. Ternary projection disabled.")

    def process_telemetry(self, data: Any, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if self.pipeline is None:
            return {"original_data": data, "ternary_projected": False}

        result = self.pipeline.run(data, metadata=metadata)
        result["ternary_projected"] = True
        return result

    def is_available(self) -> bool:
        return self.pipeline is not None
