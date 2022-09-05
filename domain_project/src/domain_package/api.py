from urllib import request
import flask
from domain_package import *

#@flask.route.gubbins
def allocate_endpoint(request):

    session = create_local_session()
    #extract order line from request
    line = OrderLine(request.json['sku'], 
                     request.json['qty'],
                     request.json['orderid'])

    #load all batches from db
    batches = session.query(Batch).all()

    #call our domain service - allocation
    allocate(line, batches)

    #save the allocation back to db - somehow
    session.commit() 
    return 201