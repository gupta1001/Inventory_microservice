from main import redis, Product
import time

key = 'order_completed'
group = 'inventory-group'

# let's create a redis consumer group with above key and name
try:
    redis.xgroup_create(key, group)
# throw exeption when the group already exists 
except:
    print('Group already exits!')

while True:
    try:
        # consume the group created
        results = redis.xreadgroup(group, key, {key:'>'}, None)
        if results != []:
            # [['order_completed', 
            #   [('1650224927729-0', {'pk': '01G0WH3Z7X9D2ZHG2VMENPWAQY', 'product_id': '01G0W84QV7HYJFP057H1MJA1DN', 'price': '20.0',  'fee': '4.0', 'total': '24.0', 'quantity': '2', 'status': 'completed'} --> [1] last) --> [0]second ]] --> [1] first
            #  ]
            # we want only the json object from above result
            for result in results:
                obj = result[1][0][1]
                try:
                    product = Product.get(obj['product_id'])
                    print(product)
                    product.quantity = product.quantity - int(obj['quantity'])
                    product.save()
                except:
                    # Here is the solution for the case if the product gets deleted before completion
                    # and customer gets charged incrorrectly
                    # Refund the money
                    redis.xadd('refund_order', obj, '*')
    except Exception as e:
        print(str(e))
    time.sleep(1)