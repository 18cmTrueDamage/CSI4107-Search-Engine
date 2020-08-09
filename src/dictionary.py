import csv
import text_processing


# Module 3 - Dictionary building
def build_vocabulary(corpus, stop_words_removal=True, stemming=True, normalization=True):
    terms = set()
    with open(corpus, 'r') as corpus_file:
        reader = csv.reader(corpus_file)
        for row in reader:

            if len(row) == 0:  # bs4 will build empty between lines in CSV somehow
                continue

            doc_id = row[0]
            title = row[1]
            content = row[2]

            # to_be_processed = [title, description]
            to_be_processed = [title + content]

            for e in to_be_processed:
                processed_tokens = text_processing.process(e, stop_words_removal=stop_words_removal, stemming=stemming,
                                                           normalization=normalization)
                for term in processed_tokens:
                    terms.add(term)

    return terms


if __name__ == "__main__":
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    corpus = current_dir + '/../course_corpus.csv'
    print(build_vocabulary(corpus))
