from cognite.extractorutils import Extractor
from dotenv import load_dotenv

from julia_frost_ts.config import Config
from julia_frost_ts.extractor import run_extractor

from . import __version__

load_dotenv()


def main() -> None:
    with Extractor(
        name="julia_frost_ts",
        description="weather data to time series data in CDF",
        config_class=Config,
        run_handle=run_extractor,
        version=__version__,
    ) as extractor:
        extractor.run()


if __name__ == "__main__":
    main()
