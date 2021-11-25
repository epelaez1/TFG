

class UserAlreadyRegistered(Exception):
    """ User already registered with this credentials """


class UserDoesNotExist(Exception):
    """ User does not exist """


class Unauthorized(Exception):
    """ Unable to process the authentication token """


class IncorrectUsername(Exception):
    """ Incorrect username """


class IncorrectPassword(Exception):
    """ The password does not match """


class UserEmailNotVerified(Exception):
    """ The current user has not verified the email address """


class UserWithoutProfile(Exception):
    """ User without profile yet """
