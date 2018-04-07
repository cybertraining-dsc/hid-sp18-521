import boto3, smart_open, pprint, pymysql, config

# AWS credentials stored in ~/.aws/credentials, connect using IAM user
# S3 bucket name = hid-sp18-521

# Pulls Medicare patient survey data set in CSV format directly from their web site into an S3 bucket
def medicare_patient_survey_data_csv_to_s3():
    with smart_open.smart_open('s3://hid-sp18-521/PatientSurveyData.csv', 'wb') as fout:
        for line in smart_open.smart_open('https://data.medicare.gov/resource/rmgi-5fhi.csv'):
            fout.write(line + '\n')

# Pulls Medicare patient survey data set in JSON format directly from their web site into an S3 bucket
def medicare_patient_survey_data_json_to_s3():
    with smart_open.smart_open('s3://hid-sp18-521/PatientSurveyData.json', 'wb') as fout:
        for line in smart_open.smart_open('https://data.medicare.gov/resource/rmgi-5fhi.json'):
            fout.write(line + '\n')

# Pulls a list of all of the files that exist in the bucket this application uses
def s3_bucket_allfiles():
    file_names = []

    s3 = boto3.resource('s3')
    bucket = s3.Bucket('hid-sp18-521')

    for object in bucket.objects.all():
        file_names.append(object.key)

    return file_names

# Import S3 File into RDS using AWS Data Pipeline (show how it was created and how it can be called from here)
def data_pipeline_s3_to_rds():
    pipeline = boto3.client('datapipeline', region_name='us-east-1')

    return pipeline.activate_pipeline(pipelineId='df-09855991V8LTRRRNJOQW')

# Return the runtime status of the S3 to RDS data pipelines
def data_pipeline_s3_to_rds_status():
    pipeline = boto3.client('datapipeline', region_name='us-east-1')

    pipeline_status = pipeline.describe_pipelines(pipelineIds=['df-09855991V8LTRRRNJOQW'])

    fields = pipeline_status['pipelineDescriptionList'][0]['fields']

    for field in fields:
        if field['key'] == '@pipelineState':
            return field['stringValue']

# Query the table that contains the data we imported into MySQL on RDS from S3
def query_mysql_data():
    connection = pymysql.connect(host='iu-sp18.cgnrvgmckfic.us-east-1.rds.amazonaws.com',
                                 user=config.mysql_user,
                                 password=config.mysql_user_password,
                                 db='I524',
                                 charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()
    sql = "SELECT * FROM PatientSurveyData"
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

def dynamodb_delete_table():
    dynamodb = boto3.client('dynamodb', region_name='us-east-1')

    return dynamodb.delete_table(TableName='PatientSurveyData')

def dynamodb_create_table():
    dynamodb = boto3.client('dynamodb', region_name='us-east-1')
    table = dynamodb.create_table(TableName='PatientSurveyData',
                                  KeySchema=[{'AttributeName': 'provider_id', 'KeyType': 'HASH'}, ],
                                  AttributeDefinitions=[{'AttributeName': 'provider_id', 'AttributeType': 'S'}],
                                  ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5},
                                  )
    return table