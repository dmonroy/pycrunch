#!/usr/bin/env python

import math
import os

import pycrunch
from pycrunch import pandaslib
from pycrunch.transformations import create_categorical
from pycrunch.recodes import combine_categories
from pycrunch.recodes import combine_responses


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
    [11, '10.0.0.10', 'NetBSD',  '2015-03-01T00:01:00+00:00', 2,     4,     3,     4,     1,     1, 1, 1, 1, 1],
    [12, '10.0.0.10', 'NetBSD',  '2015-03-01T00:02:00+00:00', 2,     4,     3,     4,     1,     2, 2, 2, 2, 2],
]


def invalid_credentials():
    return any(
        item is None
        for item in (CRUNCH_URL, CRUNCH_USER, CRUNCH_PASSWORD)
    )


def isnan(obj):
    if not isinstance(obj, float):
        return False
    return math.isnan(obj)


def main():
    assert not invalid_credentials()

    # Login.
    site = pycrunch.connect(CRUNCH_USER, CRUNCH_PASSWORD, CRUNCH_URL)
    assert isinstance(site, pycrunch.shoji.Catalog)

    # Create the test dataset.
    dataset = site.datasets.create(DATASET_DOC).refresh()
    assert isinstance(dataset, pycrunch.shoji.Entity)

    try:
        # Load initial data.
        pycrunch.importing.importer.append_rows(dataset, ROWS)

        # Check the initial number of rows.
        df = pandaslib.dataframe(dataset)
        assert len(df) == len(ROWS) - 1  # excluding the header

        # 1. Exclusion Filter Integration Tests

        # 1.1 Set a simple exclusion filter.

        pycrunch.datasets.exclusion(dataset, 'identity > 5')
        df = pandaslib.dataframe(dataset)
        assert len(df) == 5
        assert not any(r['identity'] > 5 for _, r in df.iterrows())

        # 1.2 More complex exclusion filters involving a categorical variable.

        expr = 'speak_spanish in [32766]'
        pycrunch.datasets.exclusion(dataset, expr)
        df = pandaslib.dataframe(dataset)
        valid_ids = [
            row[0] for row in ROWS
            if row[0] != 'identity' and row[4] != 32766
        ]
        assert len(df) == len(valid_ids)
        for _, row in df.iterrows():
            assert row['identity'] in valid_ids

        expr = 'speak_spanish in (32766, 32767)'
        pycrunch.datasets.exclusion(dataset, expr)
        df = pandaslib.dataframe(dataset)
        valid_ids = [
            row[0] for row in ROWS
            if row[0] != 'identity' and row[4] not in (32766, 32767)
        ]
        assert len(df) == len(valid_ids)
        for _, row in df.iterrows():
            assert row['identity'] in valid_ids
            assert not isnan(row['speak_spanish'])

        expr = 'not (speak_spanish in (1, 2) and operating_system == "Linux")'
        pycrunch.datasets.exclusion(dataset, expr)
        df = pandaslib.dataframe(dataset)
        valid_ids = [
            row[0] for row in ROWS
            if row[0] != 'identity' and row[4] in (1, 2) and row[2] == 'Linux'
        ]
        assert len(df) == len(valid_ids)
        for _, row in df.iterrows():
            assert row['identity'] in valid_ids
            assert row['speak_spanish'] in \
                   ('I speak Spanish primarily',
                    'I speak both Spanish and English equally')
            assert row['operating_system'] == 'Linux'

        # 1.3 Exclusion filters with `has_any`.

        expr = 'hobbies.has_any([32766])'
        pycrunch.datasets.exclusion(dataset, expr)
        df = pandaslib.dataframe(dataset)
        valid_ids = [
            row[0] for row in ROWS
            if row[0] != 'identity' and 32766 not in row[5:9]
        ]
        assert len(df) == len(valid_ids)
        for _, row in df.iterrows():
            assert row['identity'] in valid_ids
            assert {'?': 32766} not in row['hobbies']

        expr = 'not hobbies.has_any([32766])'
        pycrunch.datasets.exclusion(dataset, expr)
        df = pandaslib.dataframe(dataset)
        valid_ids = [
            row[0] for row in ROWS
            if row[0] != 'identity' and 32766 in row[5:9]
        ]
        assert len(df) == len(valid_ids)
        for _, row in df.iterrows():
            assert row['identity'] in valid_ids
            assert {'?': 32766} in row['hobbies']

        expr = 'hobbies.has_any([32766, 32767])'
        pycrunch.datasets.exclusion(dataset, expr)
        df = pandaslib.dataframe(dataset)
        valid_ids = [
            row[0] for row in ROWS
            if row[0] != 'identity'
            and 32766 not in row[5:9] and 32767 not in row[5:9]
        ]
        assert len(df) == len(valid_ids)
        for _, row in df.iterrows():
            assert row['identity'] in valid_ids
            assert {'?': 32766} not in row['hobbies'] and \
                   {'?': 32767} not in row['hobbies']

        expr = 'music.has_any([32766])'
        pycrunch.datasets.exclusion(dataset, expr)
        df = pandaslib.dataframe(dataset)
        valid_ids = [
            row[0] for row in ROWS
            if row[0] != 'identity' and 32766 not in row[9:14]
        ]
        assert len(df) == len(valid_ids)
        for _, row in df.iterrows():
            assert row['identity'] in valid_ids
            assert {'?': 32766} not in row['music']

        expr = 'music.has_any([1])'
        pycrunch.datasets.exclusion(dataset, expr)
        df = pandaslib.dataframe(dataset)
        valid_ids = [
            row[0] for row in ROWS
            if row[0] != 'identity' and 1 not in row[9:14]
        ]
        assert len(df) == len(valid_ids)
        for _, row in df.iterrows():
            assert row['identity'] in valid_ids
            assert 1 not in row['music']

        expr = 'music.has_any([1, 2])'
        pycrunch.datasets.exclusion(dataset, expr)
        df = pandaslib.dataframe(dataset)
        valid_ids = [
            row[0] for row in ROWS
            if row[0] != 'identity'
            and 1 not in row[9:14] and 2 not in row[9:14]
        ]
        assert len(df) == len(valid_ids)
        for _, row in df.iterrows():
            assert row['identity'] in valid_ids
            assert 1 not in row['music'] and 2 not in row['music']

        # 1.4 Exclusion filters with `has_all`.

        expr = 'hobbies.has_all([32767])'
        pycrunch.datasets.exclusion(dataset, expr)
        df = pandaslib.dataframe(dataset)
        valid_ids = [
            row[0] for row in ROWS
            if row[0] != 'identity' and row[5:9] != [32767, 32767, 32767, 32767]
        ]
        assert len(df) == len(valid_ids)
        for _, row in df.iterrows():
            assert row['identity'] in valid_ids
            assert row['hobbies'] != [{'?': 32767}, {'?': 32767},
                                      {'?': 32767}, {'?': 32767}]

        expr = 'not hobbies.has_all([32767])'
        pycrunch.datasets.exclusion(dataset, expr)
        df = pandaslib.dataframe(dataset)
        valid_ids = [
            row[0] for row in ROWS
            if row[0] != 'identity' and row[5:9] == [32767, 32767, 32767, 32767]
        ]
        assert len(df) == len(valid_ids)
        for _, row in df.iterrows():
            assert row['identity'] in valid_ids
            assert row['hobbies'] == [{'?': 32767}, {'?': 32767},
                                      {'?': 32767}, {'?': 32767}]

        expr = 'music.has_all([1])'
        pycrunch.datasets.exclusion(dataset, expr)
        df = pandaslib.dataframe(dataset)
        valid_ids = [
            row[0] for row in ROWS
            if row[0] != 'identity' and row[9:14] != [1, 1, 1, 1, 1]
        ]
        assert len(df) == len(valid_ids)
        for _, row in df.iterrows():
            assert row['identity'] in valid_ids
            assert row['music'] != [1, 1, 1, 1, 1]

        expr = 'music.has_all([1]) or music.has_all([2])'
        pycrunch.datasets.exclusion(dataset, expr)
        df = pandaslib.dataframe(dataset)
        valid_ids = [
            row[0] for row in ROWS
            if row[0] != 'identity'
            and (row[9:14] != [1, 1, 1, 1, 1] and row[9:14] != [2, 2, 2, 2, 2])
        ]
        assert len(df) == len(valid_ids)
        for _, row in df.iterrows():
            assert row['identity'] in valid_ids
            assert row['music'] != [1, 1, 1, 1, 1] and \
                   row['music'] != [2, 2, 2, 2, 2]

        expr = 'not ( music.has_all([1]) or music.has_all([2]) )'
        pycrunch.datasets.exclusion(dataset, expr)
        df = pandaslib.dataframe(dataset)
        valid_ids = [
            row[0] for row in ROWS
            if row[0] != 'identity'
            and (row[9:14] == [1, 1, 1, 1, 1] or row[9:14] == [2, 2, 2, 2, 2])
        ]
        assert len(df) == len(valid_ids)
        for _, row in df.iterrows():
            assert row['identity'] in valid_ids
            assert row['music'] == [1, 1, 1, 1, 1] or \
                   row['music'] == [2, 2, 2, 2, 2]

        # 1.5 Exclusion filters with `duplicates`.

        expr = 'ip_address.duplicates()'
        pycrunch.datasets.exclusion(dataset, expr)
        df = pandaslib.dataframe(dataset)
        seen_ip_addresses = []
        for _, row in df.iterrows():
            assert row['ip_address'] not in seen_ip_addresses
            seen_ip_addresses.append(row['ip_address'])

        # 1.6 Exclusion filters with `valid` and `missing`.

        expr = 'valid(speak_spanish)'
        pycrunch.datasets.exclusion(dataset, expr)
        df = pandaslib.dataframe(dataset)
        valid_ids = [
            row[0] for row in ROWS
            if row[0] != 'identity' and row[4] in (32766, 32767)
        ]
        assert len(df) == len(valid_ids)
        for _, row in df.iterrows():
            assert row['identity'] in valid_ids
            assert isnan(row['speak_spanish'])

        expr = 'not valid(speak_spanish)'
        pycrunch.datasets.exclusion(dataset, expr)
        df = pandaslib.dataframe(dataset)
        valid_ids = [
            row[0] for row in ROWS
            if row[0] != 'identity' and row[4] not in (32766, 32767)
        ]
        assert len(df) == len(valid_ids)
        for _, row in df.iterrows():
            assert row['identity'] in valid_ids
            assert not isnan(row['speak_spanish'])

        expr = 'missing(speak_spanish)'
        pycrunch.datasets.exclusion(dataset, expr)
        df = pandaslib.dataframe(dataset)
        valid_ids = [
            row[0] for row in ROWS
            if row[0] != 'identity' and row[4] not in (32766, 32767)
        ]
        assert len(df) == len(valid_ids)
        for _, row in df.iterrows():
            assert row['identity'] in valid_ids
            assert not isnan(row['speak_spanish'])

        expr = 'missing(hobbies)'
        pycrunch.datasets.exclusion(dataset, expr)
        df = pandaslib.dataframe(dataset)
        valid_ids = [
            row[0] for row in ROWS
            if row[0] != 'identity'
            and (row[5:9] != [32766, 32766, 32766, 32766]
                 and row[5:9] != [32767, 32767, 32767, 32767])
        ]
        assert len(df) == len(valid_ids)
        for _, row in df.iterrows():
            assert row['identity'] in valid_ids
            assert row['hobbies'] != [{'?': 32766}, {'?': 32766},
                                      {'?': 32766}, {'?': 32766}] \
                   and row['hobbies'] != [{'?': 32767}, {'?': 32767},
                                         {'?': 32767}, {'?': 32767}]

        expr = 'not missing(hobbies)'
        pycrunch.datasets.exclusion(dataset, expr)
        df = pandaslib.dataframe(dataset)
        valid_ids = [
            row[0] for row in ROWS
            if row[0] != 'identity'
            and (row[5:9] == [32766, 32766, 32766, 32766]
                 or row[5:9] == [32767, 32767, 32767, 32767])
        ]
        assert len(df) == len(valid_ids)
        for _, row in df.iterrows():
            assert row['identity'] in valid_ids
            assert row['hobbies'] == [{'?': 32766}, {'?': 32766},
                                      {'?': 32766}, {'?': 32766}] \
                   or row['hobbies'] == [{'?': 32767}, {'?': 32767},
                                         {'?': 32767}, {'?': 32767}]

        expr = 'valid(hobbies)'
        pycrunch.datasets.exclusion(dataset, expr)
        df = pandaslib.dataframe(dataset)
        valid_ids = [
            row[0] for row in ROWS
            if row[0] != 'identity' and (32766 in row[5:9] or 32767 in row[5:9])
        ]
        assert len(df) == len(valid_ids)
        for _, row in df.iterrows():
            assert row['identity'] in valid_ids
            assert {'?': 32766} in row['hobbies'] or \
                   {'?': 32767} in row['hobbies']

        expr = 'not valid(hobbies)'
        pycrunch.datasets.exclusion(dataset, expr)
        df = pandaslib.dataframe(dataset)
        valid_ids = [
            row[0] for row in ROWS
            if row[0] != 'identity'
            and (32766 not in row[5:9] and 32767 not in row[5:9])
        ]
        assert len(df) == len(valid_ids)
        for _, row in df.iterrows():
            assert row['identity'] in valid_ids
            assert {'?': 32766} not in row['hobbies'] and \
                   {'?': 32767} not in row['hobbies']

        # 1.7 Clear the exclusion filter.
        pycrunch.datasets.exclusion(dataset)
        df = pandaslib.dataframe(dataset)
        assert len(df) == len(ROWS) - 1  # excluding the header

        # 2. Integration Tests for "Transformations".

        categories = [
            {'id': 1, 'name': 'Nerds', 'numeric_value': 1, 'missing': False},
            {'id': 2, 'name': 'Normal Users', 'numeric_value': 2, 'missing': False},
            {'id': 3, 'name': 'Hipsters', 'numeric_value': 3, 'missing': False},
            {'id': 32767, 'name': 'Unknown', 'numeric_value': None, 'missing': True}
        ]

        rules = [
            'operating_system in ("Linux", "Solaris", "Minix", "FreeBSD", "NetBSD")',
            'operating_system == "Windows"',
            'operating_system == "MacOS"',
            'missing(operating_system)'
        ]

        new_var = create_categorical(
            ds=dataset,
            categories=categories,
            rules=rules,
            name='Operating System Users',
            alias='operating_system_users',
            description='Type of Operating System Users'
        )
        assert isinstance(new_var, pycrunch.shoji.Entity)
        new_var.refresh()
        assert new_var.body.type == 'categorical'

        # Check the data on the new variable.
        df = pandaslib.dataframe(dataset)
        assert 'operating_system_users' in df

        # Check the nerds.
        assert set(
            r['operating_system']
            for _, r in df[df['operating_system_users'] == 'Nerds'].iterrows()
        ) == {'Linux', 'Solaris', 'Minix', 'FreeBSD', 'NetBSD'}

        # Check the hipsters.
        assert set(
            r['operating_system']
            for _, r in df[df['operating_system_users'] == 'Hipsters'].iterrows()
        ) == {'MacOS'}

        # Check normal users.
        assert set(
            r['operating_system']
            for _, r in df[df['operating_system_users'] == 'Normal Users'].iterrows()
        ) == {'Windows'}

        # 3. Integration Tests for "Recodes".

        # 3.1 combine_categories.

        # On a 'categorical' variable.
        cat_map = {
            1: {
                'name': 'Bilingual',
                'missing': False,
                'combined_ids': [2, 3]
            },
            2: {
                'name': 'Not Bilingual',
                'missing': False,
                'combined_ids': [1, 4]
            },
            99: {
                'name': 'Unknown',
                'missing': True,
                'combined_ids': [32766, 32767]
            }
        }
        new_var = combine_categories(
            dataset, 'speak_spanish', cat_map, 'Bilingual Person', 'bilingual'
        )
        assert isinstance(new_var, pycrunch.shoji.Entity)
        new_var.refresh()
        assert new_var.body.type == 'categorical'

        df = pandaslib.dataframe(dataset)
        assert 'bilingual' in df

        # Check the data in the recoded variable.
        bilingual_ids = set(
            row[0] for row in ROWS
            if row[0] != 'identity' and row[4] in (2, 3)
        )
        assert set(
            int(r['identity'])
            for _, r in df[df['bilingual'] == 'Bilingual'].iterrows()
        ) == bilingual_ids

        non_bilingual_ids = set(
            row[0] for row in ROWS
            if row[0] != 'identity' and row[4] in (1, 4)
        )
        assert set(
            int(r['identity'])
            for _, r in df[df['bilingual'] == 'Not Bilingual'].iterrows()
        ) == non_bilingual_ids

        bilingual_null_ids = set(
            row[0] for row in ROWS
            if row[0] != 'identity' and row[4] in (32766, 32767)
        )
        assert set(
            int(r['identity'])
            for _, r in df[df['bilingual'].isnull()].iterrows()
        ) == bilingual_null_ids

        # On a 'categorical_array' variable.
        cat_map = {
            1: {
                'name': 'Interested',
                'missing': False,
                'combined_ids': [1, 2]
            },
            2: {
                'name': 'Not interested',
                'missing': False,
                'combined_ids': [3, 4]
            },
            99: {
                'name': 'Unknown',
                'missing': True,
                'combined_ids': [32766, 32767]
            }
        }
        new_var = combine_categories(
            dataset, 'hobbies', cat_map, 'Hobbies (recoded)', 'hobbies_recoded'
        )
        assert isinstance(new_var, pycrunch.shoji.Entity)
        new_var.refresh()
        assert new_var.body.type == 'categorical_array'

        df = pandaslib.dataframe(dataset)
        assert 'hobbies_recoded' in df

        # Check the data in the recoded variable.
        for _, row in df.iterrows():
            hobbies = row['hobbies']
            hobbies_rec = row['hobbies_recoded']
            assert len(hobbies) == len(hobbies_rec)

            for i, value in enumerate(hobbies):
                if value in ({'?': 32766}, {'?': 32767}):
                    assert hobbies_rec[i] == {'?': 99}
                elif value in (1, 2):
                    assert hobbies_rec[i] == 1
                elif value in (3, 4):
                    assert hobbies_rec[i] == 2

        # 3.2 combine_responses.

        response_map = {
            'music_recoded_1': ['music_1', 'music_2'],
            'music_recoded_2': ['music_97'],
            'music_recoded_3': ['music_98', 'music_99']
        }
        new_var = combine_responses(
            dataset, 'music', response_map, 'Music (alt)', 'music_recoded'
        )
        assert isinstance(new_var, pycrunch.shoji.Entity)
        new_var.refresh()
        assert new_var.body.type == 'multiple_response'

        df = pandaslib.dataframe(dataset)
        assert 'music_recoded' in df

        # TODO: Test the data in the recoded variable. Unsure of its meaning.

    finally:
        dataset.delete()


if __name__ == '__main__':
    main()
    exit(0)
