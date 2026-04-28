from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Avg

from apps.legislation.models import Law, LawAnalysis
from apps.news.models import NewsArticle, NewsAnalysis
from apps.events.models import LegislativeEvent


class DashboardSummaryView(APIView):
    def get(self, request):
        law_count = Law.objects.count()
        news_count = NewsArticle.objects.count()
        event_count = LegislativeEvent.objects.count()

        law_analysis = LawAnalysis.objects.aggregate(
            avg_hr=Avg("human_rights_score"),
            avg_dem=Avg("democratic_score")
        )
        news_analysis = NewsAnalysis.objects.aggregate(
            avg_hr=Avg("human_rights_impact"),
            avg_dem=Avg("democratic_impact")
        )

        all_hr = []
        all_dem = []
        if law_analysis["avg_hr"] is not None:
            all_hr.append(law_analysis["avg_hr"])
            all_dem.append(law_analysis["avg_dem"])
        if news_analysis["avg_hr"] is not None:
            all_hr.append(news_analysis["avg_hr"])
            all_dem.append(news_analysis["avg_dem"])

        avg_hr = sum(all_hr) / len(all_hr) if all_hr else 0
        avg_dem = sum(all_dem) / len(all_dem) if all_dem else 0

        return Response({
            "total_laws": law_count,
            "total_news": news_count,
            "total_events": event_count,
            "avg_human_rights_score": round(avg_hr, 2),
            "avg_democratic_score": round(avg_dem, 2),
        })


class HumanRightsMetricsView(APIView):
    def get(self, request):
        law_by_category = LawAnalysis.objects.values_list(
            "law__category"
        ).annotate(avg_score=Avg("human_rights_score"))

        categories = {}
        for cat, score in law_by_category:
            if cat:
                categories[cat] = round(score, 2) if score else 0

        return Response({
            "categories": categories,
            "trends": [],
        })


class DemocraticMetricsView(APIView):
    def get(self, request):
        law_by_category = LawAnalysis.objects.values_list(
            "law__category"
        ).annotate(avg_score=Avg("democratic_score"))

        categories = {}
        for cat, score in law_by_category:
            if cat:
                categories[cat] = round(score, 2) if score else 0

        return Response({
            "categories": categories,
            "trends": [],
        })
