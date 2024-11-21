#########################################################################################
#                                                                                       #
#              IF YOU'RE LOOKING FOR THE EHRQL QUIZ THIS IS THE WRONG FILE              #
#                                                                                       #
#########################################################################################
#
# The file you want is called `quiz.py`.
#
# This file defines the ehrQL quiz questions and provides the answers. If you don't want
# to spoil the quiz, don't look ahead!
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#

from ehrql import codelist_from_csv
from ehrql.quiz import Question, Questions
from ehrql.tables.core import clinical_events


introduction = """\
Welcome to the ehrQL Quiz!
"""

diabetes_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-dm_cod.csv", column="code"
)
referral_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-dsep_cod.csv", column="code"
)
mild_frailty_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-mildfrail_cod.csv", column="code"
)
moderate_frailty_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-modfrail_cod.csv", column="code"
)
severe_frailty_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-sevfrail_cod.csv", column="code"
)
hba1c_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-ifcchbam_cod.csv", column="code"
)


questions = Questions()
questions.set_dummy_tables_path("dummy_tables")

#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#

questions[0] = Question(
    """
    Create an event frame by filtering clinical_events to find just the records indicating a diabetes
    diagnosis. (Use the diabetes_codes codelist.)
    """
)
questions[0].expected = clinical_events.where(
    clinical_events.snomedct_code.is_in(diabetes_codes)
)

#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#

questions[1] = Question(
    """
    Create a patient series containing the date of each patient's earliest diabetes diagnosis.
    """
)

earliest_diagnosis_date = (
    clinical_events.where(clinical_events.snomedct_code.is_in(diabetes_codes))
    .sort_by(clinical_events.date)
    .first_for_patient()
    .date
)
questions[1].expected = earliest_diagnosis_date

#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#

questions[2] = Question(
    """
    Create a patient series containing the date of each patient's earliest structured education
    programme referral. (Use the referral_code codelist.)
    """
)

earliest_referral_date = (
    clinical_events.where(clinical_events.snomedct_code.is_in(referral_codes))
    .sort_by(clinical_events.date)
    .first_for_patient()
).date

questions[2].expected = earliest_referral_date

#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#

questions[3] = Question(
    """
    Create a boolean patient series indicating whether the date of each patient's earliest diabetes
    diagnosis was between 1st April 2023 and 31st March 2024. If the patient does not have a
    diagnosis, the value for in this series should be False.
    """
)

questions[3].expected = (
    earliest_referral_date.is_not_null()
    & earliest_referral_date.is_on_or_between("2023-04-01", "2024-03-31")
)

#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#

questions[4] = Question(
    """
    Create a patient series indicating the number of months between a patient's earliest diagnosis
    and their earliest referral.
    """
)
questions[4].expected = (earliest_referral_date - earliest_diagnosis_date).months

#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#

questions[5] = Question(
    """
    Create a boolean patient series identifying patients who have been diagnosed with diabetes for
    the first time in the past year and who have a record of being referred to a structured education
    programme within nine months after their diagnosis.
    """
)

questions[5].expected = (
    earliest_referral_date.is_not_null()
    & earliest_referral_date.is_on_or_between("2023-04-01", "2024-03-31")
    & earliest_referral_date.is_not_null()
    & ((earliest_referral_date - earliest_diagnosis_date).months <= 9)
)

#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#

questions[6] = Question(
    """
    Create a patient series with the date of the latest record of mild frailty for each patient.
    """
)

latest_mild_frailty_date = (
    clinical_events.where(clinical_events.snomedct_code.is_in(mild_frailty_codes))
    .sort_by(clinical_events.date)
    .last_for_patient()
    .date
)
questions[6].expected = latest_mild_frailty_date

#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#

questions[7] = Question(
    """
    Create a patient series with the date of the latest record of moderate or severe frailty for
    each patient.
    """
)

latest_moderate_or_severe_frailty_date = (
    clinical_events.where(
        clinical_events.snomedct_code.is_in(moderate_frailty_codes)
        | clinical_events.snomedct_code.is_in(severe_frailty_codes)
    )
    .sort_by(clinical_events.date)
    .last_for_patient()
    .date
)
questions[7].expected = latest_moderate_or_severe_frailty_date

#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#

questions[8] = Question(
    """
    Create a boolean patient series indicating whether a patient's last record of severity is
    moderate or severe. If the patient does not have a record of frailty, the value in this series
    should be False.
    """
)

has_moderate_or_severe_frailty = (
    latest_moderate_or_severe_frailty_date.is_not_null()
    & (
        latest_mild_frailty_date.is_null()
        | (latest_moderate_or_severe_frailty_date.is_after(latest_mild_frailty_date))
    )
)
questions[8].expected = has_moderate_or_severe_frailty

#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#

questions[9] = Question(
    """
    Create a patient series containing the latest HbA1c measurement for each patient.
    """
)

latest_hba1c_measurement = (
    clinical_events.where(clinical_events.snomedct_code.is_in(hba1c_codes))
    .sort_by(clinical_events.date)
    .last_for_patient()
    .numeric_value
)

questions[9].expected = latest_hba1c_measurement

#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#

questions[10] = Question(
    """
    Create a boolean patient series identifying patients without moderate or severe frailty in whom
    the last IFCC-HbA1c is 58 mmol/mol or less in the preceding twelve months
    """
)

questions[10].expected = ~has_moderate_or_severe_frailty & (
    latest_hba1c_measurement <= 58
)
