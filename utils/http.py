from colorama import Fore, Style
from requests import Session

from utils.logging_handler import get_logger

logger = get_logger(__name__)

def get_session() -> Session:
    """ 
    Hooks setup
    Returns:
        Session: requests session
    """
    def request_hook(res, *args, **kwargs):
        if 200 <= res.status_code < 300:
            color = Fore.GREEN
        elif 300 <= res.status_code < 400:
            color = Fore.YELLOW
        else:
            color = Fore.RED
        logger.info("%s%s %s - %s%s", color, res.request.method, res.status_code, res.request.url, Style.RESET_ALL)
        return res
    session = Session()
    session.hooks = {'response': request_hook}
    return session
