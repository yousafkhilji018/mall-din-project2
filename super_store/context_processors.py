from store.models import Cart


def cart_context(request):
    cart_item_count = 0
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_item_count = cart.get_item_count()
        except Cart.DoesNotExist:
            pass
    else:
        session_key = request.session.session_key
        if session_key:
            try:
                cart = Cart.objects.get(session_key=session_key)
                cart_item_count = cart.get_item_count()
            except Cart.DoesNotExist:
                pass
    return {'cart_item_count': cart_item_count}
