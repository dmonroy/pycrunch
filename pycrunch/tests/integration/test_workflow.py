import os

import pytest

import pycrunch
from pycrunch import pandaslib


CRUNCH_URL = os.environ.get('CRUNCH_TEST_URL')
CRUNCH_USER = os.environ.get('CRUNCH_TEST_USER')
CRUNCH_PASSWORD = os.environ.get('CRUNCH_TEST_PASSWORD')


# Metadata.
DATASET_DOC = {
    'body': {
        'name': 'pycrunch test dataset',
        'description': 'pycrunch integration tests',
        'table': {
            'element': 'crunch:table',
            'metadata': {
                'identity': {
                    'alias': 'identity',
                    'name': 'ID',
                    'type': 'numeric'
                },
                'ip_address': {
                    'alias': 'ip_address',
                    'name': 'Public IP Address',
                    'type': 'text'
                },
                'operating_system': {
                    'alias': 'operating_system',
                    'name': 'Operating System',
                    'type': 'text'
                },
                'registration_time': {
                    'alias': 'registration_time',
                    'name': 'Registration Time',
                    'resolution': 'ms',
                    'type': 'datetime'
                }
            },
            'order': [
                {
                    'entities': [
                        'identity',
                        'ip_address',
                        'operating_system',
                        'registration_time'
                    ],
                    'group': 'ungrouped'
                }
            ]
        }
    }
}


# Data
ROWS = [
    ['identity', 'ip_address', 'operating_system', 'registration_time'],
    [1,          '10.0.0.1',   'Linux',            '2014-04-21T10:00:00+00:00'],
    [2,          '10.0.0.2',   'Solaris',          '2014-05-10T00:00:00+00:00'],
    [3,          '10.0.0.3',   'Linux',            '2015-01-01T00:00:00+00:00'],
    [4,          '10.0.0.4',   'Windows',          '2015-01-02T00:00:00+00:00'],
    [5,          '10.0.0.5',   'Windows',          '2015-02-01T00:00:00+00:00'],
    [6,          '10.0.0.6',   'MacOS',            '2015-06-01T00:00:00+00:00'],
    [7,          '10.0.0.7',   'Windows',          '2015-12-30T00:00:00+00:00'],
    [8,          '10.0.0.8',   'Minix',            '2016-01-01T00:00:00+00:00'],
    [9,          '10.0.0.9',   'FreeBSD',          '2016-02-01T00:00:00+00:00'],
    [10,         '10.0.0.10',  'NetBSD',           '2015-03-01T00:00:00+00:00'],
]


def invalid_credentials():
    return any(
        item is None
        for item in (CRUNCH_URL, CRUNCH_USER, CRUNCH_PASSWORD)
    )


@pytest.fixture(scope='module')
def site():
    if invalid_credentials():
        pytest.skip('Invalid test credentials.')

    return pycrunch.connect(CRUNCH_USER, CRUNCH_PASSWORD, CRUNCH_URL)


@pytest.fixture(scope='module')
def dataset(site):
    if invalid_credentials():
        pytest.skip('Invalid test credentials.')

    ds = site.datasets.create(DATASET_DOC).refresh()
    yield ds
    ds.delete()


@pytest.mark.skipif(invalid_credentials(), reason='Invalid test credentials.')
def test_basic_pycrunch_workflow(site, dataset):
    # Ensure fixtures are OK.
    assert isinstance(site, pycrunch.shoji.Catalog)
    assert isinstance(dataset, pycrunch.shoji.Entity)

    # Load initial data.
    pycrunch.importing.importer.append_rows(dataset, ROWS)

    # Check the initial number of rows.
    df = pandaslib.dataframe(dataset)
    assert len(df) == len(ROWS) - 1  # excluding the header

    # Set an exclusion filter.
    pycrunch.datasets.exclusion(dataset, 'identity < 6')
    df = pandaslib.dataframe(dataset)
    assert len(df) == 5

    # Clear the exclusion filter.
    pycrunch.datasets.exclusion(dataset)
    df = pandaslib.dataframe(dataset)
    assert len(df) == len(ROWS) - 1  # excluding the header
