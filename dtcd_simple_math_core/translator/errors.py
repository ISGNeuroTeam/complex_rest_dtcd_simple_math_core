# -*- coding: utf-8 -*-
"""This module stores custom exceptions for this plugin.
"""


class OTLReadfileError(Exception):
    """Exception when there is

     "Job[9d116b48-1106-11ee-917f-0242ac140006] failed because of [SearchId:11866]
     Error in  'readfile' command."

     error"""
    ...


class OTLJobWithStatusNewHasNoCacheID(Exception):
    """Exception when there is a

    'Job with status new has no cache id'

    error"""
    ...


class OTLJobWithStatusFailedHasNoCacheID(Exception):
    """Exception when there is a

    'Job with status new has no cache id'

    error"""
    ...


class OTLSubsearchFailed(Exception):
    """Exception when there is a

     'Job[d647dd24-119d-11ee-9d6c-0242ac140006] failed because of [SearchId:12350]
     Subsearch failed. Check logs..'

     error"""
    ...


class LackingPathNameError(Exception):
    # pylint: disable=line-too-long
    """Exception when there is no path name provided

    Usually when we create query for writing swt and use template query
    from dtcd_simple_math_core.conf:[graph_globals]:otl_create_fresh_swt

    otl_create_fresh_swt = | makeresults count=1 | eval _sn=1 | eval _t=_time | writeFile format=json path=SWT/

    and add path name to the end of that line. But if we send this query without added path name,
    then otl will calc that query and delete all the SWT folder, so we must not allow that to happen.

    So if path name is not given we must raise error and try again.
    """
    ...


class OTLServiceUnavailable(Exception):
    """Exception when there is a

     'Job[d647dd24-119d-11ee-9d6c-0242ac140006] failed because of [SearchId:12350]
     Subsearch failed. Check logs..'

     error"""
    ...
