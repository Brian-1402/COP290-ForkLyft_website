# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.user import User  # noqa: E501
from swagger_server.models.userid import Userid  # noqa: E501
from swagger_server.models.userid1 import Userid1  # noqa: E501
from swagger_server.models.userid2 import Userid2  # noqa: E501
from swagger_server.models.userid3 import Userid3  # noqa: E501
from swagger_server.test import BaseTestCase


class TestUserController(BaseTestCase):
    """UserController integration test stubs"""

    def test_find_user_by_id(self):
        """Test case for find_user_by_id

        finds the data related to the particuar user and displays his contact number, name, etc
        """
        response = self.client.open(
            '/api/v1/user/{userid}/myprofile'.format(userid=Userid()),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_find_user_by_id_0(self):
        """Test case for find_user_by_id_0

        Display addresses of the user
        """
        response = self.client.open(
            '/api/v1/user/{userid}/address'.format(userid=Userid2()),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_find_user_by_idand_edit(self):
        """Test case for find_user_by_idand_edit

        displays the form to edit user details and on clicking sends a post request
        """
        response = self.client.open(
            '/api/v1/user/{userid}/myprofile/edit'.format(userid=Userid1()),
            method='PUT')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_find_user_by_idand_edit_0(self):
        """Test case for find_user_by_idand_edit_0

        help edit addresses of the user
        """
        response = self.client.open(
            '/api/v1/user/{userid}/address/edit'.format(userid=Userid3()),
            method='PUT')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_user_by_id(self):
        """Test case for get_user_by_id

        Display the user home page with different reccomendations
        """
        response = self.client.open(
            '/api/v1/user/{userid}'.format(userid=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
