from setuptools import setup, find_packages
import stopwords

setup(
    name=stopwords.__name__,
    version=stopwords.__version__,
    url='https://github.com/Kimjibeom/textrank/stopwords-ko',
    author=stopwords.__author__,
    author_email='a889997@naver.com',
    description='TextRank based Summarizer (Keyword and key-sentence extractor)',
    packages=find_packages(),
    long_description=open('README.md', encoding="utf-8").read(),
    zip_safe=False,
    setup_requires=[]
)
