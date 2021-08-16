
from django.contrib import auth
from django.contrib.auth.models import User as SuperUser
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView  # Create your views here.
from .models import *
from .serializers import *

class RegisterUser(APIView):
    def post(self, request):
        try:
            username = request.POST['username']
            # first_name = request.POST['first_name']
            # last_name = request.POST['last_name']
            # date_of_birth = request.POST['date_of_birth']
            phone = request.POST['phone']
            email = request.POST['email']
            status = request.POST['status']
            password = request.POST['password']
            # avatar = request.FILES['avatar']
        except:
            return JsonResponse({'message': 'error while receiving data'})
        #   Creating Super user to authenticate with the given data
        try:
            user = SuperUser.objects.create(username=username, is_active=True)
            user.set_password(password)
            user.save()
        except:
            return JsonResponse({'message': 'user already exist'})
        #   creating User with the given Data
        try:
            User.objects.create(username=user, phone=phone,
                                email=email, status=status)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'error while creating user'})
        token_count = Token.objects.filter(user=user)
        if len(token_count) > 0:
            Token.objects.get(user=user).delete()
            token = Token.objects.create(user=user)
        else:
            token = Token.objects.create(user=user)
        return JsonResponse({'message': 'User created', 'token': token.key})


class Login(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        global consumer, token, user_obj
        try:
            username = request.POST['username']
            password = request.POST['password']
        except:
            return JsonResponse({'message': 'error while receiving data'})
        #    authenticate user with the given data
        try:
            user = auth.authenticate(username=username, password=password)
        except:
            return JsonResponse({'message': 'Credentials are not correct !'})
        #   creating User with the given Data

        try:
            if user is not None:
                consumer = User.objects.get(username=user)
                consumer = UserSerializer(consumer).data
                token_count = Token.objects.filter(user=user)
                if len(token_count) > 0:
                    Token.objects.get(user=user).delete()
                    token = Token.objects.create(user=user)
                else:
                    token = Token.objects.create(user=user)
            else:
                return JsonResponse({'message': 'Credentials are not correct !'})
        except Exception as e:
            print('error : ',e)
            return JsonResponse({'message': 'error while getting user info'})
        return JsonResponse({'message': 'success', 'user_obj': consumer, 'username': username, 'token': token.key})


class CreateShop(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            name = request.POST['name']
            Shop.objects.create(name=name)
            return JsonResponse({'status':'true','message': 'shop : {} created seccussfully'.format(name)})

        except:
            return JsonResponse({'status':'false','message': 'error while receiving data'})


class CreateCategory(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            shop_id = request.POST['shop_id']
            title = request.POST['title']
            shop = Shop.objects.get(pk=shop_id)
            Category.objects.create(shop=shop,title=title)
            return JsonResponse({'status':'true','message': 'Category : {} for shop : {} created seccussfully'.format(title,shop.name)})

        except:
            return JsonResponse({'status':'false','message': 'error while receiving data'})


class CreateItem(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            shop_id = request.POST['shop_id']
            category_id = request.POST['category_id']
            title = request.POST['title']
            quantity = request.POST['quantity']
            price = request.POST['price']
            shop = Shop.objects.get(pk=shop_id)
            category = Category.objects.get(pk=category_id)
            Item.objects.create(shop=shop,category=category,title=title,quantity=quantity,price=price)
            return JsonResponse({'status':'true','message': 'Item : {} for category : {} from shop : {} created seccussfully'.format(title,category.title,shop.name)})

        except:
            return JsonResponse({'status':'false','message': 'error while receiving data'})


class GetShopItems(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            shop_id = request.POST.get('shop_id',None)
            category_id = request.POST.get('category_id',None)
            if shop_id:
                if not category_id:
                    items = list(Item.objects.filter(shop__id=shop_id).values())
                else:
                    items = list(Item.objects.filter(shop__id=shop_id,category__id=category_id).values())
                return JsonResponse({'status':'true','items':items})
            else:
                return JsonResponse({'status':'false','message': 'No shop_id were provided'})
        except Exception as e:
            print (e)
            return JsonResponse({'status':'false','message': 'error while receiving data'})

# class UpdateInfo(viewsets.ReadOnlyModelViewSet):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         global consumer
#         # try:
#         first_name = request.POST['first_name']
#         last_name = request.POST['last_name']
#         date_of_birth = request.POST['date_of_birth']
#         email = request.POST['email']
#         phone = request.POST['phone']
#         username = request.POST['username']
#         # except:
#         #     return JsonResponse({'message': 'error while receiving data'})
#         try:
#             print(username)
#             user = SuperUser.objects.get(username=username)
#             consumer = User.objects.get(username=user)

#         except:
#             return JsonResponse({'message': 'error while finding user'})
#         # try:
#         consumer.first_name = first_name
#         consumer.last_name = last_name
#         consumer.date_of_birth = date_of_birth
#         consumer.email = email
#         consumer.phone = phone
#         consumer.save()
#         print(last_name)
#         return JsonResponse({'message': 'success'})
#         # except:
#         #     return JsonResponse({'message': 'error while receiving data'})


# class AllMeals(viewsets.ReadOnlyModelViewSet):
#     permission_classes = [IsAuthenticated]

#     serializer_class = MealSerializer
#     queryset = Meal.objects.filter(status='Approved')


# class ApprovedMeals(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         try:
#             pending_meals = Meal.objects.filter(status='Approved').values()
#             return JsonResponse({'message': 'success', 'pending_meals': list(pending_meals)})
#         except:
#             return JsonResponse({'message': 'false'})
