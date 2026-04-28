from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import HumanRightsParameter, DemocraticParameter, ContentAnalysis
from .serializers import ParameterSerializer, ContentAnalysisSerializer


class ParseDocumentView(APIView):
    def post(self, request):
        return Response({"status": "parsed"})


class AnalyzeContentView(APIView):
    def post(self, request):
        return Response({"status": "analyzed"})


class ParametersView(generics.ListAPIView):
    serializer_class = ParameterSerializer

    def get_queryset(self):
        params = list(HumanRightsParameter.objects.filter(is_active=True))
        params.extend(DemocraticParameter.objects.filter(is_active=True))
        return params
