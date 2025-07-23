# =============================================================================
# @ 2025 Kashif Ali Siddiqui, Pakistan
# Developed by: Kashif Ali Siddiqui 
# Github: https://github.com/ksiddiqui
# LinkedIn: https://www.linkedin.com/in/ksiddiqui
# Email: kashif.ali.siddiqui@gmail.com
# Dated: July, 2025 
# -----------------------------------------------------------------------------
# This source code is the property of Kashif Ali Siddiqui and is confidential.
# Unauthorized copying or distribution of this file, via any medium, is strictly prohibited.
# ============================================================================= 

import os
import sys
import time
from datetime import datetime

# Add current directory to sys.path
sys.path.append(os.path.dirname(__file__))
os.environ['OTEL_SDK_DISABLED'] = 'true'

import json
from pathlib import Path
from typing import List, Dict, Any
import pandas as pd

from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness, context_recall, answer_relevancy

from services.rag import RAGManager 
from services.llm_langchain import LLMManager
from system.setup import do_setup
from system.data import read_text_file_without_comments

my_config, my_logger = do_setup()

base_dir = Path(__file__).parent.parent
ragas_dir = base_dir / "ragas"
measure_data_dir = ragas_dir / "measure_data"
report_dir = ragas_dir / "reports"
ragas_eval_prompt_path = base_dir / "resources/prompts/prompt_ragas_eval.txt"

def load_json_files_from_measure_data(my_dataset: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    measure_data_path = measure_data_dir
    
    if not measure_data_path.exists():
        my_logger.error(f"Directory {measure_data_path} does not exist.")
        return my_dataset
        
    json_files = list(measure_data_path.glob("*.json"))
    my_logger.info(f"JSON files found: {json_files}")
    
    if not json_files:
        my_logger.error(f"No JSON files found in {measure_data_path}")
        return my_dataset
    
    my_logger.info(f"Found {len(json_files)} JSON files:")
    
    loaded_json_data = []

    for json_file in json_files:
        try:
            my_logger.info(f"Loading: {json_file.name}")
            with open(json_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                loaded_json_data.extend(data)
                my_logger.info(f"Successfully loaded file: {json_file.name} with {len(data)} items")
        except json.JSONDecodeError as e:
            my_logger.error(f"Error decoding JSON from {json_file.name}: {e}")
        except Exception as e:
            my_logger.error(f"Error loading {json_file.name}: {e}")
    
    my_dataset.extend(loaded_json_data)
    return my_dataset

def run_ragas_on_dataset(my_dataset: List[Dict[str, Any]]):
    questions = []
    ground_truths = []
    generated_answers = []
    retrieved_contexts = []

    rag_manager = RAGManager()
    llm_manager = LLMManager()
    ragas_eval_prompt = read_text_file_without_comments(
        file_path=ragas_eval_prompt_path, ignore_comments=False)

    count = 1
    for item in my_dataset:
        the_question = item["question"]
        the_answer = item["answer"]

        my_logger.info(f"Processing question #{count}")
        my_logger.info(f"-- Question: {the_question}")
        my_logger.info(f"-- Ground Truth: {the_answer}")

        the_context_raw = rag_manager.query_context_retrieval(the_question)        
        # --- FIX: Ensure the_context is always a list of strings ---
        the_context: List[str] = []
        if isinstance(the_context_raw, list):
            # If it's a list, ensure all elements are strings
            the_context = [str(c) for c in the_context_raw]
        elif the_context_raw is not None:
            # If it's a single item (not a list), wrap it in a list and convert to string
            the_context = [str(the_context_raw)]
        # If the_context_raw is None, the_context remains an empty list, which is fine.
        my_logger.info(f"-- Context: items={len(the_context)}, total_size={sys.getsizeof(the_context)}")

        ragas_eval_prompt_spec = ragas_eval_prompt.replace("{{context}}", str(the_context))
        ragas_eval_prompt_spec = ragas_eval_prompt_spec.replace("{{query}}", the_question)
        # take a 5 sec break just to be safe ... to remain in the LLM invoke API  calling limit
        # time.sleep(10)
        the_generated_answer = llm_manager.invoke(ragas_eval_prompt_spec)
        my_logger.info(f"-- Generated Answer: {the_generated_answer}")

        questions.append(the_question)
        ground_truths.append(the_answer)
        retrieved_contexts.append(the_context)
        generated_answers.append(the_generated_answer)
        
        count += 1        
        # if count > 10:
            # break

    # the_data = {
    #     "question": questions,
    #     "contexts": retrieved_contexts,
    #     "answer": ground_truths,
    #     "generated_answer": generated_answers
    # }

    the_data = []
    for i in range(len(questions)):
        the_data.append({
            "question": questions[i],
            "answer": generated_answers[i],
            "contexts": retrieved_contexts[i],
            "ground_truth": ground_truths[i],
        })    

    the_ragas_dataset = Dataset.from_list(the_data)
        
    result = evaluate(dataset=the_ragas_dataset, metrics=[faithfulness, answer_relevancy, context_recall])
    result_df = result.to_pandas()
    # in the dataframe, I only want to keep the following columns: question, answer, contexts, ground_truth, faithfulness, answer_relevancy, context_recall
    result_df = result_df[[
        'user_input', 
        # 'response', 
        # 'retrieved_contexts', 
        # 'reference', 
        'faithfulness', 'answer_relevancy', 'context_recall']]
    
    os.makedirs(report_dir, exist_ok=True)
    report_file_suffix = datetime.now().strftime("%Y%m%d_%H%M%S")
    result_df.to_csv(f"{report_dir}/ragas_report_{report_file_suffix}.csv", index=False)     
    result_df.to_excel(f"{report_dir}/ragas_report_{report_file_suffix}.xlsx", index=False)
    result_df.to_json(f"{report_dir}/ragas_report_{report_file_suffix}.json", orient="records")
    


if __name__ == "__main__":
    my_dataset = []
    
    my_logger.info("\n=== Loading JSON files into memory ===")
    my_dataset = load_json_files_from_measure_data(my_dataset)
    
    if my_dataset:
        my_logger.info(f"Successfully loaded {len(my_dataset)} JSON files:")
        run_ragas_on_dataset(my_dataset)
        # for data in my_dataset:
        #     my_logger.info(f"  - {data}")
    else:
        my_logger.error("No JSON data was loaded.")

