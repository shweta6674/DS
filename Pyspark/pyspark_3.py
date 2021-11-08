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

#Question3

out3=airport_df.filter(airport_df.LATITUDE >=10).filter(airport_df.LATITUDE <=90).filter(airport_df.LONGITUDE <=-10).filter(airport_df.LONGITUDE >=-90)
selected1 = out3.select("NAME")
selected1.toPandas().to_csv(sys.argv[2],index=False)
