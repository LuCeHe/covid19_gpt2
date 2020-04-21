import tarfile, os, shutil
from tqdm import tqdm
from covid19_gpt2.convenience_functions.utils import download_url

url = 'https://zenodo.org/record/3385851/files/unarXive.tar.bz2?download=1'
tarpath = r'data/unarXive.tar.bz2'
final_unarxive = r'data/unarxive.txt'

if not os.path.isfile(final_unarxive):

    if not os.path.isfile(tarpath):
        download_url(url, tarpath)

    tar = tarfile.open(tarpath, "r:bz2")
    #tar.extractall('data')
    tar.close()

    articles = os.listdir(r'data/unarXive/papers')
    articles = sorted([article for article in articles if article[:2] in ['20', '19', '18', '17']])  # ]])

    # ['<|endoftext|>']
    with open('data/unarxive.txt', 'w', encoding='cp850', errors='replace') as f_write:
        for article in tqdm(articles):
            with open(r'data/unarXive/papers/' + article, 'r', encoding='cp850', errors='replace') as f_read:
                for line in f_read:
                    f_write.write(line)
                f_write.write('<|endoftext|>')

    shutil.rmtree(r'data/unarXive/', ignore_errors=True)
    os.remove('data/unarXive.tar.bz2')

