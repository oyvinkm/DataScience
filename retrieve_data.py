import execquery
import pandas as pd

def retrieve_data(nr_of_articles):
    content_train = execquery.execQuery("""SELECT contents, articleID 
                                     FROM articles 
                                     Where articleid < {};""".format(nr_of_articles))
    types_train = execquery.execQuery("""SELECT typen 
                                   FROM typer 
                                   NATURAL JOIN 
                                   (SELECT typeID FROM domains 
                                   NATURAL JOIN 
                                   (SELECT domainID from articledomains where articleID < {}) as foo) as foobar;""".format(nr_of_articles))
    train = pd.DataFrame(content_train, columns=["content", "articleID"])
    types_train = pd.DataFrame(types_train, columns=["type"])
    train["type"] = types_train["type"]
    start_id_test = nr_of_articles + 1
    end_id_test = start_id_test + (nr_of_articles/2)
    content_test = execquery.execQuery("""SELECT contents, articleID 
                                     FROM articles 
                                     Where articleid BETWEEN {} AND {};""".format(start_id_test,end_id_test))
    types_test = execquery.execQuery("""SELECT typen 
                                   FROM typer 
                                   NATURAL JOIN 
                                   (SELECT typeID FROM domains 
                                   NATURAL JOIN 
                                   (SELECT domainID FROM articledomains WHERE articleID BETWEEN {} AND {}) AS foo) AS foobar;""".format(start_id_test,end_id_test))
    test = pd.DataFrame(content_test, columns=["content", "articleID"])
    types_test = pd.DataFrame(types_test, columns=["type"])
    test["type"] = types_test["type"]
    return train, test
