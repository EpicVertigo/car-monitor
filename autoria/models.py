from django.db import models


class BaseApiModel(models.Model):
    api_url = None
    value = models.IntegerField()
    name = models.CharField(max_length=100)

    class Meta:
        abstract = True


class TransportCategory(BaseApiModel):
    api_url = 'https://developers.ria.com/auto/categories/'


class TransportBodystyle(BaseApiModel):
    api_url = 'https://developers.ria.com/auto/categories/{categoryId}/bodystyles'
    category = models.ForeignKey(TransportCategory, on_delete=models.CASCADE, related_name='bodystyles')

    class Meta(BaseApiModel.Meta):
        unique_together = ('value', 'category')


class TransportBrand(BaseApiModel):
    api_url = 'https://developers.ria.com/auto/categories/{categoryId}/marks'
    category = models.ForeignKey(TransportCategory, on_delete=models.CASCADE, related_name='brands')

    class Meta(BaseApiModel.Meta):
        unique_together = ('value', 'category')


class TransportModel(BaseApiModel):
    api_url = 'http://api.auto.ria.com/categories/{categoryId}/marks/{markId}/models'
    category = models.ForeignKey(TransportCategory, on_delete=models.CASCADE, related_name='models')
    brand = models.ForeignKey(TransportBrand, on_delete=models.CASCADE, related_name='models')

    class Meta(BaseApiModel.Meta):
        unique_together = ('value', 'brand')


class State(BaseApiModel):
    api_url = 'https://developers.ria.com/auto/states'


class City(BaseApiModel):
    api_url = 'https://developers.ria.com/auto/states/{stateId}/cities'
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='cities')

    class Meta(BaseApiModel.Meta):
        unique_together = ('value', 'state')


class TransportDriverType(BaseApiModel):
    api_url = 'https://developers.ria.com/auto/categories/{categoryId}/driverTypes'
    category = models.ForeignKey(TransportCategory, on_delete=models.CASCADE, related_name='drivertypes')

    class Meta(BaseApiModel.Meta):
        unique_together = ('value', 'category')


class TransportFuelType(BaseApiModel):
    api_url = 'https://developers.ria.com/auto/type'


class TransportGearType(BaseApiModel):
    api_url = 'https://developers.ria.com/auto/categories/{categoryId}/gearboxes'
    category = models.ForeignKey(TransportCategory, on_delete=models.CASCADE, related_name='geartypes')

    class Meta(BaseApiModel.Meta):
        unique_together = ('value', 'category')


class TransportOptions(BaseApiModel):
    api_url = 'https://developers.ria.com/auto/categories/{categoryId}/options'
    category = models.ForeignKey(TransportCategory, on_delete=models.CASCADE, related_name='options')

    class Meta(BaseApiModel.Meta):
        unique_together = ('value', 'category')


class TransportColors(BaseApiModel):
    api_url = 'https://developers.ria.com/auto/colors'


class TransportOrigin(BaseApiModel):
    api_url = 'https://developers.ria.com/auto/countries'
