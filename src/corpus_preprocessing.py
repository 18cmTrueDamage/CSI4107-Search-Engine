import csv
import re
import os

from bs4 import BeautifulSoup

current_dir = os.path.dirname(os.path.abspath(__file__))
src = current_dir + '/../UofO_Courses.html'
out = current_dir + '/../course_corpus.csv'


def _separate_files(src_file):
    end = '</html>'
    with open(src_file, 'r') as f:
        files = f.read().split(end)

    return files


def preprocess(src_file):
    soup = BeautifulSoup(src_file, 'lxml')

    course_name = []
    course_description = []
    doc_id = []

    for e in soup.find_all('div', class_='courseblock'):
        name = e.find('p', class_='courseblocktitle noindent')
        description = e.find('p', class_='courseblockdesc noindent')

        if name is not None:
            name = name.text
            if 1 <= int(name[5]) <= 3:  # english course
                course_name.append(name)

                # docid = name[:8]
                docid = re.sub(' ', '_', name[:8])
                doc_id.append(docid)

                if description is not None:
                    course_description.append(description.text.strip('\n'))
                else:
                    course_description.append('')

    with open(out, 'a') as o:
        writer = csv.writer(o)
        for docid, name, description in zip(doc_id, course_name, course_description):
            writer.writerow([docid, name, description])


# Module 2 - Corpus Pre-processing
def createCSV(src_file=None, dst_file=None):
    if src_file is None:
        src_file = src
    files = _separate_files(src_file)

    if dst_file is None:
        dst_file = out
    if os.path.exists(dst_file):
        print("Detected %s exists, removing ..." % dst_file)
        os.remove(dst_file)

    for file in files:
        preprocess(file)


if __name__ == "__main__":
    print(src)
    createCSV()
