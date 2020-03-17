#!/usr/bin/env python
import os
import re

import fire

pre_release_placeholder = 'SNAPSHOT'
version_filepath = os.path.join('.', 'VERSION')
version_pattern = re.compile(fr'^\d+.\d+.\d+(-{pre_release_placeholder})?$')


def get(with_pre_release_placeholder: bool = False):
    with open(version_filepath, 'r') as version_file:
        version_lines = version_file.readlines()
        assert len(version_lines) == 1, 'Version file is malformed'
        version = version_lines[0]
        assert version_pattern.match(version), 'Version string is malformed'
        if with_pre_release_placeholder:
            return version
        else:
            return version.replace(f'-{pre_release_placeholder}', '')


def write_version_file(major: int, minor: int, patch: int):
    version = f'{major}.{minor}.{patch}-{pre_release_placeholder}'
    with open(version_filepath, 'w') as version_file:
        version_file.write(version)


def inc_patch():
    version = get()
    major, minor, patch = version.split('.')
    write_version_file(major, minor, int(patch) + 1)


def inc_minor():
    version = get()
    major, minor, patch = version.split('.')
    write_version_file(major, int(minor) + 1, patch)


def inc_major():
    version = get()
    major, minor, patch = version.split('.')
    write_version_file(int(major) + 1, minor, patch)


if __name__ == "__main__":
    fire.Fire({
        'get': get,
        'inc-patch': inc_patch,
        'inc-minor': inc_minor,
        'inc-major': inc_major
    })
