import os
from os.path import dirname

from ai.CRAFT.try_test import load_model


class AreaSuggestion(object):
    script_dir = dirname(__file__)
    rel_path = "./CRAFT/craft_mlt_25k.pth"
    model = os.path.join(script_dir, rel_path)
    net = load_model(model)
