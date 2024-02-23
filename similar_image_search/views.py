import logging

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, JsonResponse
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from similar_image_search.serializer import SearchImagesSerializer, SearchImagesForTextSerializer, \
    StatusSerializer, ErpCodesSerializer
from similar_image_search.service.service import SearchService

logger = logging.getLogger(__name__)

service = SearchService()


@api_view(['GET'])
def searchImages(request):
    serializer = SearchImagesSerializer(data=request.GET)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    validated_data = serializer.validated_data
    product_id = validated_data['product_id']
    image_id = validated_data['image_id']

    try:

        product_ids = service.getSimilarImageSearchProductId(image_id, product_id)

    except ObjectDoesNotExist:
        raise Http404(f"ImageEmbedding with ID {image_id} does not exist.")

    except Exception as e:
        logger.error(f"Internal Server Error: {e}")
        return JsonResponse({f"Internal Server Error:{e}"}, status=500)
    response_data = {"product_ids": product_ids}
    return JsonResponse(response_data, status=status.HTTP_200_OK, safe=False)


@api_view(['GET'])
def searchImagesForText(request):
    serializer = SearchImagesForTextSerializer(data=request.GET)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    validated_data = serializer.validated_data
    text = validated_data['data']

    try:
        product_ids = service.getSimilarImageSearchForTextProductId(text)
        response_data = {"product_ids": product_ids}
        return JsonResponse(response_data, status=status.HTTP_200_OK, safe=False)

    except Exception as e:
        logger.error(f"Internal Server Error: {e}")
        return JsonResponse({"error": "Internal Server Error"}, status=500)


@api_view(['PUT'])
def discontinueStatusForERPCode(request):
    serializer = ErpCodesSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    validated_data = serializer.validated_data
    erpCodes = validated_data['erp_codes']

    try:
        service.discontinueStatusForErpCode(erpCodes)
        return Response({"message": "Status updated successfully"}, status=status.HTTP_202_ACCEPTED)
    except serializers.ValidationError as e:
        return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Internal Server Error: {e}")
        return JsonResponse({"error": "Internal Server Error"}, status=500)


@api_view(['PUT'])
def handle_payload(request):
    try:
        payload = request.data.get("payload", {})
        serializer = StatusSerializer(data=payload)
        serializer.is_valid(raise_exception=True)  # Raises ValidationError if not valid

        # Process the validated data and update your product statuses here
        product_id_status_data = serializer.validated_data.get('product_id_status', {})
        product_variant_id_status_data = serializer.validated_data.get('product_variant_id_status', {})

        service.updateStatus(product_id_status_data, product_variant_id_status_data)

        return Response({"message": "Status updated successfully"}, status=status.HTTP_202_ACCEPTED)

    except serializers.ValidationError as e:
        return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"errors": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
