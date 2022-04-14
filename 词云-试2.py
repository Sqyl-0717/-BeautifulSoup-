import jieba
import os
import os.path
from win32com import client as wc #这啥玩意儿
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image