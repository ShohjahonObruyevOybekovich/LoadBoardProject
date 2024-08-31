from symtable import Class

import pandas as pd
from django.utils import timezone
from django.views.generic import DeleteView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, get_object_or_404, UpdateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .Djangofilters import ProductFilter
from .models import CustomUser, Product
from .serializers import ProductSerializer


class UserMonthView(ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_queryset(self):
        user = get_object_or_404(CustomUser, uuid=self.kwargs['uuid'])
        return user.products.filter(date__month=timezone.now().month)


class UserYearView(ListAPIView):
    permission_classes = [IsAuthenticated,]
    authentication_classes = [JWTAuthentication]
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_queryset(self):
        user = get_object_or_404(CustomUser, uuid=self.kwargs['uuid'])
        return user.products.filter(date__year=timezone.now().year)



class DeleteUserYearProductView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def delete(self, request, uuid, product_id):
        user = get_object_or_404(CustomUser, uuid=uuid)
        product = get_object_or_404(Product, id=product_id, user=user)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# class ProductCreateAPIView(CreateAPIView):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JWTAuthentication]
#     serializer_class = ProductSerializer
#     queryset = Product.objects.all()


class ProductListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication,]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    filter_backends = (SearchFilter,)
    search_fields = ['username', 'role']

class ProductUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

# class ProductDeleteView(DeleteView):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JWTAuthentication]
#     serializer_class = ProductSerializer
#     queryset = Product.objects.all()
#

from django.http import HttpResponse, HttpResponseBadRequest
import io



import pandas as pd
from django.http import HttpResponseBadRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, CustomUser

class UploadExcelAPIView(APIView):
    def post(self, request, *args, **kwargs):
        if not request.FILES.get('file'):
            return HttpResponseBadRequest("No file uploaded")

        file = request.FILES['file']
        try:
            df = pd.read_excel(file)
            print("Columns found in the uploaded file:", df.columns)  # Add this line to debug

            # Validate required columns
            required_columns = {
                'title', 'places', 'view', 'cube', 'kg', 'cube_kg', 'price',
                'payment', 'debt', 'where_from', 'date', 'transport',
                'current_place', 'status', 'user_id'
            }
            if not required_columns.issubset(df.columns):
                return HttpResponseBadRequest("Invalid file format. Required columns are missing.")

            # Convert datetime fields to timezone-unaware
            if 'date' in df.columns:
                df['date'] = df['date'].apply(lambda x: x.replace(tzinfo=None) if pd.notnull(x) else x)

            # Process data and create/update products
            for _, row in df.iterrows():
                user_id = row.get('user_id')
                try:
                    user = CustomUser.objects.get(id=user_id)
                except CustomUser.DoesNotExist:
                    continue  # Skip rows with invalid user_id

                Product.objects.update_or_create(
                    title=row.get('title'),
                    user=user,
                    defaults={
                        'places': row.get('places'),
                        'view': row.get('view'),
                        'cube': row.get('cube'),
                        'kg': row.get('kg'),
                        'cube_kg': row.get('cube_kg'),
                        'price': row.get('price'),
                        'payment': row.get('payment'),
                        'debt': row.get('debt'),
                        'where_from': row.get('where_from'),
                        'date': row.get('date'),
                        'transport': row.get('transport'),
                        'current_place': row.get('current_place'),
                        'status': row.get('status'),
                    }
                )
            return Response({"status": "success", "message": "File processed successfully"})
        except Exception as e:
            return HttpResponseBadRequest(f"Error processing file: {str(e)}")


class DownloadExcelAllAPIView(APIView):
    def get(self, request, uuid=None, *args, **kwargs):
        # Fetch products from the database based on the user's UUID
        products = Product.objects.filter(user__uuid=uuid).values(
            'title', 'places', 'view', 'cube', 'kg', 'cube_kg', 'price',
            'payment', 'debt', 'where_from', 'date', 'transport',
            'current_place', 'status', 'user_id'
        )
        df = pd.DataFrame(products)

        # Convert datetime fields to timezone-unaware
        if 'date' in df.columns:
            df['date'] = df['date'].apply(lambda x: x.replace(tzinfo=None) if pd.notnull(x) else x)

        # Create an Excel file
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Products')

        buffer.seek(0)
        response = HttpResponse(
            buffer,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            headers={'Content-Disposition': 'attachment; filename="products.xlsx"'}
        )
        return response


class DownloadExcelFIlteredAPIView(APIView):
    def get(self, request, uuid=None, *args, **kwargs):
        # Get filters from query parameters
        month = request.query_params.get('month')
        year = request.query_params.get('year')

        # Fetch products based on UUID
        if uuid:
            products = Product.objects.filter(user__uuid=uuid)
        else:
            products = Product.objects.all()

        # Apply month and year filters if provided
        if month:
            products = products.filter(date__month=month)
        if year:
            products = products.filter(date__year=year)

        # Serialize products
        products_data = products.values(
            'title', 'places', 'view', 'cube', 'kg', 'cube_kg', 'price',
            'payment', 'debt', 'where_from', 'date', 'transport',
            'current_place', 'status', 'user_id'
        )
        df = pd.DataFrame(products_data)

        # Convert datetime fields to timezone-unaware
        if 'date' in df.columns:
            df['date'] = df['date'].apply(lambda x: x.replace(tzinfo=None) if pd.notnull(x) else x)

        # Create an Excel file
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Products')

        buffer.seek(0)
        response = HttpResponse(
            buffer,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            headers={'Content-Disposition': 'attachment; filename="products.xlsx"'}
        )
        return response
