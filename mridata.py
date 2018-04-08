import getpass
import requests
from urllib.parse import urljoin


WEBSITE = 'http://mridata-web.us-west-2.elasticbeanstalk.com/'
LOGIN_URL = urljoin(WEBSITE, 'accounts/login/')
UPLOAD_GE_URL = urljoin(WEBSITE, 'upload_ge/')
UPLOAD_SIEMENS_URL = urljoin(WEBSITE, 'upload_siemens/')
UPLOAD_PHILIPS_URL = urljoin(WEBSITE, 'upload_philips/')
UPLOAD_ISMRMRD_URL = urljoin(WEBSITE, 'upload_ismrmrd/')

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


def upload_ismrmrd(ismrmrd_file, project_name,
                   anatomy='Unknown', fullysampled=None,
                   references='', comments=''):

    if session is None:
        login()

    print('Uploading...')
    
    session.get(UPLOAD_ISMRMRD_URL)
    csrftoken = session.cookies['csrftoken']
    files = {'ismrmrd_file': open(ismrmrd_file, 'rb')}
    upload_data = {'anatomy': anatomy, 'fullysampled': fullysampled,
                   'project_name': project_name,
                   'references': references, 'comments': comments,
                   'csrfmiddlewaretoken': csrftoken}
    session.post(UPLOAD_ISMRMRD_URL, files=files, data=upload_data)
    
    print('Done.')


def upload_ge(ge_file, project_name,
              anatomy='Unknown', fullysampled=None,
              references='', comments='',
              thumbnail_horizontal_flip=False,
              thumbnail_vertical_flip=False,
              thumbnail_transpose=False,
              thumbnail_fftshift_along_z=False):

    if session is None:
        login()

    print('Uploading...')
    
    session.get(UPLOAD_GE_URL)
    csrftoken = session.cookies['csrftoken']
    files = {'ge_file': open(ge_file, 'rb')}
    upload_data = {'anatomy': anatomy, 'fullysampled': fullysampled,
                   'project_name': project_name,
                   'references': references, 'comments': comments,
                   'thumbnail_fftshift_along_z': thumbnail_fftshift_along_z,
                   'thumbnail_horizontal_flip': thumbnail_horizontal_flip,
                   'thumbnail_transpose': thumbnail_transpose,
                   'thumbnail_vertical_flip': thumbnail_vertical_flip,
                   'csrfmiddlewaretoken': csrftoken}
    session.post(UPLOAD_GE_URL, files=files, data=upload_data)
    
    print('Done.')


def upload_siemens(siemens_dat_file, project_name,
                   anatomy='Unknown', fullysampled=None,
                   references='', comments='',
                   thumbnail_horizontal_flip=False,
                   thumbnail_vertical_flip=False,
                   thumbnail_transpose=False,
                   thumbnail_fftshift_along_z=False):

    if session is None:
        login()

    print('Uploading...')
    
    session.get(UPLOAD_SIEMENS_URL)
    csrftoken = session.cookies['csrftoken']
    files = {'siemens_dat_file': open(siemens_dat_file, 'rb')}
    upload_data = {'anatomy': anatomy, 'fullysampled': fullysampled,
                   'project_name': project_name,
                   'references': references, 'comments': comments,
                   'thumbnail_fftshift_along_z': thumbnail_fftshift_along_z,
                   'thumbnail_horizontal_flip': thumbnail_horizontal_flip,
                   'thumbnail_transpose': thumbnail_transpose,
                   'thumbnail_vertical_flip': thumbnail_vertical_flip,
                   'csrfmiddlewaretoken': csrftoken}
    session.post(UPLOAD_SIEMENS_URL, files=files, data=upload_data)
    
    print('Done.')


def upload_philips(philips_basename, project_name,
                   anatomy='Unknown', fullysampled=None,
                   references='', comments='',
                   thumbnail_horizontal_flip=False,
                   thumbnail_vertical_flip=False,
                   thumbnail_transpose=False,
                   thumbnail_fftshift_along_z=False):

    if session is None:
        login()

    philips_lab_file = philips_basename + '.lab'
    philips_sin_file = philips_basename + '.sin'
    philips_raw_file = philips_basename + '.raw'

    print('Uploading...')
    
    session.get(UPLOAD_PHILIPS_URL)
    csrftoken = session.cookies['csrftoken']
    files = {'philips_lab_file': open(philips_lab_file, 'rb'),
             'philips_sin_file': open(philips_sin_file, 'rb'),
             'philips_raw_file': open(philips_raw_file, 'rb')}
    upload_data = {'anatomy': anatomy, 'fullysampled': fullysampled,
                   'project_name': project_name,
                   'references': references, 'comments': comments,
                   'thumbnail_fftshift_along_z': thumbnail_fftshift_along_z,
                   'thumbnail_horizontal_flip': thumbnail_horizontal_flip,
                   'thumbnail_transpose': thumbnail_transpose,
                   'thumbnail_vertical_flip': thumbnail_vertical_flip,
                   'csrfmiddlewaretoken': csrftoken}
    session.post(UPLOAD_PHILIPS_URL, files=files, data=upload_data)
    
    print('Done.')
