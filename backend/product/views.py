from django.db.models.query_utils import Q
from product.models import Category, Gallery, Product, Review
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from product.serializers import CategorySerializer, CreateProductSerializer, CreateReviewSerializer, GallerySerializer, ProductReviewSerializer, ProductSerializer, ReviewSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from user.permissions import IsActiveOrReadOnly, IsStaffOrReadOnly
from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from drf_yasg import openapi
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin, CreateModelMixin
from rest_framework.generics import GenericAPIView

class Categories(ListModelMixin,
                CreateModelMixin,
                GenericAPIView):

    permission_classes = [IsStaffOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @swagger_auto_schema(
        responses={
            200: CategorySerializer(),
            204: 'No Content'
        }
    )
    def get(self, request, *args, **kwargs):
        """
        Category List

        Return all available category.<br>
        Will use 204 status code if result is empty.

        ### Permission:
        * Allow Any
        """

        qs = self.list(request, *args, **kwargs)
        return qs if qs.data else Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        responses={
            201: CategorySerializer(),
            400: 'Bad Request',
            401: 'Invalid User\'s Credential',
            403: 'You Do Not Have Permission To Perform This Action'
        }
    )
    def post(self, request, *args, **kwargs):
        """
        Create Category

        Create a new category.

        ### Permission:
        * Staff Only
        """

        return self.create(request, *args, **kwargs)

class CategoryDetail(RetrieveModelMixin,
                    UpdateModelMixin,
                    DestroyModelMixin,
                    GenericAPIView):

    permission_classes = [IsStaffOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @swagger_auto_schema(
        responses={
            200: CategorySerializer(),
            404: 'No Category With That ID Found'
        }
    )
    def get(self, request, *args, **kwargs):
        """
        Detail Category

        Return the detail of category with requested id.<br>
        Return 404 if no category with that id is found.

        ### Permission:
        * Allow Any
        """
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=CategorySerializer(),
        responses={
            200: CategorySerializer(),
            400: 'Bad Request',
            401: 'Invalid User\'s Credential',
            403: 'You Do Not Have Permission To Perform This Action',
            404: 'No Category With That ID Found'
        }
    )
    def put(self, request, *args, **kwargs):
        """
        Update Category

        Update category that the id mentioned, returned the updated category if succesfull.<br>
        Return 404 if no category with that id is found.

        ### Permission:
        * Staff Only
        """
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            204: 'Category Succesfully Deleted',
            400: 'Bad Request',
            401: 'Invalid User\'s Credential',
            403: 'You Do Not Have Permission To Perform This Action',
            404: 'No Category With That ID Found'
        }
    )
    def delete(self, request, *args, **kwargs):
        """
        Delete Category

        Delete category that the id mentioned, then returned 204 if succesfull.<br>
        Return 404 if no category with that id is found.

        ### Permission:
        * Staff Only
        """
        return self.destroy(request, *args, **kwargs)

class CategoryProduct(APIView):
    permission_classes = [AllowAny]
    def get(self, request, pk):
        products = Product.objects.filter(Q(category__id__icontains=pk))
        serializer = ProductSerializer(products, many=True)

        if not products:
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, slug, pk):
        pass

class Products(APIView):

    permission_classes = [IsStaffOrReadOnly]

    @swagger_auto_schema(
        responses={
            200: ProductSerializer(),
            204: 'No Content'
        }
    )
    def get(self, request):
        """
        Product List

        Return all available product. You can set a query parameters to filter the result.<br>

        ### Valid query parameter list:<br>
        **featured**: If set to 'true' will only return featured products, if set to 'false' will do the opposite.<br>
        **category**: Expected a category's ID, 
        if properly set will only return product that contain category with mentioned ID.<br>

        ### Example request:<br>
        ```
        /api/v1/products/?category=1&featured=true
        ```
        """

        product_qs = Product.objects.all()

        # If featured parameter is set to either true or false,
        # filter the queryset first to the desired featured value
        if request.GET.get('featured') in ['true', 'false']:
            featured = True if request.GET.get('featured') == 'true' else False
            product_qs = product_qs.filter(is_featured=featured)

        # If category parameter is set,
        # check if the product have that category first before appending them to the list
        if request.GET.get('category'):
            products = [product for product in product_qs if product.category.filter(id=request.GET.get('category'))]
        else:
            products = [product for product in product_qs]

        # Return early with no content (204) if queryset is empty
        if not products:
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=CreateProductSerializer(),
        responses={
            201: openapi.Schema(type=openapi.TYPE_OBJECT, properties={'detail': 'Message', 'id': 'Product\'s ID', 'slug': 'Product\'s Slug'}),
            400: 'Bad Request',
            401: 'Invalid User\'s Credential',
            403: 'You Do Not Have Permission To Perform This Action'
        }
    )
    def post(self, request):
        """
        Create Product

        A staff account is needed to request this endpoint.<br>
        Otherwise, if user is not authenticated return 401 but if user is authenticated but is not a staff account return 403.<br>
        """

        serializer = CreateProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'detail': 'Product successfully created',
                    'id': serializer.data['id'],
                    'slug': serializer.data['slug']
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetail(APIView):

    permission_classes = [IsStaffOrReadOnly]

    def get_object(self, slug):
        try:
            return Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        responses={
            200: ProductReviewSerializer(),
            404: 'No Product With That Slug Found'
        }
    )
    def get(self, request, slug):
        """
        Detail Product

        Return the detail of product that the slug mentioned.<br>
        Return 404 if no product with that slug is found.
        """

        product = self.get_object(slug)
        serializer = ProductReviewSerializer(product)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=CreateProductSerializer(),
        responses={
            200: ProductSerializer(),
            400: 'Bad Request',
            404: 'No Product With That Slug Found',
            409: 'Some Unique Field(e.g username) Conflicted'
        }
    )
    def put(self, request, slug):
        """
        Update Product

        Update product that the slug mentioned, returned the updated product if succesful.<br>
        Return 404 if no product with that slug is found.
        """

        product = self.get_object(slug)
        try:
            serializer = ProductSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        except ValidationError:
            return Response(serializer.errors, status=status.HTTP_409_CONFLICT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={
            204: 'Succesfully Delete Product',
            404: 'No Product With That Slug Found'
        }
    )
    def delete(self, request, slug):
        """
        Delete Product

        Delete product that the slug mentioned, then returned 204 if succesful
        Return 404 if no product with that slug is found.
        """

        product = self.get_object(slug)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class GalleryList(APIView):

    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={
            200: GallerySerializer(),
            204: 'No Gallery Results Found'
        }
    )
    def get(self, request):
        """
        Gallery

        Return all available gallery image.
        You can set a GET parameter to filter the result.

        GET parameter list:<br>
        **featured**: If set to 'true' will only return featured product's gallery<br>
        **product_slug**: Will only return product's gallery with mentioned slug
        """

        gallery = Gallery.objects.all().order_by('product')
        gallery = gallery.filter(product__is_featured=True) if request.GET.get('featured') == 'true' else gallery
        gallery = gallery.filter(product__slug=request.GET.get('product_slug')) if request.GET.get('product_slug') else gallery
        
        if not gallery:
            # Return early with no content (204) if no queryset found
            return Response(status=status.HTTP_204_NO_CONTENT)

        serialize = GallerySerializer(gallery, many=True)
        return Response(serialize.data, status=status.HTTP_200_OK)

class ProductReviews(APIView):
    permission_classes = [IsActiveOrReadOnly]

    @swagger_auto_schema(
        responses={
            200: ReviewSerializer(many=True),
            204: 'No Content',
            404: 'No Product With That Slug Found',
        }
    )
    def get(self, request, slug):
        """
        Review List
        
        Return a list of reviews for product with mentioned slug.<br>
        Return 404 if no product with that slug is found.<br>
        """

        get_object_or_404(Product, slug=slug)
        reviews = Review.objects.filter(product__slug=slug)

        if not reviews:
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=CreateReviewSerializer(),
        responses={
            201: ReviewSerializer(),
            400: 'Bad Request',
            401: 'Invalid User\'s Credential',
            404: 'No Product With That Slug Found',
            409: 'This User Already Reviewed This Product'
        }
    )
    def post(self, request, slug):
        """
        Create Review

        Create a review for product with mentioned slug, the author will be automatically the requesting user.<br>
        Each user can only review one product once.<br>
        Return 401 if request are not authenticated (user aren't logged in).<br>
        Return 404 if no product with that slug is found.<br>
        Return 409 if you rty to review a product using a same user more than once.<br>
        """

        product = get_object_or_404(Product, slug=slug)
        try:
            review = Review.objects.create(user=request.user, product=product, **request.data)
        except ValidationError as e:
            return Response({'detail': e.detail[0] or 'Unknown error, please check logs'}, status=e.get_codes()[0] or 400)
        
        return Response(ReviewSerializer(review).data, status=status.HTTP_201_CREATED)

    def delete(self, request, slug):
        """
        Delete Review
        
        Delete a review for product with mentioned slug, the author will be automatically the requesting user.<br>
        Return 204 if review successfully deleted.<br>
        Return 401 if request are not authenticated (user aren't logged in).<br>
        Return 404 if no product with that slug is found or user haven't made any review for that product yet.<br>
        """

        get_object_or_404(Review, product__slug=slug, user=request.user).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductCategories(APIView):
    permission_classes = [IsStaffOrReadOnly]

    def post(self, request, slug, pk):
        product = get_object_or_404(Product, slug=slug)
        category = get_object_or_404(Category, id=pk)
        product_category = [category.id for category in product.category.all()]

        if category.id in product_category:
            return Response({'message': 'This product already on this category'}, status.HTTP_400_BAD_REQUEST)
    
        product.category.add(category)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request, slug, pk):
        product = get_object_or_404(Product, slug=slug)
        category = get_object_or_404(Category, id=pk)
        product_category = [category.id for category in product.category.all()]

        if not category.id in product_category:
            return Response({'message': 'This product is not already on this category'}, status.HTTP_400_BAD_REQUEST)
    
        product.category.remove(category)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status.HTTP_200_OK)