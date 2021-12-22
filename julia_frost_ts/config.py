from dataclasses import dataclass

from cognite.extractorutils.configtools import BaseConfig, StateStoreConfig


@dataclass
class ExtractorConfig:
    state_store: StateStoreConfig = StateStoreConfig()


@dataclass
class FrostConfig:
    client_id: str
    endpoint: str
    sources: str
    referencetime: str
    elements: str
    action: str
    ts_external_id: str


@dataclass
class Config(BaseConfig):
    frost: FrostConfig
    extractor: ExtractorConfig = ExtractorConfig()
