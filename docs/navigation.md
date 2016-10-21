Navigating the Crunch.io API with pycrunch
==========================================

This document intends to describe how to move around the different
elements and structures that the Crunch.io API exposes.

We are going to use the `site` session object previously described in the
Introduction section. It will be our intermediary between Python and
Crunch.io.


Catalogs
--------

Every collection of elements in Crunch is a Shoji Catalog. We
can quickly interact with the datasets Catalog by doing:

```python
site.datasets
```

Catalogs provide some methods to handle individual elements. Let's
say we want to interact with the Dataset named "US Elections 2016", we
could reference that particular Dataset by doing:

```python
my_dataset = site.datsets.by('name').get("US Elections 2016").entity
```

Now the variable `my_datasets` holds a reference to the Dataset
we need to interact with. Just like we interacted with the datasets
Catalog, we can interact with the Dataset variables Catalog as well:

```python
my_dataset.variables
```

In order to visualize, for example, the data contents of our dataset 
we can make use of the table entity:

```python
my_dataset.table.data
```

Pycrunch also allows us to interact with data using Pandas. To access the
Pandas Dataframe of our dataset object, we would do the following:

```python
from pycrunch import pandaslib
df = pandaslib.dataframe(my_dataset)
```
