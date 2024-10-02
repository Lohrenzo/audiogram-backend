from rest_framework import generics, status  # viewsets,
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from .models import StreamRecord, Subscription

# from api.models import Audio
from .serializers import StreamRecordSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


# 1. StreamRecord CRUD and retrieval endpoints


class StreamRecordCreateView(generics.CreateAPIView):
    """
    API to create a new StreamRecord. The user is
    automatically set to the logged-in user.
    """

    queryset = StreamRecord.objects.all()
    serializer_class = StreamRecordSerializer
    permission_classes = [IsAuthenticated]  # Require authentication

    def perform_create(self, serializer):
        # Set the user to the currently authenticated user
        serializer.save(user=self.request.user)


class AllStreamsView(generics.ListAPIView):
    """
    API to retrieve all stream records
    """

    queryset = StreamRecord.objects.all()
    serializer_class = StreamRecordSerializer
    permission_classes = [IsAuthenticated]


class ArtistStreamsView(generics.ListAPIView):
    """
    API to retrieve stream records for a specific artist
    """

    serializer_class = StreamRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        artist_id = self.kwargs["artist_id"]
        return StreamRecord.objects.filter(audio__artist_id=artist_id)


# 2. Calculate ARS (Artist's Revenue Share)


class CalculateARSView(generics.GenericAPIView):
    """
    API to calculate Artist's Revenue Share (ARS) based on streams and the Artist Revenue Pool (ARP).
    ARP is calculated as the sum of all subscription amounts in the system.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, artist_id):
        # Get the artist streams and total streams
        artist_streams = StreamRecord.objects.filter(audio__artist_id=artist_id).count()
        total_streams = StreamRecord.objects.count()

        # Calculate the Artist Revenue Pool (ARP) by summing all subscription amounts
        arp = Subscription.objects.aggregate(total_arp=Sum("amount"))["total_arp"] or 0
        # Returns soemthing like this: {'total_arp': sum_of_all_subscription_amounts}

        if arp == 0 or total_streams == 0:
            return Response(
                {
                    "error": "Artist Revenue Pool (ARP) or total streams is zero, unable to calculate ARS."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Calculate the Artist Revenue Share (ARS)
        arp = float(arp)  # Ensure APR is a float
        ars = (artist_streams * arp) / total_streams if total_streams > 0 else 0

        return Response(
            {
                "artist_id": artist_id,
                "total_streams": total_streams,
                "artist_streams": artist_streams,
                "artist_revenue_pool": arp,
                "artist_revenue_share": ars,
            }
        )
