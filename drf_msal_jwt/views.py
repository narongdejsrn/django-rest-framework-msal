import uuid

from rest_framework.response import Response
from rest_framework.views import APIView

from drf_msal_jwt.exceptions import StateException
from drf_msal_jwt.serializer import CodeSerializer
from drf_msal_jwt.settings import api_settings
from drf_msal_jwt.utils import build_auth_url, get_user_jwt_token


class MSALLoginView(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        # Create session by uuid
        state = str(uuid.uuid4())
        request.session['msal_state'] = state

        return Response({
            'login_url': build_auth_url(state=state)
        })


class MSALLoginWithCodeView(APIView):

    authentication_classes = []
    permission_classes = []
    msal_check_state = api_settings.MSAL_CHECK_STATE

    def post(self, request, format=None):
        code_serialized = CodeSerializer(request.data)

        if msal_check_state and request.session.get('msal_state', '') != code_serialized.data['state']:
            raise StateException()

        user_token = get_user_jwt_token(code_serialized.data['code'])
        return Response({
            'token': user_token
        })


