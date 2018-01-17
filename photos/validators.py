# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError

from photos.settings import BADWORDS


def badwords_detector(value):
    """
    Method to control bad words in the form
    :return: Boolean
    """

    for badword in BADWORDS:
        if badword.lower() in value.lower():
            raise ValidationError(u'La palabra {0}, no está permitida.'.format(badword))
    # Si todo va ok, devuelvo True

    return True