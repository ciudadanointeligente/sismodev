from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Law, LawAnalysis
from .serializers import LawSerializer, LawAnalysisSerializer


class LawListView(generics.ListAPIView):
    queryset = Law.objects.all()
    serializer_class = LawSerializer


class LawDetailView(generics.RetrieveAPIView):
    queryset = Law.objects.all()
    serializer_class = LawSerializer


class LawAnalysisView(generics.RetrieveAPIView):
    queryset = Law.objects.select_related("analysis")
    serializer_class = LawAnalysisSerializer


class LawSearchView(generics.ListAPIView):
    serializer_class = LawSerializer

    def get_queryset(self):
        queryset = Law.objects.all()
        jurisdiction = self.request.query_params.get("jurisdiction")
        status = self.request.query_params.get("status")
        category = self.request.query_params.get("category")
        q = self.request.query_params.get("q")

        if jurisdiction:
            queryset = queryset.filter(jurisdiction=jurisdiction)
        if status:
            queryset = queryset.filter(status=status)
        if category:
            queryset = queryset.filter(category=category)
        if q:
            queryset = queryset.filter(title__icontains=q)

        return queryset


class LawReanalyzeView(APIView):
    def post(self, request, pk):
        try:
            law = Law.objects.get(pk=pk)
        except Law.DoesNotExist:
            return Response({"error": "Law not found"}, status=404)

        analysis, created = LawAnalysis.objects.get_or_create(
            law=law,
            defaults={
                "human_rights_score": 0,
                "democratic_score": 0,
                "concerns": [],
                "recommendations": [],
            }
        )
        analysis.save()

        return Response({
            "status": "queued for reanalyze",
            "analysis_id": str(analysis.id),
        })
