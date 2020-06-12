import retrieve_data
import predict
import baselines


trainData, testData = retrieve_data.retrieve_data(8000)
baselines.baseline_performance(trainData, testData)
predict.model(trainData, testData)


