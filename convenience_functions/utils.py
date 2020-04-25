# Copyright (c) 2018, 
#
# authors: Luca Celotti
# during their PhD at Universite' de Sherbrooke
# under the supervision of professor Jean Rouat
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#  - Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#  - Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import os, sys, io
import logging

import numpy as np
import yagmail
from tqdm import tqdm
import urllib.request
import pandas as pd

logger = logging.getLogger('mylogger')


class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def download_url(url, output_path):
    with DownloadProgressBar(unit='B', unit_scale=True,
                             miniters=1, desc=url.split('/')[-1]) as t:
        urllib.request.urlretrieve(url, filename=output_path, reporthook=t.update_to)


def email_results(
        folders_list=[],
        filepaths_list=[],
        text='',
        name_experiment='',
        receiver_emails=[]):
    if not isinstance(receiver_emails, list): receiver_emails = [receiver_emails]
    random_string = ''.join([str(r) for r in np.random.choice(10, 4)])
    yag = yagmail.SMTP('my.experiments.336@gmail.com', ':(1234abcd')
    subject = random_string + ' The Experiment is [DONE] ! ' + name_experiment

    logger.info('Sending Results via Email!')
    # send specific files specified
    for filepath in filepaths_list + [text]:
        try:
            contents = [filepath]
            for email in receiver_emails:
                yag.send(to=email, contents=contents, subject=subject)
        except:
            pass

    # send content of folders
    for folderpath in folders_list:
        content = os.listdir(folderpath)
        failed = []
        for dir in tqdm(content):
            try:
                path = os.path.join(folderpath, dir)
                contents = [path]
                for email in receiver_emails:
                    yag.send(to=email, contents=contents, subject=subject)
            except:
                failed.append(dir)

        contents = ['among all the files\n\n{} \n\nthese failed to be sent: \n\n{}'.format('\n'.join(content),
                                                                                           '\n'.join(failed))]
        for email in receiver_emails:
            yag.send(to=email, contents=contents, subject=subject)



def small_version(long_txt, short_txt):
    if not os.path.isfile(short_txt):
        data = pd.read_csv(long_txt, sep=" ", header=None)
        small_data = data.sample(2)
        small_data.to_csv(short_txt, header=None, index=None, sep=' ', mode='a')



class ProgressFileObject(io.FileIO):
    def __init__(self, path, *args, **kwargs):
        self._total_size = os.path.getsize(path)
        io.FileIO.__init__(self, path, *args, **kwargs)

    def read(self, size):
        percentage = np.array(self.tell()/self._total_size*100).round(3)
        percentage_string = str(percentage*1e3)
        if percentage_string[-2] == '5':
            sys.stdout.write("Decompress progress: {}% \r".format(percentage))
            sys.stdout.flush()
        return io.FileIO.read(self, size)

