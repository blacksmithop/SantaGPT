from os import environ
from dotenv import load_dotenv
from langchain.chat_models import AzureChatOpenAI
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

load_dotenv()

llm = AzureChatOpenAI(deployment_name=environ["DEPLOYMENT_NAME"])

prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(
            "Speak like you are Santa Claus. Ensure answers short and witty"
        ),
        # The `variable_name` here is what must align with memory
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{question}")
    ]
)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

conversation = LLMChain(
    llm=llm,
    prompt=prompt,
    verbose=True,
    memory=memory
)
def chat(question: str):
    response = conversation({"question": question})
    message = response["text"]
    message = message[:250] # truncate response
    return message