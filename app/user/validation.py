import re
from difflib import SequenceMatcher
from pathlib import Path

from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation
from django.utils.translation import gettext as _, ngettext


class UserAttributeSimilarityValidator:
    """
    Validate whether the password is sufficiently different from the user's
    attributes.
    If no specific attributes are provided, look at a sensible list of
    defaults. Attributes that don't exist are ignored. Comparison is made to
    not only the full attribute value, but also its components, so that, for
    example, a password is validated against either part of an email address,
    as well as the full address.
    """
    DEFAULT_USER_ATTRIBUTES = ['email']

    def __init__(self, user_attributes=DEFAULT_USER_ATTRIBUTES, max_similarity=0.7):
        self.user_attributes = user_attributes
        self.max_similarity = max_similarity

    def validate(self, password, user=None):
        if not user:
            return
        for attribute_name in self.user_attributes:
            value = getattr(user, attribute_name, None)
            if not value or not isinstance(value, str):
                continue
            value_parts = re.split(r'\W+', value) + [value]
            for value_part in value_parts:
                if SequenceMatcher(a=password.lower(), b=value_part.lower()).quick_ratio() >= self.max_similarity:
                    try:
                        verbose_name = str(user._meta.get_field(attribute_name).verbose_name)
                    except FieldDoesNotExist:
                        verbose_name = attribute_name
                    raise ValidationError(
                        _("The password is too similar to the %(verbose_name)s."),
                        code='password_too_similar',
                        params={'verbose_name': verbose_name},
                    )

    def get_help_text(self):
        return _("Your password can't be too similar to your other personal information.")


class MinimumNumberValidator:
    """Validator for chacking munimum numbers """

    def __init__(self, min_number=0):
        self.min_number = min_number

    def count_number(self, password):
        count = 0
        for ch in password:
            count += 1 if ch.isdigit() else 0
        return count

    def validate(self, password, user=None):
        if self.count_number(password) < self.min_number:
            raise ValidationError(
                ngettext(
                    "This password must contain at least %(min_number)d number.",
                    "This password must contain at least %(min_number)d numbers.",
                    self.min_number
                ),
                code='password_number_short',
                params={'min_number': self.min_number},
            )

    def get_help_text(self):
        return ngettext(
            "Your password must contain at least %(min_number)d number.",
            "Your password must contain at least %(min_number)d number.",
            self.min_number
        ) % {'min_number': self.min_number}


class MinimumLowerCaseValidator:
    """Validator for checking minimum lower char"""

    def __init__(self, min_lower=0):
        self.min_lower = min_lower

    def count_lower(self, password):
        count = 0
        for ch in password:
            count += 1 if ch.islower() else 0
        return count

    def validate(self, password, user=None):
        if self.count_lower(password) < self.min_lower:
            raise ValidationError(
                ngettext(
                    "This password must contain at least %(min_lower)d lower case character.",
                    "This password must contain at least %(min_lower)d lower case characters.",
                    self.min_lower
                ),
                code='password_lower_case_short',
                params={'min_lower': self.min_lower},
            )

    def get_help_text(self):
        return ngettext(
            "Your password must contain at least %(min_lower)d lower case character.",
            "Your password must contain at least %(min_lower)d lower case characters.",
            self.min_lower
        ) % {'min_lower': self.min_lower}


class MinimumUpperCaseValidator:
    """Validator for checking minimum upper char"""

    def __init__(self, min_upper=0):
        self.min_upper = min_upper

    def count_upper(self, password):
        count = 0
        for ch in password:
            count += 1 if ch.isupper() else 0
        return count

    def validate(self, password, user=None):
        if self.count_upper(password) < self.min_upper:
            raise ValidationError(
                ngettext(
                    "This password must contain at least %(min_upper)d upper case character.",
                    "This password must contain at least %(min_upper)d upper case characters.",
                    self.min_upper
                ),
                code='password_upper_case_short',
                params={'min_upper': self.min_upper},
            )

    def get_help_text(self):
        return ngettext(
            "Your password must contain at least %(min_upper)d upper case character.",
            "Your password must contain at least %(min_upper)d upper case characters.",
            self.min_upper
        ) % {'min_upper': self.min_upper}


class MinimumSpecialValidator:
    """Validator for checking minimum special char"""

    def __init__(self, min_special=0):
        self.min_special = min_special

    def count_special(self, password):
        count = 0
        special = "[@_!#$%^&*()<>?/\|}{~:]"
        for ch in password:
            count += 1 if ch in special else 0
        return count

    def validate(self, password, user=None):
        if self.count_special(password) < self.min_special:
            raise ValidationError(
                ngettext(
                    "This password must contain at least %(min_special)d special case character.",
                    "This password must contain at least %(min_special)d special case characters.",
                    self.min_special
                ),
                code='password_special_case_short',
                params={'min_special': self.min_special},
            )

    def get_help_text(self):
        return ngettext(
            "Your password must contain at least %(min_special)d special case character.",
            "Your password must contain at least %(min_special)d special case characters.",
            self.min_special
        ) % {'min_special': self.min_special}


class MinimumDifferentValidator:
    """Validator for checking minimum different char"""

    def __init__(self, min_diff=0):
        self.min_diff = min_diff

    def count_diff(self, password):
        count = 0
        diff = ""
        for ch in password:
            if ch not in diff:
                count += 1
                diff += ch
        return count

    def validate(self, password, user=None):
        if self.count_diff(password) < self.min_diff:
            raise ValidationError(
                ngettext(
                    "This password must contain at least %(min_diff)d different character.",
                    "This password must contain at least %(min_diff)d different characters.",
                    self.min_diff
                ),
                code='password_different_short',
                params={'min_diff': self.min_diff},
            )

    def get_help_text(self):
        return ngettext(
            "Your password must contain at least %(min_diff)d different character.",
            "Your password must contain at least %(min_diff)d different characters.",
            self.min_diff
        ) % {'min_diff': self.min_diff}


class MaximumRepeatingValidator:
    """Validator for checking maximum reapeating char"""

    def __init__(self, max_repeating=5):
        self.max_repeating = max_repeating

    def count_repeating(self, password):
        n = len(password)
        count = 0
        res = password[0]
        cur_count = 1
        for i in range(n):
            if (i < n - 1 and password[i] == password[i + 1]):
                cur_count += 1
            elif cur_count > count:
                count = cur_count
                res = password[i]
                cur_count = 1
        return count

    def validate(self, password, user=None):
        if self.count_repeating(password) > self.max_repeating:
            raise ValidationError(
                ngettext(
                    "This password must not contain more than %(max_repeating)d repeating character.",
                    "This password must not contain more than %(max_repeating)d repeating characters.",
                    self.max_repeating
                ),
                code='password_maximum_repeating',
                params={'max_repeating': self.max_repeating},
            )

    def get_help_text(self):
        return ngettext(
            "Your password must not contain more than %(max_repeating)d repeating character.",
            "Your password must not contain more than %(max_repeating)d repeating characters.",
            self.max_repeating
        ) % {'max_repeating': self.max_repeating}


class MaximumRepeatingTypeValidator:
    """Validator for checking maximum reapeating type char"""

    def __init__(self, max_repeating=5):
        self.max_repeating = max_repeating

    def find_type(self, ch):
        if ch.isalpha():
            return 'char'
        elif ch.isdigit():
            return 'num'
        return 'spe'

    def count_repeating(self, password):
        n = len(password)
        count = 0
        res = password[0]
        cur_count = 0
        for i in range(n):
            if (i < n - 1 and self.find_type(password[i]) == self.find_type(password[i+1])):
                cur_count += 1
            elif cur_count > count:
                count = cur_count
                res = password[i]
                cur_count = 0
        return count

    def validate(self, password, user=None):
        if self.count_repeating(password) > self.max_repeating:
            raise ValidationError(
                ngettext(
                    "This password must not contain more than %(max_repeating)d repeating type character.",
                    "This password must not contain more than %(max_repeating)d repeating type characters.",
                    self.max_repeating
                ),
                code='password_maximum_repeating',
                params={'max_repeating': self.max_repeating},
            )

    def get_help_text(self):
        return ngettext(
            "Your password must not contain more than %(max_repeating)d repeating type character.",
            "Your password must not contain more than %(max_repeating)d repeating type characters.",
            self.max_repeating
        ) % {'max_repeating': self.max_repeating}
