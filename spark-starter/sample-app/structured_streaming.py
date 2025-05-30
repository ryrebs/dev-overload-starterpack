## Spark structured streaming
## Run this command on other terminal: `nc -lk 9999` then type something.
from pyspark.sql.functions import explode, split
from pyspark.sql import SparkSession, Row

spark = SparkSession.builder.master("local[*]").appName("StructuredNetworkWordCount").getOrCreate()
lines = spark \
    .readStream \
    .format("socket") \
    .option("host", "localhost") \
    .option("port", 9999) \
    .load()


## For every line that you typed it will split by single space: split(lines.value, " ").
## Create a new row: explode(split(lines.value, " ")).alias("word") and name column as word.
words = lines.select(explode(split(lines.value, " ")).alias("word"))

## Group and count each row
wordCounts = words.groupBy("word").count()

## Start running the query that prints the running counts to the console
query = wordCounts \
    .writeStream \
    .outputMode("complete") \
    .format("console") \
    .start()

query.awaitTermination()

## nc -lk 9999's 
## Input: 
## cat dog
## cat bird
## Sample outputs:
## Batch 1
# +---------+-----+
# |     word|count|
# +---------+-----+
# |      cat|    1|
# |      dog|    1|
# +---------+-----+
## Batch 2
# +---------+-----+
# |     word|count|
# +---------+-----+
# |      cat|    2|
# |      dog|    1|
# |     bird|    1|
# +---------+-----+