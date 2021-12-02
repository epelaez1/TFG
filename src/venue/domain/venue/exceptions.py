

class VenueDoesNotExist(Exception):
    """ Venue does not exist """


class AuthorIsNotTheOwner(Exception):
    """ Only the owner of the venue can perform modifications """


class PrivateSpotNumberAlreadyAssigned(Exception):
    """" The spot number is already in use """
