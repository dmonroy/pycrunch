Dataset Manipulation
====================

This document describes and gives examples of how
to manipulate the data on datasets.


## Drop Rules

#### Exclusion Filters

Drop rules are used to delete invalid cases -- respondents who spent too little 
time answering the survey ("speeders"), cases with inconsistent data, etc. 
In Crunch, these are supported using *exclusion filters*, which are specified using a logical expression.

For example, suppose `Omnibus` is the name of a crunch dataset and `disposition` 
is the alias of a variable, start by loading the dataset:

```python
my_dataset = site.datasets.by('name').get('Omnibus').entity
```

Now apply the exclusion filter:

```python
my_dataset.exclude("disposition != 0")
```

(Here, zero is the id (or code) assigned to completed interviews.)

We can also exclude a list of ids using:

```python
my_dataset.exclude("disposition in [0, 1]")
```

#### Filter expressions

At the moment *filter expressions* can be composed using the following logical expressions:

| operator | meaning               |
|:--------:|-----------------------|
| ==       | equal                 |
| !=       | unequal               |
| >        | greater than          |
| >=       | greater or equal      |
| <        | less than             |
| <=       | less or equal         |
| and      | logical *and*         |
| or       | logical *or*          |
| in       | in *list/tuple*       |
| not in   | not in *list/tuple*   |
| has_any  | has_any(*list/tuple*) |
| has_all  | has_all(*list/tuple*) |

`Note:` The expression needs to contain the **alias** and the **value**.

## Derived variables

## Recodes

#### Combine categories

A common operation is to create a new variable out of an existing variable by combining categories. 
For example, if brandrating is a variable with categories:
`Very favorable`, `Somewhat favorable`, `Neutral`, `Somewhat unfavorable`, `Very unfavorable`, `Don't know`. 
With codes 1,2,3,4,5,9 respectively), we may want to create a new variable brandrating2 using the following:

```python
category_recode = {
    1: {
        'name': 'Favorable',
        'missing': False,
        'combined_ids': [1, 2]
    },
    2: {
        'name': 'Neutral',
        'missing': False,
        'combined_ids': [3]
    },
    3: {
        'name': 'Unfavorable',
        'missing': False,
        'combined_ids': [4, 5]
    }
}

new_var = my_dataset.combine_categories(
    variable='brandrating', 
    category_map=category_recode, 
    name='Brandrating 2', 
    alias='brandrating2', 
    description='Recoding brandrating')
```

#### Combine responses

For a variable with subvariables (like multiple choice questions) you may want to create a 
new variable with combined subvariables.

```python
response_mappings = {
    'new_subvar_alias1': ['from_subvar_alias1', 'from_subvar_alias2'],
    'new_subvar_alias2': ['from_subvar_alias3', 'from_subvar_alias4']
}

new_var = my_dataset.combine_responses(
    variable='original_variable_alias', 
    response_map=response_mappings,
    name='Brandrating 3', 
    alias='brandrating3', 
    description='Combining responses for brandrating')
```

## Transformations

#### Creating a categorical variable

Transformations create new variables based upon the values of one or more input variables. 

```python
categories = [
    {"id": 1, "name": "Hipsters", "numeric_value": None, "missing": False},
    {"id": 2, "name": "Techies", "numeric_value": None, "missing": False},
    {"id": 3, "name": "Others", "numeric_value": None, "missing": False}
]

rules = ['var1 == 1 and var2 == 1', 'var1 == 2 and var2 == 2']

new_var = my_dataset.create_categorical(
    categories=categories,
    rules=rules,
    name='New variable',
    alias='alias', 
    description='description')
```

*Rules* are evaluated in order (as if this were a sequence of if/elif/else statements. The values for the rule expressions must be valid values on the source variables.
