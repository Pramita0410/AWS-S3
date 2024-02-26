import boto3
bucket_name = "prami-boto-tutorial-bucket1"
s3 = boto3.client("s3")

#listing all the buckets
buckets_resp = s3.list_buckets( )
for buckets in buckets_resp["Buckets"]:
    print (buckets)



#listing the objects in the bucket
list_object  = s3.list_objects_v2(Bucket = bucket_name) 
for object in list_object["Contents"]:
    print(object)




#uploading a file using boto3 and not by using ui
with open('./cover_new_upload.jpg', "rb") as f:
    s3.upload_fileobj(f, bucket_name, "new_cover_upload")



#  we can also give extra arguments like set the ACL to public
with open('./cover_new_upload.jpg', "rb") as f:
    s3.upload_fileobj(f, bucket_name, "new_cover_upload_with_public_read", ExtraArgs =  {'ACL': "public-read"} )



#downloading a file
s3.download_file(bucket_name, "cover.jpg", "downloaded_cover_from_s3.jpg")

#download with binary mode
#why wb (write-binary mode) so that in future we can do some image manipulation for  frontend
#note : here the method is download_fileobj() and not download_file() because we passed the file 
with open("download_binary_cover.jpg", "wb") as f:
   s3.download_fileobj(bucket_name, "cover.jpg", f)
              #write here code to send to frontend 



#Creating a presigned url to grant access to an unauthorized user
#to get the url that would be accessible by the frontend/ user for some time we'll have to use a method
# method: generate_presigned_url()

url = s3.generate_presigned_url("get_object", Params = {"Bucket": bucket_name, 
    "Key": "cover.jpg"  }, ExpiresIn= 30)
print(url)



#create a new bucket
#method used : create_bucket()
bucket_location= s3.create_bucket( Bucket = "create-boto3-bucket")
print(bucket_location)

 #public bucket
bucket_location1= s3.create_bucket( ACL= "public-read", Bucket = "create-boto3-bucket-public")
print(bucket_location1)


#Copying the objects from one bucket to another
# source bucket is bucket_name and destination bucket is create-boto3-bucket
#method : copy_object(), arguments: bucket, copysource, key, [acl (optional)]

s3.copy_object(
    Bucket = "create-boto3-bucket",
    CopySource= f"/{bucket_name}/cover.jpg",
    Key= "copied_cover.jpg"
)

#to get the details about the object
#method : get_object(), arguments : bucket, key

response = s3.get_object(Bucket = bucket_name, Key= "cover.jpg")
print(response)
