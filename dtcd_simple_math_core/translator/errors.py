# -*- coding: utf-8 -*-
"""This module stores custom exceptions for this plugin.
"""


class OTLReadfileError(Exception):
    """Exception when there is

     "Job[9d116b48-1106-11ee-917f-0242ac140006] failed because of [SearchId:11866]
     Error in  'readfile' command."

     error"""
    pass


class OTLJobWithStatusNewHasNoCacheID(Exception):
    """Exception when there is a

    'Job with status new has no cache id'

    error"""
    pass


class OTLSubsearchFailed(Exception):
    """Exception when there is a

     'Job[d647dd24-119d-11ee-9d6c-0242ac140006] failed because of [SearchId:12350]
     Subsearch failed. Check logs..'

     error"""
    pass
