# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest

from ansible.module_utils._text import to_native
from ansible.module_utils.common.validation import check_missing_parameters


@pytest.fixture
def arguments_terms():
    return {"path": ""}


def test_check_missing_parameters():
    assert check_missing_parameters([], {}) == []


def test_check_missing_parameters_list():
    expected = "missing required arguments: path"

    with pytest.raises(TypeError) as e:
        check_missing_parameters({}, ["path"])

    assert to_native(e.value) == expected


def test_check_missing_parameters_positive():
    assert check_missing_parameters({"path": "/foo"}, ["path"]) == []
