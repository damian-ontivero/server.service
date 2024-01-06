from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Query:
    def to_dict(self) -> dict[str, any]:
        return asdict(self)
