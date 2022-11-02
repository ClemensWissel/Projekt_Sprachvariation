"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFPlone.utils import get_installer
from sprachvariation.testing import SPRACHVARIATION_INTEGRATION_TESTING  # noqa: E501

import unittest


class TestSetup(unittest.TestCase):
    """Test that sprachvariation is properly installed."""

    layer = SPRACHVARIATION_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.setup = self.portal.portal_setup
        self.installer = get_installer(self.portal, self.layer["request"])

    def test_product_installed(self):
        """Test if sprachvariation is installed."""
        self.assertTrue(self.installer.is_product_installed("sprachvariation"))

    def test_browserlayer(self):
        """Test that ISPRACHVARIATIONLayer is registered."""
        from plone.browserlayer import utils
        from sprachvariation.interfaces import ISPRACHVARIATIONLayer

        self.assertIn(ISPRACHVARIATIONLayer, utils.registered_layers())

    def test_latest_version(self):
        """Test latest version of default profile."""
        self.assertEqual(
            self.setup.getLastVersionForProfile("sprachvariation:default")[0],
            "20221026001",
        )


class TestUninstall(unittest.TestCase):

    layer = SPRACHVARIATION_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstall_product("sprachvariation")
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if sprachvariation is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed("sprachvariation"))

    def test_browserlayer_removed(self):
        """Test that ISPRACHVARIATIONLayer is removed."""
        from plone.browserlayer import utils
        from sprachvariation.interfaces import ISPRACHVARIATIONLayer

        self.assertNotIn(ISPRACHVARIATIONLayer, utils.registered_layers())
