import io
import json
from snips_nlu import SnipsNLUEngine, load_resources
from snips_nlu.default_configs import CONFIG_EN
load_resources("en")
engine = SnipsNLUEngine(config=CONFIG_EN)
default_engine = SnipsNLUEngine()
