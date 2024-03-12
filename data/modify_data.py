import json
import random

with open("old_products.json") as f:
    products = json.load(f)
    f.close()

    
for p in products:
    p["stock"] = random.randrange(0,100)
    

with open("products.json", "w") as f:
    prods = json.dumps(products)
    f.write(prods)
    f.close()
