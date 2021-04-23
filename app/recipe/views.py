from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import Tag, Ingredient, Recipe
from recipe import serializers


class BaseRecipeAttrViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    """Base viewset for user owned recipe attributes"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database"""
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage ingredients in the database"""
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database"""
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def _params_to_ints(self, qd):
        """Convert a list of string IDs to a list of integers"""

        #
        # getting  ['1', '2']
        # making [1,2]
        return [int(str_id) for str_id in qd]

    def get_queryset(self):
        """Retrieve the recipes for the authenticated user"""
        # query_params - dict containing all the params provided in request
        # To make a multiple filter you should do:
        # recipes/?ingredients=1&ingredients=2
        # so query_params =  <QueryDict: {'ingredients': ['1', '2']}>

        print(self.request.query_params)
        # !!!! .get will return LAST VALUE OF THE LIST !!!
        # USE GET LIST INSTEAD
        tags = self.request.query_params.getlist('tags', None)
        ingredients = self.request.query_params.getlist('ingredients', None)
        queryset = self.queryset
        if tags:
            tag_ids = self._params_to_ints(tags)
            # __in will return all the ids which are in the list we provide
            # todo read more about it
            queryset = queryset.filter(tags__id__in=tag_ids)
        if ingredients:
            ingredient_ids = self._params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredient_ids)
        return queryset.filter(user=self.request.user)

    # list action is for many. retrieve is for detail view
    def get_serializer_class(self):
        """Retrieve appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer

        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save(user=self.request.user)

    # add custom function and define it as action
    # url_path means /recipes/1/upload-image/
    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to a recipe"""
        # this will get object based on the id from queryset
        recipe = self.get_object()
        # get serializer will call get_serializer_class
        # so we need to override get_serializer_class
        # may be set here but best practice to get_serializer_class
        serializer = self.get_serializer(
            recipe,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()  # saves the object with the updated data
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        # generates error if serializer not valid
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

# class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
#                  mixins.CreateModelMixin):
#     """Manage tags in the database"""
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)
#
#     queryset = Tag.objects.all()
#     serializer_class = serializers.TagSerializer
#
#     def get_queryset(self):
#         """Return objects for the current authenticated user only"""
#         return self.queryset.filter(user=self.request.user).order_by('-name')
#
#     def perform_create(self, serializer):
#         """Create a new tag and assign it to correct user """
#         serializer.save(user=self.request.user)
#
#
# class IngredientViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
#                         mixins.CreateModelMixin):
#     """Manage ingredients in the database"""
#
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)
#     queryset = Ingredient.objects.all()
#     serializer_class = serializers.IngredientSerializer
#
#     def get_queryset(self):
#         """Return objects for the current authenticated user only"""
#         return self.queryset.filter(user=self.request.user).order_by('-name')
#
#     def perform_create(self, serializer):
#         """Create a new ingredient and assign it to correct user """
#         serializer.save(user=self.request.user)
