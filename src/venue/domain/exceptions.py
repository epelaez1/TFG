#  noqa: WPS202
class VenueDoesNotExist(Exception):
    """ Venue does not exist """


class AuthorIsNotTheOwner(Exception):
    """ Only the owner of the venue can perform modifications """


class PrivateSpotNumberAlreadyAssigned(Exception):
    """" The spot number is already in use """


class SocialEventDoesNotExist(Exception):
    """" There is no social event with that id """


class EmployeeCodeAlreadyInUse(Exception):
    """" The employee code provided is already in use in other list """


class PrivateSpotNotFound(Exception):
    """ The spot number provided does not match with any spot of the venue """


class SpotOfferAlreadyExists(Exception):
    """" The private spot is already included in the social event """


class PrivateSpotOfferDoesNotExist(Exception):
    """ The private spot does not exists """


class PrivateSpotIsNotAvailable(Exception):
    """ The private spot is no available for reservations"""


class UserIsNotInsideTheSocialEvent(Exception):
    """ The user has never accessed the social event"""


class EmployeeCodeDoesNotExist(Exception):
    """ The employee code does not exist """
