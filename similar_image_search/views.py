from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from similar_image_search.serializer import SearchImagesSerializer, SearchImagesForTextSerializer
from similar_image_search.service.service import SearchService


@api_view(['GET'])
def searchImages(request):
    serializer = SearchImagesSerializer(data=request.GET)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    validated_data = serializer.validated_data
    product_id = validated_data['product_id']
    image_id = validated_data['image_id']

    try:
        service = SearchService()
        product_ids = service.getSimilarImageSearchProductId(image_id, product_id)

    except ObjectDoesNotExist:
        raise Http404(f"ImageEmbedding with ID {image_id} does not exist.")

    response_data = {"product_ids": product_ids}
    return JsonResponse(response_data, status=200, safe=False)


@api_view(['GET'])
def searchImagesForText(request):
    serializer = SearchImagesForTextSerializer(data=request.GET)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    validated_data = serializer.validated_data
    text = validated_data['data']

    try:
        service = SearchService()
        product_ids = service.getSimilarImageSearchForTextProductId(text)

    except ObjectDoesNotExist:
        raise Http404(f"ImageEmbedding with ID does not exist.")

    response_data = {"product_ids": product_ids}
    return JsonResponse(response_data, status=200, safe=False)
