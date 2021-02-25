# ADCenter Network Code challenge - Gene Sequencing

Python3 mRNA sequence processing

# Software requirements

- If you don't already, install [Python3.6+](https://www.python.org/downloads/) on your device.

# Run locally

- Plain mode (Challenge 1)

Run:

```sh
python3 main.py
```

which prints in /dev/stdout a `Array<Array<Gene>>` or `ErrorMessage`.

- Streams mode (Challenge 2)

The lazy evaluation or streaming functionality of this mode has been natively implemented in Python by using generator functions.

Run exactly as above but with `-s` flag:

```sh
python3 main.py -s
```

which prints in /dev/stdout a `Array<Gene>` and `ErrorMessage` if applicable.

In both modes, you will be asked to input your local file text path. For testing purposes, try out with `data.txt`.

# Run tests

Install pytest with pip3:

```sh
pip3 install pytest
```

And then simply run:

```sh
pytest
```
