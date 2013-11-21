__author__ = 'chase'


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import urllib2

from models import Block, Session


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

    session = Session.objects.create(
        session_id=params['session_id']
    )

    #TODO verify token
    #TODO request table names

    url = params['destination'] + '/highway/intercept/schema/'

    #TODO fill out the data parameter
    data = None

    response = urllib2.urlopen(url, data)

    #TODO check response, if not 200, warn the marketplace

    block_count = Block.objects.all().count()
    block_url = params['destination'] + '/highway/intercept/block/'

    for x in range(block_count):
        block = Block.objects.all()[x]
        session.current_block = block
        session.save()

        data = None
        #TODO fill out data param with JSON
        response = urllib2.urlopen(block_url, data)
        if response.get_code() != status.HTTP_200_OK:
            #TODO some sort of checking here
            pass



@api_view(['POST'])
def transfer_schema(request):
    #TODO lookup session
    #TODO grab schema in json format
    #TODO return to sender
    pass


@api_view(['POST'])
def transfer_block(request):
    """
    Requests a block

    :param block_id: ID of block being requested
    """


    #TODO look up session
    #TODO grab block in json format (need someone to calculate blocks)
    #TODO return to sender
    pass


@api_view(['POST'])
def intercept_schema(request):

    params = request.QUERY_PARAMS.dict()
    schema = params['schema']

    #TODO run syncdb to create the new database (need auto naming convention)
    #TODO input schema into loading dock
    #TODO re-request on failure to create
    pass


@api_view(['POST'])
def intercept_block(request):
    #TODO grab block and shove into database @Jarus
    #TODO upon failure, check if need for re-request
    pass