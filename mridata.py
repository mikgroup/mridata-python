import getpass
import requests
import urllib.parse


WEBSITE = 'http://mridata-web.us-west-2.elasticbeanstalk.com/'
LOGIN_URL = urllib.parse.urljoin(WEBSITE, 'accounts/login/')
UPLOAD_GE_URL = urllib.parse.urljoin(WEBSITE, 'upload_ge/')
UPLOAD_SIEMENS_URL = urllib.parse.urljoin(WEBSITE, 'upload_siemens/')

session = None


def login():
    global session
    username = input('Username: ')
    password = getpass.getpass('Password: ')

    session = requests.Session()
    session.get(LOGIN_URL)
    csrftoken = session.cookies['csrftoken']
    login_data = {'username': username, 'password': password,
                  'csrfmiddlewaretoken': csrftoken}
    p = session.post(LOGIN_URL, data=login_data)

    if 'login'in p.url:
        raise Exception('Cannot find user with the given credentials.')


def upload_ge(*ge_files,
              anatomy='Unknown', fullysampled=None,
              references='', comments=''):

    if session is None:
        login()
    
    session.get(UPLOAD_GE_URL)
    csrftoken = session.cookies['csrftoken']
    files = [('ge_file', open(ge_file, 'rb'))
             for ge_file in ge_files]
    upload_data = {'anatomy': anatomy, 'fullysampled': fullysampled,
                   'references': references, 'comments': comments,
                   'csrfmiddlewaretoken': csrftoken}
    session.post(UPLOAD_GE_URL, files=files, data=upload_data)



def upload_siemens(*siemens_dat_files,
                   anatomy='Unknown', fullysampled=None,
                   references='', comments=''):

    if session is None:
        login()

    session.get(UPLOAD_SIEMENS_URL)
    csrftoken = session.cookies['csrftoken']
    files = [('siemens_dat_file', open(siemens_dat_file, 'rb'))
             for siemens_dat_file in siemens_dat_files]
    upload_data = {'anatomy': anatomy, 'fullysampled': fullysampled,
                   'references': references, 'comments': comments,
                   'csrfmiddlewaretoken': csrftoken}
    session.post(UPLOAD_SIEMENS_URL, files=files, data=upload_data)
