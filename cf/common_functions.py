# coding:utf8
import jieba
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
from sklearn.feature_extraction.text import TfidfTransformer
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class CommonFuction:
    @staticmethod
    def cut_sentence(sentence):
        """ 
        分句 
        :param sentence: 
        :return: 
        """
        if not isinstance(sentence, unicode):
            sentence = sentence.decode('utf-8')
        delimiters = frozenset(u'。！？')
        buf = []
        for ch in sentence:
            buf.append(ch)
            if delimiters.__contains__(ch):
                yield ''.join(buf)
                buf = []
        if buf:
            yield ''.join(buf)

    @staticmethod
    def load_stopwords(path='chinese_stopword.txt'):
        """ 
        加载停用词 
        :param path: 
        :return: 
        """
        with open(path) as f:
            stopwords = filter(lambda x: x, map(lambda x: x.strip().decode('utf-8'), f.readlines()))
        stopwords.extend([' ', '\t', '\n'])
        return frozenset(stopwords)

    @staticmethod
    def cut_words(sentence):
        """ 
        分词 
        :param sentence: 
        :return: 
        """
        stopwords = CommonFuction.load_stopwords()
        return filter(lambda x: not stopwords.__contains__(x), jieba.cut(sentence))

    @staticmethod
    def get_abstract(content, size=3):
        """ 
        利用textrank提取摘要 
        :param content: 
        :param size: 
        :return: 
        """
        docs = list(CommonFuction.cut_sentence(content))
        tfidf_model = TfidfVectorizer(tokenizer=jieba.cut, stop_words=CommonFuction.load_stopwords())
        tfidf_matrix = tfidf_model.fit_transform(docs)
        normalized_matrix = TfidfTransformer().fit_transform(tfidf_matrix)
        similarity = nx.from_scipy_sparse_matrix(normalized_matrix * normalized_matrix.T)
        scores = nx.pagerank(similarity)
        tops = sorted(scores.iteritems(), key=lambda x: x[1], reverse=True)
        size = min(size, len(docs))
        indices = map(lambda x: x[0], tops)[:size]
        return map(lambda idx: docs[idx], indices)

