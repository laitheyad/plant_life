import ast
import datetime

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
                return JsonResponse({'status': 'false', 'message': 'Credentials are not correct !'})
        except Exception as e:
            print('error : ', e)
            return JsonResponse({'status': 'success', 'message': 'error while getting user info'})
        return JsonResponse(
            {'status': 'success', 'message': 'user logged in successfully', 'user_obj': consumer, 'username': username,
             'token': token.key})


class CreateShop(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            name = request.POST['name']
            Shop.objects.create(name=name)
            return JsonResponse({'status': 'true', 'message': 'shop : {} created successfully'.format(name)})

        except:
            return JsonResponse({'status': 'false', 'message': 'error while receiving data'})

    def get(self, request):
        shops = list(Shop.objects.all().values())
        for shop in shops:
            cat_list = []
            cat = Category.objects.filter(shop=shop['id'])
            for c in cat:
                cat_list.append({'title': c.title, 'id': c.id})
            shop['category_list'] = cat_list
        return JsonResponse({'status': 'true', 'items': shops})


class CreateCategory(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            username = request.POST['username']
            title = request.POST['title']
            shop = Shop.objects.get(owner__username__username=username)
            Category.objects.create(shop=shop, title=title)
            return JsonResponse({'status': 'true',
                                 'message': 'Category : {} for shop : {} created successfully'.format(title,
                                                                                                      shop.name)})
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'false', 'message': str(e)})

    def get(self, request):
        username = request.POST['username']
        shop = Shop.objects.get(owner__username__username=username)
        categories = list(Category.objects.filter(shop=shop).values())
        return JsonResponse({'status': 'success', 'items': categories})


class CreateItem(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            username = request.POST['username']
            category_id = request.POST['category_id']
            title = request.POST['title']
            price = request.POST['price']
            description = request.POST['description']
            shop = Shop.objects.get(owner__username__username=username)
            category = Category.objects.get(pk=category_id)
            image1 = request.FILES['image1']
            image2 = request.FILES['image2']
            Item.objects.create(shop=shop, category=category, title=title, description=description, price=price,
                                avatar=image1, avatar_2=image2)
            return JsonResponse({'status': 'true',
                                 'message': 'Item : {} for category : {} from shop : {} created successfully'.format(
                                     title, category.title, shop.name)})

        except  Exception as e:
            return JsonResponse({'status': 'false', 'message': str(e)})


class GetShopItems(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request):

        try:
            shop_id = request.POST.get('shop_id', None)
            category_id = request.POST.get('category_id', None)
            categories = Category.objects.filter(shop__id=shop_id)
            cat_objects = {}
            for cat in categories:
                cat_objects[cat.pk] = cat.title
            if shop_id:
                if not category_id:
                    items = list(Item.objects.filter(shop__id=shop_id).values())
                else:
                    items = list(Item.objects.filter(shop__id=shop_id, category__id=category_id).values())
                for item in items:
                    item['category_title'] = cat_objects[item['category_id']]
                return JsonResponse({'status': 'success', 'items': items})
            else:
                return JsonResponse({'status': 'false', 'message': 'No shop_id were provided'})
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'false', 'message': 'error while receiving data'})


def convert_to_list(string):
    string_list = ast.literal_eval(string)
    return string_list


def random_name(length):
    return ''.join(
        random.choice(string.digits) for _ in range(length))


class SliderImages(APIView):
    def get(self, request):
        items = list(Slider.objects.all().values())
        return JsonResponse({'status': 'true', 'items': items})


class Orders(APIView):
    def post(self, request):
        try:
            items_ids = request.POST['items_ids']
            username = request.POST['username']
            shop_id = request.POST['shop_id']
            user = User.objects.get(username__username=username)
            print(items_ids)
            bill_id = random_name(10)
            items_ids = convert_to_list(items_ids)
            for item_id in items_ids:
                item = Item.objects.get(pk=list(item_id.keys())[0])
                order = Order.objects.create(shop=Shop.objects.get(id=shop_id), item=item, user=user,
                                             quantity=item_id[list(item_id.keys())[0]],
                                             total_price=item_id[list(item_id.keys())[0]] * item.price, bill_id=bill_id)

            return JsonResponse({'status': 'success', 'message': bill_id})
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'false', 'message': str(e)})

    def get(self, request):
        username = request.POST['username']
        user = User.objects.get(username__username=username)
        orders = list(Order.objects.filter(user=user).values())
        for order in orders:
            item = Item.objects.get(pk=order['item_id'])
            shop = Shop.objects.get(pk=order['shop_id'])
            order['title'] = item.title
            order['shop'] = shop.name
            order['username'] = username
            order['username'] = username
            order['price'] = item.price
            order['avatar'] = item.avatar.name
            order['avatar_2'] = item.avatar_2.name

        return JsonResponse({'status': 'true', 'items': orders})


class UploadImage(APIView):
    def post(self, request):
        try:
            order_id = request.POST['order_id']
            image = request.FILES['file']
            order = Order.objects.get(pk=order_id)
            order.image = image
            order.save()
            return JsonResponse({'status': 'true', 'message': 'image uploaded successfully'})
        except Exception as e:
            return JsonResponse({'status': 'false', 'message': str(e)})


class GetUserInfo(APIView):
    def post(self, request):
        username = request.POST['username']
        user = User.objects.get(username__username=username)
        return JsonResponse({'status': 'true', 'user': user})


class GetOrdersItems(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request):

        try:
            username = request.POST.get('username', None)
            category_id = request.POST.get('category_id', None)
            shop = Shop.objects.get(owner__username__username=username)
            categories = Category.objects.filter(shop=shop)
            cat_objects = {}
            for cat in categories:
                cat_objects[cat.pk] = cat.title
            if username:
                if not category_id:
                    items = list(Order.objects.filter(shop=shop).values())
                else:
                    items = list(Order.objects.filter(shop=shop, item__category__id=category_id).values())
                for item in items:
                    te_object = Item.objects.get(pk=item['item_id'])
                    item['category_title'] = te_object.category.title
                    item['avatar'] = te_object.avatar.name
                    item['title'] = te_object.title
                    item['price'] = te_object.price
                    user = User.objects.get(pk=item['user_id'])
                    item['username'] = user.username.username
                return JsonResponse({'status': 'success', 'items': items})
            else:
                return JsonResponse({'status': 'false', 'message': 'No username were provided'})
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'false', 'message': 'error while receiving data'})
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
