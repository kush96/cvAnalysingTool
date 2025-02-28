from openai import OpenAI
from pyrate_limiter import RequestRate, Duration, Limiter
from src.util.config import config


class LLMService:
    def __init__(self):
        self.client = client = OpenAI(api_key=config['openai_api_key'])
        self.model = config['openai_model']
        # Create a shared rate limiter: 10 calls per minute

    # Currently only putting per-minute-rate. We can also put hourly and daily rates along with current rates
    RATE = RequestRate(10, Duration.MINUTE)
    openai_rate_limiter = Limiter(RATE)

    @openai_rate_limiter.ratelimit("openai_rate_limiter", delay=True)
    def query_llm(self, prompt, assistant_prompt):
        response = self.client.chat.completions.create(
            model=self.model,
            store=True,
            messages=[
                {"role": "developer",
                 "content": assistant_prompt},
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return response.choices[0].message

    @openai_rate_limiter.ratelimit("openai_rate_limiter", delay=True)
    def get_structured_response(self, prompt, assistant_prompt, response_schema):
        """
        :param prompt: The actual prompt that is to be answered by gpt
        :param assistant_prompt: we can instruct our assistant to the minute details on how to answer the query
        :param response_schema:
        :return:
        """
        res = self.client.beta.chat.completions.parse(
            model=self.model,
            messages=[
                {"role": "developer", "content": assistant_prompt},
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            response_format=response_schema,
        )
        return res.choices[0].message.parsed
