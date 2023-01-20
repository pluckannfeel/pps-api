import json
import os
import fillpdf
from fillpdf import fillpdfs
from datetime import datetime

# helpers
from helpers.datetime import to_day_string


def fill_pdf_professional(data):
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
    print('job1', job_positions[0])
    
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
    
    recagr_form = os.path.join(os.getcwd(), 'static', 'pdf', 'professional', '3_professional_recagreement_form.pdf')
    
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

