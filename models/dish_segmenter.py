import json
from models.word_unit import WordUnit

class Dish:
    def __init__(self, raw_text):
        self.chinese_name = []
        self.english_name = []
        self.chinese_description = []
        self.english_description = []
        self.raw_text = raw_text

    def __str__(self):
        return f"Chinese Name: {self.chinese_name}\n" \
               f"English Name: {self.english_name}\n" \
               f"Chinese Description: {self.chinese_description}\n" \
               f"English Description: {self.english_description}\n" \
               f"Raw text: {self.raw_text}\n" \

    def output(self):
        return f"Chinese Name: {self.chinese_name}\n" \
               f"English Name: {self.english_name}\n" \
               f"Chinese Description: {self.chinese_description}\n" \
               f"English Description: {self.english_description}\n" \
               f"Raw text: {self.raw_text}\n" \
                   
    def to_dict(self):
        def handle_list(data_list):
            
            # If the list is empty or None, return an empty list
            if not data_list:
                return []
            # If it contains single WordUnit objects or other non-list items, just convert them to dicts

            # Otherwise, handle as a list of lists
            result = []
            for item in data_list:
                if isinstance(item, WordUnit):
                    result.append(item.word)
                else:
                    result.append([word_unit.word for word_unit in item])
            return result
        return {
            "chinese_name": handle_list(self.chinese_name),
            "english_name": handle_list(self.english_name),
            "chinese_description": handle_list(self.chinese_description),
            "english_description": handle_list(self.english_description),
            "raw_text": handle_list(self.raw_text)
        }

    # def to_dict(self):
    #     def handle_list(data_list):
            
    #         # If the list is empty or None, return an empty list
    #         if not data_list:
    #             return []
    #         # If it contains single WordUnit objects or other non-list items, just convert them to dicts

    #         # Otherwise, handle as a list of lists
    #         result = []
    #         for item in data_list:
    #             if isinstance(item, WordUnit):
    #                 result.append(item.to_dict())
    #             else:
    #                 result.append([word_unit.to_dict() for word_unit in item])
    #         return result
    #     return {
    #         "chinese_name": handle_list(self.chinese_name),
    #         "english_name": handle_list(self.english_name),
    #         "chinese_description": handle_list(self.chinese_description),
    #         "english_description": handle_list(self.english_description),
    #         "raw_text": handle_list(self.raw_text)
    #     }

    def __dict__(self):
        return self.to_dict()

class DishEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Dish):
            return obj.__dict__()
        return super().default(obj)