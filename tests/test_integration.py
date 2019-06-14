#!/usr/bin/env python
# pylint: disable=no-self-use, invalid-name

"""Integration tests for cm package."""

import cm

import pytest
import testinfra


class TestIntegrations:
    """Integration Tests"""

    def test_package_apache(self):
        """Test run"""
        # Assert false because no tests have actually been implemented.
        assert False
