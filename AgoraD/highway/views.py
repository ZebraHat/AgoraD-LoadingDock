__author__ = 'chase'


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import urllib2


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
    #TODO calculate blocks


@api_view(['POST'])
def transfer_schema(request):
    #TODO lookup session
    #TODO grab schema in json format
    #TODO return to sender
    pass


@api_view(['POST'])
def transfer_block(request):
    #TODO look up session
    #TODO grab block in json format (need someone to calculate blocks)
    #TODO return to sender
    pass


@api_view(['POST'])
def intercept_schema(request):
    #TODO run syncdb to create the new database (need auto naming convention)
    #TODO input schema into loading dock
    #TODO re-request on failure to create
    pass


@api_view(['POST'])
def intercept_block(request):
    #TODO grab block and shove into database @Jarus
    #TODO upon failure, check if need for re-request
    pass