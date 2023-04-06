# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class Send(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, name: str=None, email_id: str=None, message: str=None):  # noqa: E501
        """Send - a model defined in Swagger

        :param name: The name of this Send.  # noqa: E501
        :type name: str
        :param email_id: The email_id of this Send.  # noqa: E501
        :type email_id: str
        :param message: The message of this Send.  # noqa: E501
        :type message: str
        """
        self.swagger_types = {
            'name': str,
            'email_id': str,
            'message': str
        }

        self.attribute_map = {
            'name': 'name',
            'email_id': 'email_id',
            'message': 'message'
        }
        self._name = name
        self._email_id = email_id
        self._message = message

    @classmethod
    def from_dict(cls, dikt) -> 'Send':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The send of this Send.  # noqa: E501
        :rtype: Send
        """
        return util.deserialize_model(dikt, cls)

    @property
    def name(self) -> str:
        """Gets the name of this Send.


        :return: The name of this Send.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this Send.


        :param name: The name of this Send.
        :type name: str
        """

        self._name = name

    @property
    def email_id(self) -> str:
        """Gets the email_id of this Send.


        :return: The email_id of this Send.
        :rtype: str
        """
        return self._email_id

    @email_id.setter
    def email_id(self, email_id: str):
        """Sets the email_id of this Send.


        :param email_id: The email_id of this Send.
        :type email_id: str
        """

        self._email_id = email_id

    @property
    def message(self) -> str:
        """Gets the message of this Send.


        :return: The message of this Send.
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message: str):
        """Sets the message of this Send.


        :param message: The message of this Send.
        :type message: str
        """

        self._message = message
