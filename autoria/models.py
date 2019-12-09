from django.db import models
from autoria.utils.decorators import periodic_task
from django_celery_beat.models import PeriodicTask
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator


@periodic_task
class MonitorQuery(PeriodicTask):
    default_task = 'autoria.tasks.monitor_query'
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='monitors')
    average_price = models.IntegerField(null=True, blank=True)
    query_string = models.CharField(max_length=100)


class BaseApiModel(models.Model):
    api_url = None
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class TransportCategory(BaseApiModel):
    api_url = 'https://developers.ria.com/auto/categories/'


class TransportBodystyle(BaseApiModel):
    api_url = 'https://developers.ria.com/auto/categories/{categoryId}/bodystyles'
    category = models.ForeignKey(TransportCategory, on_delete=models.CASCADE, related_name='bodystyles')

    class Meta(BaseApiModel.Meta):
        unique_together = ('id', 'category')


class TransportBrand(BaseApiModel):
    api_url = 'https://developers.ria.com/auto/categories/{categoryId}/marks'
    category = models.ForeignKey(TransportCategory, on_delete=models.CASCADE, related_name='brands')

    class Meta(BaseApiModel.Meta):
        unique_together = ('id', 'category')


class TransportModel(BaseApiModel):
    api_url = 'http://api.auto.ria.com/categories/{categoryId}/marks/{markId}/models'
    category = models.ForeignKey(TransportCategory, on_delete=models.CASCADE, related_name='models')
    brand = models.ForeignKey(TransportBrand, on_delete=models.CASCADE, related_name='models')

    class Meta(BaseApiModel.Meta):
        unique_together = ('id', 'brand')


class State(BaseApiModel):
    api_url = 'https://developers.ria.com/auto/states'


class City(BaseApiModel):
    api_url = 'https://developers.ria.com/auto/states/{stateId}/cities'
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='cities')

    class Meta(BaseApiModel.Meta):
        unique_together = ('id', 'state')


class TransportDriverType(BaseApiModel):
    api_url = 'https://developers.ria.com/auto/categories/{categoryId}/driverTypes'
    category = models.ForeignKey(TransportCategory, on_delete=models.CASCADE, related_name='drivertypes')

    class Meta(BaseApiModel.Meta):
        unique_together = ('id', 'category')


class TransportFuelType(BaseApiModel):
    api_url = 'https://developers.ria.com/auto/type'


class TransportGearType(BaseApiModel):
    api_url = 'https://developers.ria.com/auto/categories/{categoryId}/gearboxes'
    category = models.ForeignKey(TransportCategory, on_delete=models.CASCADE, related_name='geartypes')

    class Meta(BaseApiModel.Meta):
        unique_together = ('id', 'category')


class TransportOptions(BaseApiModel):
    api_url = 'https://developers.ria.com/auto/categories/{categoryId}/options'
    category = models.ForeignKey(TransportCategory, on_delete=models.CASCADE, related_name='options')

    class Meta(BaseApiModel.Meta):
        unique_together = ('id', 'category')


class TransportColors(BaseApiModel):
    api_url = 'https://developers.ria.com/auto/colors'


class TransportOrigin(BaseApiModel):
    api_url = 'https://developers.ria.com/auto/countries'


class MonitorResult(models.Model):
    monitor = models.ForeignKey(MonitorQuery, on_delete=models.CASCADE, related_name='results')
    brand = models.ForeignKey(TransportBrand, on_delete=models.SET_NULL, null=True, related_name='results')
    model = models.ForeignKey(TransportModel, on_delete=models.SET_NULL, null=True, related_name='results')
    year = models.IntegerField(validators=[MinLengthValidator(1900), MaxLengthValidator(2050)])
    title = models.CharField(max_length=250)
    uri = models.CharField(max_length=250)


class MonitorPriceChangeEvent(models.Model):
    old_price = models.IntegerField()
    new_price = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    announced = models.BooleanField(default=True)
    result = models.ForeignKey(MonitorResult, on_delete=models.CASCADE, related_name='events')

    @property
    def difference(self):
        return NotImplementedError

    def __str__(self):
        return f'Price change event: {self.id}'
