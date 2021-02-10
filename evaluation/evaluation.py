#!/usr/bin/env python
import json
from argparse import ArgumentParser
from tqdm import tqdm
from collections import OrderedDict 


def load_normal_file(path):
    array = []

    with open(path, 'r', encoding='utf-8') as fp:
        for cnt, line in enumerate(fp):
            array.append(line.strip())
    
    return array


def load_json_file(path):
    data = []

    with open(path, 'r', encoding='utf-8') as row:
        data = json.load(row)
    
    return data


def eval_query_components(ground_truth, predicted_json):
    # Make single components matching 
    select_cl = eval_single_component(ground_truth["select_columns"], predicted_json["select_columns"])

    tables_cl = eval_single_component(ground_truth["from_tables"], predicted_json["from_tables"])
    
    where_cl = eval_single_component(ground_truth["where"], predicted_json["where"])

    group_by_cl = eval_single_component(ground_truth["group_by"], predicted_json["group_by"])

    having_cl = eval_single_component(ground_truth["having"], predicted_json["having"])

    order_by_cl = eval_single_component(ground_truth["order_by"], predicted_json["order_by"])

    limit_cl = eval_single_component(ground_truth["limit"], predicted_json["limit"])

    return select_cl, tables_cl, where_cl, group_by_cl, having_cl, order_by_cl, limit_cl


def eval_single_component(source_item, predicted_item):
    source_item = json.dumps(source_item, sort_keys=True)
    predicted_item = json.dumps(predicted_item, sort_keys=True)

    source_item = json.loads(source_item.lower())
    predicted_item = json.loads(predicted_item.lower())

    return check_predictions(source_item, predicted_item)

def avg_accuracies(*accuracies):
    return sum(accuracies)/len(accuracies)


def check_predictions(source_item, predicted_item):
    try:          
        if len(predicted_item) != len(source_item):
            return 0

        seen_predicted_items = []

        for i, row in enumerate(predicted_item):

            if row in seen_predicted_items:
                return 0

            # print(str(row))

            if "value\':" in str(row) and len(str(row["value"]))>1 and str(row["value"])[0] == "{" and "select_columns" in row["value"]:  
                select_cl, tables_cl, where_cl, group_by_cl, having_cl, order_by_cl, limit_cl = eval_query_components(source_item[i]["value"], row["value"])

                avg = avg_accuracies(select_cl, tables_cl, where_cl, group_by_cl, having_cl, order_by_cl, limit_cl)
                
                if avg != 1.0:
                    return 0

            elif row not in source_item:
                return 0

            seen_predicted_items.append(row)

    except Exception as e:
        print(source_item)
        print(predicted_item)
        return 0
    
    return 1
    

def check(json_object):

    res = OrderedDict()
    for k, v in sorted(json_object.items()):
        if isinstance(v, dict):
            res[k] = sort_json_recursively(v)
        else:
            res[k] = v
    return res


if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument('dataset_file_path', help='source file for the prediction(train, dev or test set file)')
    
    parser.add_argument('predicted_sqls_file_path', help='SQL predictions by the model. One SQL query per line')
    
    parser.add_argument('predicted_components_file_path', help='component predictions by the model. Has the same structure of the ground truth of the dataset files')

    args = parser.parse_args()

    all_select_cl = []
    all_tables_cl = []
    all_where_cl = []
    all_group_by_cl = []
    all_having_cl = []
    all_order_by_cl = []
    all_limit_cl = []


    all_exact_match = []
    all_string_exact_match = []


    print("=======================Files load start=======================")
    source_file = load_json_file(args.dataset_file_path) # train, dev or test set file
    predicted_sqls = load_normal_file(args.predicted_sqls_file_path) # the predicted SQLs file, contains one SQL query per line
    predicted_components = load_json_file(args.predicted_components_file_path) # the predicted components file (json format)

    print("=======================Files load end=======================")
    print("    ")
    print("    ")
    print("=======================Evaluation start=======================")

    total_samples = len(source_file)
    total_sql_queries = len(predicted_sqls)
    total_json_components_queries = len(predicted_components)

    #Check the length of each file and make sure they have all the same length
    if (total_samples == total_sql_queries == total_json_components_queries):
        
        # loop over files 
        # get each sample from the source file, the predicted String SQL query and the predicted json components  
        for sample, predicted_sql, predicted_json in tqdm(zip(source_file, predicted_sqls, predicted_components), total = total_samples):
            
            #Get the SQL label from the source file
            source_sql = sample["sql"].lower().strip()
            predicted_sql = predicted_sql.lower().strip()
            # Get the ground truth from the source file
            ground_truth = sample["ground_truth"]


            #Remove the schema_index if it exists# we don't need it in the evaluation
            if "schema_index" in ground_truth: 
                del ground_truth["schema_index"]

            if "schema_index" in predicted_json: 
                del predicted_json["schema_index"]


            # Make components matching 
            select_cl, tables_cl, where_cl, group_by_cl, having_cl, order_by_cl, limit_cl = eval_query_components(ground_truth, predicted_json)



            # components_match 
            all_select_cl.append(select_cl)
            all_tables_cl.append(tables_cl)
            all_where_cl.append(where_cl)
            all_group_by_cl.append(group_by_cl)
            all_having_cl.append(having_cl)
            all_order_by_cl.append(order_by_cl)
            all_limit_cl.append(limit_cl)


            # ground_truth_d = json.loads(json.dumps(ground_truth, sort_keys=True))
            # predicted_json_d = json.loads(json.dumps(predicted_json, sort_keys=True))
            # exact_match = ground_truth_d == predicted_json_d

            # Make exact matching
            avg = avg_accuracies(select_cl, tables_cl, where_cl, group_by_cl, having_cl, order_by_cl, limit_cl)

            exact_match = 1
            if avg != 1.0:
                exact_match = 0


            # Make String Exact matching 
            string_exact_match = source_sql == predicted_sql


            all_exact_match.append(exact_match)
            all_string_exact_match.append(string_exact_match)


        print("=======================Evaluation end=======================")
        print("    ")
        print("    ")
        
        print("=======================Global Accuracy=======================")
        print(json.dumps({
            'em_accuracy': sum(all_exact_match) / len(all_exact_match),
            'sem_accuracy': sum(all_string_exact_match) / len(all_string_exact_match),
            }, indent=2))

        print("=======================Partial Accuracy=======================")
        print(json.dumps({
            'cm_accuracy': {
                'select_accuracy': sum(all_select_cl) / len(all_select_cl),
                'tables_accuracy': sum(all_tables_cl) / len(all_tables_cl),
                'where_accuracy': sum(all_where_cl) / len(all_where_cl),
                'group_by_accuracy': sum(all_group_by_cl) / len(all_group_by_cl),
                'having_accuracy': sum(all_having_cl) / len(all_having_cl),
                'order_by_accuracy': sum(all_order_by_cl) / len(all_order_by_cl),
                'limit_accuracy': sum(all_limit_cl) / len(all_limit_cl)
                }
            }, indent=2))

    else:
        print("The files have not the same number of queries. Please check that predicted queries are included in the SQLs and components files")
        exit()