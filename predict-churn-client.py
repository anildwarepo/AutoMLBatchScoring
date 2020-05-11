#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
# 
#    http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
 
import requests
import json
import pandas
import sys

httpheaders = {'Content-Type': 'application/json'}


# Auto ML Deployed scoring endpoint using Azure Container Instances
scoring_uri = "http://<containerinstanceendpoint>.westus2.azurecontainer.io/score"


print(httpheaders)

# Load Churn data from CSV.  
df = pandas.read_csv("WA_Fn-UseC_-Telco-Customer-Churn.csv",header=0, index_col="customerID")

del df["Churn"]
testdata = []
churnpredictiondata = []
rowcount = 0
colcount = 0
for row in df.itertuples():
    for col in row:
        if(col == "Yes"):
            col = 1
        if(col == "No"):
            col = 0 
        colcount += 1
        if(colcount == 20):
            testdata.append(float(col))
            colcount = 0
        else:
            testdata.append(col)
        

    test_sample = json.dumps({'data': [
        testdata
    ]})
    response = requests.post(
        scoring_uri, data=test_sample, headers=httpheaders)
    try:
        churnpredictionresult = [row[0], json.loads(response.json())["result"][0]]
    except:
        churnpredictionresult = [row[0], "error occurred"]
        print("Unexpected error:", sys.exc_info())
    churnpredictiondata.append(churnpredictionresult)

    print(f'count:{rowcount}---{row[0]} --> churn prediction={churnpredictionresult[1]}')
    testdata = []
    rowcount += 1
    
newdf = pandas.DataFrame(churnpredictiondata, columns = ['customerId', 'churnPrediction'])
newdf.to_csv("churnprediction.csv")
