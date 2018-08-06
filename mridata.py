import getpass
import boto3
from boto3.s3.transfer import S3Transfer
import os
import uuid
import json
import requests
from urllib.parse import urljoin
from tqdm import tqdm


MRIDATA_ORG = 'http://mridata.org/'
LOGIN_URL = urljoin(MRIDATA_ORG, 'accounts/login/')
UPLOAD_GE_URL = urljoin(MRIDATA_ORG, 'upload/ge')
UPLOAD_SIEMENS_URL = urljoin(MRIDATA_ORG, 'upload/siemens')
UPLOAD_PHILIPS_URL = urljoin(MRIDATA_ORG, 'upload/philips')
UPLOAD_ISMRMRD_URL = urljoin(MRIDATA_ORG, 'upload/ismrmrd')
UPLOAD_GET_TEMPORARL_CREDENTIALS_URL = urljoin(MRIDATA_ORG, 'upload/get_temp_credentials')

S3_URL = 'https://mridata-assets.s3.amazonaws.com/'
S3_BUCKET = 'mridata-assets'
S3_FOLDER = 'media/uploads'


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
    r = requests.get(urljoin(MRIDATA_ORG, 'download/{}'.format(uuid)), stream=True)
    total_size = int(r.headers.get('content-length', 0))
    chunk_size = 1024
    total_chunks = (total_size + chunk_size - 1) // chunk_size
    with open('{}.h5'.format(uuid), 'wb') as f:
        for chunk in tqdm(r.iter_content(chunk_size=chunk_size), total=total_chunks, unit='KB'):
            if chunk:
                f.write(chunk)


def get_temporary_credentials(session):
    r = session.get(UPLOAD_GET_TEMPORARL_CREDENTIALS_URL)

    return json.loads(r.content)


def hook(t):
  def inner(bytes_amount):
    t.update(bytes_amount)
  return inner


def upload_file_to_s3(session, filename):

    credentials = get_temporary_credentials(session)
    client = boto3.client(
        's3',
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],
    )
    transfer = S3Transfer(client)
    s3_filename = os.path.join(S3_FOLDER, '{}_{}'.format(uuid.uuid4(),
                                                         os.path.split(filename)[-1]))

    with tqdm(total=os.path.getsize(filename), unit='B', unit_scale=True) as t:
        transfer.upload_file(filename, S3_BUCKET, s3_filename,
                             extra_args={'ACL': 'public-read'}, callback=hook(t))

    s3_url = urljoin(S3_URL, s3_filename)
    return s3_url
    

def upload_ismrmrd(username, password,
                   ismrmrd_file, project_name,
                   anatomy='Unknown', fullysampled=None,
                   references='', comments='', funding_support='',
                   thumbnail_horizontal_flip=False,
                   thumbnail_vertical_flip=False,
                   thumbnail_transpose=False):

    if not username:
        username = input('Enter your user name: ')
    if not password:
        password = getpass.getpass('Enter your password: ')
    if not project_name:
        project_name = input('Enter your project name: ')

    print('Uploading {}...'.format(ismrmrd_file))
    session = login(username, password)
    ismrmrd_url = upload_file_to_s3(session, ismrmrd_file)

    session.get(UPLOAD_ISMRMRD_URL)
    csrftoken = session.cookies['csrftoken']
    upload_data = {'anatomy': anatomy, 'fullysampled': fullysampled,
                   'project_name': project_name,
                   'references': references, 'comments': comments,
                   'funding_support': funding_support,
                   'ismrmrd_file': ismrmrd_url,
                   'thumbnail_horizontal_flip': thumbnail_horizontal_flip,
                   'thumbnail_transpose': thumbnail_transpose,
                   'thumbnail_vertical_flip': thumbnail_vertical_flip,
                   'csrfmiddlewaretoken': csrftoken}
    p = session.post(UPLOAD_ISMRMRD_URL, data=upload_data)


def upload_ge(username, password,
              ge_file, project_name,
              anatomy='Unknown', fullysampled=None,
              references='', comments='', funding_support='',
              thumbnail_horizontal_flip=False,
              thumbnail_vertical_flip=False,
              thumbnail_transpose=False):

    if not username:
        username = input('Enter your user name: ')
    if not password:
        password = getpass.getpass('Enter your password: ')
    if not project_name:
        project_name = input('Enter your project name: ')

    print('Uploading {}...'.format(ge_file))
    session = login(username, password)
    ge_url = upload_file_to_s3(session, ge_file)
    
    session.get(UPLOAD_GE_URL)
    csrftoken = session.cookies['csrftoken']
    upload_data = {'anatomy': anatomy, 'fullysampled': fullysampled,
                   'project_name': project_name,
                   'references': references, 'comments': comments,
                   'funding_support': funding_support,
                   'ge_file': ge_url,
                   'thumbnail_horizontal_flip': thumbnail_horizontal_flip,
                   'thumbnail_transpose': thumbnail_transpose,
                   'thumbnail_vertical_flip': thumbnail_vertical_flip,
                   'csrfmiddlewaretoken': csrftoken}
    p = session.post(UPLOAD_GE_URL, data=upload_data)


def upload_siemens(username, password,
                   siemens_dat_file, project_name,
                   anatomy='Unknown', fullysampled=None,
                   references='', comments='', funding_support='',
                   thumbnail_horizontal_flip=False,
                   thumbnail_vertical_flip=False,
                   thumbnail_transpose=False):

    if not username:
        username = input('Enter your user name: ')
    if not password:
        password = getpass.getpass('Enter your password: ')
    if not project_name:
        project_name = input('Enter your project name: ')

    print('Uploading {}...'.format(siemens_dat_file))
    session = login(username, password)
    siemens_dat_url = upload_file_to_s3(session, siemens_dat_file)
    
    session.get(UPLOAD_SIEMENS_URL)
    csrftoken = session.cookies['csrftoken']
    upload_data = {'anatomy': anatomy, 'fullysampled': fullysampled,
                   'project_name': project_name,
                   'references': references, 'comments': comments,
                   'funding_support': funding_support,
                   'siemens_dat_file': siemens_dat_url,
                   'thumbnail_horizontal_flip': thumbnail_horizontal_flip,
                   'thumbnail_transpose': thumbnail_transpose,
                   'thumbnail_vertical_flip': thumbnail_vertical_flip,
                   'csrfmiddlewaretoken': csrftoken}
    p = session.post(UPLOAD_SIEMENS_URL, data=upload_data)

    
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
        username = input('Enter your user name: ')
    if not password:
        password = getpass.getpass('Enter your password: ')
    if not project_name:
        project_name = input('Enter your project name: ')

    print('Uploading {} {} {}...'.format(philips_lab_file, philips_sin_file, philips_raw_file))
    session = login(username, password)
    philips_lab_url = upload_file_to_s3(session, philips_lab_file)
    philips_sin_url = upload_file_to_s3(session, philips_sin_file)
    philips_raw_url = upload_file_to_s3(session, philips_raw_file)
    
    session.get(UPLOAD_PHILIPS_URL)
    csrftoken = session.cookies['csrftoken']
    upload_data = {'anatomy': anatomy, 'fullysampled': fullysampled,
                   'project_name': project_name,
                   'references': references, 'comments': comments,
                   'funding_support': funding_support,
                   'philips_sin_file': philips_sin_url,
                   'philips_lab_file': philips_lab_url,
                   'philips_raw_file': philips_raw_url,
                   'thumbnail_horizontal_flip': thumbnail_horizontal_flip,
                   'thumbnail_transpose': thumbnail_transpose,
                   'thumbnail_vertical_flip': thumbnail_vertical_flip,
                   'csrfmiddlewaretoken': csrftoken}
    p = session.post(UPLOAD_PHILIPS_URL, data=upload_data)
