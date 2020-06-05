import retrieve_data
import predict
import baselines


trainData, testData = retrieve_data.retrieve_data(3000)
baselines.baseline_performance(trainData, testData)
model = predict.train(trainData)
predict.predict(testData, model, targets=list(testData["type"]))


