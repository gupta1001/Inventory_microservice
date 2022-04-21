from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

app = FastAPI()

redis = get_redis_connection(
    host="redis-11018.c9.us-east-1-4.ec2.cloud.redislabs.com",
    port = 11018,
    password = "r7e0O71D8foGqHMskzmlA879VGcDjXSh",
    decode_responses = True
)

app.add_middleware(
    CORSMiddleware, 
    allow_origins = ['http://localhost:3000'],
    allow_methods = ['*'],
    allow_headers = ['*']
)

class Product(HashModel):
    name: str
    price: float
    quantity: int
    
    class Meta():
        database = redis

@app.get('/products')
def all():
    return [format(pk) for pk in Product.all_pks()] # return the primary key of the products but not the product itself


def format(pk: str):
    #This will query product from database using Primary Key
    product = Product.get(pk)

    return {
        'id' : product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity
    }

# adding a new product
@app.post('/products')
def create(product: Product):
    return product.save()

# getting a specific product
@app.get('/products/{pk}')
def get(pk: str):
    return Product.get(pk)

# deleting the specified product
@app.delete('/products/{pk}')
def delete(pk: str):
    return Product.delete(pk)
