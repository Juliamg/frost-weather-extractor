import datetime
from logging import Logger
from typing import List

import requests

from julia_frost_ts.config import Config


def calculate_referencetime(config: Config) -> str:
    client = config.cognite.get_cognite_client(config.cognite.project)
    latest = client.datapoints.retrieve_latest(external_id=config.frost.ts_external_id)
    latest = datetime.datetime.fromtimestamp((latest[0].timestamp) / 1000.0).date()
    referencetime = str(latest) + "/" + datetime.datetime.today().strftime("%Y-%m-%d")

    return referencetime


def structure_data(data: List[dict], logger: Logger) -> List:
    logger.info("Starting to structure data..")
    data_points = []
    for item in data:  # row is now a dict we want to unravel
        value = item["observations"][0]["value"]  # this should also go in config..
        time_stamp = datetime.datetime.strptime(item["referenceTime"], "%Y-%m-%dT%H:%M:%S.%fZ")
        data_points.append((time_stamp, value))
    return data_points


def get_datapoints(config: Config, logger: Logger) -> List:
    if config.frost.action == "update":
        referencetime = calculate_referencetime(config)
    elif config.frost.action == "create":
        referencetime = config.frost.referencetime
    else:
        logger.info("No reference time provided.. add action to config file")
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
