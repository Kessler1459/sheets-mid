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
    session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    session.hooks = {'response': request_hook}
    return session
