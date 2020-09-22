from .content_filtering import content_filtering
from .facial_features import facial_features
from .facial_localization import facial_localization
from .fer import fer
from .image_features import image_features
from .image_recognition import image_recognition

IMAGE_APIS = {
    "content_filtering": content_filtering,
    "facial_features": facial_features,
    "facial_localization": facial_localization,
    "fer": fer,
    "image_features": image_features,
    "image_recognition": image_recognition,
}
