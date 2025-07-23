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

from typing import List, Tuple, Dict, Any
from typing import Optional

from crewai import Agent, Task, Crew, Process
from crewai.tools import tool
from langchain_openai import ChatOpenAI

from system.setup import get_config_logger
from services.rag import RAGManager
from services.llm_llama_index import LLMManager

_rag_manager = None

@tool
def document_search(query: str) -> str:
    """
    CrewAI/LangChain compatible: Search through the document collection to find relevant context and information. Input should be a question or search query. Returns relevant document excerpts with sources.
    """
    try:
        # Validate input
        if not query or not isinstance(query, str):
            return "Error: Query must be a non-empty string"
        # Clean and validate query
        query = query.strip()
        if not query:
            return "Error: Query cannot be empty"
 
        context = _rag_manager.query_context_retrieval(query)        
        return context
    except Exception as e:
        error_msg = f"Error in Document Search Tool. Exception occurred: {str(e)}"
        return error_msg

class MultiAgentsManager:
    def __init__(self, rag_manager: RAGManager, llm_manager: LLMManager):
        global _rag_manager
        _rag_manager = rag_manager
        
        self.config, self.logger = get_config_logger()
        self.rag_manager = rag_manager
        self.llm_manager = llm_manager
        self.multi_agents = None

        self.llm = None
        self.model_id = 'Ollama'
        self.inference_model = self.config["llm_ollama_model"]
        self.llm_ollama_base_url = self.config['llm_ollama_base_url']
        self.llm_ollama_temperature = self.config['llm_ollama_temperature']

        self.retriever_agent = None
        self.validator_agent = None
        self._create_agents()

    # @tool
    # def document_search(self, query: str) -> str:
    #     """
    #     CrewAI/LangChain compatible: Search through the document collection to find relevant context and information. Input should be a question or search query. Returns relevant document excerpts with sources.
    #     """
    #     try:
    #         self.logger.info(f"Document Search Tool called with query: {query}")
    #         context = self.rag_manager.query_context_retrieval(query)
            
    #         self.logger.info(f"Document Search Tool returning context: {context[:200]}...")
    #         return context
    #     except Exception as e:
    #         error_msg = f"Error in Document Search Tool. Exception occurred: {str(e)}"
    #         self.logger.error(error_msg)
    #         return error_msg

    def _create_agents(self):
        self.llm = ChatOpenAI(
            api_key=self.config['llm_openai_api_key'],
            model=self.config['llm_openai_model'],
            temperature=self.config['llm_openai_temperature'],
            # max_tokens=self.config['llm_openai_max_tokens'],
            # temperature=self.config['llm_openai_temperature'],
            # model=f"ollama/{self.inference_model}",
            # base_url=self.llm_ollama_base_url,
        )
        
        self.retriever_agent = Agent(
            role="Document Retriever and Answer Generator",
            goal="Use the document_search tool to find relevant context and generate comprehensive answers based on the retrieved information",
            backstory="""You are an expert document analyst who excels at using the document_search tool to find relevant context 
            from document collections and then synthesizing that context into clear, comprehensive answers. You always 
            base your responses strictly on the context returned by the document_search tool and cite sources clearly.
            
            Your process:
            1. Use the document_search tool to get relevant context
            2. Analyze the context carefully which includes sources and sections
            3. Generate an answer based only on that context
            4. Include proper citations from the sources mentioned in the context""",
            tools=[document_search],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            max_iter=3,
            memory=False,
        )

        self.validator_agent = Agent(
            role="Quality Checker and Validator",
            goal="Review answers to ensure they are grounded in the provided context and actually answer the question asked",
            backstory="""You are a meticulous quality checker who ensures answers meet three criteria:
            1. No hallucination - all information comes from the document context provided by the search tool
            2. Proper grounding - claims are supported by the retrieved context
            3. Question relevance - the answer actually addresses what was asked
            
            You can optionally use the document_search tool to verify information if needed. You flag any issues and suggest improvements when needed.""",
            tools=[document_search],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            max_iter=3,
            memory=False,
        )

    def _create_crew(self, question: str) -> Crew:
        retrieval_task = Task(
            description=f"""You MUST use the 'document_search' tool to get relevant context for this question:
            '{question}'
            
            REQUIRED STEPS:
            1. FIRST: Call the 'document_search' tool with the question as input
            2. The tool will return relevant context from documents with sources and sections formatted like:
               [Source 1 - filename.pdf]
               Section: section_name
               content text...
            3. THEN: Carefully analyze the context returned by the tool
            4. Generate a comprehensive answer based ONLY on the context provided by the tool
            5. Include specific citations referencing the sources from the context
            6. If the context is insufficient, clearly state what's missing
            
            IMPORTANT: 
            - You must use the document_search tool to get context first
            - Base your answer ONLY on the context returned by the tool
            - Do not add information that isn't in the provided context
            - Include proper citations from the sources mentioned in the context""",
            agent=self.retriever_agent,
            expected_output="A comprehensive answer with clear source citations based on the context returned by document_search tool",
        )

        validation_task = Task(
            description=f"""Review the previous agent's answer for the question: '{question}'
            
            You may optionally use the 'document_search' tool to get context and verify information if needed.
            
            Perform these validation checks:
            
            HALLUCINATION CHECK: 
            - Verify claims in the previous answer are reasonable and could come from document context
            - Flag any information that seems to be added without supporting context
            
            GROUNDING CHECK:
            - Check that the answer references specific sources and citations
            - Verify the reasoning is based on provided context
            - Ensure citations match actual sources mentioned
            
            RELEVANCE CHECK:
            - Ensure the answer actually addresses the specific question asked
            - Verify no important aspects of the question are ignored
            - Check that the response is focused and not overly broad
            
            OUTPUT FORMAT:
            If the answer passes all checks, respond with:
            "VALIDATION PASSED: The answer is well-grounded, relevant, and based on provided context."
            
            If there are issues, provide specific feedback and suggestions for improvement.""",
            agent=self.validator_agent,
            expected_output="Validation status (PASSED or specific improvement suggestions)",
        )

        tasks = [retrieval_task, validation_task]
        agents = [self.retriever_agent, self.validator_agent]

        try:
            crew = Crew(
                agents=agents,
                tasks=tasks,
                process=Process.sequential,
                verbose=False,
                max_execution_time=300,  # 5 minute timeout
                memory=False,
            )
            self.logger.info(f"Crew created successfully for question: {question}")
            return crew
        except Exception as e:
            self.logger.error(f"Error creating crew. Exception occurred: {e}")
            return None

    def answer_question(self, question: str) -> Dict[str, Any]:
        self.logger.info(f"Starting CrewAI processing for: {question}")
        response = None
        
        try:
            crew = self._create_crew(question)
            # Execute crew with timeout
            try:
                self.logger.info(">>> Starting crew execution...")
                self.logger.info("------------------------------")
                crew.kickoff()
                self.logger.info("------------------------------")
                self.logger.info("<<< Crew execution completed...")
            except Exception as e:
                self.logger.info("------------------------------")
                self.logger.error(f"!!! Crew execution failed... with exception: {e}")
                raise e
                
            # Get individual task outputs
            retrieval_output = ""
            validation_output = ""

            for task in crew.tasks:
                if task.agent.role == "Document Retriever and Answer Generator":
                    retrieval_output = task.output.raw_output if hasattr(task.output, "raw_output") else str(task.output)
                elif task.agent.role == "Quality Checker and Validator":
                    validation_output = task.output.raw_output if hasattr(task.output, "raw_output") else str(task.output)

            # Use the retrieval output as the final answer
            final_answer = retrieval_output

            response = {
                "question": question,
                "final_answer": final_answer,
                "retrieval_output": retrieval_output,
                "validation_output": validation_output,
                "sources": retrieval_output,
                "metadata": validation_output,
                "agents_used": [agent.role for agent in crew.agents],
                "model_id": self.model_id,
            }

        except Exception as e:
            self.logger.error(f"Crew execution failed. Exception occurred: {e}")
        
        return response
        
        