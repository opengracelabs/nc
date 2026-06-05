from typing import Any
from pydantic import Field
from ..core.base import NCBase, NCRecord

class PlaceKnowledgeProfile(NCRecord):
    """
    Formal representation of the complete knowledge and asset record for a Place.
    Aligns with CIDOC CRM (E53 Place) and Darwin Core (DwC) for cross-domain coherence.
    Discussion shorthand: 'Place Genome'.
    """
    place_id: str = Field(description="Foreign key to core.Place record")
    
    # CIDOC CRM Alignment (Cultural Heritage)
    cultural_heritage_profile: dict[str, Any] = Field(
        default_factory=dict, 
        description="Mappings to E53 Place and related CIDOC CRM classes"
    )
    
    # Darwin Core Alignment (Natural History)
    natural_heritage_profile: dict[str, Any] = Field(
        default_factory=dict, 
        description="Mappings to DwC Taxon, Occurrence, and Event classes"
    )
    
    # Asset Coverage Matrix (Place Asset Profile)
    asset_coverage: dict[str, bool] = Field(
        default_factory=dict,
        description="Matrix of required vs covered asset classes (NH, FA, HM, PH, etc.)"
    )
    
    # Metadata Standards
    standards_alignment: dict[str, str] = Field(
        default_factory=dict,
        description="Mapping to Schema.org, IIIF, and CIDOC CRM URIs"
    )

