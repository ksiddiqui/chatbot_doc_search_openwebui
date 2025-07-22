# =============================================================================
# © 2025 Kashif Ali Siddiqui, Pakistan
# Developed by: Kashif Ali Siddiqui 
# Github: https://github.com/ksiddiqui
# LinkedIn: https://www.linkedin.com/in/ksiddiqui
# Email: kashif.ali.siddiqui@gmail.com
# Dated: July, 2025 
# -----------------------------------------------------------------------------
# This source code is the property of Kashif Ali Siddiqui and is confidential.
# Unauthorized copying or distribution of this file, via any medium, is strictly prohibited.
# ============================================================================= 

from datetime import datetime

# from ragas.data import Dataset
# from ragas.metrics import faithfulness, answer_relevancy, context_recall
# from ragas import evaluate

from system.setup import get_config_logger


config, logger = get_config_logger()

the_question = None
the_contexts = []
the_answer = None

def observability_reset():
    global the_question
    global the_contexts
    global the_answer
    the_question = None
    the_contexts = []
    the_answer = None

def observability_set_question(question):
    global the_question
    the_question = question

def observability_set_contexts(contexts):
    global the_contexts
    the_contexts = contexts

def observability_set_answer(answer):
    global the_answer
    the_answer = answer

def observability_evaluate_now():

    if the_question is None or the_contexts is None or the_answer is None:
        return None

    report_file_suffix = datetime.now().strftime("%Y%m%d_%H%M%S")

    # dataset = Dataset.from_dict({
    #     "question": [the_question],
    #     "contexts": the_contexts,
    #     "answer": [the_answer]
    # })

    # result = evaluate(dataset, metrics=[faithfulness, answer_relevancy, context_recall])
    # result.to_csv(f"./ragas/ragas_report_{report_file_suffix}.csv", index=False)      # Save as CSV
    # result.to_json(f"./ragas/ragas_report_{report_file_suffix}.json", orient="records")
    