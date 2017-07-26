# coding:utf8
import jieba
import jieba.posseg as pseg
import networkx as nx
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer, CountVectorizer
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
        delimiters = frozenset(u'。！？?!.')
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
    def get_abstract(content, size=2):
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

    @staticmethod
    def get_article_tags(content):
        stop_word = [unicode(line.rstrip()) for line in open('chinese_stopword.txt')]
        print len(stop_word)
        content = content.strip().replace('\n', '').replace(' ', '').replace('\t', '').replace('\r', '')
        seg_list = pseg.cut(content)
        seg_list_after = []
        # 去停用词
        for seg in seg_list:
            if seg.word not in stop_word:
                seg_list_after.append(seg.word)
        result = ' '.join(seg_list_after)
        wordslist = [result]
        vectorizer = CountVectorizer()
        transformer = TfidfTransformer()
        tfidf = transformer.fit_transform(vectorizer.fit_transform(wordslist))

        words = vectorizer.get_feature_names()  # 所有文本的关键字
        weight = tfidf.toarray()

        n = 5  # 前五位
        tag_list = []
        for w in weight:
            # 排序
            loc = np.argsort(-w)
            for i in range(n):
                tag_list.append(words[loc[i]])
        return tag_list

