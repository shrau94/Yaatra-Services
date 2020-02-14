from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED
)

from user.models import User
from utils.validator import validate_username
import ratelimit.decorators
from .models import DailyCommute
from .serializers import DailyCommuteSerializer
import logging
import socket
from django.forms.models import model_to_dict


host_name = socket.gethostname()
machine_ip = socket.gethostbyname(host_name)

@ratelimit.decorators.ratelimit(key='ip', rate='200/h')
@csrf_exempt
@api_view(["GET"])
def get_daily_commutes_for_user(request):
    logger = logging.getLogger()
    logger.info("Get-Daily-Commute: Request is being served by Instance: {} at IP: {}".format(host_name, machine_ip))
    """
    This view should return the list of all daily commutes that user have configured.
    return: should return jouney_id (pk) of each list item of DailyCommute Model to be used by daily_commute_user_list view
    to fetch the list of user for a particular daily commute journey.
    """
    data = [
        {
            'jouney_id': 123,
            'title': 'Ghatkopar',
            'Source': 'Dublin 8, Cork Street',
            'Destination': 'Trinity College Dublin, College Green'},
        {
            'jouney_id': 124,
            'title': 'Ghatkopar',
            'Source': 'Dublin 8, Cork Street',
            'Destination': 'Spar, College Green'},
        {
            'jouney_id': 125,
            'title': 'Ghatkopar',
            'Source': 'Dublin 8, Cork Street',
            'Destination': 'Trinity College Dublin, College Green'}, ]

    return Response(data, status=HTTP_200_OK)


@ratelimit.decorators.ratelimit(key='ip', rate='200/h')
@csrf_exempt
@api_view(["GET"])
def get_user_list_for_journey(request):
    logger = logging.getLogger()
    logger.info("User-List-for-Journey: Request is being served by Instance: {} at IP: {}".format(host_name, machine_ip))
    """
        This view should return the list of all daily commuters for the selected jouney_id
        input: journey_id (pk)
        return:  list of users that matched the given journey_id details
        to fetch the list of user for a particular daily commute journey.

        data = [
            {
                'first_name': alex,
                'gender': M
                'age': 20
                'Source': 'Dublin 8, Cork Street',
                'Destination': 'Trinity College Dublin, College Green'},
            {
                'first_name': alex,
                'gender': M
                'age': 20
                'Source': 'Dublin 8, Cork Street',
                'Destination': 'Trinity College Dublin, College Green'},
            {
                'first_name': alex,
                'gender': M
                'age': 20
                'Source': 'Dublin 8, Cork Street',
                'Destination': 'Trinity College Dublin, College Green'},
        ]
        """
    data = []
    return Response(data, status=HTTP_200_OK)

@ratelimit.decorators.ratelimit(key='ip', rate='50/m')
@csrf_exempt
@api_view(["GET"])
def daily_commuter_notification(request):
    logger = logging.getLogger()
    logger.info("Create-Daily-Notification: Request is being served by Instance: {} at IP: {}".format(host_name, machine_ip))
    """
    Input: Notification   """
    data = []
    return Response(data, status=HTTP_200_OK)

@ratelimit.decorators.ratelimit(key='ip', rate='50/m')
@csrf_exempt
@api_view(["POST"])
def create_daily_commute(request):
    """
    Input: Journey Details: longitude, latitude, start_time
    """
    logger = logging.getLogger()
    logger.info("Create-Daily-Commute: Request is being served by Instance: {} at IP: {}".format(host_name, machine_ip))
    if request.method == 'POST':

        if request.data.get('journey_title') is None or request.data.get('destination_lat') is None or \
                request.data.get('start_time') is None or request.data.get('journey_frequency') is None or request.data.get('username') is None:
            return Response({'message': 'Form Data is missing!',
                             'response': 'Error', },
                            status=HTTP_400_BAD_REQUEST)

        username = request.data.get('username')
        if validate_username(username) is None:
            return Response({'message': 'Username does not Exist!',
                             'response': 'Error', },
                            status=HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        user = User.objects.get(username=username)
        data['user'] = user.pk
        serializer = DailyCommuteSerializer(data=data)

        if serializer.is_valid():
            dailyCommuteDetails = serializer.save()
            dailyCommuteData = model_to_dict(dailyCommuteDetails,
                                 fields=['journey_title', 'source_long', 'source_lat', 'destination_lat', 'destination_long', 'start_time', 'journey_frequency'])
            dailyCommuteData['message'] = 'Journey creation Successful!'
            dailyCommuteData['response'] = 'Success'
        else:
            dailyCommuteData = serializer.errors
        return Response(dailyCommuteData, status=HTTP_201_CREATED)

@ratelimit.decorators.ratelimit(key='ip', rate='50/m')
@csrf_exempt
@api_view(["DELETE"])
def delete_daily_commute(request):
    """
    Input: Journey Details: journey_id
    """
    logger = logging.getLogger()
    logger.info("Delete-Daily-Commute: Request is being served by Instance: {} at IP: {}".format(host_name, machine_ip))
    data = []
    return Response(data, status=HTTP_200_OK)


@ratelimit.decorators.ratelimit(key='ip', rate='50/m')
@csrf_exempt
@api_view(["PUT"])
def update_daily_commute(request):
    logger = logging.getLogger()
    logger.info("Update-Daily-Commute: Request is being served by Instance: {} at IP: {}".format(host_name, machine_ip))
    """
    Input: Journey Details: journey_id
    """
    data = []
    return Response(data, status=HTTP_200_OK)
