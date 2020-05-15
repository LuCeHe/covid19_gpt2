import tarfile, os, shutil
from tqdm import tqdm
from covid19_gpt2.convenience_functions.utils import download_url, small_version, ProgressFileObject

CDIR = os.path.dirname(os.path.realpath(__file__))
DATADIR = os.path.join(CDIR, 'data')

comm_url = 'https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/latest/comm_use_subset.tar.gz'
noncomm_url = 'https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/latest/noncomm_use_subset.tar.gz'
custom_url = 'https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/latest/custom_license.tar.gz'
biorxiv_url = 'https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/latest/biorxiv_medrxiv.tar.gz'
metadata_url = 'https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/latest/metadata.csv'


url = 'https://zenodo.org/record/3385851/files/unarXive.tar.bz2?download=1'
tarpath = os.path.join(DATADIR, 'unarXive.tar.bz2')
UNATXT = os.path.join(DATADIR, 'unarxive.txt')
UNASMALLTXT = os.path.join(DATADIR, 'unarxive_small.txt')

DATADIR = os.path.join(CDIR, 'data')
COVIDTXT = os.path.join(DATADIR, 'covid19.txt')

if not os.path.isfile(UNATXT):
    try:
        os.mkdir(DATADIR)
    except:
        pass

    if not os.path.isfile(tarpath):
        try:
            download_url(url, tarpath)
        except Exception as e:
            print(e)


if not os.path.isfile(COVIDTXT):
    try:
        os.mkdir(DATADIR)
    except:
        pass

    print('Downloading Data...')

    for url in [comm_url, noncomm_url, custom_url, biorxiv_url, metadata_url]:
        _, filename = os.path.split(url)

        path = os.path.join(*[CDIR, 'data', filename])
        if not os.path.isdir(path[:-7]):
            download_url(url, path)