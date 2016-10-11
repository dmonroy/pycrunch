import os

import pytest

import pycrunch


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


@pytest.mark.skipif(None in (CRUNCH_URL, CRUNCH_USER, CRUNCH_PASSWORD),
                    reason='Invalid test credentials.')
def test_basic_pycrunch_workflow():
    # Login.
    site = pycrunch.connect(CRUNCH_USER, CRUNCH_PASSWORD, CRUNCH_URL)
    assert isinstance(site, pycrunch.shoji.Catalog)

    # Create dataset.
    ds = site.datasets.create(DATASET_DOC).refresh()
    assert ds

    # Load initial data.
    pycrunch.importing.importer.append_rows(ds, ROWS)

    # Check the number of rows.
    table = site.session.get(ds.fragments.table, params=dict(limit=100)).payload
    col = list(table.data.values())[0]
    assert len(col) == len(ROWS) - 1  # excluding the header

    # Set an exclusion filter.
    pycrunch.datasets.exclusion(ds, 'identity < 6')
    table = site.session.get(ds.fragments.table, params=dict(limit=100)).payload
    col = list(table.data.values())[0]
    assert len(col) == 5

    # Clear the exclusion filter.
    pycrunch.datasets.exclusion(ds)
    table = site.session.get(ds.fragments.table, params=dict(limit=100)).payload
    col = list(table.data.values())[0]
    assert len(col) == len(ROWS) - 1  # excluding the header

    # Delete dataset.
    ds_url = ds.self
    ds.delete()
    with pytest.raises(pycrunch.ClientError):
        site.session.get(ds_url)


if __name__ == '__main__':
    test_basic_pycrunch_workflow()
    exit(0)
