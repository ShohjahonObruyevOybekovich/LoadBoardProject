import io

import pandas as pd
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from openpyxl.utils import get_column_letter
from rest_framework import status, generics
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, get_object_or_404, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .Djangofilters import ProductFilter
from .models import Product, CustomUser
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

    def get_object(self):
        # Ensure that the object is retrieved based on the primary key or other identifier
        product_id = self.kwargs.get("pk")
        return Product.objects.get(id=product_id)

# class ProductDeleteView(DeleteView):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JWTAuthentication]
#     serializer_class = ProductSerializer
#     queryset = Product.objects.all()
#



class UploadExcelAPIView(APIView):
    def post(self, request, *args, **kwargs):
        if not request.FILES.get('file'):
            return HttpResponseBadRequest("No file uploaded")

        file = request.FILES['file']
        try:
            df = pd.read_excel(file)
            print("Columns found in the uploaded file:", df.columns)

            # Validate required columns
            required_columns = {
                'title', 'places', 'view', 'cube', 'kg', 'cube_kg', 'price',
                'payment', 'debt', 'where_from', 'date', 'transport',
                'current_place', 'status', 'user_id'
            }
            if not required_columns.issubset(df.columns):
                missing_columns = required_columns - set(df.columns)
                return HttpResponseBadRequest(f"Invalid file format. Missing columns: {', '.join(missing_columns)}")

            # Convert datetime fields to timezone-unaware
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'], errors='coerce')
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

        # Convert QuerySet to DataFrame
        df = pd.DataFrame(products)

        # Convert datetime fields to timezone-unaware and format date
        if 'date' in df.columns:
            df['date'] = df['date'].apply(
                lambda x: x.replace(tzinfo=None).strftime('%Y-%m-%d %H:%M:%S') if pd.notnull(x) else x)

        # Create an Excel file in memory
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Products')

            # Auto-adjust column widths
            workbook = writer.book
            sheet = workbook.active
            for col_num, col in enumerate(df.columns, 1):
                column = get_column_letter(col_num)
                max_length = max(df[col].astype(str).apply(len).max(), len(col))
                sheet.column_dimensions[column].width = max_length + 2  # Adjust width with a small buffer

        buffer.seek(0)
        response = HttpResponse(
            buffer,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            headers={'Content-Disposition': 'attachment; filename="products.xlsx"'}
        )
        return response

class DownloadExcelFilteredAPIView(APIView):
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

        # Convert 'date' field to a timezone-unaware format and to a readable string format
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            df['date'] = df['date'].apply(lambda x: x.replace(tzinfo=None).strftime('%Y-%m-%d %H:%M:%S') if pd.notnull(x) else '')

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