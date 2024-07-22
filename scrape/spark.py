from pyspark.sql import SparkSession
from pyspark.sql.functions import split, explode, concat, lit, regexp_replace
from font_imgs.font_imgs import fetch_fonts, get_urls, save_img_from_url

spark = SparkSession.builder \
    .appName("Imgs") \
    .getOrCreate()

all_urls = get_urls(fetch_fonts())

urls_rdd = spark.sparkContext.parallelize(all_urls)

results = urls_rdd.map(save_img_from_url).collect()

spark.stop()