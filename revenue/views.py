from rest_framework import generics  # status, viewsets,
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from .models import StreamRecord, Subscription

from .serializers import StreamRecordSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


# 1. StreamRecord creation and list endpoint
class StreamRecordListCreateView(generics.ListCreateAPIView):
    """
    API to retrieve all StreamRecords, and create a new StreamRecord.
    The user is automatically set to the logged-in user.
    """

    queryset = StreamRecord.objects.all()
    serializer_class = StreamRecordSerializer
    permission_classes = [IsAuthenticated]  # Require authentication

    def perform_create(self, serializer):
        # Set the user to the currently authenticated user
        serializer.save(user=self.request.user)


# class ArtistStreamCountView(generics.GenericAPIView):
#     """
#     API to retrieve stream count for a specific artist
#     """

#     serializer_class = StreamRecordSerializer
#     permission_classes = [IsAuthenticated]

#     def get(self, request, artist_id):
#         # Count the number of streams for the specified artist
#         stream_count =
# StreamRecord.objects.filter(audio__artist_id=artist_id).count()

#         return Response(stream_count)


# 2. Calculate ARS (Artist's Revenue Share)
class CalculateARSView(generics.GenericAPIView):
    """
    API to calculate Artist's Revenue Share (ARS)
    based on streams and the Artist Revenue Pool (ARP).
    ARP is calculated as the sum of all subscription amounts in the system.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, artist_id):
        # Get the artist streams and total streams
        artist_streams = StreamRecord.objects.filter(audio__artist_id=artist_id).count()
        total_streams = StreamRecord.objects.count()

        # Calculate the Artist Revenue Pool (ARP)
        # by summing all subscription amounts
        arp = Subscription.objects.aggregate(total_arp=Sum("amount"))["total_arp"] or 0
        # Returns soemthing like this:
        # {'total_arp': sum_of_all_subscription_amounts}

        if arp == 0 or total_streams == 0:
            return Response(
                {
                    "artist_id": artist_id,
                    "total_streams": total_streams,
                    "artist_streams": artist_streams,
                    "artist_revenue_pool": arp,
                    "artist_revenue_share": 0,
                },
                # status=status.HTTP_400_BAD_REQUEST,
            )

        # Calculate the Artist Revenue Share (ARS)
        arp = float(arp)  # Ensure APR is a float
        ars = (artist_streams * arp) / total_streams if total_streams > 0 else 0

        # Round ARS to 2 decimal places
        ars = round(ars, 2)

        return Response(
            {
                "artist_id": artist_id,
                "total_streams": total_streams,
                "artist_streams": artist_streams,
                "artist_revenue_pool": arp,
                "artist_revenue_share": ars,
            }
        )


class AudioTrackStreamCountView(generics.GenericAPIView):
    """
    API to retrieve the number of streams for a specific audio track.
    """

    permission_classes = [IsAuthenticated]  # Require authentication

    def get(self, request, audio_id):
        # Filter StreamRecord for the given
        # audio_id and count the number of streams
        stream_count = StreamRecord.objects.filter(audio_id=audio_id).count()

        return Response({"audio_id": audio_id, "stream_count": stream_count})
