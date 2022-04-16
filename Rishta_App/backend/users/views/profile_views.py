from datetime import datetime
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from backend.users.models import ProfileView
from backend.users.serializers import ProfileViewSerializer


DATETIME_FORMATE = '%Y-%m-%d'

class ProfileViewAPIViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = ProfileView.objects
    serializer_class = ProfileViewSerializer

    def get_queryset(self):
        start_date = self.request.query_params.get('start')
        end_date = self.request.query_params.get('end')
        
        if not (start_date or end_date):
            return self.queryset.all()

        queryset = self.queryset
        if start_date:
            start_date = datetime.strptime(start_date, DATETIME_FORMATE)
            queryset = queryset.filter(created_at__gte=start_date)
       
        if end_date:
            end_date = datetime.strptime(end_date, DATETIME_FORMATE)
            queryset = queryset.filter(created_at__lte=end_date)
        
        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='start datge', location=OpenApiParameter.QUERY,
                description='Starting date (YYYY-MM-DD)', required=False, type=str
            ),
            OpenApiParameter(
                name='end date', location=OpenApiParameter.QUERY,
                description='Ending date (YYYY-MM-DD)', required=False, type=str
            )
        ],
    )
    def list(self, request, *args, **kwargs):
        return super(ProfileViewAPIViewSet, self).list(request, *args, **kwargs)
