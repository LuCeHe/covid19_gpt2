import tarfile, os, shutil
from tqdm import tqdm
from covid19_gpt2.convenience_functions.utils import download_url, small_version

CDIR = os.path.dirname(os.path.realpath(__file__))
DATADIR = os.path.join(CDIR, 'data')

url = 'https://zenodo.org/record/3385851/files/unarXive.tar.bz2?download=1'
tarpath = os.path.join(DATADIR, 'unarXive.tar.bz2')
UNATXT = os.path.join(DATADIR, 'unarxive.txt')
UNASMALLTXT = os.path.join(DATADIR, 'unarxive_small.txt')

if not os.path.isfile(UNATXT):
    try:
        os.mkdir(DATADIR)
    except:
        pass

    if not os.path.isfile(tarpath):
        download_url(url, tarpath)

    os.system('pv data/unarXive.tar.bz2 | tar xzf - -C data')
    #os.system('tar -v -xf {} -C {} | tqdm --total $(tar -tvf {} | wc -l) > /dev/null'.format(tarpath, DATADIR, tarpath))

    #try:
        #tar = tarfile.open(tarpath, "r:bz2")

        #tar.extractall('data')
        #tar.close()
    #except KeyboardInterrupt:
    #    pass

    articles = os.listdir(r'data/unarXive/papers')
    articles = sorted([article for article in articles if article[:2] in ['20', '19', '18', '17']])  # ]])

    # ['<|endoftext|>']
    with open(UNATXT, 'w', encoding='cp850', errors='replace') as f_write:
        for article in tqdm(articles):
            with open(r'data/unarXive/papers/' + article, 'r', encoding='cp850', errors='replace') as f_read:
                for line in f_read:
                    f_write.write(line)
                f_write.write('<|endoftext|>')

    shutil.rmtree(r'data/unarXive/', ignore_errors=True)
    os.remove('data/unarXive.tar.bz2')


    small_version(UNATXT, UNASMALLTXT)

