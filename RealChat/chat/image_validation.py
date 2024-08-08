import json
import os

from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.conf import settings
from django.utils.deconstruct import deconstructible


@deconstructible
class FileExtensionValidator(object):
    message = "File extension '%(extension)s' is not allowed. Allowed extensions are: '%(allowed_extensions)s'."
    code = 'invalid_extension'

    def __init__(self, allowed_extensions=None, message=None, code=None):
        if allowed_extensions is not None:
            allowed_extensions = [allowed_extension.lower() for allowed_extension in allowed_extensions]
        self.allowed_extensions = allowed_extensions
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        extension = os.path.splitext(value.name)[1][1:].lower()
        if self.allowed_extensions is not None and extension not in self.allowed_extensions:
            raise ValidationError(
                self.message,
                code=self.code,
                params={
                    'extension': extension,
                    'allowed_extensions': ', '.join(self.allowed_extensions)
                }
            )

    def __eq__(self, other):
        return (
            isinstance(other, FileExtensionValidator) and
            self.allowed_extensions == other.allowed_extensions and
            self.message == other.message and
            self.code == other.code
        )


class ImageDimensionsValidator:
    message = {
        'empty': 'The image is empty',
        'min_width': "Min width: '%(min_width)spx'",
        'max_width': "Max width: '%(max_width)spx'",
        'min_height': "Min height: '%(min_height)spx'",
        'max_height': "Max height: '%(max_height)spx'",
        'width': 'The width %(width)spx is wrong, it should be %(allowed_width)s',
        'height': 'The height %(height)spx is wrong, it should be %(allowed_height)s',
        'dimensions': 'The image dimensions are not allowed, it should be %(allowed_dimensions)s'
    }
    code = 'wrong_dimensions'

    min_width = None
    min_height = None
    max_width = None
    max_height = None
    width = []
    height = []
    dimensions = []

    def __init__(self,
                 min_width=None,
                 min_height=None,
                 max_width=None,
                 max_height=None,
                 width=None,
                 height=None,
                 dimensions=None
                 ):
        if min_width is not None:
            self.min_width = min_width
        if min_height is not None:
            self.min_height = min_height
        if max_width is not None:
            self.max_width = max_width
        if max_height is not None:
            self.max_height = max_height
        if width is not None:
            self.width = width
            if isinstance(self.width, int):
                self.width = [self.width]
        if height is not None:
            self.height = height
            if isinstance(self.height, int):
                self.height = [self.height]
        if dimensions is not None:
            self.dimensions = dimensions

    def __call__(self, value):
        # if isinstance(value, str):
        #     # Assume we're deserializing
        #     value = json.loads(value)
        #
        # if not value or len(value) == 0:
        #     self.raise_error('empty')
        #     return

        if self.width or self.height:
            image = value
            image_w, image_h = get_image_dimensions(image)

            if self.width:
                width_found = self.check_width_height(self.width, image_w)
                if not width_found:
                    self.raise_error('width', width=image_w)

            if self.height:
                height_found = self.check_width_height(self.height, image_h)
                if not height_found:
                    self.raise_error('height', height=image_h)

        elif self.dimensions:
            image = value
            image_w, image_h = get_image_dimensions(image)

            valid_image_dimensions = False
            for dimension in self.dimensions:
                width = dimension[0]
                height = dimension[1]
                if width == image_w and height == image_h:
                    valid_image_dimensions = True

            if not valid_image_dimensions:
                self.raise_error('dimensions')
        else:
            # for image in value:
            w, h = get_image_dimensions(settings.MEDIA_ROOT + car.photo.name)
            self.check_min_width_height(w, h)

    def check_width_height(self, image_dimensions, dimension):
        for dim in image_dimensions:
            if dim is dimension:
                return True
        return False

    def check_min_width_height(self, w, h):
        if self.min_width and w < self.min_width:
            self.raise_error('min_width')
        if self.min_height and h < self.min_height:
            self.raise_error('min_height')
        if self.max_width and w > self.max_width:
            self.raise_error('max_width')
        if self.max_height and h > self.max_height:
            self.raise_error('max_height')

    def raise_error(self, code, width=None, height=None):

        raise ValidationError(self.message[code], code=code, params={
            'min_width': str(self.min_width),
            'max_width': str(self.max_width),
            'min_height': str(self.min_height),
            'max_height': str(self.max_height),
            'width': width if width else str(self.width),
            'height': height if height else str(self.height),
            'allowed_width': ', '.join(map(str, self.width)),
            'allowed_height': ', '.join(map(str, self.height)),
            'allowed_dimensions': ', '.join(map(str, self.dimensions))
        })

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.min_width == other.min_width and
            self.min_height == other.min_height and
            self.max_width == other.max_width and
            self.max_height == other.max_height and
            self.message == other.message and
            self.code == other.code
        )


class ImageExtensionValidator(FileExtensionValidator):

    def __call__(self, value):
        class val(dict):
            __getattr__ = dict.__getitem__
            __setattr__ = dict.__setitem__

        val = val()
        val.name = value[0]
        super(ImageExtensionValidator, self).__call__(value=val)


class ImageOrientationValidator:

    message = {
        'no_orientation': 'The orientation is not defined for this validation',
        'wrong_orientation': 'The image is in %(wrong_orientation)s and should be in %(orientation)s',
        'square': 'The image is neither in portrait or in landscape'
    }

    orientation = None
    wrong_orientation = None

    def __init__(self, orientation):
        self.orientation = orientation

        if orientation == 'landscape':
            self.wrong_orientation = 'portrait'
        elif orientation == 'portrait':
            self.wrong_orientation = 'landscape'

    def __call__(self, value):

        if isinstance(value, str):
            # Assume we're deserializing
            value = json.loads(value)

        if not value or len(value) == 0:
            self.raise_error('empty')
            return

        if self.orientation != 'landscape' or self.orientation != 'portrait':
            self.raise_error('no_orientation')
            return

        for image in value:
            w, h = get_image_dimensions(image)

            if w > h and self.orientation == 'portrait':
                self.raise_error('wrong_orientation')
            elif h > w and self.orientation == 'landscape':
                self.raise_error('wrong_orientation')
            else:
                self.raise_error('square')

    def raise_error(self, code):
        raise ValidationError(self.message, code=code, params={
            'orientation': self.orientation,
            'wrong_orientation': self.wrong_orientation
        })


class ImageFileSizeValidator:

    message = {
        'min_size': "Minimal size of the file is %(min)sKB and currently %(size)sKB.",
        'max_size': "Max size of file is %(max_size)sKB and currently %(size)sKB."
    }

    min_size = None
    max_size = None

    def __init__(self, max_size=None, min_size=None):
        if max_size is not None:
            self.max_size = max_size
        if min_size is not None:
            self.min_size = min_size

    def __call__(self, value):
        for image in value:
            file_size = os.stat(image).st_size/1024

            if self.max_size and file_size > self.max_size:
                self.raise_error('max_size', size=file_size)
            if self.min_size and file_size < self.min_size:
                self.raise_error('min_size', size=file_size)

    def raise_error(self, code, size):
        raise ValidationError(self.message[code], code=code, params={
            'size': round(size, 2),
            'min_size': self.min_size,
            'max_size': self.max_size
        })

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.message == other.message and
            self.min_size == other.min_size and
            self.max_size == other.max_size
        )
