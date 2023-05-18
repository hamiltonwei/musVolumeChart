# This script simply takes the last.fm CSV data, and transform it into the format we need:
# Date, Scruble #, New Scruble #
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


def aggregate_scrubbles(df: pd.DataFrame):
    '''
    aggregate the number of old scrubbles and new scrubbles by date
    '''
    #TODO
    raise NotImplementedError


if __name__ == "__main__":
    # Allow this script to take a CSV file as argument. 
    print(sys.argv)
    filename = sys.argv[1]

    #TODO: Check if the CSV file is of the correct format. If not, give an error message and exit.

    # Load the CSV file with Panda
    df = pd.read_csv(filename)
    df["Time"] = pd.to_datetime(df.Time, format="mixed")

    # add a column that indicates if a scrubble is new or not
    find_new_scrubbles(df)

    # 4. Run a SQL query or something that aggregate # of scrubbles and new scrubbles, sorted by date. Fill 0 if a date has no scrubbles
    df_agg = aggregate_scrubbles(df)

    # 5. Export the result of the above query to a CSV. Done.
    df_agg.to_csv('processed_data/With_New_Scrubbles.csv', index=False)