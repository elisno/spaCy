from typing import Union, Iterable, Dict, Any
from pathlib import Path
import warnings
import sys

warnings.filterwarnings("ignore", message="numpy.dtype size changed")  # noqa
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")  # noqa

# These are imported as part of the API
from thinc.api import prefer_gpu, require_gpu  # noqa: F401
from thinc.api import Config

from . import pipeline  # noqa: F401
from .cli.info import info  # noqa: F401
from .glossary import explain  # noqa: F401
from .about import __version__  # noqa: F401
from .util import registry, logger  # noqa: F401

from .errors import Errors
from .language import Language
from . import util


if sys.maxunicode == 65535:
    raise SystemError(Errors.E130)


def load(
    name: Union[str, Path],
    disable: Iterable[str] = util.SimpleFrozenList(),
    exclude: Iterable[str] = util.SimpleFrozenList(),
    config: Union[Dict[str, Any], Config] = util.SimpleFrozenDict(),
) -> Language:
    """Load a spaCy model from an installed package or a local path.

    name (str): Package name or model path.
    disable (Iterable[str]): Names of pipeline components to disable. Disabled
        pipes will be loaded but they won't be run unless you explicitly
        enable them by calling nlp.enable_pipe.
    exclude (Iterable[str]): Names of pipeline components to exclude. Excluded
        components won't be loaded.
    config (Dict[str, Any] / Config): Config overrides as nested dict or dict
        keyed by section values in dot notation.
    RETURNS (Language): The loaded nlp object.
    """
    return util.load_model(name, disable=disable, exclude=exclude, config=config)


def blank(
    name: str, *, config: Union[Dict[str, Any], Config] = util.SimpleFrozenDict()
) -> Language:
    """Create a blank nlp object for a given language code.

    name (str): The language code, e.g. "en".
    config (Dict[str, Any] / Config): Optional config overrides.
    RETURNS (Language): The nlp object.
    """
    LangClass = util.get_lang_class(name)
    return LangClass.from_config(config)
