from datetime import timedelta as td

vocab_list_path = r'C:\Users\Amber\Documents\Code\vocab_drill_generator\\'
vocab_lists = {
                'Korean': 'vocab lists\Korean.csv'
              }
# # generation rules #
# words_to_generate = 10
# max_review_words = 8

# repetition_rules - minimum number of days between repetitions, as a function so can be applied indefinitely #
def calculate_next_review(current_date, number_reviews):
    return current_date + td(days=(2**number_reviews)+1)
