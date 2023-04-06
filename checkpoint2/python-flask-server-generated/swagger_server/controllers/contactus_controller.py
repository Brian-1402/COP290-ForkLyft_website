import connexion
import six

from swagger_server.models.order import Order  # noqa: E501
from swagger_server.models.send import Send  # noqa: E501
from swagger_server import util


def find_orderby_user_id(send):  # noqa: E501
    """order history

    gets the different kinds of orders of users # noqa: E501

    :param send: data to be sent
    :type send: dict | bytes

    :rtype: List[Order]
    """
    if connexion.request.is_json:
        send = Send.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
