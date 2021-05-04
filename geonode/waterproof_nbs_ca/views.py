"""
Views for the ``django-WaterproofNbsCa`` application.

"""

import logging

from math import fsum
from geonode.base.enumerations import PROFESSIONAL_ROLES
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from django_libs.views_mixins import AccessMixin
from django.shortcuts import render
from .forms import WaterproofNbsCaForm
from .models import WaterproofNbsCa
from geonode.waterproof_parameters.models import Regions, Countries, Cities
from .models import RiosActivity, RiosTransition,RiosTransformation, ActivityShapefile
from django.contrib.gis.geos import Polygon, MultiPolygon, GEOSGeometry
from django.contrib.gis.gdal import OGRGeometry
from django.core import serializers
from django.views import View
from django import template
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from decimal import Decimal
import json
from shapely.geometry import shape, Point, Polygon
logger = logging.getLogger(__name__)
register = template.Library()


def createNbs(request, countryId):
    # Login required
    if not request.user.is_authenticated:
        return render(request, 'waterproof_nbs_ca/waterproofnbsca_login_error.html')
    else:
        # If is post get the fields, validate & save to DB
        if request.POST.get('action') == 'create-nbs':
            # Get all parameters from form
            nameNBS = request.POST.get('nameNBS')
            descNBS = request.POST.get('descNBS')
            countryNBS = request.POST.get('countryNBS')
            currencyCost = request.POST.get('currencyCost')
            maxBenefitTime = request.POST.get('maxBenefitTime')
            benefitTimePorc = Decimal(request.POST.get('benefitTimePorc').replace(',', '.'))
            maintenancePeriod = request.POST.get('maintenancePeriod')
            implementCost = Decimal(request.POST.get('implementCost').replace(',', '.'))
            maintenanceCost = Decimal(request.POST.get('maintenanceCost').replace(',', '.'))
            oportunityCost = Decimal(request.POST.get('oportunityCost').replace(',', '.'))
            transformations = request.POST.get('riosTransformation')
            extensionFile = request.POST.get('extension')
            riosTransformation = transformations.split(",")
            if (
                nameNBS and descNBS and countryNBS and currencyCost
            ):
                # Check duplicated NBS name
                try:
                    existingNbs = WaterproofNbsCa.objects.get(name=nameNBS)
                    errorMessage = _('Duplicated nbs')
                    context = {
                        'status': '400', 'message': str(errorMessage)
                    }
                    response = HttpResponse(json.dumps(context), content_type='application/json')
                    response.status_code = 400
                    return response
                except WaterproofNbsCa.DoesNotExist:
                    country = Countries.objects.get(id=countryNBS)
                    currency = Countries.objects.get(id=currencyCost)
                    if (extensionFile):
                        # Validate if file is geojson or shapefile
                        if (extensionFile == 'zip'):  # Zip shapefile
                            restrictedArea = request.POST.get('restrictedArea')  # request.FILES used for to get files
                            areaJson = json.loads(restrictedArea)
                        else:  # GeoJSON
                            restrictedArea = request.FILES.get('restrictedArea')  # request.FILES used for to get files
                            areaJson = json.load(restrictedArea)
                        areas = []

                        for feature in areaJson['features']:
                            areaObject = {}
                            areaObject['action'] = feature['properties']['action']
                            areaObject['activity'] = feature['properties']['activity_n']
                            areaObject['geometry'] = GEOSGeometry(str(feature['geometry']))
                            areas.append(areaObject)
                        for area in areas:
                            shapefile = ActivityShapefile.objects.create(
                                action=area['action'],
                                activity=area['activity'],
                                area=area['geometry']
                            )
                            shapefile.save()
                    else:
                        shapefile = None

                    nbs = WaterproofNbsCa(
                        country=country,
                        currency=currency,
                        name=nameNBS,
                        description=descNBS,
                        max_benefit_req_time=maxBenefitTime,
                        profit_pct_time_inter_assoc=benefitTimePorc,
                        unit_implementation_cost=implementCost,
                        unit_maintenance_cost=maintenanceCost,
                        periodicity_maitenance=maintenancePeriod,
                        unit_oportunity_cost=oportunityCost,
                        activity_shapefile=shapefile,
                        added_by=request.user
                    )
                    nbs.save()
                    if (transformations):
                        for trans in riosTransformation:
                            transformation = RiosTransformation.objects.get(id=trans)
                            nbs.rios_transformations.add(transformation)
                    context = {
                        'status': '200', 'message': 'Success'
                    }
                    response = HttpResponse(json.dumps(context), content_type='application/json')
                    response.status_code = 200
                    return response
            else:
                errorMessage = _('Field empty')
                context = {
                    'status': '400', 'message': str(errorMessage)
                }
                response = HttpResponse(json.dumps(context), content_type='application/json')
                response.status_code = 400
                return response
                # Get render form
        else:  # GET METHOD
            nbs = WaterproofNbsCa.objects.all()
            country = Countries.objects.get(id=countryId)
            usaCountry = Countries.objects.get(iso3='USA')
            region = Regions.objects.get(id=country.region_id)
            currency = Countries.objects.get(id=country.id)
            countries = Countries.objects.all()
            currencies = Countries.objects.all()
            transitions = RiosTransition.objects.all()
            riosActivity = RiosActivity.objects.all()
            riosTransformation = RiosTransformation.objects.all()
            if (request.user.professional_role == 'ADMIN'):
                countryEnable = 'disabled'
            else:
                countryEnable = ''
            return render(
                request, 'waterproof_nbs_ca/waterproofnbsca_form.html',
                {
                    'country': country,
                    'usaCountry': usaCountry,
                    'countryEnable': countryEnable,
                    'region': region,
                    'currency': currency,
                    'nbs': nbs,
                    'countries': countries,
                    'currencies': currencies,
                    'transitions': transitions,
                    'riosActivity': riosActivity,
                    'riosTransformation': riosTransformation
                }
            )


def listNbs(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            if (request.user.professional_role == 'ADMIN'):
                userCountry = Countries.objects.get(iso3=request.user.country)
                nbs = WaterproofNbsCa.objects.all()
                region = Regions.objects.get(id=userCountry.region_id)
                currency = Countries.objects.get(id=userCountry.id)
                return render(
                    request,
                    'waterproof_nbs_ca/waterproofnbsca_list.html',
                    {
                        'nbs': nbs,
                        'userCountry': userCountry,
                        'region': region,
                        'currency': currency
                    }
                )

            if (request.user.professional_role == 'ANALYS'):
                nbs = WaterproofNbsCa.objects.all()
                userCountry = Countries.objects.get(iso3=request.user.country)
                region = Regions.objects.get(id=userCountry.region_id)
                currency = Countries.objects.get(id=userCountry.id)
                return render(
                    request,
                    'waterproof_nbs_ca/waterproofnbsca_list.html',
                    {
                        'nbs': nbs,
                        'userCountry': userCountry,
                        'region': region,
                        'currency': currency
                    }
                )

            if (request.user.professional_role == 'COPART'):
                nbs = WaterproofNbsCa.objects.all()
                userCountry = Countries.objects.get(iso3=request.user.country)
                region = Regions.objects.get(id=userCountry.region_id)
                currency = Countries.objects.get(id=userCountry.id)
                return render(
                    request,
                    'waterproof_nbs_ca/waterproofnbsca_list.html',
                    {
                        'nbs': nbs,
                        'userCountry': userCountry,
                        'region': region,
                        'currency': currency
                    }
                )

            if (request.user.professional_role == 'ACDMC'):
                nbs = WaterproofNbsCa.objects.all()
                userCountry = Countries.objects.get(iso3=request.user.country)
                region = Regions.objects.get(id=userCountry.region_id)
                currency = Countries.objects.get(id=userCountry.id)
                return render(
                    request,
                    'waterproof_nbs_ca/waterproofnbsca_list.html',
                    {
                        'nbs': nbs,
                        'userCountry': userCountry,
                        'region': region,
                        'currency': currency
                    }
                )

            if (request.user.professional_role == 'SCADM'):
                nbs = WaterproofNbsCa.objects.all()
                userCountry = Countries.objects.get(iso3=request.user.country)
                region = Regions.objects.get(id=userCountry.region_id)
                currency = Countries.objects.get(id=userCountry.id)
                return render(
                    request,
                    'waterproof_nbs_ca/waterproofnbsca_list.html',
                    {
                        'nbs': nbs,
                        'userCountry': userCountry,
                        'region': region,
                        'currency': currency
                    }
                )

            if (request.user.professional_role == 'MCOMC'):
                nbs = WaterproofNbsCa.objects.all()
                userCountry = Countries.objects.get(iso3=request.user.country)
                region = Regions.objects.get(id=userCountry.region_id)
                currency = Countries.objects.get(id=userCountry.id)
                return render(
                    request,
                    'waterproof_nbs_ca/waterproofnbsca_list.html',
                    {
                        'nbs': nbs,
                        'userCountry': userCountry,
                        'region': region,
                        'currency': currency
                    }
                )

            if (request.user.professional_role == 'CITIZN'):
                nbs = WaterproofNbsCa.objects.all()
                userCountry = Countries.objects.get(iso3=request.user.country)
                region = Regions.objects.get(id=userCountry.region_id)
                currency = Countries.objects.get(id=userCountry.id)
                return render(
                    request,
                    'waterproof_nbs_ca/waterproofnbsca_list.html',
                    {
                        'nbs': nbs,
                        'userCountry': userCountry,
                        'region': region,
                        'currency': currency
                    }
                )

            if (request.user.professional_role == 'REPECS'):
                nbs = WaterproofNbsCa.objects.all()
                userCountry = Countries.objects.get(iso3=request.user.country)
                region = Regions.objects.get(id=userCountry.region_id)
                currency = Countries.objects.get(id=userCountry.id)
                return render(
                    request,
                    'waterproof_nbs_ca/waterproofnbsca_list.html',
                    {
                        'nbs': nbs,
                        'userCountry': userCountry,
                        'region': region,
                        'currency': currency
                    }
                )

            if (request.user.professional_role == 'OTHER'):
                nbs = WaterproofNbsCa.objects.all()
                userCountry = Countries.objects.get(iso3=request.user.country)
                region = Regions.objects.get(id=userCountry.region_id)
                currency = Countries.objects.get(id=userCountry.id)
                return render(
                    request,
                    'waterproof_nbs_ca/waterproofnbsca_list.html',
                    {
                        'nbs': nbs,
                        'userCountry': userCountry,
                        'region': region,
                        'currency': currency
                    }
                )
        else:
            nbs = WaterproofNbsCa.objects.all()
            userCountry = Countries.objects.get(iso3='COL')
            region = Regions.objects.get(id=userCountry.region_id)
            currency = Countries.objects.get(id=userCountry.id)
            return render(
                request,
                'waterproof_nbs_ca/waterproofnbsca_list.html',
                {
                    'nbs': nbs,
                    'userCountry': userCountry,
                    'region': region,
                    'currency': currency
                }
            )


def editNbs(request, idx):
    if not request.user.is_authenticated:
        return render(request, 'waterproof_nbs_ca/waterproofnbsca_login_error.html')
    else:
        if request.method == 'GET':
            countries = Countries.objects.all()
            currencies = Countries.objects.all()
            usaCountry = Countries.objects.get(iso3='USA')
            filterNbs = WaterproofNbsCa.objects.get(id=idx)
            country = Countries.objects.get(id=filterNbs.country_id)
            transitions = RiosTransition.objects.all()
            riosActivity = RiosActivity.objects.all()
            riosTransformation = RiosTransformation.objects.all()
            selectedTransformations = list(filterNbs.rios_transformations.all().values_list('id', flat=True))
            if (len(selectedTransformations) > 0):
                selectedTransition = filterNbs.rios_transformations.first().activity.transition
            else:
                selectedTransition = ''
            if (request.user.professional_role == 'ADMIN'):
                countryEnable = 'disabled'
            else:
                countryEnable = ''
            return render(
                request, 'waterproof_nbs_ca/waterproofnbsca_edit.html',
                {
                    'nbs': filterNbs,
                    'countries': countries,
                    'country': country,
                    'usaCountry': usaCountry,
                    'countryEnable': countryEnable,
                    'currencies': currencies,
                    'transitions': transitions,
                    'riosActivity': riosActivity,
                    'riosTransformation': riosTransformation,
                    'selectedTransf': selectedTransformations,
                    'selectedTransition': selectedTransition
                }
            )
        else:
            duplicatedNbs = True
            # Get all parameters from form
            nameNBS = request.POST.get('nameNBS')
            descNBS = request.POST.get('descNBS')
            countryNBS = request.POST.get('countryNBS')
            currencyCost = request.POST.get('currencyCost')
            maxBenefitTime = request.POST.get('maxBenefitTime')
            benefitTimePorc = Decimal(request.POST.get('benefitTimePorc').replace(',', '.'))
            maintenancePeriod = request.POST.get('maintenancePeriod')
            implementCost = Decimal(request.POST.get('implementCost').replace(',', '.'))
            maintenanceCost = Decimal(request.POST.get('maintenanceCost').replace(',', '.'))
            oportunityCost = Decimal(request.POST.get('oportunityCost').replace(',', '.'))
            transformations = request.POST.get('riosTransformation')
            riosTransformation = transformations.split(",")
            riosTransformation = list(map(int, riosTransformation))
            uploadNewArea = request.POST.get('uploadNewArea')
            if (
                    nameNBS and descNBS and countryNBS and currencyCost
                    and maxBenefitTime and benefitTimePorc and maintenancePeriod
                    and implementCost and maintenanceCost and oportunityCost

            ):
                # Check duplicated NBS name
                try:
                    existingNbs = WaterproofNbsCa.objects.get(name=nameNBS)
                    if (existingNbs.pk == idx):
                        duplicatedNbs = False
                    else:
                        duplicatedNbs = True
                        errorMessage = _('Duplicated nbs')
                        context = {
                            'status': '400', 'message': str(errorMessage)
                        }
                        response = HttpResponse(json.dumps(context), content_type='application/json')
                        response.status_code = 400
                        return response
                except WaterproofNbsCa.DoesNotExist:
                    duplicatedNbs = False
                if (not duplicatedNbs):
                    country = Countries.objects.get(id=countryNBS)
                    currency = Countries.objects.get(id=currencyCost)
                    nbs = WaterproofNbsCa.objects.get(id=idx)
                    if(nbs.activity_shapefile != None):
                        shapefile = ActivityShapefile.objects.get(id=nbs.activity_shapefile.id)
                    else:
                        shapefile = None
                    actualTranstormations = list(nbs.rios_transformations.all().values_list('id', flat=True))
                    # Get land use to add in edition
                    transformationsAdd = [item for item in riosTransformation if item not in actualTranstormations]
                    # Get land use to remove from DB
                    transformationsRemove = [item for item in actualTranstormations if item not in riosTransformation]
                    # Add not existing transformations selected for the user
                    for trans in transformationsAdd:
                        transformation = RiosTransformation.objects.get(id=trans)
                        nbs.rios_transformations.add(transformation)
                    # Remove unselected options for user
                    for trans in transformationsRemove:
                        transformation = RiosTransformation.objects.get(id=trans)
                        nbs.rios_transformations.remove(transformation)
                    # Validate if active upload new restricted area

                    if (uploadNewArea == 'true'):  # upload
                        if (extensionFile):
                            extensionFile = request.POST.get('extension')
                            if (extensionFile == 'zip'):  # Zip shapefile
                                # request.FILES used for to get files
                                restrictedArea = request.POST.get('restrictedArea')
                                areaJson = json.loads(restrictedArea)
                            else:  # GeoJSON
                                # request.FILES used for to get files
                                restrictedArea = request.FILES.get('restrictedArea')
                                areaJson = json.load(restrictedArea)
                            areas = []

                            for feature in areaJson['features']:
                                areaObject = {}
                                areaObject['name'] = areaJson['fileName']
                                areaObject['action'] = feature['properties']['action']
                                areaObject['activity'] = feature['properties']['activity_n']
                                areaObject['geometry'] = GEOSGeometry(str(feature['geometry']))
                                areas.append(areaObject)
                            for area in areas:
                                shapefile.action = areaObject['action']
                                shapefile.activity = areaObject['activity']
                                shapefile.area = areaObject['geometry']
                                shapefile.save()

                    nbs.name = nameNBS
                    nbs.description = descNBS
                    nbs.country = country
                    nbs.currency = currency
                    nbs.max_benefit_req_time = maxBenefitTime
                    nbs.profit_pct_time_inter_assoc = benefitTimePorc
                    nbs.unit_implementation_cost = implementCost
                    nbs.unit_maintenance_cost = maintenanceCost
                    nbs.periodicity_maitenance = maintenancePeriod
                    nbs.unit_oportunity_cost = oportunityCost
                    nbs.save()
                    context = {
                        'status': '200', 'message': 'Success'
                    }
                    response = HttpResponse(json.dumps(context), content_type='application/json')
                    response.status_code = 200
                    return response
            else:
                errorMessage = _('Field empty')
                context = {
                    'status': '400', 'message': str(errorMessage)
                }
                response = HttpResponse(json.dumps(context), content_type='application/json')
                response.status_code = 400
                return response


def cloneNbs(request, idx):
    if not request.user.is_authenticated:
        return render(request, 'waterproof_nbs_ca/waterproofnbsca_login_error.html')
    else:
        if request.method == 'GET':
            countries = Countries.objects.all()
            currencies = Countries.objects.all()
            usaCountry = Countries.objects.get(iso3='USA')
            userCountry = Countries.objects.get(iso3=request.user.country)
            filterNbs = WaterproofNbsCa.objects.get(id=idx)
            country = Countries.objects.get(id=filterNbs.country_id)
            transitions = RiosTransition.objects.all()
            riosActivity = RiosActivity.objects.all()
            riosTransformation = RiosTransformation.objects.all()
            selectedTransformations = list(filterNbs.rios_transformations.all().values_list('id', flat=True))
            selectedTransition = filterNbs.rios_transformations.first().activity.transition
            if (request.user.professional_role == 'ADMIN'):
                countryEnable = 'disabled'
            else:
                countryEnable = ''
            return render(
                request, 'waterproof_nbs_ca/waterproofnbsca_clone.html',
                {
                    'nbs': filterNbs,
                    'countries': countries,
                    'userCountry': userCountry,
                    'country': country,
                    'usaCountry': usaCountry,
                    'countryEnable': countryEnable,
                    'currencies': currencies,
                    'transitions': transitions,
                    'riosActivity': riosActivity,
                    'riosTransformation': riosTransformation,
                    'selectedTransf': selectedTransformations,
                    'selectedTransition': selectedTransition
                }
            )
        else:
            # Get all parameters from form
            nameNBS = request.POST.get('nameNBS')
            descNBS = request.POST.get('descNBS')
            countryNBS = request.POST.get('countryNBS')
            currencyCost = request.POST.get('currencyCost')
            maxBenefitTime = request.POST.get('maxBenefitTime')
            benefitTimePorc = request.POST.get('benefitTimePorc')
            maintenancePeriod = request.POST.get('maintenancePeriod')
            implementCost = request.POST.get('implementCost')
            maintenanceCost = request.POST.get('maintenanceCost')
            oportunityCost = request.POST.get('oportunityCost')
            transformations = request.POST.get('riosTransformation')
            uploadNewArea = request.POST.get('uploadNewArea')
            nbs = WaterproofNbsCa.objects.get(id=idx)
            riosTransformation = transformations.split(",")
            if (
                nameNBS and descNBS and countryNBS and currencyCost
                and maxBenefitTime and benefitTimePorc and maintenancePeriod
                and implementCost and maintenanceCost and oportunityCost
            ):
                # Check duplicated NBS name
                try:
                    existingNbs = WaterproofNbsCa.objects.get(name=nameNBS)
                    errorMessage = _('Duplicated nbs')
                    context = {
                        'status': '400', 'message': str(errorMessage)
                    }
                    response = HttpResponse(json.dumps(context), content_type='application/json')
                    response.status_code = 400
                    return response
                except WaterproofNbsCa.DoesNotExist:
                    # Validate if user want's to upload new area
                    if (uploadNewArea == 'true'):  # Upload new area
                        extensionFile = request.POST.get('extension')
                        if (extensionFile == 'zip'):  # Zip shapefile
                            restrictedArea = request.POST.get('restrictedArea')  # request.FILES used for to get files
                            areaJson = json.loads(restrictedArea)
                        else:  # GeoJSON
                            restrictedArea = request.FILES.get('restrictedArea')  # request.FILES used for to get files
                            areaJson = json.load(restrictedArea)
                        areas = []

                        for feature in areaJson['features']:
                            areaObject = {}
                            areaObject['name'] = areaJson['fileName']
                            areaObject['action'] = feature['properties']['action']
                            areaObject['activity'] = feature['properties']['activity_n']
                            areaObject['geometry'] = GEOSGeometry(str(feature['geometry']))
                            areas.append(areaObject)
                        shapefile = ActivityShapefile(
                            action=areaObject['action'],
                            activity=areaObject['activity'],
                            area=areaObject['geometry']
                        )
                        shapefile.save()
                    else:  # Maitain same area
                        if(nbs.activity_shapefile != None):
                            shapefileOld = ActivityShapefile.objects.get(id=nbs.activity_shapefile.id)
                            shapefileOld = ActivityShapefile.objects.get(id=nbs.activity_shapefile.id)
                            shapefile = ActivityShapefile(
                                action=shapefileOld.action,
                                activity=shapefileOld.activity,
                                area=shapefileOld.area
                            )
                            shapefile.save()
                        else:
                            shapefile = None

                    country = Countries.objects.get(id=countryNBS)
                    currency = Countries.objects.get(id=currencyCost)
                    nbs = WaterproofNbsCa(
                        country=country,
                        currency=currency,
                        name=nameNBS,
                        description=descNBS,
                        max_benefit_req_time=maxBenefitTime,
                        profit_pct_time_inter_assoc=benefitTimePorc,
                        unit_implementation_cost=implementCost,
                        unit_maintenance_cost=maintenanceCost,
                        periodicity_maitenance=maintenancePeriod,
                        unit_oportunity_cost=oportunityCost,
                        activity_shapefile=shapefile,
                        added_by=request.user
                    )
                    nbs.save()
                    if (transformations):
                        for trans in riosTransformation:
                            transformation = RiosTransformation.objects.get(id=trans)
                            nbs.rios_transformations.add(transformation)
                    context = {
                        'status': '200', 'message': 'Success'
                    }
                    response = HttpResponse(json.dumps(context), content_type='application/json')
                    response.status_code = 200
                    return response
            else:
                errorMessage = _('Field empty')
                context = {
                    'status': '400', 'message': str(errorMessage)
                }
                response = HttpResponse(json.dumps(context), content_type='application/json')
                response.status_code = 400
                return response


def viewNbs(request, idx):
    filterNbs = WaterproofNbsCa.objects.filter(id=idx)
    nbs = WaterproofNbsCa.objects.get(id=idx)
    country = Countries.objects.get(id=nbs.country_id)
    countries = Countries.objects.all()
    userCountry = Countries.objects.get(iso3=request.user.country)
    region = Regions.objects.get(id=nbs.country.region_id)
    currency = Countries.objects.get(id=country.id)
    currencies = Countries.objects.all()
    transitions = RiosTransition.objects.all()
    riosTransition = RiosActivity.objects.filter(transition_id=2)
    return render(request, 'waterproof_nbs_ca/waterproofnbsca_detail_list.html',
                  {
                      'region': region,
                      'userCountry': userCountry,
                      'country': country,
                      'nbs': filterNbs,
                      'currency': currency,
                      'countries': countries,
                      'currencies': currencies,
                      'riosTransition': riosTransition,
                      'transitions': transitions
                  }
                  )


def deleteNbs(request, idx):
    if request.method == "POST":
        nbs = WaterproofNbsCa.objects.get(id=idx)
        if not nbs:
            context = {
                'status': '400', 'reason': 'NBS not found'
            }
            response = HttpResponse(json.dumps(context), content_type='application/json')
            response.status_code = 400
            return response
        else:
            # delete object
            nbs.delete()
            # after deleting redirect to
            # home page
            context = {
                'status': '200', 'reason': 'sucess'
            }
            response = HttpResponse(json.dumps(context), content_type='application/json')
            response.status_code = 200
            return response


def loadAllTransitions(request):
    transitions = RiosTransition.objects.all()
    transitions_serialized = serializers.serialize('json', transitions)
    return JsonResponse(transitions_serialized, safe=False)


def loadActivityByTransition(request):
    transition = request.GET.get('transition')
    activities = RiosActivity.objects.filter(transition_id=transition)
    activities_serialized = serializers.serialize('json', activities)
    return JsonResponse(activities_serialized, safe=False)


def loadTransformationbyActivity(request):
    activity = request.GET.get('activity')
    trasformations = RiosTransformation.objects.filter(activity_id=activity)
    transformations_serialized = serializers.serialize('json', trasformations)
    return JsonResponse(transformations_serialized, safe=False)
