from django.db.models import F, Sum
from rest_framework.viewsets import ReadOnlyModelViewSet
from services.models import Subscription
from services.serializers import SubscriptionSerializer


class SubscriptionView(ReadOnlyModelViewSet):
    queryset = Subscription.objects.all().select_related('plan', 'client', 'client__user').only(
        'client__user__email',
        'client__company_name',
        'plan_id',
    ).annotate(price=F('service__full_price') -
                     F('service__full_price') * (F('plan__discount_percent') / 100.00))
    serializer_class = SubscriptionSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        response = super().list(request, *args, **kwargs)

        response_data = {'result': response.data}
        response_data['total_amount'] = queryset.aggregate(total=Sum('price')).get('total')
        response.data = response_data
        return response
