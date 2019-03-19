import glob

from Tests.test_utils import re, print_error, os, get_yaml
from Tests.scripts.constants import INTEGRATION_REGEX, INTEGRATION_YML_REGEX


class DescriptionValidator(object):
    """DescriptionValidator was designed to make sure we provide a detailed description properly.

    Attributes:
        file_path (string): Path to the checked file.
        _is_valid (bool): the attribute which saves the valid/in-valid status of the current file.
    """

    def __init__(self, file_path):
        self._is_valid = True

        if re.match(INTEGRATION_REGEX, file_path, re.IGNORECASE):
            self.file_path = file_path
        else:
            if re.match(INTEGRATION_YML_REGEX, file_path, re.IGNORECASE):
                try:
                    self.file_path = glob.glob(os.path.join(os.path.dirname(file_path), '*.md'))[0]
                except IndexError:
                    self._is_valid = False
                    print_error("You've created/modified a package but failed to provide a description as a .md file, "
                                "please add a detailed description in order to proceed.")

    def is_valid(self):
        """Validate that the description exists."""
        if self._is_valid is False:  # In case we encountered an IndexError in the init - we don't have a description
            return self._is_valid

        if '.md' not in self.file_path:
            self.is_existing_description()

        return self._is_valid

    def is_existing_description(self):
        """Check if the integration as a description."""
        is_description_in_yml = False
        is_description_in_package = False
        if get_yaml(self.file_path).get('detaileddescription'):
            is_description_in_yml = True

        if not re.match(INTEGRATION_REGEX, self.file_path, re.IGNORECASE):
            package_path = os.path.dirname(self.file_path)
            if is_description_in_yml:
                print_error("You have added a detailed description in the yml "
                            "file, please update the package {}".format(package_path))
                return False

            description_file = glob.glob(package_path + '/*.md')
            if description_file:
                is_description_in_package = True

        if not (is_description_in_package or is_description_in_yml):
            print_error("You have failed to add a detailed description in the package for {}".format(self.file_path))
            self._is_valid = False
            return False

        return True