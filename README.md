pycrunch
========

A Python client library for Crunch.io.


Using pycrunch
--------------

To use pycrunch in your project, run:


    $ python setup.py develop

This will make the code in this directory available to other projects.

Getting started
---------------

Start a simple site session via:

```python
import pycrunch
site = pycrunch.connect("me@mycompany.com", "yourpassword", "https://beta.crunch.io/api/")
```
Or, if you have a crunch access token:

```python
import pycrunch
site = pycrunch.connect_with_token("DFIJFIJWIEJIJFKSJLKKDJKFJSLLSLSL", "https://beta.crunch.io/api/")
```

Then, you can browse the site. Use `print` to pretty-indent JSON payloads:

```python
>>> print site
>>> pycrunch.shoji.Catalog(**{
>>>     "element": "shoji:catalog",
>>>     "self": "https://beta.crunch.io/api/",
>>>     "description": "The API root.",
>>>     "catalogs": {
>>>         "datasets": "https://beta.crunch.io/api/datasets/",
>>>         "specifications": "https://beta.crunch.io/api/specifications/",
>>>         ...
>>>     },
>>>     "urls": {
>>>         "logout_url": "https://beta.crunch.io/api/logout/",
>>>         ...
>>>     },
>>>     "views": {
>>>         "migration": "https://beta.crunch.io/api/migration/"
>>>     }
>>> })
```

URI's in payloads' catalogs, views, fragments, and urls collections
are followable automatically:

```python
>>> print site.datasets
>>> pycrunch.shoji.Catalog(**{
>>>     "self": "https://beta.crunch.io/api/datasets/",
>>>     "element": "shoji:catalog",
>>>     "index": {
>>>         "https://beta.crunch.io/api/datasets/dbf9fca7b727/": {
>>>             "owner_display_name": "me@mycompany.com",
>>>             "description": "",
>>>             "id": "dbf9fca7b727",
>>>             "owner_id": "https://beta.crunch.io/api/users/253b68/",
>>>             "archived": false,
>>>             "name": "Hog futures tracking (May 2014)"
>>>         },
>>>     },
>>>     ...
>>> })
```

Each recognized JSON payload also automatically gives dotted-attribute
access to the members of each JSON object:

```python
>>> print site.datasets.index.values()[0]
>>> pycrunch.shoji.Tuple(**{
>>>     "owner_display_name": "me@mycompany.com",
>>>     "description": "",
>>>     "id": "dbf9fca7b727",
>>>     "owner_id": "https://beta.crunch.io/api/users/253b68/",
>>>     "archived": false,
>>>     "name": "Hog futures tracking (May 2014)"
>>> })
```

Responses may also possess additional helpers, like the `entity` property of
each Tuple in a catalog's index, which follows the link to the Entity resource:

```python
>>> print site.datasets.index.values()[0].entity_url
>>> "https://beta.crunch.io/api/datasets/dbf9fca7b727/"

>>> print site.datasets.index.values()[0].entity
>>> pycrunch.shoji.Entity(**{
>>> "self": "https://beta.crunch.io/api/datasets/dbf9fca7b727/",
>>> "element": "shoji:entity",
>>> "description": "Detail for a given dataset",
>>> "specification": "https://beta.crunch.io/api/specifications/datasets/",
>>>     "body": {
>>>         "archived": false,
>>>         "user_id": "253b68",
>>>         "name": "Hog futures tracking (May 2014)"
>>>         "weight": "https://beta.crunch.io/api/datasets/dbf9fca7b727/variables/36f5404/",
>>>         "creation_time": "2014-03-06T18:23:26.780752+00:00",
>>>         "description": ""
>>>     },
>>>     "catalogs": {
>>>         "batches": "https://beta.crunch.io/api/datasets/dbf9fca7b727/batches/",
>>>         "joins": "https://beta.crunch.io/api/datasets/dbf9fca7b727/joins/",
>>>         "variables": "https://beta.crunch.io/api/datasets/dbf9fca7b727/variables/",
>>>         "filters": "https://beta.crunch.io/api/datasets/dbf9fca7b727/filters/",
>>>         ...
>>>     },
>>>     "views": {
>>>         "cube": "https://beta.crunch.io/api/datasets/dbf9fca7b727/cube/",
>>>         ...
>>>     },
>>>     "urls": {
>>>         "revision_url": "https://beta.crunch.io/api/datasets/dbf9fca7b727/revision/",
>>>         ...
>>>     },
>>>     "fragments": {
>>>         "table": "https://beta.crunch.io/api/datasets/dbf9fca7b727/table/"
    }
>>> })
```

If you want to print all the table output you can do that with:

```python
>>> print ds.table.data
>>> pycrunch.elements.JSONObject(**{
>>>     "e7f361628": [
>>>         1,
>>>         2,
>>>         {"?": -1},
>>>         2
>>>     ]
>>> })
```

`Note` that the output can get *very* large and is limited by default to the first 100 rows. 

To access a Pandas Dataframe of the data in your dataset:

```python
>>> from pycrunch import pandaslib as crunchpandas
>>> df = crunchpandas.dataframe_from_dataset(site,'baadf00d000339d9faadg00beab11e')
>>> print(df)
< Draws a dataframe table >
```

Usage Examples
-----------

#### Creating a dataset

You need to provide a dictionary containing the basic body of the dataset.

```python
ds_body = {
    'body': {
        'name': 'My first dataset'
        }
    }

ds = site.datasets.create(ds_body)
```

#### Loading an existing dataset

Here's how you can load an existing dataset.

```python
ds = site.datasets.by('name').get('My Name').entity
```

#### Creating a variable

In this example we create a categorical variable. As for the dataset you have to provide a dictionary with it's body.

```python
var_body = {
    'body': {
        'name': 'Gender',
        'alias': 'gender',
        'type': 'categorical',
        'categories': [
            {'id': 1, 'name': 'M', 'numeric_value': None, 'missing': False},
            {'id': 2, 'name': 'F', 'numeric_value': None, 'missing': False},
            {'id': -1, 'name': 'No Data', 'numeric_value': None, 'missing': True}
        ],
        'values': [1, 2, 2, 2, 2, 1, {'?': -1}]
    }
}

var = ds.variables.create(var_body)
```

#### Loading an existing variable

```python
var = ds.variables.by('alias').get('my_alias').entity
```

#### Change the variable's attributes

You can change any variable's attribute by providing them as keyword arguments in the *edit* method:

```python
var.edit(name="my new name", alias='gender_ng')
```

#### Adding a description

```python
var.edit(description='My awesome description')
```

#### Hiding variables in the UI

`Note` that variables are simply not presented in the UI but accessible in the API!


```python
var.edit(discarded=True)
```

#### Changing categories

Either provide a complete list of new categories like in the *gender* example above or if you want to change for instance only the name of a category you can archieve that with:

```python
var.body.categories[0]['name'] = 'My new category'
var.edit(categories=var.body.categories)
```

## Ordering

#### Rearanging variables

Rearanging variables is as easy as rearaging the order of their respective URL's in the `ds.variables.hier.graph` list

```python
ds.variables.hier.graph = [var2.self, var1.self]
```

#### Grouping variables

You can group variables in *topics* by providing a dictionary in that list. If we wanted to group `var1` and `var2` we can simply:

```python
group = {'My Aweseome Group': [var1.self, var2.self]}
ds.variables.hier.graph = [group]
```

Of cause you can also rearange them as shown above

## Drop Rules

#### Exclusion Filters

Drop rules are used to delete invalid cases -- respondents who spent too little time answering the survey ("speeders"), cases with inconsistent data, etc. In Crunch, these are supported using *exclusion filters*, which are specified using a logical expression.

For example, suppose `Omnibus` is the name of a crunch dataset (assigned to the Python object `ds` ) and `disposition` is the alias of a variable in this dataset:

```python
exclusion(ds, "disposition != 0")
```

(Here, zero is the id (or code) assigned to completed interviews.)

We can also exclude a list of ids using either:

```python
exclusion(ds, "disposition in [0, 1]")
```

#### Filter expressions

At the moment *filter expressions* can be composed using the following logical expressions:

| operator | meaning               |
|:--------:|-----------------------|
| ==       | eqal                  |
| !=       | uneqal                |
| >        | greater than          |
| >=       | greater or eqal       |
| <        | less than             |
| <=       | less or qual          |
| and      | logical *and*         |
| or       | logical *or*          |
| in       | in *list/tuple*       |
| not in   | not in *list/tuple*   |
| has_any  | has_any(*list/tuple*) |
| has_all  | has_all(*list/tuple*) |

`Note` that the expressions needs to contain the **alias** and the **value**.

## Derived variables

## Recodes

#### Combine categories

A common operation is to create a new variable out of an existing variable by combining categories. For example, if brandrating is a variable with categories `Very favorable`, `Somewhat favorable`, `Neutral`, `Somewhat unfavorable`, `Very unfavorable`, `Don't know` (with codes 1,2,3,4,5,9 respectively), we may want to create a new variable brandrating2 using the following:

```python
from pycrunch.recodes import combine_categories
    
cat_map = {
    1: {
        'label': 'Favorable',
        'missing': False,
        'num_value': 1,
        'ids': [1, 2]
    },
    2: {
        'label': 'Neutral',
        'missing': False,
        'num_value': 2,
        'ids': [3]
    },
    3: {
        'label': 'Unfavorable',
        'missing': False,
        'num_value': 2,
        'ids': [4, 5]
    }
}

new_var = combine_categories(ds, 'from_alias', cat_map, 'name', 'alias', 'description')
```

#### Combine responses

For a variable with subvariables - like a multiple choice questions - you may want to create a new variable with combined subvariables. You can do that like:

```python
from pycrunch.recodes import combine_responses

response_map = {
    'new_subvar_alias1': ['from_subvar_alias1', 'from_subvar_alias2'],
    'new_subvar_alias2': ['from_subvar_alias3', 'from_subvar_alias4']
}

new_var = combine_responses(ds, 'from_alias', response_map, 'name', 'alias', 'description')
```

## Tranformations

#### Creating a categorical variable

Transformations create new variables based upon the values of one or more input variables. 

```python
from pycrunch.transformations import create_categorical

categories = [
    {"id": 1, "name": "Hipsters", "numeric_value": None, "missing": False},
    {"id": 2, "name": "Techies", "numeric_value": None, "missing": False},
    {"id": 3, "name": "Others", "numeric_value": None, "missing": False}
]

rules = ['var1 == 1 and var2 == 1', 'var1 == 2 and var2 == 2']

new_var = create_categorical(ds, 'alias', 'name', categories, rules, 'description')
```

The *rules* are evaluated in order (as if this were a sequence of if/elif/else statements. The values for the rule expressions must be valid values on the source variables.