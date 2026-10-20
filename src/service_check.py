
from urllib.request import urlopen
from urllib.error import URLError


def check_http_service(url, timeout=2):
    try:
        with urlopen(url, timeout=timeout) as response:
            return 200 <= response.status < 300

    except (URLError, TimeoutError, OSError):
        return False
