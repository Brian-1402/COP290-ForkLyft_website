# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.order import Order  # noqa: E501
from swagger_server.models.userid4 import Userid4  # noqa: E501
from swagger_server.test import BaseTestCase


class TestOrderController(BaseTestCase):
    """OrderController integration test stubs"""

    def test_find_orderby_user_id(self):
        """Test case for find_orderby_user_id

        order history
        """
        response = self.client.open(
            '/api/v1/user/{userid}/myorders'.format(userid=Userid4()),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
