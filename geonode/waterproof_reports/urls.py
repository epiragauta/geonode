
from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.reportMenu, name='reports'),
    path('data', views.pivot_data, name='pivot_data'),
    path('physical/', views.physicalIndicators, name='physical'),
    path('financial/', views.financialIndicators, name='financial'),
    path('decision/', views.decisionIndicators, name='decision'),
    path('getSensibilityAnalysisCost/', api.getSensibilityAnalysisCost, name='get-sensibility-analysis-cost'),
    path('getSensibilityAnalysisBenefits/', api.getSensibilityAnalysisBenefits, name='get-sensibility-analysis-benefits'),
    path('getSensibilityAnalysisCostVsBenefit/', api.getSensibilityAnalysisCostVsBenefit, name='get-sensibility-analysis-cost-vs-benefit'),
    path('getSensibilityAnalysisReturnOfInvest/', api.getSensibilityAnalysisReturnOfInvest, name='get-sensibility-analysis-return-of-invest'),
    path('getNetPresentValueSummary/', api.getNetPresentValueSummary, name='get-net-present-value-summary'),
    path('getCostAndBenefit/', api.getCostAndBenefit, name='get_cost_and_benefit'),
    path('getTotalBenefitsForMilion/', api.getTotalBenefitsForMilion, name='get_total_benefits_for_milion'),
    path('getReportCostsAnalysisRoi/', api.getReportCostsAnalysisRoi, name='get_report_costs_analysis_roi'),
    path('getReportCostsAnalysisFilter/', api.getReportCostsAnalysisFilter, name='get_report_costs_analysis_filter'),
    path('getReportAnalysisBenefitsFilter/', api.getReportAnalysisBenefitsFilter, name='get_report_analysis_benefits_filter'),
    path('getReportCostsAnalysisFilter/', api.getReportCostsAnalysisFilter, name='get_report_costs_analysis_filter'),
    path('getReportCostsAnalysisFilterNbs/', api.getReportCostsAnalysisFilterNbs, name='get_report_costs_analysis_filter_nbs'),
    path('getReportAnalysisBenefitsFilterSum/', api.getReportAnalysisBenefitsFilterSum, name='get_report_analysis_benefits_filter_sum'),
    path('getWaterproofReportsAnalysisBenefits/', api.getWaterproofReportsAnalysisBenefits, name='get_waterproof_reports_analysis_benefits'),
    path('getReportOportunityResultIndicators/', api.getReportOportunityResultIndicators, name='get_report_oportunity_result_indicators'),
    path('getReportAnalisysBenefics/', api.getReportAnalisysBenefics, name='get_report_analisys_benefics'),
    path('getReportAnalisysBeneficsB/', api.getReportAnalisysBeneficsB, name='get_report_analisys_benefics_b'),
    path('getReportAnalisysBeneficsC/', api.getReportAnalisysBeneficsC, name='get_report_analisys_benefics_c'),
    path('getSelectorStudyCasesId/', api.getSelectorStudyCasesId, name='get_selector_study_cases_id'),
    path('getStudyCasesIntake/', api.getStudyCasesIntake, name='get_study_cases_intake'),
    path('getDistinctGroupErr/', api.getDistinctGroupErr, name='get_distinct_group_err'),
    path('getWpAqueductIndicatorGraph/', api.getWpAqueductIndicatorGraph, name='get_wp_aqueduct_indicator_graph'),
    
    
    
]