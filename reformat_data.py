from datetime import timedelta, datetime

import glob
import json
import os
import pandas as pd
from copy import deepcopy
from random import randrange
from tqdm import tqdm


def fix_nans_metadata():
    if not os.path.isfile('data/nonan_metadata.csv'):
        metadata = pd.read_csv('data/metadata.csv')

        index = metadata['publish_time'].index[metadata['publish_time'].isnull()]
        for i in index:
            sample = metadata['publish_time'].sample(1).values[0]
            print(sample)
            metadata['publish_time'][i] = sample
            print(metadata['publish_time'][i])

        metadata.to_csv('data/nonan_metadata.csv', index=False)


def format_name(author):
    middle_name = " ".join(author['middle'])

    if author['middle']:
        return " ".join([author['first'], middle_name, author['last']])
    else:
        return " ".join([author['first'], author['last']])


def format_affiliation(affiliation):
    text = []
    location = affiliation.get('location')
    if location:
        text.extend(list(affiliation['location'].values()))

    institution = affiliation.get('institution')
    if institution:
        text = [institution] + text
    return ", ".join(text)


def format_authors(authors, with_affiliation=False):
    name_ls = []

    for author in authors:
        name = format_name(author)
        if with_affiliation:
            affiliation = format_affiliation(author['affiliation'])
            if affiliation:
                name_ls.append(f"{name} ({affiliation})")
            else:
                name_ls.append(name)
        else:
            name_ls.append(name)

    return ", ".join(name_ls)


def format_body(body_text):
    texts = [(di['section'], di['text']) for di in body_text]
    texts_di = {di['section']: "" for di in body_text}

    for section, text in texts:
        texts_di[section] += text

    body = ""

    for section, text in texts_di.items():
        body += section
        body += "\n\n"
        body += text
        body += "\n\n"

    return body


def format_bib(bibs):
    if type(bibs) == dict:
        bibs = list(bibs.values())
    bibs = deepcopy(bibs)
    formatted = []

    for bib in bibs:
        bib['authors'] = format_authors(
            bib['authors'],
            with_affiliation=False
        )
        formatted_ls = [str(bib[k]) for k in ['title', 'authors', 'venue', 'year']]
        formatted.append(", ".join(formatted_ls))

    return "; ".join(formatted)


def load_files(dirname):
    filenames = os.listdir(dirname)
    raw_files = []

    for filename in tqdm(filenames):
        filename = dirname + filename
        file = json.load(open(filename, 'rb'))
        raw_files.append(file)

    return raw_files


def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


def generate_clean_df(all_files):
    d1 = datetime.strptime('1/1/2019 1:30 PM', '%m/%d/%Y %I:%M %p')
    d2 = datetime.strptime('1/3/2020 4:50 AM', '%m/%d/%Y %I:%M %p')

    cleaned_files = []
    metadata = pd.read_csv('data/nonan_metadata.csv')

    for file in tqdm(all_files):
        publish_time = metadata[metadata['sha'] == file['paper_id']]['publish_time'].values

        if len(publish_time) == 0:
            publish_time = str(random_date(d1, d2))[:10]
        else:
            publish_time = publish_time[0]

        features = [
            file['paper_id'],
            publish_time,
            file['metadata']['title'],
            format_authors(file['metadata']['authors']),
            format_authors(file['metadata']['authors'],
                           with_affiliation=True),
            format_body(file['abstract']),
            format_body(file['body_text']),
            format_bib(file['bib_entries']),
            file['metadata']['authors'],
            file['bib_entries']
        ]

        cleaned_files.append(features)

    col_names = ['paper_id', 'publish_time', 'title', 'authors',
                 'affiliations', 'abstract', 'text',
                 'bibliography', 'raw_authors', 'raw_bibliography']

    clean_df = pd.DataFrame(cleaned_files, columns=col_names)
    clean_df.head()

    return clean_df


travelling_paths = {
    'biorxiv': {
        'from': b'data/biorxiv_medrxiv/biorxiv_medrxiv/',
        'to': b'data/clean_biorxiv.csv'},
    'pmc': {
        'from': b'data/custom_license/custom_license/',
        'to': b'data/clean_pmc.csv'},
    'comm': {
        'from': b'data/comm_use_subset/comm_use_subset/',
        'to': b'data/clean_comm.csv'},
    'noncomm': {
        'from': b'data/noncomm_use_subset/noncomm_use_subset/',
        'to': b'data/clean_noncomm.csv'}
}


def main():
    if not os.path.isfile('data/transformer_finetuner.csv'):

        fix_nans_metadata()

        for k in travelling_paths.keys():
            if not os.path.isfile(travelling_paths[k]['to'].decode("utf-8")) and not os.path.isfile("data/merged.csv"):
                pmc_dir = travelling_paths[k]['from']
                pmc_files = load_files(pmc_dir)
                pmc_df = generate_clean_df(pmc_files)
                pmc_df.to_csv(travelling_paths[k]['to'].decode("utf-8"), index=False)

        # concatenate them csvs

        if not os.path.isfile("data/merged.csv"):
            all_paths = glob.glob('data/clean_*.csv')
            data = pd.concat([pd.read_csv(path) for path in all_paths], ignore_index=True)

            # cronological order and save
            data = data.sort_values(by=['publish_time'])
            data.drop_duplicates(['abstract', 'text'], inplace=True)
            data.to_csv('data/merged.csv')

        # concatenate title, abstract, authors, text, references

        data = pd.read_csv('data/merged.csv')
        one_column = data['title'] + data['authors'] + data['affiliations'] + data['abstract'] + data['text'] + data[
            'bibliography']

        one_column.to_csv('data/transformer_finetuner.csv')

        # format Transformers library


if __name__ == '__main__':
    main()
