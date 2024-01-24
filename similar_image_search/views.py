from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseBadRequest, HttpResponse, Http404

from similar_image_search.service.service import SearchService


def search(request):
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
    return HttpResponse(productIds)
