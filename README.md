# GreatSQL


a new large-scale, cross-domain and balanced dataset for Natural Language to SQL translation task [SQLSketch: Generating SQL Queries using a sketch-based approach](under peer-review).


## Citation

If you use GreatSQL, please cite the following work:

> Karam Ahkouk, Mustapha Machkour, Khadija Majhadi, Rachid Mama. 2021. SQLSketch: Generating SQL Queries using a sketch-based approach.

```
@article{zhongSeq2SQL2017,
  author    = {Karam Ahkouk and Mustapha Machkour and Khadija Majhadi and Rachid Mama},
  title     = {SQLSketch: Generating SQL Queries using a sketch-based approach},
  journal   = {-},
  volume    = {-},
  year      = {2021}
}
```

## Notes

Tokenization and annotation are made manually. Please note that this is a limited version of GreatSQL(the paper is under-review). The full version will be available once the paper is approved

## Leaderboard

If you submit papers on GreatSQL, please consider sending a pull request to merge your results onto the leaderboard. By submitting, you acknowledge that your results are obtained purely by training on the training split and tuned on the dev split (e.g. you only evaluted on the test set once).

### Weakly supervised without logical forms

| Model | Test execution accuracy |
| :---: | :---:         |
| [Modified SQLNet (Xu et al, 2017)] | 10.9 |
| [Modified Seq2SQL (Zhong et al 2017)] | 1.9 |



## Content and format

Inside the data folder you will find the files in `json` format.


### Sample

These files are contained in the `*.json` files. A line looks like the following:

```json
{
    "question": "list the clubs that have less than 7 athletes",
    "query_id": 45291,
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


