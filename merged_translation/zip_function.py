from collections import OrderedDict
from typing import Dict


def dictZip(*dictionaries: Dict):
    """If key is not found, then the element is skipped"""
    keys = OrderedDict()
    for d in dictionaries:
        for k in d.keys():
            keys[k] = None

    for k in keys:
        values = []
        for d in dictionaries:
            # cannot use get method, because ConfigParser has different get signature
            try:
                val = d[k]
            except KeyError:
                continue
            values.append(val)

        yield k, tuple(values)
