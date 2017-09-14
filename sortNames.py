import pandas as pd

import pandas as pd

csvdata = pd.read_csv(r'thing.csv', skipinitialspace=True,delimiter=",")

saved_column = csvdata["Names"]

for row in saved_column:
    player = row[5:]
    if str(player[0]).islower():
        player = row[4:]

    print str(player)

