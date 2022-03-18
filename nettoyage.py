import re
import string
from nltk.corpus import stopwords

def remove_URL (text):
    url = re.compile(r"https?://\s+ www\.\s+")
    return url.sub(r"", text)


def remove_html(text):
    html = re.compile(r"<.*?>")
    return html.sub(r"", text)
         

def remove_emoji(string):
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F" # emoticons
        u"\U0001F300-\U0001F5FF" # symbols & pictographs
        u"\U0001F680-\U0001F6FF" # transport & map symbols
        u"\U0001F1E0-\U0001F1FF" # flags (i0s)
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+",
        flags=re.UNICODE,
    )
    return emoji_pattern.sub(r"", string)


def remove_punct (text):
    table = str.maketrans ("","",string.punctuation)
    return text.translate(table)

stop = set (stopwords.words ( "english"))
def remove_stopwords (text):
    text = [word.lower () for word in text.split() if word.lower() not in stop]
    return " ".join (text)