from django.http import JsonResponse
from .models import Drink
from .serializers import DrinkSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET', "POST"])
def drink_list(request):

    # if the request's methos is GET
    if request.method == 'GET':
        # get all objects of Django model
        drinks = Drink.objects.all()

        # serialize Django model objects
        # many: whether to serialize a list of items.
        serializer = DrinkSerializer(drinks, many=True)
        print(serializer.data)
        # can return a json response,
        return JsonResponse({"drinks": serializer.data})

    # if the request's methos is POST
    if request.method == 'POST':
        # deserialize the post data
        serializer = DrinkSerializer(data=request.data)
        print(serializer)

        # Check whether the post object valid
        # .is_valid():  Deserializes and validates incoming data.
        if serializer.is_valid():
            # .save():  Persists the validated data into an object instance.
            serializer.save()
            # return an api response with the created data and a status.
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', "PUT", "DELETE"])
def drink_detail(request, id):      # accept 2nd parameter

    # try to get Django object based on the id
    # otherwise , return 404
    try:
        drink = Drink.objects.get(pk=id)
    except Drink.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # retrive
    if request.method == "GET":
        # parse Django object to a serialier
        serializer = DrinkSerializer(drink)
        # return a api response with data
        return Response(serializer.data)

    # update
    if request.method == "PUT":
        serializer = DrinkSerializer(drink, data=request.data)

        # if valid
        if serializer.is_valid():
            # save update
            serializer.save()
            # return with newest data
            return Response(serializer.data)
        # Otherwise, return 400 status with errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # remove
    if request.method == "DELETE":
        # delete item using Django
        drink.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
