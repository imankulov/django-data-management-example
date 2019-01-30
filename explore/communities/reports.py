import datetime
from collections import defaultdict, Counter

import pandas as pd

from explore.communities.models import Group


def top_groups():
    """
    Get a dataframe with top groups in Portugal, sorted by the number of
    members
    """
    groups = Group.objects.filter(country='PT').order_by('-members')[:10]
    df = pd.DataFrame.from_records(groups.values())
    return df


def meetup_groups_growth():
    """
    Get a dataframe outlining the meetup groups growth in Portugal. For
    every month it shows the number of meetup groups in each city.

    The dataframe contains city names as columns and dates as rows
    """
    # groups we are interested in.
    groups = list(Group.objects.filter(country='PT').order_by('created'))

    # take the start and end dates for the group dynamic
    start = groups[0].created
    end = datetime.datetime.utcnow().replace(tzinfo=start.tzinfo)

    # counter, which will have a structure like this:
    # {"Lisbon": {"2012-01-01": 1, "2012-02-01": 5}}
    # every edge value represents the number of groups in the specific city
    # for a specific moment in time
    group_counter = defaultdict(lambda: Counter())

    # date range, essentially a list with datetimes for every month
    # from start to end
    idx = pd.date_range(start=start, end=end, freq='M', normalize=True)

    # populate the counter
    for moment in idx:
        for group in groups:
            if group.created <= moment:
                group_counter[group.city][moment] += 1

    # convert this to a dataframe and replace all missing values with 0's
    df = pd.DataFrame.from_dict(group_counter).fillna(0).astype(int)
    # sort columns from "most active" to "least active" city at the moment
    df = df.sort_values(axis=1, by=df.index[-1], ascending=False)
    return df


def meetup_groups_dynamic(growth_df):
    """
    Get the group dynamic dataframe, which represents a normalized
    (in percents) impact of each city to the total number of communities
    in Portugal.

    Take the output of "meetup_groups_growth"

    The dataframe structure of the output is the same as for the input, but
    returned values contain percents instead of absolute values
    """

    def convert_to_percent(row):
        total_groups = row.sum()
        return row.apply(lambda x: x * 100 / total_groups)

    return growth_df.apply(convert_to_percent, axis=1)
