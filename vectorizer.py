import requests

from sklearn.feature_extraction.text import TfidfVectorizer

class VectorHolder():
    vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.6, stop_words='english', ngram_range=(1, 3))

    def preprocess(self):
        '''
        tfidf vectorizer by treating each raw post or comment as a document
        only receive post or comment longer than 1 sentence as a valid input
        '''
        url = 'http://localhost:8000/api/lead'
        page = requests.get(url).json()  # List[dict()]
        for content in page:
            msg = content['message'].split(' ')
            if len(msg) > 1:
                X = self.vectorizer.fit_transform(msg)


if __name__ == '__main__':
    VectorHolder().preprocess()