# import django_filters
# from congrats.models import CustomUser
# from rest_framework import filters

# from congrats.serializers import UsersSerializer

# from rest_framework.generics import ListAPIView


# class CategoryFilter(ListAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = UsersSerializer
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['name']
#     my_tags = ['search']