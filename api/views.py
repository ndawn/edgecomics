from django.http import JsonResponse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from commerce.models import CartItem, Item
from json.decoder import JSONDecodeError
import time
import json


# TODO: разделить вьюхи для аккаунтов и коммерции по файлам, сделать для аккаунтов апи:
# TODO: в моделях методы по аналогии с коммерцией - as_dict(),
# TODO: вьюхи - get, register, login, logout, update, remove
# TODO: в register сделать капчу


class CartView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if not request.user.is_anonymous:
            return JsonResponse({'response': CartItem.cart.get_list(request.user)})
        else:
            CartView.update_anonymous_cart(request.session.setdefault('cart', []))

            return JsonResponse({'response': request.session.setdefault('cart', [])})

    def post(self, request, *args, **kwargs):
        method = kwargs.get('method', '')

        if method == '':
            return self.get(request, *args, **kwargs)

        if request.user.is_anonymous:
            CartView.update_anonymous_cart(request.session.setdefault('cart', []))

        if hasattr(CartView, kwargs.get('method', '')):
            return getattr(CartView, method)(request)
        else:
            return JsonResponse({'error': 'invalid request'}, status=400)

    @staticmethod
    def update_anonymous_cart(cart):
        updated = []

        for cart_item in cart:
            try:
                item = Item.objects.get(id=cart_item['item']['id'])

                if not item.active:
                    continue
            except ObjectDoesNotExist:
                continue

            if cart_item['item']['quantity'] != item.quantity:
                cart_item['item']['quantity'] = item.quantity

            updated.append(cart_item)

        cart[:] = updated

    @staticmethod
    def add(request):
        try:
            item_id = json.loads(request.body.decode('utf-8'))['id']
        except (KeyError, JSONDecodeError):
            return JsonResponse({'error': 'invalid request'}, status=400)
        except:
            return JsonResponse({'error': 'server error'}, status=500)

        if not request.user.is_anonymous:
            CartItem.cart.add(request.user, item_id)

            return JsonResponse({'response': CartItem.cart.get_list(request.user)})
        else:
            request.session.modified = True

            cart = request.session.setdefault('cart', [])

            try:
                item = Item.objects.get(id=item_id)

                if not item.active:
                    return JsonResponse({'response': cart})
            except ObjectDoesNotExist:
                return JsonResponse({'response': cart})

            cart_item = {
                'id': str(time.time()),
                'quantity': 1,
                'item': item.as_dict(),
            }

            cart.append(cart_item)

            return JsonResponse({'response': cart})

    @staticmethod
    def update(request):
        try:
            payload = json.loads(request.body.decode('utf-8'))
            item_id = payload.get('id')
            item_quantity = payload.get('quantity')
        except JSONDecodeError:
            return JsonResponse({'error': 'invalid request'}, status=400)

        if not request.user.is_anonymous:
            resp_tuple = CartItem.cart.update(item_id, item_quantity)

            if resp_tuple[0]:
                return JsonResponse({'response': CartItem.cart.get_list(request.user)})
            else:
                return JsonResponse({'error': resp_tuple[1]}, status=resp_tuple[2])
        else:
            request.session.modified = True

            cart = request.session.setdefault('cart', [])

            for i in range(len(cart)):
                if cart[i]['id'] == item_id:
                    cart_item = cart[i]

                    try:
                        item = Item.objects.get(id=cart_item['item']['id'])

                        if not item.active:
                            del cart[i]

                            return JsonResponse({'response': cart})
                    except ObjectDoesNotExist:
                        del cart[i]

                        return JsonResponse({'response': cart})

                    if item_quantity <= 0:
                        del cart[i]

                        return JsonResponse({'response': cart})
                    elif item_quantity >= item.quantity:
                        cart_item['quantity'] = item.quantity

                        return JsonResponse({'response': cart})
                    else:
                        cart_item['quantity'] = item_quantity

                        return JsonResponse({'response': cart})

                return JsonResponse({'error': 'object does not exist'}, status=404)

    @staticmethod
    def remove(request):
        try:
            item_id = json.loads(request.body.decode('utf-8'))['id']
        except (KeyError, JSONDecodeError):
            return JsonResponse({'error': 'invalid request'}, status=400)
        except:
            return JsonResponse({'error': 'server error'}, status=500)

        if not request.user.is_anonymous:
            CartItem.cart.remove(item_id)

            return JsonResponse({'response': CartItem.cart.get_list(request.user)})
        else:
            request.session.modified = True

            cart = request.session.setdefault('cart', [])

            for i in range(len(cart)):
                if cart[i]['id'] == item_id:
                    del cart[i]
                    break

            return JsonResponse({'response': cart})

    @staticmethod
    def clear(request):
        if not request.user.is_anonymous:
            return JsonResponse({'response': CartItem.cart.clear(request.user)})
        else:
            cart = request.session.setdefault('cart', []).clear()

            return JsonResponse({'response': cart})
