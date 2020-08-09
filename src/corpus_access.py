import os
import json


# Module 5 - Corpus access
class CorpusAccess():
    COURSE_DICT = os.path.dirname(
        os.path.abspath(__file__)) + '/../courses.json'

    def __init__(self, course_dict_file=COURSE_DICT):
        self.course_dict_file = course_dict_file

        # setup corpus access
        with open(course_dict_file, 'r', encoding='utf-8') as f:
            self.course_dict = json.loads(f.read())

        print(type(self.course_dict))

    def get(self, key):
        return self.course_dict.get(key)
