import connexion
import six

from swagger_server.models.user import User  # noqa: E501
from swagger_server.models.userid import Userid  # noqa: E501
from swagger_server.models.userid1 import Userid1  # noqa: E501
from swagger_server.models.userid2 import Userid2  # noqa: E501
from swagger_server.models.userid3 import Userid3  # noqa: E501
from swagger_server import util


def find_user_by_id(userid):  # noqa: E501
    """finds the data related to the particuar user and displays his contact number, name, etc

    profile of the user is displayed # noqa: E501

    :param userid: Numeric id of the user to get
    :type userid: dict | bytes

    :rtype: List[User]
    """
    if connexion.request.is_json:
        userid = Userid.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def find_user_by_id_0(userid):  # noqa: E501
    """Display addresses of the user

    Displays the different kinds of addresses of user ex- Home, Office, Other # noqa: E501

    :param userid: Numeric id of the user to get
    :type userid: dict | bytes

    :rtype: List[User]
    """
    if connexion.request.is_json:
        userid = Userid2.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def find_user_by_idand_edit(userid):  # noqa: E501
    """displays the form to edit user details and on clicking sends a post request

    profile of the user to be edited # noqa: E501

    :param userid: Numeric id of the user to post
    :type userid: dict | bytes

    :rtype: List[User]
    """
    if connexion.request.is_json:
        userid = Userid1.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def find_user_by_idand_edit_0(userid):  # noqa: E501
    """help edit addresses of the user

    Edits the different kinds of addresses of user ex- Home, Office, Other # noqa: E501

    :param userid: Numeric id of the user to get
    :type userid: dict | bytes

    :rtype: List[User]
    """
    if connexion.request.is_json:
        userid = Userid3.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def get_user_by_id(userid):  # noqa: E501
    """Display the user home page with different reccomendations

    user home page display # noqa: E501

    :param userid: Numeric id of the user to get
    :type userid: int

    :rtype: User
    """
    return 'do some magic!'
