from src.profile.domain.entities.profile import Profile
from src.profile.domain.exceptions import ProfileAlreadyInitialized
from src.profile.domain.repository import ProfileRepository


def register_profile(name: str, email: str, phone: str, profile_repository: ProfileRepository) -> Profile:
    if profile_repository.has(email):
        raise ProfileAlreadyInitialized
    new_profile = Profile(name=name, phone=phone, email=email)
    profile_repository.add(new_profile)
    return new_profile


def get_profile(email: str, profile_repository: ProfileRepository) -> Profile:
    return profile_repository.get(email=email)
