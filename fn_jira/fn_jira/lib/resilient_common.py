# (c) Copyright IBM Corp. 2010, 2018. All Rights Reserved.
import html2markdown

from bs4 import BeautifulSoup
from six import string_types


INCIDENT_FRAGMENT = '#incidents'

def build_incident_url(url, incidentId):
    """
    build the url to link to an resilient incident
    :param url: base url
    :param incidentId:
    :return: full url
    """
    return '/'.join([url, INCIDENT_FRAGMENT, str(incidentId)])

def build_resilient_url(host, port):
    """
    build basic url to resilient instance
    :param host: host name
    :param port: port
    :return: base url
    """
    return "https://{0}:{1}".format(host, port)

def clean_html(htmlFragment):
    """
    Resilient textarea fields return html fragments. This routine will remove the html and insert any code within <div></div>
    with a linefeed
    :param htmlFragment:
    :return: cleaned up code
    """

    if not htmlFragment or not isinstance(htmlFragment, string_types):
        return htmlFragment

    return BeautifulSoup(unescape(htmlFragment), "html.parser")

def html2markdwn(htmlFragment):
    """
    convert html to markdown as some environments (aka Jira, Slack) use markdown for their rich text
    :param htmlFragment:
    :return: markdownstring
    """

    if not htmlFragment or not isinstance(htmlFragment, string_types):
        return htmlFragment

    htmlparser = html2markdown.MarkdownParser(bold="*", underline="_")
    return htmlparser.convert(htmlFragment)


def unescape(data):
    """ Return unescaped data such as &gt; -> >, &quot -> ', etc. """
    try:
        return htmlparser.unescape(data)
    except:
        return data

def merge_two_dicts(x, y):
    """
    merge to dictionaries
    :param x:
    :param y:
    :return: merged dict
    """
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z

def validateFields(fieldList, kwargs):
    """
    ensure required fields are present. Throw ValueError if not
    :param fieldList:
    :param kwargs:
    :return: no return
    """
    for field in fieldList:
        if field not in kwargs or kwargs.get(field) == '':
            raise ValueError('Required field is missing or empty: '+field)

def parse_bool(value):
    """Represents value as boolean.
    :param value:
    :rtype: bool
    """
    if isinstance(value, bool):
        return value

    value = str(value).lower()
    return value in ('1', 'true', 'yes')