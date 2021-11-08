import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os

from pyspark.sql import SparkSession
import sys
# Create my_spark

#my_spark = SparkSession.builder.getOrCreate()
my_spark = SparkSession \
    .builder \
    .appName("ALSRecommendation") \
    .master("local[{}]".format(int(sys.argv[1])) )\
    .getOrCreate();
# Print my_spark
airport_df = my_spark.read.csv("airports.csv",header=True)

#question1
# Group by country
group_country = airport_df.groupBy("COUNTRY")

# Number of airports for each country

out1=group_country.count()
#out1.toPandas().to_csv(sys.argv[2],index=False)

#question2
#out1.groupBy().max("count").show()
out2=out1.orderBy(out1['count'].desc()).limit(1)
out2.toPandas().to_csv(sys.argv[2],index=False)

