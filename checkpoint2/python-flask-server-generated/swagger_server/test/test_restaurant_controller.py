# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.restaurant import Restaurant  # noqa: E501
from swagger_server.test import BaseTestCase


class TestRestaurantController(BaseTestCase):
    """RestaurantController integration test stubs"""

    def test_find_by_restaurant_id(self):
        """Test case for find_by_restaurant_id

        display restaurant order history and menu (homepage)
        """
        response = self.client.open(
            '/api/v1/restaurant/{restaurantid}'.format(restaurantid='restaurantid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_find_by_restaurant_id_0(self):
        """Test case for find_by_restaurant_id_0

        display restaurant order menu fully
        """
        response = self.client.open(
            '/api/v1/restaurant/{restaurantid}/menu'.format(restaurantid='restaurantid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_find_by_restaurant_id_1(self):
        """Test case for find_by_restaurant_id_1

        display restaurant order menu fully
        """
        response = self.client.open(
            '/api/v1/restaurant/{restaurantid}/menu'.format(restaurantid='restaurantid_example', foodid='foodid_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_find_by_restaurant_idand_submit(self):
        """Test case for find_by_restaurant_idand_submit

        add restaurant item
        """
        response = self.client.open(
            '/api/v1/restaurant/{restaurantid}/menu/additem'.format(restaurantid='restaurantid_example'),
            method='POST')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_restaurant_restaurantid_menu_additem_get(self):
        """Test case for restaurant_restaurantid_menu_additem_get

        display restaurant add item page
        """
        response = self.client.open(
            '/api/v1/restaurant/{restaurantid}/menu/additem',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
