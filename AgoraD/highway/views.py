__author__ = 'chase'


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import urllib2

from models import Block, Session
from loading_dock.models import toJSON, fromJSON
from modules import blocks
import json


@api_view(['POST'])
def transfer_start(request):
    """
    Starts a transfer to another AgoraD loading dock

    :param token: API token for this loading dock
    :param table_names: A list of table names to transfer
    :param destination: The IP or host to transfer to
    :param session_id: ID of session from the MarketPlace
    :param database_name: Name of database to transfer
    """

    ## do a quick check to make sure it is actually a POST request
    if request.method != 'POST':
        return Response(status=status.HTTP_400_BAD_REQUEST)

    params = request.QUERY_PARAMS.dict()

    #### CALCULATE BLOCKS ####

    error = blocks.create_blocks(params['database_name'])
    if error:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    session = Session.objects.create(
        session_id=params['session_id']
    )

    #TODO verify token
    #TODO request table names

    #### SEND THE SCHEMA ####

    url = params['destination'] + '/highway/intercept/schema/'
    data = toJSON(params['database_name'], params['table_names'])
    response = urllib2.urlopen(url, data)
    if response.get_code() != status.HTTP_200_OK:
        return Response(status=response.get_code())

    #### START BLOCK TRANSFER ####

    block_count = Block.objects.all().count()
    block_url = params['destination'] + '/highway/intercept/block/'

    for x in range(block_count):
        block = Block.objects.all()[x]
        session.current_block = block
        session.save()

        data = dict()
        data['block_id'] = block.pk
        data['session_id'] = params['session_id']
        data['block_data'] = json.loads(blocks.json_from_block(block))

        #TODO fill out data param with JSON
        response = urllib2.urlopen(block_url, json.dumps(data))
        if response.get_code() != status.HTTP_200_OK:
            return Response(status=response.get_code())



@api_view(['POST'])
def transfer_schema(request):
    """
    Use this to request only a schema. Must have an active session id.

    :param session_id: ID of session from marketplace
    :param database_name: Name of database to get schema from
    :param table_names: An array of table names to pull schema for
    """
    #TODO lookup session

    params = request.QUERY_PARAMS.dict()

    try:
        data = toJSON(params['database_name'], params['table_names'])
        return Response(data=data, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def transfer_block(request):
    """
    Requests a block

    :param session_id: ID associated with this transfer
    :param block_id: ID of block being requested
    """

    params = request.QUERY_PARAMS.dict()
    #TODO look up session

    try:
        block = Block.objects.get(pk=params['block_id'])
        block_data = json.loads(blocks.json_from_block(block))

        return Response(data=block_data, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def intercept_schema(request):
    """
    Intercepts a schema and shoves it into the dB

    :param schema: JSON schema from the database
    """
    params = request.QUERY_PARAMS.dict()
    error = fromJSON(params['schema'])

    if error:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def intercept_block(request):
    """
    Intercepts a block and shoves it into the db

    :param data: data JSON consisting of block_id, session_id, and block_data, where block data is the data dictionary
    to shove into the database
    """
    params = request.QUERY_PARAMS.dict()['data']

    block_id = params['block_id']
    session_id = params['session_id']
    block_data = params['block_data']

    #TODO shove this into the db

    return Response(status=status.HTTP_200_OK)