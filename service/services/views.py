from django.conf import settings
from django.db.models import F, Sum
from rest_framework.viewsets import ReadOnlyModelViewSet
from services.models import Subscription
from django.core.cache import cache
from services.serializers import SubscriptionSerializer


class SubscriptionView(ReadOnlyModelViewSet):
    queryset = Subscription.objects.all().select_related('plan', 'client', 'client__user').only(
        'client__user__email',
        'client__company_name',
        'plan_id',
    )  # .annotate(price=F('service__full_price') -
    #                  F('service__full_price') * (F('plan__discount_percent') / 100.00))
    serializer_class = SubscriptionSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        response = super().list(request, *args, **kwargs)

        price_cache = cache.get(settings.PRICE_CACHE)

        if price_cache:
            total_price = price_cache
        else:
            total_price = queryset.aggregate(total=Sum('price')).get('total')
            cache.set(settings.PRICE_CACHE, total_price, 60*60)

        response_data = {'result': response.data, 'total_amount': total_price}
        response.data = response_data
        return response
