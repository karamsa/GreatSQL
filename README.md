# GreatSQL
[![Build Status](https://travis-ci.org/karamsa/GreatSQL.svg?branch=master)](https://travis-ci.org/karamsa/GreatSQL)


A new large-scale, cross-domain and balanced dataset for Natural Language to SQL translation task. GreatSQL is part of our work [SQLSketch: Generating SQL Queries using a sketch-based approach](https://ip.ios.semcs.net/articles/journal-of-intelligent-and-fuzzy-systems/ifs210359).
<br />
| \# pairs | Cross-domain  | \# DBs | \# Domains | \# Tables/DB |
| :---: | :---: |  :---: | :---: |  :---:        |
| 45969 | Yes | 224 | 195 | 5.6 |

## Notes

- Tokenization and annotation are made manually. <br /> 
- The dataset includes all kind of types, except blob or files <br /> 
- Not all queries return results as in the perfect situation  in the task of NL2SQL the model should return the correct SQL query even if there is no rows in database tables.


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

| Model | Test exact matching accuracy |
| :---: | :---:         |
| SQLSketch-TVC<br />(Ahkouk 2021) | ![#43c641](https://via.placeholder.com/15/43c641/000000?text=+) `34.2` |
| [SQLSketch<br />(Ahkouk 2021)](https://ip.ios.semcs.net/articles/journal-of-intelligent-and-fuzzy-systems/ifs210359) | 23.98 |
| [Modified SQLova <br />(Hwang et all 2021)](https://github.com/naver/sqlova) | 16.3 |
| [Modified SQLNet<br />(Xu 2017)](https://arxiv.org/abs/1711.04436) | 10.9 |
| [Modified Seq2SQL<br />(Zhong 2017)](https://arxiv.org/abs/1709.00103) | 1.9 |



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

We provide the code for the evaluation as a standalone script file in `evaluation/evaluation.py`. We integrated 3 metrics for the evaluation the Exact Match (EM) and the String Exact Match (SEM) and also we provide partial accuracies for evaluating the performance of the model. Note that the EM metric is based on components matching and ignores the order of conditions. For more information on how EM is calculated please see in `evaluation/evaluation.py`.

The evaluation script requires 3 parameters:  

```code
usage: evaluation.py [-h]
                     dataset_file_path predicted_sqls_file_path predicted_components_file_path

positional arguments:
  dataset_file_path     source file for the prediction(train, dev or test set
                        file)
  predicted_sqls_file_path
                        SQL predictions by the model. One SQL query per line
  predicted_components_file_path
                        component predictions by the model. Has the same
                        structure of the ground truth of the dataset files
```
Example of the predicted sqls file, that should include one sql query per line and the predicted json components file that contains the json annotations of sql queries, are included in the `/evaluation` folder.<br/>

When runnunig the code, the result should be something like this:

```code
=======================Evaluation start=======================
100%|████████████████████████████████████████████████████████████████████████████████| 31897/31897 [00:03<00:00, 8151.64it/s]
=======================Evaluation end=======================

=======================Global Accuracy=======================
{
  "em_accuracy": 23.9899686454442562,
  "sem_accuracy": 15.5678778978978909 //this metric is not included in the paper (String Exact Match of SQLs)
}
=======================Partial Accuracy=======================
{
  "cm_accuracy": {
    "select_accuracy": 80.9999686490892561,
    "tables_accuracy": 63.4969636470345417,
    "where_accuracy": 55.6234535675675862,
    "group_by_accuracy": 26.5453646786786789,
    "having_accuracy": 23.9999686454442562,
    "order_by_accuracy": 33.7799372981785121,
    "limit_accuracy": 60.9999372981785127
  }
}

```




### Acknowledgement

We thank all the anonymous annotators for their help and work in creating the GreatSQL dataset. We also thank all people near or far who provided feedback and participated in the promising discussions. 

## FAQ

