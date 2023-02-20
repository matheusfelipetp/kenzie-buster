from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Request, Response, status
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Movie
from .permissions import IsEmployee
from .serializers import MovieOrderSerializer, MovieSerializer


class MovieView(APIView, PageNumberPagination):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsEmployee]

    def get(self, request: Request):
        movies = Movie.objects.all()
        result_page = self.paginate_queryset(movies, request, view=self)
        serializer = MovieSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, request: Request):
        serializer = MovieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        return Response(serializer.data, status.HTTP_201_CREATED)


class MovieDetailsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsEmployee]

    def get(self, request: Request, movie_id: int):
        movie = get_object_or_404(Movie, id=movie_id)
        serializer = MovieSerializer(movie)

        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request: Request, movie_id: int):
        movie = get_object_or_404(Movie, id=movie_id)
        movie.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class MovieOrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, movie_id: int):
        movie = get_object_or_404(Movie, id=movie_id)
        order = MovieOrderSerializer(data=request.data)
        order.is_valid(raise_exception=True)
        order.save(order_user=request.user, order_movie=movie)

        return Response(order.data, status.HTTP_201_CREATED)
