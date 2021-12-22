import datetime
import logging
from threading import Event

from cognite.client import CogniteClient
from cognite.extractorutils.statestore import AbstractStateStore

from julia_frost_ts.config import Config
from julia_frost_ts.utils import get_datapoints

logger = logging.getLogger(__name__)


def run_extractor(cognite: CogniteClient, states: AbstractStateStore, config: Config, stop_event: Event) -> None:
    logger.info(
        f"Extracting content from {config.frost.endpoint}, uploading to timeseries {config.frost.ts_external_id}"
    )
    data_points = get_datapoints(config, logger)
    cognite.datapoints.insert(data_points, external_id=config.frost.ts_external_id)
    logger.info(f"Successfully inserted {len(data_points)} datapoints")
