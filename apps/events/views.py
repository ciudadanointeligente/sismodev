from rest_framework import generics
from .models import LegislativeEvent
from .serializers import EventSerializer


class EventListView(generics.ListAPIView):
    queryset = LegislativeEvent.objects.all()
    serializer_class = EventSerializer


class EventDetailView(generics.RetrieveAPIView):
    queryset = LegislativeEvent.objects.all()
    serializer_class = EventSerializer


class EventCalendarView(generics.ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        queryset = LegislativeEvent.objects.all()
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")
        event_type = self.request.query_params.get("event_type")

        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        if event_type:
            queryset = queryset.filter(event_type=event_type)

        return queryset
