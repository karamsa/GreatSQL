# GreatSQL
[![Build Status](https://travis-ci.org/karamsa/GreatSQL.svg?branch=master)](https://travis-ci.org/karamsa/GreatSQL)

### !Important! ------
(3 years ago when this corpus was created, the goal was to provide a corpus for training new models. Now this repository is no longer supported. but you can still fork the project or use/modify the data in it or even combine the data in this project with other corpuses without prior authorization)
### ------------------

A new large-scale, cross-domain and balanced dataset for Natural Language to SQL translation task. GreatSQL is part of our work [SQLSketch: Generating SQL Queries using a sketch-based approach](https://ip.ios.semcs.net/articles/journal-of-intelligent-and-fuzzy-systems/ifs210359).
<br />
| \# pairs | Cross-domain  | \# DBs | \# Domains | \# Tables/DB |
| :---: | :---: |  :---: | :---: |  :---:        |
| 45969 | Yes | 224 | 195 | 5.6 |

## Notes

- Tokenization and annotation are made manually. <br /> 
- The dataset includes the majority of types, except blob or files <br /> 
- Not all queries return results as in the perfect situation in the task of NL2SQL the model should return the correct SQL query even if there is no rows in database tables.
- Not dedicated for models that use Query execution.
- Exact Match (EM) is the main metric used for evaluating models on this corpus.
- For baseline models, we ignore parts of queries that are not compatible with our dataset like sub-queries, joins, etc...


## Citation

If you use GreatSQL, please cite the following work:

> Karam Ahkouk, Mustapha Machkour, Khadija Majhadi, Rachid Mama. 2021. SQLSketch: Generating SQL Queries using a sketch-based approach.

```
@article{ahkoukSQLSketch2021,
  author    = {Karam Ahkouk and Mustapha Machkour and Khadija Majhadi and Rachid Mama},
  title     = {SQLSketch: Generating SQL Queries using a sketch-based approach},
  journal   = {Journal of Intelligent & Fuzzy Systems},
  volume    = {40},
  year      = {2021}
}
```

## Leaderboard

If you submit papers on GreatSQL, please make a pull request to merge your results onto the leaderboard. By submitting, you acknowledge that your results are obtained purely by training on the train split and tuned on the dev split (e.g. you only evaluted on the test set once).

### supervised learning (Result of the test set only)

| Model | Test exact match accuracy |
| :---: | :---:         |
| SQLSketch-TVC<br />(Ahkouk 2021) | ![#43c641](https://via.placeholder.com/15/43c641/000000?text=+) `34.2` |
| [SQLSketch<br />(Ahkouk 2021)](https://ip.ios.semcs.net/articles/journal-of-intelligent-and-fuzzy-systems/ifs210359) | 23.98 |
| [Modified SQLNet<br />(Xu 2017)](https://arxiv.org/abs/1711.04436) | 10.9 |
| [Modified Seq2SQL<br />(Zhong 2017)](https://arxiv.org/abs/1709.00103) | 1.9 |

- For baseline models, we ignore parts of queries that are not compatible with our dataset like sub-queries, joins, etc...


## Content and format

Inside the `data` folder you will find the files in `json` format.


### Sample

The pairs are included in `*.json` files. A line looks like the following:

```json
{
    "question": "list the clubs that have less than 7 athletes",
    "query_id": 2,
    "sql": "SELECT clubs.id, COUNT(athletes.*) FROM athletes JOIN clubs ON athletes.club_id = clubs.id GROUP BY clubs.id HAVING COUNT(athletes.*) < 7",
    "ground_truth": {
      "schema_index": 93,
      "select_columns": [
        {
          "table_name": "clubs",
          "table_ind": 0,
          "column_name": "id",
          "column_ind": 0,
          "aggregation_ind": 0,
          "column_distinct": "false"
        },
        {
          "table_name": "athletes",
          "table_ind": 1,
          "column_name": "*",
          "column_ind": -1,
          "aggregation_ind": 0,
          "column_distinct": "false"
        }
      ],
      "from_tables": [
        [
          "clubs",
          ""
        ],
        [
          "athletes",
          ""
        ]
      ],
      "where": [],
      "where_conjunction_ops": [],
      "group_by": [
        {
          "table_name": "clubs",
          "table_ind": 0,
          "column_name": "id",
          "column_ind": 0
        }
      ],
      "having": [
        {
          "aggregation_ind": 1,
          "table_name": "athletes",
          "table_ind": 1,
          "column_name": "*",
          "column_ind": -1,
          "operator_ind": 1,
          "value": "7",
          "column_distinct": "false",
          "value_starts_at": 7,
          "value_ends_at": 7
        }
      ],
      "having_conjunction_ops": [],
      "order_by": [],
      "limit": [],
      "where_conditions_groups": [],
      "joins": [
        {
          "table_name": "athletes",
          "table_ind": 1,
          "column_name": "club_id",
          "column_ind": 5,
          "alias": ""
        },
        {
          "table_name": "clubs",
          "table_ind": 0,
          "column_name": "id",
          "column_ind": 0,
          "alias": ""
        }
      ]
    },
    "question_tokens": [
      "list",
      "the",
      "clubs",
      "that",
      "have",
      "less",
      "than",
      "7",
      "athletes"
    ]
  },
```



### Databases

The `database-names` file contains the full list of all used databases in this dataset. The `schema_index` attribute follows the same order of the schemas in the `database-names` file. 
<br />
For example:<br />
`schema_index`: 0 is academia <br />
`schema_index`: 8 is yelp <br />
`schema_index`: 175 is Stack Overflow <br />

## "from_tables":

```code

[
  "clubs", //table name
  ""  // alias
],

```

### Operators
Operators: 

```json
["=", "<", ">", "<=", ">=", "!=", "BETWEEN", "IN", "LIKE", "NOT IN", "NOT LIKE", "IS NULL", "IS NOT NULL"]
```

For example:<br />
`op 0`: is `=` <br />
`op 6`: is `BETWEEN` <br />

### Aggregation functions
```json
["", "COUNT", "MAX", "MIN", "AVG", "SUM"]
```

### Conjuction functions
```json
["AND", "OR"] 
```

### Order types
```json
["ASC", "DESC"]
```

### Evaluation

We provide the code for the evaluation as a standalone script file in `evaluation/evaluation.py`. We integrated 3 metrics for the evaluation the Exact Match (EM) and the String Exact Match (SEM) (The SEM is not included in our paper) and also we provide partial accuracies for evaluating the performance of the model. Note that the EM metric is based on components matching and ignores the order of conditions. For more information on how EM is calculated please see in `evaluation/evaluation.py`.

The evaluation script requires 3 parameters:  

```code
usage: evaluation.py [-h]
                     dataset_file_path predicted_sqls_file_path predicted_components_file_path

positional arguments:
  dataset_file_path     source file for the prediction(train, dev or test set
                        file)
  predicted_sqls_file_path
                        SQL predictions by the model. One SQL query per line (Please put an empty file if you don't use SEM)
  predicted_components_file_path
                        component predictions by the model. Has the same
                        structure of the ground truth of the dataset files
```
Example of the predicted sqls file, that should include one sql query per line and the predicted json components file that contains the json annotations of sql queries, are included in the `/evaluation` folder.<br/>


### FAQ
- This corpus is created in a question/answer concept. we don't support the use of content of databases(data Rows) in the generation of queries.
- The evaluation script is an example for evaluation only. It contains CM & EM accuracies only. You might need to calculate the CM scores in your code or by modifying the evaluation script to include CM scores in addition to CM accuracies to reflect what is in the paper.
- Only EM accuracy is required to be included in the leaderbord. Please make a pull-request then. 

### Acknowledgement

We thank all the anonymous annotators for their help and work in creating the GreatSQL dataset. We also thank all people near or far who provided feedback and participated in the promising discussions. 



