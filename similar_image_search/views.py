from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseBadRequest, Http404, JsonResponse

from similar_image_search.service.service import SearchService


def searchImages(request):
    # Get the productId and Image_id from the request's GET parameters
    product_id = request.GET.get("product_id", None)
    image_id = request.GET.get("image_id", None)

    # Check if both parameters are present
    if product_id is None or image_id is None:
        return HttpResponseBadRequest("Both product Id and Image id are required.")

    try:
        service = SearchService()
        productIds = service.getSimilarImageSearchProductId(image_id, product_id)

    except ObjectDoesNotExist:
        raise Http404(f"ImageEmbedding with ID {image_id} does not exist.")

    # Return a response, for example, just an HTTP response with the parameters
    response_data = {"product_ids": productIds}
    return JsonResponse(response_data, status=200, safe=False)
