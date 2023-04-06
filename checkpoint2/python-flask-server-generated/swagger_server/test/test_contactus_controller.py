# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.order import Order  # noqa: E501
from swagger_server.models.send import Send  # noqa: E501
from swagger_server.test import BaseTestCase


class TestContactusController(BaseTestCase):
    """ContactusController integration test stubs"""

    def test_find_orderby_user_id(self):
        """Test case for find_orderby_user_id

        order history
        """
        response = self.client.open(
            '/api/v1/contactus/send'.format(send=Send()),
            method='POST')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
