import datetime
from logging import Logger
from typing import List

import requests

from julia_frost_ts.config import Config


def get_referencetime(config: Config, logger: Logger) -> str:
    if config.frost.action == "update":
        client = config.cognite.get_cognite_client(config.cognite.project)
        # probably more optimal to just store this value in a text file
        latest = client.datapoints.retrieve_latest(external_id=config.frost.ts_external_id)
        latest = datetime.datetime.fromtimestamp((latest[0].timestamp) / 1000.0).date()
        referencetime = str(latest) + "/" + datetime.datetime.today().strftime("%Y-%m-%d")
        return referencetime
    elif config.frost.action == "create":
        return config.frost.referencetime
    else:
        logger.info("No reference time available.. check config")
        return ""


def structure_data(data: List[dict], logger: Logger) -> List:
    data_points = []
    for item in data:
        value = item["observations"][0]["value"]  # this should also go in config..
        time_stamp = datetime.datetime.strptime(item["referenceTime"], "%Y-%m-%dT%H:%M:%S.%fZ")
        data_points.append((time_stamp, value))
    return data_points


def get_datapoints(config: Config, logger: Logger) -> List:
    referencetime = get_referencetime(config, logger)
    logger.info(f"Extracting data for time period {referencetime}")
    parameters = {"sources": config.frost.sources, "referencetime": referencetime, "elements": config.frost.elements}
    r = requests.get(config.frost.endpoint, parameters, auth=(config.frost.client_id, ""))
    json = r.json()
    if r.status_code == 200:
        data = json["data"]  # Data is now a list of dicts
        logger.info("Data retrieved from frost.met.no!")
        return structure_data(data, logger)
    else:
        logger.info(f"Error! Returned status code {r.status_code}")
        logger.info(f"Message: {json['error']['message']}")
        logger.info(f"Reason: {json['error']['reason']}")
        raise Exception(f"Reason: {json['error']['reason']}")
