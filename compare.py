import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set()


def _genre_encoder(dataframe):
    """
    One-hot encodes the genres column and merges it to the dataframe,
    returns the newly merged dataframe
    """
    filtered_df = dataframe[['genre', 'score']]
    df_melt = filtered_df.assign(genre=filtered_df.genre.str[1:-1])
    df_melt = df_melt.assign(genre=df_melt.genre.str.split(","))
    filtered_df = df_melt[['genre', 'score']]
    genre_df = df_melt['genre'].str.join('|').str.get_dummies()
    genre_df.columns = genre_df.columns.str.replace(' ', '')
    genre_df.columns = genre_df.columns.str.replace('\'', '')
    genre_result = filtered_df.merge(genre_df, right_index=True,
                                     left_index=True)
    genre_result = genre_result.loc[:, ~genre_result.columns.duplicated()]
    return(genre_result)


def _studio_encoder(dataframe):
    """
    One-hot encodes the studio column and merges it to the dataframe,
    returns the newly merged dataframe
    """
    filtered_df = dataframe[['studio', 'score']]
    df_melt = filtered_df.assign(studio=filtered_df.studio.str[1:-1])
    df_melt = df_melt.assign(studio=df_melt.studio.str.split(","))
    studio_df = df_melt['studio'].str.join('|').str.get_dummies()
    studio_df.columns = studio_df.columns.str.replace(' ', '')
    studio_df.columns = studio_df.columns.str.replace('\'', '')
    studio_result = filtered_df.merge(studio_df, right_index=True,
                                      left_index=True)
    studio_result = studio_result.loc[:, ~studio_result.columns.duplicated()]
    return(studio_result)


def _producer_encoder(dataframe):
    """
    One-hot encodes the producers column and merges it to the dataframe,
    returns the newly merged dataframe
    """
    filtered_df = dataframe[['producers', 'score']]
    df_melt = filtered_df.assign(producers=filtered_df.producers.str[1:-1])
    df_melt = df_melt.assign(producers=df_melt.producers.str.split(","))
    producers_df = df_melt['producers'].str.join('|').str.get_dummies()
    producers_df.columns = producers_df.columns.str.replace(' ', '')
    producers_df.columns = producers_df.columns.str.replace('\'', '')
    prodcuers_result = filtered_df.merge(producers_df, right_index=True,
                                         left_index=True)
    prodcuers_result = prodcuers_result.loc[:, ~prodcuers_result.
                                            columns.duplicated()]
    return(prodcuers_result)


def _avg_score(dataframe, feature):
    """
    Returns the average score for a given feature
    """
    mask = (dataframe[feature] == 1)
    avg_score = dataframe[mask]['score'].mean()
    avg_score = round(avg_score, 2)
    return(avg_score)


def plot_genre_ratings(dataframe):
    """
    Plots a bar chart of all the genres and their average rating
    and saves it to genreVsRating.png
    """
    data = []
    genres = dataframe.iloc[:, 2:]
    for genre in genres.columns:
        data.append([genre, (_avg_score(dataframe, genre))])
        df = pd.DataFrame(data, columns=['Genre', 'Avg Rating'])

    sns.catplot(data=df, x="Genre", y="Avg Rating", color='b',
                kind='bar', height=6, aspect=4)
    plt.xticks(rotation=-45)
    plt.title('Average rating for each genre of anime')
    plt.xlabel('Genre')
    plt.ylabel('Average Rating')
    plt.ylim(0, 10)
    plt.savefig('/home/genresVsRating.png', bbox_inches='tight')


def plot_studio_ratings(dataframe):
    """
    Plots a bar chart of all the studios and their average rating
    and saves it to studioVsRating.png
    """
    data = []
    studios = dataframe.iloc[:, 2:]
    for studio in studios.columns:
        data.append([studio, (_avg_score(dataframe, studio))])
        df = pd.DataFrame(data, columns=['Studio', 'Avg Rating'])

    df = df.sort_values('Avg Rating', ascending=False).head(5)

    sns.catplot(data=df, x="Studio", y="Avg Rating", color='b',
                kind='bar', height=10, aspect=3)
    plt.xticks(rotation=-60)
    plt.title('Average rating for each anime studio')
    plt.xlabel('Studio')
    plt.ylabel('Average Rating')
    plt.ylim(0, 10)
    plt.savefig('/home/studioVsRating.png', bbox_inches='tight')


def plot_producers_ratings(dataframe):
    """
    Plots a scatter plot of all the producers and their average rating
    and saves it to producerVsRating.png
    """
    data = []
    prodcuers = dataframe.iloc[:, 2:]
    for producer in prodcuers.columns:
        data.append([producer, (_avg_score(dataframe, producer))])
        df = pd.DataFrame(data, columns=['Producer', 'Avg Rating'])

    fig, ax = plt.subplots()
    ax = sns.scatterplot(data=df, x="Producer", y="Avg Rating", ax=ax)
    ax.set(xticklabels=[])
    plt.title('Average rating for accross anime producers')
    plt.ylabel('Average Rating')
    plt.ylim(0, 10)
    plt.savefig('/home/producerVsRating.png', bbox_inches='tight')


def plot_num_eps_ratings(dataframe):
    """
    Plots a scatter plot of number of episodes Vs the rating
    and saves it to numEpsVsRating.png
    """
    fig, ax = plt.subplots()
    sns.scatterplot(data=dataframe, x="episodes", y="score", hue='type', ax=ax)
    plt.title('Ratings per number of episodes')
    plt.xlabel('Number of episodes')
    plt.ylabel('Rating given')
    plt.ylim(0, 10)
    plt.savefig('/home/numEpsVsRating.png', bbox_inches='tight')


def plot_source_rating(dataframe):
    """
    Plots a bar chart of the average rating for each anime source
    and saves it to sourcesVsRating.png
    """
    masked_df = dataframe[['source', 'score']]
    result = masked_df.groupby('source')['score'].mean()

    fig, ax = plt.subplots()
    sns.barplot(x=result.index, y=result.values, color='b', ax=ax)
    plt.xticks(rotation=-45)
    plt.title('Average rating for each anime source')
    plt.xlabel('Source')
    plt.ylabel('Average Rating')
    plt.ylim(0, 10)
    plt.savefig('/home/sourcesVsRating.png', bbox_inches='tight')


def plot_type_rating(dataframe):
    """
    Plots a bar chart of the average rating for each type of anime
    and saves it to typeVsRating.png
    """
    masked_df = dataframe[['type', 'score']]
    result = masked_df.groupby('type')['score'].mean()

    fig, ax = plt.subplots()
    sns.barplot(x=result.index, y=result.values, color='b', ax=ax)
    plt.xticks(rotation=-45)
    plt.title('Average rating for each type of anime')
    plt.xlabel('Type of Anime')
    plt.ylabel('Average Rating')
    plt.ylim(0, 10)
    plt.savefig('/home/typeVsRating.png', bbox_inches='tight')


def boxplot_producers(dataframe):
    """
    Plots a box plot of the average rating across each anime producer
    and saves it to boxProdVsRating.png
    """
    data = []
    prodcuers = dataframe.iloc[:, 2:]
    for producer in prodcuers.columns:
        data.append([producer, (_avg_score(dataframe, producer))])
        df = pd.DataFrame(data, columns=['Producer', 'Avg Rating'])

    fig, ax = plt.subplots()
    sns.boxplot(y='Avg Rating', data=df, ax=ax)
    plt.title('Average score across anime producers')
    plt.ylabel('Average score')
    plt.ylim(0, 10)
    plt.savefig('/home/boxProdVsRating.png', bbox_inches='tight')


def boxplot_studio(dataframe):
    """
    Plots a box plot of the average rating across each anime studios
    and saves it to boxStudVsRating.png
    """
    data = []
    studios = dataframe.iloc[:, 2:]
    for studio in studios.columns:
        data.append([studio, (_avg_score(dataframe, studio))])
        df = pd.DataFrame(data, columns=['Studio', 'Avg Rating'])

    fig, ax = plt.subplots()
    sns.boxplot(y='Avg Rating', data=df, ax=ax)
    plt.title('Average score across anime studios')
    plt.ylabel('Average score')
    plt.ylim(0, 10)
    plt.savefig('/home/boxStudVsRating.png', bbox_inches='tight')


def main():
    anime1 = pd.read_csv('/home/anime1_sample.csv')
    anime1.columns = anime1.columns.str.replace(' ', '')
    genre_encoded_df = _genre_encoder(anime1)
    studio_encoded_df = _studio_encoder(anime1)
    producers_encoded_df = _producer_encoder(anime1)
    boxplot_producers(producers_encoded_df)
    boxplot_studio(studio_encoded_df)
    plot_type_rating(anime1)
    plot_source_rating(anime1)
    plot_num_eps_ratings(anime1)
    plot_producers_ratings(producers_encoded_df)
    plot_genre_ratings(genre_encoded_df)
    plot_studio_ratings(studio_encoded_df)


if __name__ == "__main__":
    main()
