import json

"""
TODO:
    - resolve variable_name to crunch_url
"""


skeleton = {
    "name": "name",
    "description": "description",
    "alias": "alias",
    "expr": {
        "function": "combine_categories",
        "args": [
            {
                "variable": "https://beta.crunch.io/api/datasets/3ad42c/variables/0000f5/"
            },
            {
                "value": []
            }
        ]
    }
}


sample = {
    "name": "Recode",
    "description": "This is a recoded variable",
    "alias": "recode",
    "expr": {
        "function": "combine_categories",
        "args": [
            {
                "variable": "https://alpha.crunch.io/api/datasets/71f9ff66a4ad4e9385bbc4172f681d5f/variables/000003/"
            },
            {
                "value": [
                    {
                        "name": "China",
                        "combined_ids": [2, 3]
                    },
                    {
                        "name": "Other",
                        "combined_ids": [1]
                    },
                    {
                        "name": "Missing",
                        "missing": True,
                        "combined_ids": [-1]
                    },
                ]
            }
        ]
    }
}


def combine_categories(ds, from_name, category_map, name, alias='', description=''):
    """
    category_map = {
        1: {
            "label": "Favorable",
            "missing": True,    # optional
            "num_value": 1,     # optional
            "ids": [1,2]
        },
    }
    Create a new variable in the given dataset that is a recode
    of an existing variable
    :param ds:
    :param from_name:
    :param name:
    :param alias:
    :param description:
    :return:
    """
    payload = {}
    return ds.session.patch(
        ds.fragments.exclusion,
        data=json.dumps(dict(expression=expr))
    )

# ===    T E S T S
from pycrunch import connect, connect_with_token


def crunch_session():
    site = connect('gryphon-streaming@yougov.com', '71N8bDIoLwkqvvy7', 'https://alpha.crunch.io/api/')
    return connect_with_token(site.session.cookies['token'], 'https://alpha.crunch.io/api/')


if __name__ == '__main__':
    session = crunch_session()
    # get Gryphon EMEA ES_HK_OM_mooncake_Campaign_Ctrl dataset
    ds = session.projects.by('id')['614a7b2ebe9a4292bba54edce83563ae'].entity.datasets.by('id')['71f9ff66a4ad4e9385bbc4172f681d5f']
    print(ds)
