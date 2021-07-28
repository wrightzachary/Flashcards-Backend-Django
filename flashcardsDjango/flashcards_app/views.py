from django.http import Http404
from .models import Collection, Flashcard
from .serializers import CollectionSerializer, FlashcardSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class CollectionList(APIView):
    def get(self, request):
        collection = Collection.objects.all()
        serializer = CollectionSerializer(collection, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CollectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FlashcardList(APIView):
    def filter_by_id(self, collectionId):
        try:
            return Flashcard.objects.filter(collectionId=collectionId)
        except collectionId.DoesNotExist:
            raise Http404

    def get(self, request, collectionId):
        collection_id = self.filter_by_id(collectionId)
        serializer = FlashcardSerializer(collection_id, many=True)
        return Response(serializer.data)


class CreateFlashcard(APIView):
    def post(self, request):
        serializer = FlashcardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FlashcardDetails(APIView):
    def get_by_id(self, pk):
        try:
            return Flashcard.objects.get(pk=pk)
        except Flashcard.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        flashcard_id = self.get_by_id(pk)
        updateFlashcard = FlashcardSerializer(flashcard_id, data=request.data, partial=True)
        if updateFlashcard.is_valid():
            updateFlashcard.save()
            return Response(updateFlashcard.data, status=status.HTTP_202_ACCEPTED)
        return Response(updateFlashcard.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    def delete(self, request, pk):
        flashcard_id = self.get_by_id(pk)
        deleteFlashcard = FlashcardSerializer(flashcard_id)
        flashcard_id.delete()
        return Response(deleteFlashcard.data, status=status.HTTP_200_OK)