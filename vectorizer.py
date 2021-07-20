import requests

from sklearn.feature_extraction.text import TfidfVectorizer


class VectorHolder():

    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))

    def preprocess(self):
        '''
        tfidf vectorizer by treating each raw post or comment as a document
        only receive post or comment longer than 1 sentence as a valid input
        '''

        url = 'http://localhost:8000/api/lead'
        try:
            page = requests.get(url).json()  # List[dict()]
        except:
            print('host the Django web service first')
            raise

        for content in page:
            msg = content['message'].split(' ')
            if len(msg) > 1:
                X = self.vectorizer.fit_transform(msg)
            else:
                print('posts not longer than 1 in sentence length is not considered')


if __name__ == '__main__':
    VectorHolder().preprocess()