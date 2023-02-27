import json
import os
import fillpdf
from fillpdf import fillpdfs
from datetime import datetime

# helpers
from helpers.datetime import to_day_string


def fill_pdf_application_professional(data):
    now = datetime.now()
    now.strftime("_%Y%m%d_%H%M%S")
    new_pdf_app_form_name = 'application_form_' + now.strftime("_%Y%m%d_%H%M") + '.pdf'
    # locate the template pdf file
    # app_form
    app_form = os.path.join(os.getcwd(), 'static', 'pdf', 'professional', '1_professional_application_form.pdf')
    
    app_form_to_path = os.path.join(os.getcwd(), 'static', 'pdf', 'professional', new_pdf_app_form_name)
    
    # object to be filled
    app_form_fields = fillpdfs.get_form_fields(app_form)
    
    # fill the fields 
    app_form_fields['company_name'] = data[0]['company_name']
    app_form_fields['company_rep_name'] = data[0]['company_rep_name']
    app_form_fields['company_rep_position'] = data[0]['company_rep_position']
    app_form_fields['company_address'] = data[0]['company_address']
    app_form_fields['company_contact_number'] = data[0]['company_contact_number']
    app_form_fields['company_website'] = data[0]['company_website']
    app_form_fields['company_contact_person_name'] = data[0]['company_contact_person_name']
    app_form_fields['company_contact_person_position'] = data[0]['company_contact_person_position']
    app_form_fields['company_contact_person_number'] = data[0]['company_contact_person_number']
    app_form_fields['company_contact_person_email'] = data[0]['company_contact_person_email']
    app_form_fields['company_year_established'] = data[0]['company_year_established']
    app_form_fields['company_registered_industry'] = data[0]['company_registered_industry']
    # change comma symbol to break line on data.services
    app_form_fields['services'] = data[0]['company_services'].replace(', ', '\n')
    app_form_fields['company_total_workers'] = sum([data[0]['company_regular_workers'], data[0]['company_parttime_workers'], data[0]['company_foreign_workers']])
    app_form_fields['company_regular_workers'] = data[0]['company_regular_workers']
    app_form_fields['company_parttime_workers'] = data[0]['company_parttime_workers']
    app_form_fields['company_foreign_workers'] = data[0]['company_foreign_workers']
    app_form_fields['agency_name'] = data[0]['agency_name']
    app_form_fields['agency_rep_name'] = data[0]['agency_rep_name']
    app_form_fields['agency_rep_position'] = data[0]['agency_rep_position']
    app_form_fields['agency_address'] = data[0]['agency_address']
    
    fillpdfs.write_fillable_pdf(app_form, app_form_to_path, app_form_fields)
    
    new_pdf_mpreq_form_name = 'manpower_request_form_' + now.strftime("_%Y%m%d_%H%M") + '.pdf'
    
    # manpower request form
    mpreq_form = os.path.join(os.getcwd(), 'static', 'pdf', 'professional', '2_professional_manpowerrequest_form.pdf')
    
    # object to be filled
    mpreq_form_fields = fillpdfs.get_form_fields(mpreq_form)
    
    mpreq_form_fields['company_name'] = data[0]['company_name']
    mpreq_form_fields['company_rep_name'] = data[0]['company_rep_name']
    mpreq_form_fields['company_rep_position'] = data[0]['company_rep_position']
    mpreq_form_fields['company_address_contact_number'] = data[0]['company_address'] + ' | ' + data[0]['company_contact_number']
    mpreq_form_fields['date_filled'] = data[0]['date_filled']
    mpreq_form_fields['agency_name'] = data[0]['agency_name']
    mpreq_form_fields['agency_rep_name'] = data[0]['agency_rep_name']
    mpreq_form_fields['agency_rep_position'] = data[0]['agency_rep_position']
    mpreq_form_fields['agency_address'] = data[0]['agency_address']
    mpreq_form_fields['dear_agency_rep_name'] = data[0]['agency_rep_name']
    # create a dict that contains job positions values
    job_positions = json.loads(data[0]['job_positions'])
    # print('job1', job_positions[0])
    
    #1 job
    mpreq_form_fields['job_position1'] = job_positions[0]['job_title']
    
    mpreq_form_fields['job_no_workers1'] = job_positions[0]['job_no_workers']
    
    mpreq_form_fields['job_basic_salary1'] = job_positions[0]['job_basic_salary']
    
    #2 job
    mpreq_form_fields['job_position2'] = job_positions[1]['job_title']
    
    mpreq_form_fields['job_no_workers2'] = job_positions[1]['job_no_workers']
    
    mpreq_form_fields['job_basic_salary2'] = job_positions[0]['job_basic_salary']
    
    # total number of workers
    total_workers = int(job_positions[1]['job_no_workers']) + int(job_positions[0]['job_no_workers'])
    
    mpreq_form_fields['job_total_no_workers'] = total_workers
    mpreq_form_fields['visa_type'] = data[0]['visa_type']
    
    mpreq_form_to_path = os.path.join(os.getcwd(), 'static', 'pdf', 'professional', new_pdf_mpreq_form_name)
    
    fillpdfs.write_fillable_pdf(mpreq_form, mpreq_form_to_path, mpreq_form_fields)
    
    # recruitment agreement
    new_pdf_recagr_form_name = 'recruitment_agreement_form_' + now.strftime("_%Y%m%d_%H%M") + '.pdf'
    
    recagr_form = os.path.join(os.getcwd(), 'static', 'pdf', 'professional', '4_professional_recagreement_form.pdf')
    
    recagr_form_to_path = os.path.join(os.getcwd(), 'static', 'pdf', 'professional', new_pdf_recagr_form_name)
    
     # object to be filled
    recagr_form_fields = fillpdfs.get_form_fields(recagr_form)
    
    recagr_form_fields['company_name'] = data[0]['company_name']
    recagr_form_fields['company_address'] = data[0]['company_address']
    recagr_form_fields['company_rep_name'] = data[0]['company_rep_name']
    
    recagr_form_fields['agency_name'] = data[0]['agency_name']
    recagr_form_fields['agency_address'] = data[0]['agency_address']
    recagr_form_fields['agency_rep_name'] = data[0]['agency_rep_name']
    recagr_form_fields['agency_rep_position'] = data[0]['agency_rep_position']
    
    # specific formate dates to input
    recagr_form_fields['date_filled_day'] = to_day_string(int(data[0]['date_filled'].strftime('%d')))
    recagr_form_fields['date_filled_monthyear'] = data[0]['date_filled'].strftime('%B %Y')
    
    recagr_form_fields['place_filled'] = data[0]['place_filled']
    
    recagr_form_fields['company_name2'] = data[0]['company_name']
    recagr_form_fields['company_rep_name2'] = data[0]['company_rep_name']
    recagr_form_fields['agency_name2'] = data[0]['agency_name']
    recagr_form_fields['agency_rep_name2'] = data[0]['agency_rep_name']
    
    fillpdfs.write_fillable_pdf(recagr_form, recagr_form_to_path, recagr_form_fields)
    
    # return 3 pdf file paths to be downloaded in a dictionary
    return [app_form_to_path, mpreq_form_to_path,  recagr_form_to_path]
    # return {'application_form': [app_form_to_path, new_pdf_app_form_name], 'manpowerrequest_form': mpreq_form_to_path, 'recruitmentagreement_form': recagr_form_to_path}

def fill_pdf_contract_professional(data):
    now = datetime.now()
    now.strftime("_%Y%m%d_%H%M%S")
    new_pdf_cont_form_name = 'employmentcontract_form_' + now.strftime("_%Y%m%d_%H%M") + '.pdf'
    # locate the template pdf file
    # app_form
    cont_form = os.path.join(os.getcwd(), 'static', 'pdf', 'professional', '3_professional_employmentcontract_form.pdf')
    
    cont_form_to_path = os.path.join(os.getcwd(), 'static', 'pdf', 'professional', new_pdf_cont_form_name)
    
    # object to be filled
    cont_form_fields = fillpdfs.get_form_fields(cont_form)
    
    # company name texts and sign
    cont_form_fields['company_name'] = data[0]['company_name']
    cont_form_fields['company_name2'] = data[0]['company_name']
    cont_form_fields['company_name3'] = data[0]['company_name']
    cont_form_fields['sign1_company'] = data[0]['company_name']
    cont_form_fields['sign2_company'] = data[0]['company_name']
    cont_form_fields['sign3_company'] = data[0]['company_name']
    cont_form_fields['sign4_company'] = data[0]['company_name']
    cont_form_fields['sign5_company'] = data[0]['company_name']
    
    cont_form_fields['company_address'] = data[0]['company_address']
    cont_form_fields['company_contact_number'] = data[0]['company_contact_number']
    
    # agency text and sign
    cont_form_fields['agency_name'] = data[0]['agency_name']
    cont_form_fields['sign1_agency'] = data[0]['agency_name']
    cont_form_fields['sign2_agency'] = data[0]['agency_name']
    cont_form_fields['sign3_agency'] = data[0]['agency_name']
    cont_form_fields['sign4_agency'] = data[0]['agency_name']
    cont_form_fields['sign5_agency'] = data[0]['agency_name']
    
    cont_form_fields['agency_address'] = data[0]['agency_address']
    
    #worker name
    cont_form_fields['worker_name'] = data[0]['worker_name']
    cont_form_fields['worker_name2'] = data[0]['worker_name']
    cont_form_fields['worker_name3'] = data[0]['worker_name']
    
    # job details
    cont_form_fields['site_employment'] = data[0]['site_employment']
    cont_form_fields['contract_duration'] = data[0]['contract_duration']
    
    contract_term = data[0]['contract_terms']
    if contract_term == 'renew':
        cont_form_fields['contract_renew']  = 'x'
    elif contract_term == 'non_renew':
        cont_form_fields['contract_non_renew']  = 'x'
    elif contract_term == 'renew_by_performance':
        cont_form_fields['contract_by_performance']  = 'x'
        
    bonus = data[0]['bonus']
    if bonus == 'once':
        cont_form_fields['bonus_once']  = 'x'
    elif bonus == 'twice':
        cont_form_fields['bonus_twice']  = 'x'
        
    salary_increase = data[0]['salary_increase']
    if salary_increase == 'once':
        cont_form_fields['salary_increase_once']  = 'x'
    elif salary_increase == 'twice':
        cont_form_fields['salary_twice']  = 'x'
    # elif salary_increase == 'performance':
    #     cont_form_fields['salary_twice']  = 'x'
    
    cont_form_fields['work_start_time'] = data[0]['work_start_time']
    cont_form_fields['work_end_time'] = data[0]['work_end_time']
    cont_form_fields['work_rest'] = data[0]['work_rest']
    cont_form_fields['work_working_days'] = data[0]['work_working_days']
    cont_form_fields['work_days_off'] = data[0]['work_days_off']
    cont_form_fields['work_leave'] = data[0]['work_leave']
    cont_form_fields['work_other_leave'] = data[0]['work_other_leave']
    
    housing_accomodation = data[0]['housing_accomodation']
    if housing_accomodation == 'a_deduction':
        cont_form_fields['housing_option_a_not_free'] = 'x'
        cont_form_fields['housing_option_a_cost'] = data[0]['housing_cost']
    elif housing_accomodation == 'a_free':
        cont_form_fields['housing_option_a_free'] = 'x'
        cont_form_fields['housing_option_b_monthlyallowance_cost'] = data[0]['housing_cost']
    elif housing_accomodation == 'b_allowance':
        cont_form_fields['housing_option_b_allowance'] = 'x'
        cont_form_fields['housing_option_b_monthlydeduct_cost'] = data[0]['housing_cost']
    elif housing_accomodation == 'b_deduction':
        cont_form_fields['housing_option_b_deduction'] = 'x'
        cont_form_fields['housing_option_b_percentageallowance_cost'] = data[0]['housing_cost']
    elif housing_accomodation == 'b_rental_percent':
        cont_form_fields['housing_option_b_actualpercentage'] = 'x'
    elif housing_accomodation == 'b_free':
        cont_form_fields['housing_option_b_free'] = 'x'
        
    utilities = data[0]['utilities']
    if utilities == 'free':
        cont_form_fields['utilities_free'] = 'x'
    elif utilities == 'monthly_included':
        cont_form_fields['utilities_included'] = 'x'
    elif utilities == 'direct':
        cont_form_fields['utilities_direct'] = 'x'
    elif utilities == 'actual':
        cont_form_fields['utilities_deduct'] = 'x'
    elif utilities == 'monthly_allowancne':
        cont_form_fields['utilities_allowance'] = 'x'
        
    cont_form_fields['company_repname_position_companyname'] = f"{data[0]['company_rep_name']}, {data[0]['company_rep_position']} /  {data[0]['company_name']}"
    
    cont_form_fields['agency_repname_position_agencyname'] = f"{data[0]['agency_rep_name']}, {data[0]['agency_rep_position']} / {data[0]['agency_name']}"
    
    cont_form_fields['job_title'] = data[0]['job_title']
    cont_form_fields['job_title2'] = data[0]['job_title']
    cont_form_fields['job_description'] = data[0]['job_description']
    
    # uses split = ; to make a list and distribute to every duties stated/inputted
    if data[0]['job_duties']:
        if ';' not in data[0]['job_duties']:
            cont_form_fields['job_duties1'] = data[0]['job_duties']
        else:
            job_duties = data[0]['job_duties'].split(';')
            for duty in job_duties:
                index = job_duties.index(duty)
                text_field = f'job_duties{1 + index}' 
                cont_form_fields[text_field] = job_duties[index]
    
    cont_form_fields['job_criteria_degree'] = data[0]['job_criteria_degree']
    # jlpt (only n2 , n3 is present on pdf)
    jlpt_level = data[0]['job_criteria_jlpt_level']
    if jlpt_level == 'N3':
        cont_form_fields['jlpt_n3'] = 'x'
    elif jlpt_level == 'N2':
        cont_form_fields['jlpt_n2'] = 'x'
        
    cont_form_fields['job_criteria_year_exp'] = data[0]['job_criteria_year_exp']
    
    if data[0]['job_criteria_other']:
        if ';' not in data[0]['job_criteria_other']:
            cont_form_fields['job_criteria_other1'] = data[0]['job_criteria_other']
        else:
            job_criteria_other = data[0]['job_criteria_other'].split(';')
            for criteria in job_criteria_other:
                index = job_criteria_other.index(criteria)
                text_field = f'job_criteria_other{1 + index}' 
                cont_form_fields[text_field] = job_criteria_other[index]
    
    # salary scheme
    cont_form_fields['job_basic_salary'] = data[0]['job_basic_salary']
    cont_form_fields['job_income_tax'] = data[0]['job_income_tax']
    cont_form_fields['job_social_insurance'] = data[0]['job_social_insurance']
    cont_form_fields['job_accomodation'] = data[0]['job_accomodation']
    cont_form_fields['job_total_deductions'] = data[0]['job_total_deductions']
    cont_form_fields['job_net_salary'] = data[0]['job_net_salary']
    
    # benefits
    cont_form_fields['benefits_housing'] = data[0]['benefits_housing']
    cont_form_fields['benefits_utilities'] = data[0]['benefits_utilities']
    cont_form_fields['benefits_transportation'] = data[0]['benefits_transportation']
    
    if data[0]['benefits_other']:
        if ';' not in data[0]['benefits_other']:
            cont_form_fields['benefits_other1'] = data[0]['benefits_other']
        else:
            benefits_other = data[0]['benefits_other'].split(';')
            for benefit in benefits_other:
                index = benefits_other.index(benefit)
                text_field = f'benefits_other{1 + index}' 
                cont_form_fields[text_field] = benefits_other[index]
    
    fillpdfs.write_fillable_pdf(cont_form, cont_form_to_path, cont_form_fields) 
    
    print('pdf fields: ', cont_form_fields)
    
    return [cont_form_to_path]
    
    # return list(cont_form_fields)
    # try:
        
    # except Exception as e:
    #     print("Generate PDF Error Conversion: ", str(e))
    #     return f"Generate PDF Error Conversion:, {str(e)}"
