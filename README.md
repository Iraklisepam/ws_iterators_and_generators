# Python Iterators and Generators

```text
python-iterators-generators-workshop/
├── README.md
├── exercises/
│   ├── pipeline.py
├── tests/
│   └── test_pipeline.py
├── data/
│   └── orders.csv
└── main.py
```

## Setup

Python 3.10+ is recommended.

Install pytest:

```bash
python -m pip install pytest
```

Run the tests:

```bash
pytest -q
```

## Hands-on exercise

Complete the TODO sections in the pipeline.py file:

- implement `OrderIterator`. Iterates to all rows of the file iterator.  
- make `Orders` reusable
- Implement functions: paid_sales, above_threshold
- Fix the generator in report_all_sales function
