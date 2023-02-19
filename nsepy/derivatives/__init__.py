import datetime

import dateutil.relativedelta
import pandas

from .. import live


class ExpiryDateError(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(ExpiryDateError, self).__init__(message)


def is_valid_expiry(dt):
    # not a perfect logic :P
    if (dt.month != 2 and dt.day >= 23) or (dt.month == 2 and dt.day >= 21):
        return True


def get_expiry_date(year, month, index=True, stock=False):
    if not index ^ stock:
        raise ValueError("index and stock params have to be XOR. Both can't be True of False at the same time.")

    stexpiry = set()
    monthstart = datetime.datetime(year, month, 1).date()
    monthend = (monthstart + dateutil.relativedelta.relativedelta(months=1)) - dateutil.relativedelta.relativedelta \
        (days=1)

    # Indices have weekly expiry every Thursday. If Thursday is a holiday then the previous working day
    for d in pandas.date_range(start=monthstart, end=monthend, freq='W-THU').date:
        # Make sure its not a holiday
        stexpiry |= {live.nearestworkingday(d)}

    if index:
        # Indices have weekly expiry
        return stexpiry

    elif stock:
        # Indices have monthly expiry. Get last expirty of index
        return {max(stexpiry)}

    return stexpiry
