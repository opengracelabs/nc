from .base import BaseSource, FetchResult, RawRecord
from .unesco_whc import UnescoWHCSource
from .wikidata import WikidataSource

REGISTRY: dict[str, BaseSource] = {
    UnescoWHCSource.source_id: UnescoWHCSource(),
    WikidataSource.source_id: WikidataSource(),
}

__all__ = ["BaseSource", "FetchResult", "RawRecord", "REGISTRY"]
