from math import isnan
from pandas import Timestamp
from pandas._libs import NaTType


def panda_json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, Timestamp):
        return obj.isoformat()
    if isinstance(obj, NaTType):
        return None

    try:
        if isnan(obj):
            return None
    except:
        pass

    return obj