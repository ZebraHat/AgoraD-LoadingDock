__author__ = 'chase'


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import urllib2

import datetime
import json


@api_view(['POST'])
def transfer_start(request):
    """
    Starts a transfer to another AgoraD loading dock

    :param token: API token for this loading dock
    :param tableNames: A list of table names to transfer
    :param destination: The IP or host to transfer to
    :param session_id: ID of session from the MarketPlace
    """

    ## do a quick check to make sure it is actually a GET request
    if request.method != 'POST':
        return Response(status=status.HTTP_400_BAD_REQUEST)

    params = request.QUERY_PARAMS.dict()

    #TODO verify token
    #TODO request table names

    url = params['destination'] + '/highway/intercept/schema/'

    #TODO fill out the data parameter
    data = None

    response = urllib2.urlopen(params['destination'], data)

    #TODO check response, if not 200, warn the marketplace