"""robots.txt compliance gate. Every connector calls allowed() before fetching."""
import urllib.robotparser
from urllib.parse import urlparse

USER_AGENT = "ncr-battery-leads-bot/1.0 (lead research; contact: compliance@carbonsettle.com)"

_PARSERS: dict[str, urllib.robotparser.RobotFileParser] = {}


def allowed(url: str) -> bool:
    """True iff robots.txt for the URL's host permits fetching it.
    Unreachable robots.txt => permissive (standard convention), but network
    errors during read => conservative False."""
    host = urlparse(url).netloc
    rp = _PARSERS.get(host)
    if rp is None:
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(f"https://{host}/robots.txt")
        try:
            rp.read()
        except Exception:
            rp.disallow_all = True
        _PARSERS[host] = rp
    return rp.can_fetch(USER_AGENT, url)
