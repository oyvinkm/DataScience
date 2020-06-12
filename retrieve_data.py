import execquery
import pandas as pd
from sklearn.model_selection import train_test_split

def retrieve_data(nr_of_articles):
    content_train = execquery.execQuery("""SELECT contents, typen 
                                     FROM ml_view_2
                                     ORDER by random()
                                     LIMIT {};""".format(nr_of_articles))
    train, test = train_test_split(pd.DataFrame(content_train, columns=["content", "type"]), test_size=0.20)
    return train, test
