from __future__ import annotations

import logging
import sys

_LOGGER_NAME = "semantic_search"

logger = logging.getLogger(_LOGGER_NAME)

if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )

    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False
