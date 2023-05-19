# This script simply takes the last.fm CSV data, and transform it into the format we need:
# Date, Total Scrubble, Old Scrubble, New Scrubble
# It will output a new CSV file with the correct format

import pandas as pd
from datetime import date
import sys


def find_new_scrubbles(df: pd.DataFrame):
    '''
    add a column of this data frame indicating whether each scrubble is new or not
    a scrubble of the song is "new" if the same song has been played less than 3 times prior
    '''
    # we could use a dp algorithm, iterate through each row and add the count to a hashtable
    # however it seems pandas already have those algorithm pre-made for you (cumCount), so I'm just gonna use that.
    df["ScrubblesPrior"] = df.groupby(["Artist", "Track"]).cumcount(ascending=False)
    df.loc[df['ScrubblesPrior'] > 2, "IsNewScrubble"] = 'False'
    df.loc[df['ScrubblesPrior'] <= 2, "IsNewScrubble"] = 'True'


def my_agg(x):
    '''
    This is used in df.gropby.apply to apply multiple aggregation functions to a group.
    '''
    names = {
        "Total_Count": x["Date"].count(),
        "Old_Count": x[x["IsNewScrubble"] == "False"]["Date"].count(),
        "New_Count": x[x["IsNewScrubble"] == "True"]["Date"].count()
    }
    return pd.Series(names)


def fill_missing_dates_with_zero(df_agg: pd.DataFrame):
    # get the min and max date range of the dataframe "df_agg". In this case the date is the index, so we call "df_agg.index" to get the date
    date_range = pd.date_range(df_agg.index.min(), df_agg.index.max(), freq="D")
    # swap the index of df_agg. So the index has the correct range. Note we MUST make a copy of the dataframe when reindexing. fill all the NaN values with 0.
    df_agg = df_agg.reindex(date_range).fillna(0)
    return df_agg


def aggregate_scrubbles(df: pd.DataFrame):
    '''
    aggregate the number of old scrubbles and new scrubbles by date
    '''
    df_agg = df.groupby("Date").apply(my_agg)
    df_agg = fill_missing_dates_with_zero(df_agg)
    # reset_index also returns a new df by default. So we want this to be in-place instead
    df_agg.reset_index(inplace=True)
    #rename the date column (it's called "index" by default)
    date_col_name = df_agg.columns[0]
    df_agg.rename(columns={date_col_name:"Date"}, inplace=True)
    return df_agg


def load_csv(filename):
    df = pd.read_csv(filename)
    df["Time"] = pd.to_datetime(df["Time"], format="mixed")
    df["Date"] = df['Time'].dt.date
    return df


if __name__ == "__main__":
    # Allow this script to take a CSV file as argument. 
    filename = sys.argv[1]

    #TODO: Check if the CSV file is of the correct format. If not, give an error message and exit.

    #TODO: If it's simply missing the column names, add them.

    df = load_csv(filename)
    find_new_scrubbles(df)
    df_agg = aggregate_scrubbles(df)
    print(df_agg)

    df_agg.to_csv('processed_data/With_New_Scrubbles.csv', index=False)