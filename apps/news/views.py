from rest_framework import generics
from .models import NewsArticle, NewsAnalysis
from .serializers import NewsSerializer, NewsAnalysisSerializer


class NewsListView(generics.ListAPIView):
    queryset = NewsArticle.objects.all()
    serializer_class = NewsSerializer


class NewsDetailView(generics.RetrieveAPIView):
    queryset = NewsArticle.objects.all()
    serializer_class = NewsSerializer


class NewsAnalysisView(generics.RetrieveAPIView):
    queryset = NewsArticle.objects.select_related("analysis")
    serializer_class = NewsAnalysisSerializer


class NewsSearchView(generics.ListAPIView):
    serializer_class = NewsSerializer

    def get_queryset(self):
        queryset = NewsArticle.objects.all()
        country = self.request.query_params.get("country")
        source = self.request.query_params.get("source")
        q = self.request.query_params.get("q")

        if country:
            queryset = queryset.filter(country=country)
        if source:
            queryset = queryset.filter(source=source)
        if q:
            queryset = queryset.filter(title__icontains=q)

        return queryset
