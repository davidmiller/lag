"""
Generic Utility functions for LAG
"""

import random


def qs_rand(queryset):
    """
    Return a random item from the queryset

    Arguments:
    - `queryset`:
    """
    qs_index = random.randrange(0, queryset.count())
    return queryset[qs_index]
