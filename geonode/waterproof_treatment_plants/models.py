from django.db import models
from django.conf import settings
from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
from geonode.waterproof_parameters.models import Cities
from geonode.waterproof_intake.models import ElementSystem

class Header(models.Model):
    plant_name = models.CharField(max_length=100,verbose_name=_('Name Plant'))
    plant_description = models.CharField(max_length=300,verbose_name=_('Description Plant'))
    plant_suggest = models.CharField(max_length=1,verbose_name=_('Suggest Plant'))
    plant_user = models.CharField(max_length=100,verbose_name=_('User Plant'))
    plant_date_create = models.DateTimeField(auto_now=True,verbose_name=_('Date Create Plant'))
    plant_date_update = models.DateTimeField(auto_now=True,verbose_name=_('Date Update Plant'))
    plant_city = models.ForeignKey(Cities, on_delete=models.CASCADE, null=True)

class Function(models.Model):
    function_name = models.CharField(max_length=100,verbose_name=_('Name Function'))
    function_graph_id = models.CharField(max_length=100,verbose_name=_('Graph Id Function'))
    function_value = models.CharField(max_length=300,verbose_name=_('Value Function'))
    function_currency = models.CharField(max_length=1,verbose_name=_('Currency Function'))
    function_factor = models.CharField(max_length=100,verbose_name=_('Factor'))
    function_id_sub_process = models.CharField(max_length=100,verbose_name=_('Sub Process'))
    function_user = models.CharField(max_length=100,verbose_name=_('User'))
    function_date_create = models.DateTimeField(auto_now=True,verbose_name=_('Date Create'))
    function_date_update = models.DateTimeField(auto_now=True, verbose_name=_('Date Update'))
    function_transported_water = models.CharField(max_length=100,verbose_name=_('Water'))
    function_sediments_retained = models.CharField(max_length=100,verbose_name=_('Sediments'))
    function_nitrogen_retained = models.CharField(max_length=100,verbose_name=_('Nitrogen'))
    function_phosphorus_retained = models.CharField(max_length=100,verbose_name=_('Phosphorus'))
    function_technology = models.CharField(max_length=100,verbose_name=_('Technology'))
    function_plant = models.ForeignKey(Header, on_delete=models.CASCADE, null=True)

class Element(models.Model):
    element_normalize_category = models.CharField(max_length=100,verbose_name=_('Name Element'))
    element_graph_id = models.IntegerField(verbose_name=_('Id Graph'))
    element_on_off = models.BooleanField(default=False, verbose_name=_('On off Element'))
    element_q_l = models.FloatField(null=True,blank=True,default=None,verbose_name=_('Q L Element'))
    element_awy = models.FloatField(null=True,blank=True,default=None,verbose_name=_('Awy Element'))
    element_cn_mg_l = models.FloatField(null=True,blank=True,default=None,verbose_name=_('CN Mg L Element'))
    element_cp_mg_l = models.FloatField(null=True,blank=True,default=None,verbose_name=_('CP Mg L Element'))
    element_csed_mg_l = models.FloatField(null=True,blank=True,default=None,verbose_name=_('Mg L Csed Element'))
    element_wn_kg = models.FloatField(null=True,blank=True,default=None,verbose_name=_('Wn Kg Element'))
    element_wn_rent_kg = models.FloatField(null=True,blank=True,default=None,verbose_name=_('Wn Rent Kg Element'))
    element_wp_rent_ton = models.FloatField(null=True,blank=True,default=None,verbose_name=_('Wn Rent Ton Element'))
    element_wsed_tom = models.FloatField(null=True,blank=True,default=None,verbose_name=_('Wsed Ton Element'))
    element_wp_kg = models.FloatField(null=True,blank=True,default=None,verbose_name=_('Wp Kg Element'))
    element_user = models.CharField(max_length=100,verbose_name=_('User Element'))
    element_date_create = models.DateTimeField(auto_now=True,verbose_name=_('Date Create Element'))
    element_date_update = models.DateTimeField(auto_now=True,verbose_name=_('Date Update Element'))
    element_plant = models.ForeignKey(Header, on_delete=models.CASCADE, null=True)

class Csinfra(models.Model):
    csinfra_user = models.CharField(max_length=100,verbose_name=_('User'))
    csinfra_date_create = models.DateTimeField(auto_now=True,verbose_name=_('Date Create'))
    csinfra_date_update = models.DateTimeField(auto_now=True,verbose_name=_('Date Update'))
    csinfra_elementsystem = models.ForeignKey(ElementSystem, on_delete=models.CASCADE)
    csinfra_plant = models.ForeignKey(Header, on_delete=models.CASCADE, null=True)

class Ptap(models.Model):
    ptap_user = models.CharField(max_length=100,verbose_name=_('User'))
    ptap_type = models.CharField(max_length=100,verbose_name=_('Type ptap'))
    ptap_date_create = models.DateTimeField(auto_now=True,verbose_name=_('Date Update'))
    ptap_awy = models.FloatField(null=True,blank=True,default=None,verbose_name=_('Awy ptap'))
    ptap_cn = models.FloatField(null=True,blank=True,default=None,verbose_name=_('Cn ptap'))
    ptap_cp = models.FloatField(null=True,blank=True,default=None,verbose_name=_('Cp ptap'))
    ptap_cs = models.FloatField(null=True,blank=True,default=None,verbose_name=_('Cs ptap'))
    ptap_wn = models.FloatField(null=True,blank=True,default=None,verbose_name=_('Wn ptap'))
    ptap_wp = models.FloatField(null=True,blank=True,default=None,verbose_name=_('Wp ptap'))
    ptap_ws = models.FloatField(null=True,blank=True,default=None,verbose_name=_('Ws ptap'))
    ptap_plant = models.ForeignKey(Header, on_delete=models.CASCADE, null=True)