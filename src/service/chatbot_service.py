from pydantic import BaseModel

from src.util.prompts import INITIAL_FILTER_PROMPT, INITIAL_FILTER_ASSISTANT_PROMPT, CHAT_FILTER_ASSISTANT_PROMPT
from src.service.cv_parser_service import CvParserService
from src.service.llm_service import LLMService


# The below class is a structured response we are enforcing after a basic filtering of
class FilteredCvListStructuredResponse(BaseModel):
    cv_names: list[str]


class ChatFilterResponse(BaseModel):
    has_user_ask_to_quit: bool
    has_user_asked_to_restart_filtering: bool
    has_user_asked_unrelated_query: bool
    response_text: str


class ChatBotService:
    def __init__(self):
        self._cv_parser_service = CvParserService()
        self._llm_service = LLMService()

    def initiate_chat(self):
        print("""
Welcome to the CV Query Chatbot!
All files placed inside data/sample_cvs have now been processed 
To begin with, pls start with entering a few basic filter criteria
""")
        continue_chat = True
        while continue_chat:
            """
            The idea of introducing some basic filters is to filter by some basic criteria manually before
            using llm for further querying. This can save us from the high cost of querying a great number of input
            tokens in query. However, for the time being since parser isn't able to accurately parse information like
            skills, companies and experience with a high accuracy, we will be using llm structured query response  
            """
            skills_input = input("\nEnter required skills (comma-separated): ..... Press Enter to Skip :\n")
            required_skills = [skill.strip() for skill in skills_input.split(",")] if skills_input else ['Any']

            min_experience_input = input("\nMinimum years of experience: ..... Press Enter to Skip :\n")
            min_experience = float(min_experience_input) if min_experience_input else 0

            designations_input = input("\nDesignations to filter by (comma-separated): ..... Press Enter to Skip :\n")
            desired_designations = [comp.strip() for comp in designations_input.split(",")] if designations_input else ['Any']

            all_cv_data = self._cv_parser_service.load_all_cv_data()
            filtered_cv_data = {
                k: {
                    'company_names': v.get('company_names', []),
                    'designation': v.get('designation', []),
                    'total_experience': v.get('total_experience', 0.0),
                    'skills': v.get('skills', [])
                }
                for k, v in all_cv_data.items()
            }

            print("Filtering CVs based on given data......")

            response = self._llm_service.get_structured_response(
                INITIAL_FILTER_PROMPT.format(filtered_cv_data, min_experience, required_skills, desired_designations),
                INITIAL_FILTER_ASSISTANT_PROMPT, FilteredCvListStructuredResponse)
            if not response.cv_names:
                print("....no CVs found with the given criteria, pls enter the filters again")
                continue

            print("\nThe below CVs must be of interest to you ")
            print(response.cv_names)
            parsed_cv_data = self._cv_parser_service.load_cv_data(response.cv_names)
            print("\nRobo : Hello!! I am here to help you with clearing through the clutter on CVs."
                  "Feel free to quit chat or restart chat from the start.\n")
            while continue_chat:
                user_prompt = input("\nYou: ")

                # Safeguard against empty input
                if not user_prompt.strip():
                    continue

                # Query the LLM to interpret the user’s intent and return a structured response
                structured_response = self._llm_service.get_structured_response(
                    user_prompt,  # The user's last input
                    CHAT_FILTER_ASSISTANT_PROMPT.format(parsed_cv_data),
                    ChatFilterResponse  # Your new Pydantic model
                )

                # Convert the Pydantic model to a dictionary for easy field access
                response_data = structured_response.dict()

                # Check flags in the structured response
                if response_data["has_user_ask_to_quit"]:
                    # The LLM determined the user wants to end
                    print("Exiting the chat as per user request...")
                    continue_chat = False
                    break

                elif response_data["has_user_asked_to_restart_filtering"]:
                    # The LLM determined the user wants to restart
                    print("Restarting the filtering process as per user request...")
                    # Break out of this inner loop
                    # (so we return to the outer loop and prompt for new filter criteria)
                    break

                elif response_data["has_user_asked_unrelated_query"]:
                    # The LLM determined the user digressed
                    # Possibly provide a short clarifying response, or just let them ask again
                    print(
                        "Robo : " + response_data['response_text'])
                    # Continue the chat loop so the user can try something else
                    continue

                else:
                    # If none of the flags are true, the LLM might have simply provided an answer
                    # You can do anything here — e.g., keep chatting, or just loop back for more user input
                    # For now, we just let the user ask again
                    print("Robo : " + response_data['response_text'])
