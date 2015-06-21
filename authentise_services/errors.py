"""Error classes for authentise_services"""


class ResourceError(Exception):
    """arbitrary error whenever a call to a authentise resource doesnt go according to plan"""
    pass


class ResourceStillProcessing(Exception):
    """most authentise resources have a status property to tell the user what state its in
        Whenever the resource isnt ready in some way or another, throw one of these"""
    pass
