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
                },
                'speak_spanish': {
                    'alias': 'speak_spanish',
                    'categories': [
                        {
                            'id': 1,
                            'missing': False,
                            'name': 'I speak Spanish primarily',
                            'numeric_value': 1
                        },
                        {
                            'id': 2,
                            'missing': False,
                            'name': 'I speak both Spanish and English equally',
                            'numeric_value': 2
                        },
                        {
                            'id': 3,
                            'missing': False,
                            'name': 'I speak English primarily but can speak Spanish',
                            'numeric_value': 3
                        },
                        {
                            'id': 4,
                            'missing': False,
                            'name': 'I can not speak Spanish',
                            'numeric_value': 4
                        },
                        {
                            'id': 32766,
                            'missing': True,
                            'name': 'skipped',
                            'numeric_value': None
                        },
                        {
                            'id': 32767,
                            'missing': True,
                            'name': 'not asked',
                            'numeric_value': None
                        },
                        {
                            'id': -1,
                            'missing': True,
                            'name': 'No Data',
                            'numeric_value': None
                        }
                    ],
                    'name': 'Do you speak Spanish?',
                    'type': 'categorical'
                },
                'hobbies': {
                    'alias': 'hobbies',
                    'categories': [
                        {
                            'id': 1,
                            'missing': False,
                            'name': 'Very interested',
                            'numeric_value': 1
                        },
                        {
                            'id': 2,
                            'missing': False,
                            'name': 'Somewhat interested',
                            'numeric_value': 2
                        },
                        {
                            'id': 3,
                            'missing': False,
                            'name': 'A little interested',
                            'numeric_value': 3
                        },
                        {
                            'id': 4,
                            'missing': False,
                            'name': 'Not at all interested',
                            'numeric_value': 4
                        },
                        {
                            'id': 32766,
                            'missing': True,
                            'name': 'skipped',
                            'numeric_value': None
                        },
                        {
                            'id': 32767,
                            'missing': True,
                            'name': 'not asked',
                            'numeric_value': None
                        },
                        {
                            'id': -1,
                            'missing': True,
                            'name': 'No Data',
                            'numeric_value': None
                        }
                    ],
                    'name': 'Hobbies',
                    'subvariables': [
                        {
                            'alias': 'hobbies_1',
                            'name': 'Sports'
                        },
                        {
                            'alias': 'hobbies_2',
                            'name': 'Video Games'
                        },
                        {
                            'alias': 'hobbies_3',
                            'name': 'Reading'
                        },
                        {
                            'alias': 'hobbies_4',
                            'name': 'Outdoor Activities'
                        }
                    ],
                    'type': 'categorical_array'
                },
                'music': {
                    'alias': 'music',
                    'categories': [
                        {
                            'id': 1,
                            'missing': False,
                            'name': 'selected',
                            'numeric_value': 1,
                            'selected': True
                        },
                        {
                            'id': 2,
                            'missing': False,
                            'name': 'not selected',
                            'numeric_value': 2,
                            'selected': False
                        },
                        {
                            'id': 32767,
                            'missing': True,
                            'name': 'not asked',
                            'numeric_value': None
                        },
                        {
                            'id': 32766,
                            'missing': True,
                            'name': 'skipped',
                            'numeric_value': None
                        },
                        {
                            'id': -1,
                            'missing': True,
                            'name': 'No Data',
                            'numeric_value': None
                        }
                    ],
                    'name': 'Music',
                    'subvariables': [
                        {
                            'alias': 'music_1',
                            'name': 'Pop'
                        },
                        {
                            'alias': 'music_2',
                            'name': 'Rock'
                        },
                        {
                            'alias': 'music_97',
                            'name': 'Other'
                        },
                        {
                            'alias': 'music_98',
                            'name': 'Don\'t know'
                        },
                        {
                            'alias': 'music_99',
                            'name': 'None of these'
                        }
                    ],
                    'type': 'multiple_response'
                }
            },
            'order': [
                {
                    'entities': [
                        'identity',
                        'ip_address',
                        'operating_system',
                        'registration_time',
                        'speak_spanish',
                        'hobbies',
                        'music'
                    ],
                    'group': 'ungrouped'
                }
            ]
        }
    }
}

# Data
ROWS = [
    ['identity', 'ip_address', 'operating_system', 'registration_time', 'speak_spanish', 'hobbies_1', 'hobbies_2', 'hobbies_3', 'hobbies_4', 'music_1', 'music_2', 'music_97', 'music_98', 'music_99'],
    [1,  '10.0.0.1',  'Linux',   '2014-04-21T10:00:00+00:00', 1,     32767, 32767, 32767, 32767, 2, 2, 1, 2, 2],
    [2,  '10.0.0.2',  'Solaris', '2014-05-10T00:00:00+00:00', 1,     32766, 1,     1,     4,     1, 1, 1, 2, 2],
    [3,  '10.0.0.3',  'Linux',   '2015-01-01T00:00:00+00:00', 2,     2,     1,     2,     2,     2, 2, 2, 2, 1],
    [4,  '10.0.0.4',  'Windows', '2015-01-02T00:00:00+00:00', 3,     4,     3,     2,     1,     1, 2, 1, 2, 2],
    [5,  '10.0.0.5',  'Windows', '2015-02-01T00:00:00+00:00', 1,     1,     2,     32766, 4,     1, 1, 1, 2, 2],
    [6,  '10.0.0.6',  'MacOS',   '2015-06-01T00:00:00+00:00', 4,     2,     4,     4,     1,     2, 2, 1, 2, 2],
    [7,  '10.0.0.7',  'Windows', '2015-12-30T00:00:00+00:00', 32766, 1,     32766, 4,     3,     2, 2, 2, 1, 2],
    [8,  '10.0.0.8',  'Minix',   '2016-01-01T00:00:00+00:00', 32766, 2,     1,     1,     2,     2, 2, 2, 1, 2],
    [9,  '10.0.0.9',  'FreeBSD', '2016-02-01T00:00:00+00:00', 32767, 1,     1,     1,     32766, 1, 2, 1, 2, 2],
    [10, '10.0.0.10', 'NetBSD',  '2015-03-01T00:00:00+00:00', 2,     4,     3,     4,     1,     2, 2, 1, 2, 2],
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
