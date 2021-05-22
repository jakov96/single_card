from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.views import APIView
from imagemanager.models import BaseImage
from imagemanager.serialazer.api_v1 import BaseImageSerializer


class ImageInformation(APIView):
    def get(self, request):
        image = get_object_or_404(BaseImage, id=int(request.GET.get('id', '-1')))
        return JsonResponse(image.to_json())


class ImagesInformation(APIView):
    def get(self, request):
        images_ids = [int(image_id) for image_id in request.GET.getlist('images_ids[]', [])]
        images = BaseImage.objects.filter(id__in=images_ids)
        return JsonResponse([image.to_json() for image in images], safe=False)


class ImageUpload(APIView):
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)
    serializer_class = BaseImageSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            obj = serializer.save()
            return JsonResponse(obj.to_json())

        return JsonResponse({
            'errors': serializer.errors,
            'detail': 'Форма заполена не верно'
        }, status=400)
