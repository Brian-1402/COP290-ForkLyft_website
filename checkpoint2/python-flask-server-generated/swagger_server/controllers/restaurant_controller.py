import connexion
import six

from swagger_server.models.restaurant import Restaurant  # noqa: E501
from swagger_server import util


def find_by_restaurant_id(restaurantid):  # noqa: E501
    """display restaurant order history and menu (homepage)

     # noqa: E501

    :param restaurantid: numeric id of the restaurant
    :type restaurantid: str

    :rtype: List[Restaurant]
    """
    return 'do some magic!'


def find_by_restaurant_id_0(restaurantid):  # noqa: E501
    """display restaurant order menu fully

     # noqa: E501

    :param restaurantid: numeric id of the restaurant
    :type restaurantid: str

    :rtype: List[Restaurant]
    """
    return 'do some magic!'


def find_by_restaurant_id_1(restaurantid, foodid):  # noqa: E501
    """display restaurant order menu fully

     # noqa: E501

    :param restaurantid: numeric id of the restaurant
    :type restaurantid: str
    :param foodid: numeric id of the food
    :type foodid: str

    :rtype: List[Restaurant]
    """
    return 'do some magic!'


def find_by_restaurant_idand_submit(restaurantid):  # noqa: E501
    """add restaurant item

     # noqa: E501

    :param restaurantid: numeric id of the restaurant
    :type restaurantid: str

    :rtype: List[Restaurant]
    """
    return 'do some magic!'


def restaurant_restaurantid_menu_additem_get():  # noqa: E501
    """display restaurant add item page

     # noqa: E501


    :rtype: List[Restaurant]
    """
    return 'do some magic!'
