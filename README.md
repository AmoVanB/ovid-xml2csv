# XML to CSV converter for data exported from Ovid

Converts the XML format exported from the [Ovid database](https://ovidsp.ovid.com/) to CSV.

The scripts reads all the `xml` files in the running directory, parses them, merges them, and outputs the result to a `merged.csv` file.

## Usage

```shell
  python3 xml2csv.py
```
