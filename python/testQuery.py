import os
import json
import time
import weaviate
from tqdm import tqdm
import weaviate.classes.config as cf
from weaviate.classes.query import MetadataQuery

client = weaviate.connect_to_local(host="172.19.0.4", port=8080)

client.collections.delete_all()
client.collections.create(
    name = 'whisky',
    properties = [
        cf.Property(name="uuid", data_type=cf.DataType.TEXT, skip_vectorization=True),
        cf.Property(name="Name", data_type=cf.DataType.TEXT, skip_vectorization=True),
        cf.Property(name="Price", data_type=cf.DataType.TEXT, skip_vectorization=True),
        cf.Property(name="Category", data_type=cf.DataType.TEXT, skip_vectorization=True),
        cf.Property(name="Review", data_type=cf.DataType.TEXT),
        ],
    
    vectorizer_config = [
        cf.Configure.NamedVectors.text2vec_transformers(
            name='review_vector', source_properties=['review']
        ),
        cf.Configure.NamedVectors.text2vec_transformers(
            name='category_vector', source_properties=['category']
        ),
        cf.Configure.NamedVectors.text2vec_transformers(
            name='name_vector', source_properties=['name']
        ),            
    ],
    inverted_index_config=cf.Configure.inverted_index(  # Optional
        bm25_b=0.7,
        bm25_k1=1.25,
        index_null_state=True,
        index_property_length=True,
        index_timestamps=True
    )
)

whiskyColl = client.collections.get("whisky")

with open('./dataList.json', 'r') as f:
    json_data = json.load(f)
    
whiskyItemJson = json.dumps(json_data)
whiskyItem = json.loads(whiskyItemJson)


with whiskyColl.batch.fixed_size(5) as batch:
    for whisky in tqdm(whiskyItem):  
        if whiskyColl.batch.failed_objects:
            for obj in whiskyColl.batch.failed_objects:
                print(obj)    
        propertiesObject = {
            "uuid": whisky["uuid"],
            "Name": whisky["Name"],
            "Price": whisky["Price"],
            "Category": whisky["Category"],
            "Review": whisky["Review"]
        }
        # print(propertiesObject)
        batch.add_object(
                    uuid = whisky["uuid"],
                    properties=propertiesObject)
    time.sleep(5)

    response_review = whiskyColl.query.near_text(
    query="피트 향이 나는 일본의 싱글몰트 위스키",
    target_vector="review_vector",
    return_metadata=MetadataQuery(score=True, explain_score=True),
    limit=3
)

res = []
for obj in response_review.objects:
    res.append(obj.properties["name"])
    print(obj.properties["name"])
    print(obj.properties["review"])
    print(obj.properties["category"])
    print("======================")