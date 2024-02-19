# from typing import List
# from models.chat_models import UserMessage

# # Look into convetering this file to work with Assistants API


# class Conversation:
#     def __init__(self, system_message: UserMessage):
#         self.messages = []
#         if system_message:
#             self.add_system_message(system_message)

#     def add_system_message(self, content):
#         self.messages.append({"role": "system", "content": content})

#     def add_user_message(self, content: Message):
#         self.messages.append(content)

#     def add_assistant_message(self, content: Message):
#         self.messages.append(content)

#     def add_function_message(self, function_name, content):
#         self.messages.append(
#             {"role": "function", "name": function_name, "content": content}
#         )

#     def get_messages(self) -> List[Message]:
#         return self.messages
