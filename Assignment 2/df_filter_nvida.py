import re


def insert_empty_column_to_df(df, original_column, extension, default_value_column):
    column_index = df.columns.get_loc(original_column)
    nr_word_column_name = f"{original_column}_{extension}"
    if not nr_word_column_name in df.columns:
        if default_value_column == "list":
            df.insert(loc=column_index + 1, column=nr_word_column_name, value=[])
        else:
            df.insert(loc=column_index + 1, column=nr_word_column_name, value=default_value_column)
    return nr_word_column_name


def check_article_NVIDA_keyword_match(text, key_words="nvidia|nvda"):
    try:
        if re.search(key_words, text.lower()):
            return True
        else:
            return False
    except AttributeError:
        print(text)
        return False


def add_nvidia_topic_title_content(df):
    """

    :param df: df to process
    :param column_name_to_count: the column name to count the nr of words present
    :return:
    """
    title_column_name = insert_empty_column_to_df(df=df,
                                                  original_column="title",
                                                  extension="NVIDIA_topic",
                                                  default_value_column=False)
    content_column_name = insert_empty_column_to_df(df=df,
                                                    original_column="content",
                                                    extension="NVIDIA_topic",
                                                    default_value_column=False)

    for index, row in df.iterrows():
        df.at[index, title_column_name] = check_article_NVIDA_keyword_match(row["title"])
        df.at[index, content_column_name] = check_article_NVIDA_keyword_match(row["content"])


def add_improved_NVDA_ticker_column(df, tickers_to_add="NVDA"):
    """
    We are only going to take the articles that are related to NVIDIA, therefore we filter the articles based on the
    improved NVDA ticker symbol. Since in the original article, multiple tickers are connected to each article. but
    in the dataset, only a single ticker is associated with each article
    :param df:
    :param tickers_to_add: all the companies to add, default is "NVDA"
    :return:
    """
    improved_ticker_column = insert_empty_column_to_df(df=df,
                                                       original_column="ticker",
                                                       extension="NVDA_improved",
                                                       default_value_column=False)
    for index, row in df.iterrows():
        # if NVDA is ticker but NVDA is not mentioned in the topic or in the content, so must be mistake
        # ticker is not NVDA but NVIDA is mentioned in the topic or in the content
        if (row['ticker'] != "NVDA") & ((row['title_NVIDIA_topic'] == True) | (row['content_NVIDIA_topic'] == True)):
            df.at[index, improved_ticker_column] = True
        #NVIDA is the ticker
        elif row['ticker'] == tickers_to_add:
            df.at[index, improved_ticker_column] = True
        else:
            df.at[index, improved_ticker_column] = False


def filter_df_to_nvida(df, related_tickers="NVDA"):
    """

    :param df:
    :param related_tickers:
    :return:
    """
    # add nvidia mentioned in content and title columns
    add_nvidia_topic_title_content(df)

    add_improved_NVDA_ticker_column(df, related_tickers)
    return df[df["ticker_NVDA_improved"] == True]

