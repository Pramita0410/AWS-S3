import boto3
import os
import io
import pandas as pd

s3 = boto3.client("s3")

job = s3.get_object(Bucket = "food-delivery-system", Key= "job")
bytes = job["Body"].read()
job_data = pd.read_csv(io.BytesIO(bytes))
print(job_data.columns)

person = s3.get_object(Bucket = "food-delivery-system", Key= "person")
bytes = person["Body"].read()
person_data = pd.read_csv(io.BytesIO(bytes))
print(person_data.columns)


savings = s3.get_object(Bucket = "food-delivery-system", Key= "saving")
bytes = savings["Body"].read()
savings_data = pd.read_csv(io.BytesIO(bytes))
print(savings_data.columns)


taxes = s3.get_object(Bucket = "food-delivery-system", Key= "taxe")
bytes = taxes["Body"].read()
taxes_data = pd.read_csv(io.BytesIO(bytes))
print(taxes_data.columns)

# merging dfs

job_person = pd.merge(job_data, person_data, how="right", left_on="Job_id", right_on="job_id").drop(columns=["job_id", 'Unnamed: 0']) 
# print(job_person.columns)

job_person_savings = pd.merge(job_person, savings_data, how="left",on="account_no" )
# print(job_person_savings.columns)

job_person_savings_tax = pd.merge(job_person_savings, taxes_data, how="left", left_on = "Job_Location", right_on="location").drop(columns=["location"])
json_data= job_person_savings_tax.to_json(orient="records")

