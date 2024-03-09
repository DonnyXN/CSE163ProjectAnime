import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import warnings


def popularity_vs_rating(data):
    """
    Plots a scatter plot of the rating score given for each anime
    review vs the popularity of that anime.
    """
    data = data[["anime_uid", "gender", "title", "popularity", "score_x"]]
    warnings.filterwarnings("ignore")
    sns.relplot(data=data, x="popularity", y="score_x", hue="gender")
    plt.title("Popularity vs. Rating Score by Gender")
    plt.xlabel("Popularity")
    plt.ylabel("Score Given")
    plt.savefig("popularity_vs_rating_by_gender.png", bbox_inches="tight")


def episodes_vs_gender(data):
    """
    Plots a violin graph for the amount of reviews given by each
    gender for each anime vs the episode length of that anime.
    """
    data = data[["anime_uid", "gender", "title", "episodes"]]
    # Filter out outliers
    data = data[(data["episodes"] <= 40)]
    warnings.filterwarnings("ignore")
    sns.catplot(data=data, kind="violin", x="gender",
                y="episodes", hue="gender")
    plt.title("Number of Reviews vs Episode Count by Gender")
    plt.xlabel("Gender")
    plt.ylabel("Number of Episodes")
    plt.savefig("episodes_vs_gender.png", bbox_inches="tight")


def avg_score_vs_rating(data):
    """
    Plots a line graph of the rating score given for each anime review
    vs the overall average score of that anime.
    """
    data = data[["anime_uid", "gender", "title", "score_y", "score_x"]]
    warnings.filterwarnings("ignore")
    sns.relplot(data=data, kind="line", x="score_y", y="score_x", hue="gender")
    plt.title("Rating Given vs Average Rating by Gender")
    plt.xlabel("Overall Rating")
    plt.ylabel("Rating Given")

    plt.savefig("avg_score_vs_rating_by_gender.png", bbox_inches="tight")


def ranking_vs_gender(data):
    """
    Plots a violin graph for the amount of reviews given by each
    gender for each anime vs the anime's ranking.
    """
    data = data[["anime_uid", "gender", "title", "ranked"]]
    warnings.filterwarnings("ignore")
    sns.catplot(data=data, kind="violin", x="gender", y="ranked", hue="gender")
    plt.title("Anime Ranking vs Number of Reviews by Gender")
    plt.xlabel("Gender")
    plt.ylabel("Ranking")
    plt.savefig("ranking_vs_gender.png", bbox_inches="tight")


def main():
    # Reads and merges files
    profile_df = pd.read_csv("/home/profile_sample.csv")
    review_df = pd.read_csv("/home/review_sample.csv")
    anime_df = pd.read_csv("/home/anime_list_sample.csv",
                           encoding="unicode_escape")
    merged_temp = review_df.merge(anime_df, left_on="anime_uid",
                                  right_on="uid")
    merged_df = merged_temp.merge(profile_df, left_on="profile",
                                  right_on="profile")
    # Graphs
    popularity_vs_rating(merged_df)
    episodes_vs_gender(merged_df)
    avg_score_vs_rating(merged_df)
    ranking_vs_gender(merged_df)


if __name__ == "__main__":
    main()
