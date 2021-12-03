
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
