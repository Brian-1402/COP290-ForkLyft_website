import connexion
import six

from swagger_server.models.order import Order  # noqa: E501
from swagger_server.models.userid4 import Userid4  # noqa: E501
from swagger_server import util


def find_orderby_user_id(userid):  # noqa: E501
    """order history

    gets the different kinds of orders of users # noqa: E501

    :param userid: Numeric id of the user to get
    :type userid: dict | bytes

    :rtype: List[Order]
    """
    if connexion.request.is_json:
        userid = Userid4.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
