import warnings

warnings.filterwarnings("ignore", category=UserWarning)
from src.service.chatbot_service import ChatBotService

if __name__ == "__main__":
    ChatBotService().initiate_chat()
