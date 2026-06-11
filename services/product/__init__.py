"""NC-PRODUCT-001 product runtime domain helpers."""

from .catalog import PRODUCT_RUNTIME_VERSION
from .export import build_publication_snapshot
from .rights_gate import verify_candidate_gates
from .template import verify_template_dimensions

__all__ = [
    "PRODUCT_RUNTIME_VERSION",
    "build_publication_snapshot",
    "verify_candidate_gates",
    "verify_template_dimensions",
]
