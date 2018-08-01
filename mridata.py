import datetime
import requests
from urllib.parse import urljoin
from tqdm import tqdm


WEBSITE = 'http://mridata-web.us-west-2.elasticbeanstalk.com/'
LOGIN_URL = urljoin(WEBSITE, 'accounts/login/')
UPLOAD_GE_URL = urljoin(WEBSITE, 'upload_ge/')
UPLOAD_SIEMENS_URL = urljoin(WEBSITE, 'upload_siemens/')
UPLOAD_PHILIPS_URL = urljoin(WEBSITE, 'upload_philips/')
UPLOAD_ISMRMRD_URL = urljoin(WEBSITE, 'upload_ismrmrd/')


def login(username, password):

    session = requests.Session()
    session.get(LOGIN_URL)
    csrftoken = session.cookies['csrftoken']
    login_data = {'username': username, 'password': password,
                  'csrfmiddlewaretoken': csrftoken}
    p = session.post(LOGIN_URL, data=login_data)

    if 'login'in p.url:
        raise Exception('Cannot find user with the given credentials.')

    return session


def download(uuid):
    
    r = requests.get(urljoin(WEBSITE, 'data/{}/download'.format(uuid)), stream=True)
    total_size = int(r.headers.get('content-length', 0))
    chunk_size = 1024
    total_chunks = (total_size + chunk_size - 1) // chunk_size
    with open('{}.h5'.format(uuid), 'wb') as f:
        for chunk in tqdm(r.iter_content(chunk_size=chunk_size), total=total_chunks, unit='KB'):
            if chunk:
                f.write(chunk)    


def upload_ismrmrd(username, password,
                   ismrmrd_file, project_name,
                   anatomy='Unknown', fullysampled=None,
                   references='', comments='', funding_support='',
                   thumbnail_horizontal_flip=False,
                   thumbnail_vertical_flip=False,
                   thumbnail_transpose=False):

    if not username:
        username = input('Enter your user name:')
    if not password:
        password = input('Enter your password:')
    if not project_name:
        project_name = input('Enter your project name:')

    with open(ismrmrd_file, 'rb') as f:
        files = {'ismrmrd_file': f}
        done = False
        while not done:
            print('Uploading {}...'.format(ismrmrd_file))
            session = login(username, password)
            session.get(UPLOAD_ISMRMRD_URL)
            csrftoken = session.cookies['csrftoken']
            upload_data = {'anatomy': anatomy, 'fullysampled': fullysampled,
                           'project_name': project_name,
                           'references': references, 'comments': comments,
                           'funding_support': funding_support,
                           'thumbnail_horizontal_flip': thumbnail_horizontal_flip,
                           'thumbnail_transpose': thumbnail_transpose,
                           'thumbnail_vertical_flip': thumbnail_vertical_flip,
                           'csrfmiddlewaretoken': csrftoken}
            p = session.post(UPLOAD_ISMRMRD_URL, files=files, data=upload_data)
            done = '{} uploaded.'.format(ismrmrd_file) in p.text
            if not done:
                print('Uploading failed, retrying...')
    
    print('Upload successful.')


def upload_ge(username, password,
              ge_file, project_name,
              anatomy='Unknown', fullysampled=None,
              references='', comments='', funding_support='',
              thumbnail_horizontal_flip=False,
              thumbnail_vertical_flip=False,
              thumbnail_transpose=False):

    if not username:
        username = input('Enter your user name:')
    if not password:
        password = input('Enter your password:')
    if not project_name:
        project_name = input('Enter your project name:')

    with open(ge_file, 'rb') as f:
        files = {'ge_file': f}
        done = False
        while not done:
            print('Uploading {}...'.format(ge_file))
            session = login(username, password)
            session.get(UPLOAD_GE_URL)
            csrftoken = session.cookies['csrftoken']
            upload_data = {'anatomy': anatomy, 'fullysampled': fullysampled,
                           'project_name': project_name,
                           'references': references, 'comments': comments,
                           'funding_support': funding_support,
                           'thumbnail_horizontal_flip': thumbnail_horizontal_flip,
                           'thumbnail_transpose': thumbnail_transpose,
                           'thumbnail_vertical_flip': thumbnail_vertical_flip,
                           'csrfmiddlewaretoken': csrftoken}
            p = session.post(UPLOAD_GE_URL, files=files, data=upload_data)
            done = '{} uploaded.'.format(ge_file) in p.text
            if not done:
                print('Uploading failed, retrying...')
    
    print('Upload successful.')


def upload_siemens(username, password,
                   siemens_dat_file, project_name,
                   anatomy='Unknown', fullysampled=None,
                   references='', comments='', funding_support='',
                   thumbnail_horizontal_flip=False,
                   thumbnail_vertical_flip=False,
                   thumbnail_transpose=False):

    if not username:
        username = input('Enter your user name:')
    if not password:
        password = input('Enter your password:')
    if not project_name:
        project_name = input('Enter your project name:')

    with open(siemens_dat_file, 'rb') as f:
        files = {'siemens_dat_file': f}
        done = False
        while not done:
            print('Uploading {}...'.format(siemens_dat_file))
            session = login(username, password)
            session.get(UPLOAD_SIEMENS_URL)
            csrftoken = session.cookies['csrftoken']
            upload_data = {'anatomy': anatomy, 'fullysampled': fullysampled,
                           'project_name': project_name,
                           'references': references, 'comments': comments,
                           'funding_support': funding_support,
                           'thumbnail_horizontal_flip': thumbnail_horizontal_flip,
                           'thumbnail_transpose': thumbnail_transpose,
                           'thumbnail_vertical_flip': thumbnail_vertical_flip,
                           'csrfmiddlewaretoken': csrftoken}
            p = session.post(UPLOAD_SIEMENS_URL, files=files, data=upload_data)
            done = '{} uploaded.'.format(siemens_dat_file) in p.text
            if not done:
                print('Uploading failed, retrying...')
    
    print('Upload successful.')

    
def upload_philips(username, password,
                   philips_basename, project_name,
                   anatomy='Unknown', fullysampled=None,
                   references='', comments='', funding_support='',
                   thumbnail_horizontal_flip=False,
                   thumbnail_vertical_flip=False,
                   thumbnail_transpose=False):
    
    philips_lab_file = philips_basename + '.lab'
    philips_sin_file = philips_basename + '.sin'
    philips_raw_file = philips_basename + '.raw'
    
    if not username:
        username = input('Enter your user name:')
    if not password:
        password = input('Enter your password:')
    if not project_name:
        project_name = input('Enter your project name:')

    with open(philips_lab_file, 'rb') as f1, open(philips_sin_file, 'rb') as f2, open(philips_raw_file, 'rb') as f3:
        files = {'philips_lab_file': f1,
                 'philips_sin_file': f2,
                 'philips_raw_file': f3}
        done = False
        while not done:
            print('Uploading {} {} {}...'.format(philips_lab_file,
                                                 philips_sin_file, philips_raw_file))
            session = login(username, password)
            session.get(UPLOAD_PHILIPS_URL)
            csrftoken = session.cookies['csrftoken']
            upload_data = {'anatomy': anatomy, 'fullysampled': fullysampled,
                           'project_name': project_name,
                           'references': references, 'comments': comments,
                           'funding_support': funding_support,
                           'thumbnail_horizontal_flip': thumbnail_horizontal_flip,
                           'thumbnail_transpose': thumbnail_transpose,
                           'thumbnail_vertical_flip': thumbnail_vertical_flip,
                           'csrfmiddlewaretoken': csrftoken}
            p = session.post(UPLOAD_PHILIPS_URL, files=files, data=upload_data)
            done = '{} {} {} uploaded.'.format(philips_lab_file,
                                               philips_sin_file, philips_raw_file) in p.text
            if not done:
                print('Uploading failed, retrying...')
    
    print('Upload successful.')
