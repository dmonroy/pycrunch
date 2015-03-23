from __future__ import unicode_literals

import io
import csv
import six


def rows_as_csv_file(rows):
    """Return rows (iterable of lists of cells) as an open CSV file.

    Any cells in the given
    rows which contain None will be emitted as an empty cell in the CSV
    (nothing between the commas), which Crunch interprets as {"?": -1},
    the "No Data" system missing value.
    """
    # Write to a StringIO because it joins lines as we go
    # and a .read() of it (like requests.post will do) does not make a copy.
    out = io.StringIO() if six.PY3 else io.BytesIO()

    sentinel = "__CSV_SENTINEL_NONE__"

    class EphemeralWriter():
        def write(self, line):
            line = line.replace(str('"' + sentinel + '"'), str(""))
            out.write(line)
    pipe = EphemeralWriter()

    writer = csv.writer(pipe, quoting=csv.QUOTE_NONNUMERIC, lineterminator='\n')
    for row in rows:
        row = [sentinel if cell is None else cell for cell in row]
        row = [
            cell.encode('utf-8')
                if six.PY2 and isinstance(cell, six.text_type)
                else cell
            for cell in row
        ]
        writer.writerow(row)

    out.seek(0)

    if six.PY3:
        out = io.BytesIO(out.getvalue().encode('utf-8'))

    return out
