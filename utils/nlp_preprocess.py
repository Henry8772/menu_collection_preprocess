

import spacy
from models.dish_segmenter import Dish
import re

nlp_en = None
nlp_zh = None
precomputed_reference_vectors = []

from models.word_unit import WordUnit

def load_spacy_models():
    global nlp_en, nlp_zh, precomputed_reference_vectors
    if nlp_en is None:
        nlp_en = spacy.load("en_core_web_lg")
    if nlp_zh is None:
        nlp_zh = spacy.load("zh_core_web_lg")

    if precomputed_reference_vectors == []:
        precomputed_reference_vectors = {
            "en": {word: nlp_en(word).vector for word in reference_words["en"]},
            "zh": {word: nlp_zh(word).vector for word in reference_words["zh"]}
        }


reference_words = {
    "en": [
        "food", "dish", "meal", "beverage", "drink", "appetizer", "dessert",
        "starter", "main", "entree", "side", "course", "soup", "salad", 
        "grill", "roast", "fried", "steamed", "baked", "boiled", "sautéed", 
        "stir-fry", "casserole", "pasta", "noodles", "rice", "sandwich",
        "burger", "pizza", "wrap", "taco", "sushi", "roll", "dumpling",
        "pie", "cake", "pastry", "scone", "muffin", "ice-cream", "smoothie", 
        "cocktail", "coffee", "tea", "juice", "soda", "wine", "beer", "liqueur",
        "steak", "chicken", "fish", "pork", "beef", "lamb", "curry", "stew",
        "healthy", "vegan", "vegetarian", "gluten-free", "organic", "raw", 
        "kebab", "falafel", "tagine", "tapas", "paella", "ceviche", "bruschetta", 
        "risotto", "gnocchi", "quesadilla", "kimchi", "tempura", "masala", 
        "satay", "pho", "tandoori", "dim sum", "shawarma", "fajitas", "brulee", 
        "bisque", "miso", "ramen", "biryani", "tartare", "caviar", "escargot", 'piece'
    ],
    "zh": [
        "食物", "菜肴", "饭菜", "饮料", "饮品", "开胃菜", "甜点", "头盘", "主菜", "汤", 
        "沙拉", "烤", "炸", "蒸", "煮", "炒", "焖", "面", "饭", "寿司", "卷", "饺子", 
        "汉堡", "披萨", "三明治", "蛋糕", "面包", "冰淇淋", "果汁", "鸡尾酒", "咖啡", 
        "茶", "汽水", "红酒", "啤酒", "白酒", "牛肉", "羊肉", "鸡肉", "鱼", "猪肉", 
        "咖喱", "炖肉", "清蒸", "卤", "酱", "汁", "酸辣", "五香", "酸甜", "辣",
        "健康", "素食", "全素", "无麸质", "有机", "生食", "串烧", "中东烤肉", "烧烤", "酸奶",
        "糖醋", "煲", "拌", "烩", "炖", "香煎", "泡菜", "天妇罗", "咸鱼", "糯米饭",
        "冷面", "烧卖", "炸酱面", "烤鸭", "牛腩", "糖葫芦", "花卷", "云吞", "馄饨", "鱼香", "块"
    ]
}




def is_english(s):
    # Checking if there are any English alphabets in the string
    return bool(re.search('[a-zA-Z]', s))

def is_chinese(s):
    return bool(re.search(r"[\u4e00-\u9fff]+", s))

def split_dish_info(dish_data):
    dish = Dish(dish_data)

    in_chinese_mode = True  # start with the assumption that the data starts with a Chinese name

    chinese_parts = []
    english_parts = []
    temp_text = []

    context_size = 2  # can adjust based on your requirement
    context_buffer = []

    for wordUnit in dish_data:

        word = wordUnit.word
        if word.strip() == '':
            continue

        # Detect language change
        if is_chinese(word) and not in_chinese_mode:
            english_parts.append(temp_text)  # Dump the temp_text to english_parts
            temp_text = []  # Reset temp_text
            context_buffer = []  # Reset context buffer
            in_chinese_mode = True
        elif is_english(word) and in_chinese_mode:
            chinese_parts.append(temp_text)  # Dump the temp_text to chinese_parts
            temp_text = []  # Reset temp_text
            context_buffer = []  # Reset context buffer
            in_chinese_mode = False

        if is_chinese(word):
            if not is_word_relevant(word, context_buffer, "zh"):
                continue
        elif is_english(word):
            if not is_word_relevant(word, context_buffer, "en"):
                continue
        
        
        # Update context_buffer
        context_buffer.append(word)
        if len(context_buffer) > context_size:
            context_buffer.pop(0)


        

        temp_text.append(wordUnit)

    # Handle any remaining text in temp_text after the loop
    if in_chinese_mode:
        chinese_parts.append([wordUnit])
    else:
        english_parts.append([wordUnit])


    if chinese_parts:
        dish.chinese_name = chinese_parts[0]
        if len(chinese_parts) > 1:
            dish.chinese_description = chinese_parts[1:]
        # doc_zh = nlp_zh(''.join(chinese_parts))
        # chinese_sentences = [sent.text for sent in doc_zh.sents]
        # dish.chinese_name = chinese_sentences[0]
        # if len(chinese_sentences) > 1:
        #     dish.chinese_description = ''.join(chinese_sentences[1:])

    if english_parts:
        dish.english_name = english_parts[0]
        if len(english_parts) > 1:
            dish.english_description = english_parts[1:]


    # if chinese_parts:
    #     dish.chinese_name = ''.join(chinese_parts[0])
    #     if len(chinese_parts) > 1:
    #         dish.chinese_description = ''.join([''.join(part) for part in chinese_parts[1:]])
    #     # doc_zh = nlp_zh(''.join(chinese_parts))
    #     # chinese_sentences = [sent.text for sent in doc_zh.sents]
    #     # dish.chinese_name = chinese_sentences[0]
    #     # if len(chinese_sentences) > 1:
    #     #     dish.chinese_description = ''.join(chinese_sentences[1:])

    # if english_parts:
    #     dish.english_name = ' '.join(english_parts[0])
    #     if len(english_parts) > 1:
    #         dish.english_description = ' '.join([' '.join(part) for part in english_parts[1:]])
        # doc_en = nlp_en(' '.join(english_parts))
        # english_sentences = [sent.text for sent in doc_en.sents]
        # dish.english_name = english_sentences[0]
        # if len(english_sentences) > 1:
        #     dish.english_description = ' '.join(english_sentences[1:])

    return dish

def is_word_relevant(word, context, language):
    
    # Select the appropriate spaCy model based on the language
    model = nlp_en if language == "en" else nlp_zh if language == "zh" else None
    if not model:
        raise ValueError("Unsupported language!")

    if language == 'en':
        combined_text = ' '.join(context) + ' ' + word
    else:
        combined_text = ''.join(context) + '' + word
    
    combined_vector = model(combined_text).vector

    # Define a set of reference words for each language
    

    # Calculate the similarity between the combined_text and each reference word
    similarities = [cosine_similarity(combined_vector, precomputed_reference_vectors[language][reference_word]) for reference_word in reference_words[language]]

    # Check if the maximum similarity exceeds a threshold (e.g., 0.5)
    if max(similarities) > 0.4:
        return True
    return False

def cosine_similarity(vecA, vecB):
    dot = sum(a*b for a, b in zip(vecA, vecB))
    normA = sum(a*a for a in vecA) ** 0.5
    normB = sum(b*b for b in vecB) ** 0.5
    return dot / (normA*normB)