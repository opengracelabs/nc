from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class RawRecord:
    """A single record as returned by a source, before normalization."""
    source_id: str          # the source's own identifier for this record
    payload: dict[str, Any] # raw response fields


@dataclass
class FetchResult:
    source: str
    run_id: str
    records: list[RawRecord]
    raw_bytes: bytes        # full serialized response for MinIO storage
    total: int              # total records reported by source (may differ from len(records))
    errors: list[str] = field(default_factory=list)


class BaseSource(ABC):
    source_id: str

    @abstractmethod
    async def fetch(self, config: dict[str, Any], run_id: str) -> FetchResult:
        """Fetch all records from the source. Must be idempotent."""
        ...
