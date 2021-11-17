

class UserAlreadyRegistered(Exception):
    """ User already exists """


class Unauthorized(Exception):
    """ Unable to process the authentication token """


class UserDoesNotExists(Exception):
    """ User does not exists """


class IncorrectUsername(Exception):
    """ Incorrect username """


class IncorrectPassword(Exception):
    """ The password does not match """
