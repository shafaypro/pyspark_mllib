from pyspark import SQLContext, SparkContext
from pyspark.ml import Pipeline
from pyspark.ml.feature import VectorIndexer, StringIndexer
from pyspark.ml.classification import GBTClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

sc = SparkContext("local", "samp")
sqlContext = SQLContext(sc)

data = sqlContext.read.format("libsvm").load("D:\Spark\spark-1.6.1-bin-hadoop2.6\data\mllib\sample_libsvm_data.txt")
labelIndexer = StringIndexer(inputCol="label", outputCol="indexedLabel").fit(data)
featureIndexer = VectorIndexer(inputCol="features", outputCol="indexedFeatures", maxCategories=4).fit(data)
(trainingData, testData) = data.randomSplit([0.7, 0.3])
gbt = GBTClassifier(labelCol="indexedLabel", featuresCol="indexedFeatures", maxIter=10)
pipeline = Pipeline(stages=[labelIndexer, featureIndexer, gbt])
model = pipeline.fit(trainingData)
# make predictions
predictions = model.transform(testData)
predictions.select("prediction", "indexedLabel", "features").show(7)

evaluator = MulticlassClassificationEvaluator(labelCol="indexedLabel", predictionCol="prediction",
                                              metricName="precision")
accuracy = evaluator.evaluate(predictions)
print("Test Error= %g " % (1.0 - accuracy))
gbtModel=model.stages[2]

print(gbtModel)

"""OUTPUT - Gradient-boosted tree 
+----------+------------+--------------------+
|prediction|indexedLabel|            features|
+----------+------------+--------------------+
|       1.0|         1.0|(692,[121,122,123...|
|       1.0|         1.0|(692,[123,124,125...|
|       1.0|         1.0|(692,[123,124,125...|
|       1.0|         1.0|(692,[124,125,126...|
|       1.0|         1.0|(692,[126,127,128...|
|       1.0|         1.0|(692,[127,128,129...|
|       1.0|         1.0|(692,[150,151,152...|
+----------+------------+--------------------+
Test Error= 0
GBTClassificationModel (uid=GBTClassifier_48d294503b745ab57dd9) with 10 trees
"""
