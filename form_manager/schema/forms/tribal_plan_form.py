"""The CSBG Tribal Plan and Application form definition."""

from datetime import date
from decimal import Decimal

from django import forms
from pydantic import ConfigDict, Field
from pydantic_extra_types.semantic_version import SemanticVersion

from form_manager.constants import AllFormNames, CSBGTribalPlanApplicationForms, FormFamilies
from form_manager.schema.fields import acf_fields
from form_manager.schema.forms.base import BaseFields, BaseFormSchema, UIDefinition
from form_manager.schema.layout import (
    AccordionBlock,
    AccordionItem,
    AlertBoxBlock,
    FieldBlock,
    FieldGroupBlock,
    PermanentPageBlock,
    ReviewSubheadingBlock,
    SectionBlock,
    StepBlock,
    TextBlock,
)

_US_STATES = [
    ("", "Select a state"),
    ("Alabama", "Alabama"),
    ("Alaska", "Alaska"),
    ("Arizona", "Arizona"),
    ("Arkansas", "Arkansas"),
    ("California", "California"),
    ("Colorado", "Colorado"),
    ("Connecticut", "Connecticut"),
    ("Delaware", "Delaware"),
    ("Florida", "Florida"),
    ("Georgia", "Georgia"),
    ("Hawaii", "Hawaii"),
    ("Idaho", "Idaho"),
    ("Illinois", "Illinois"),
    ("Indiana", "Indiana"),
    ("Iowa", "Iowa"),
    ("Kansas", "Kansas"),
    ("Kentucky", "Kentucky"),
    ("Louisiana", "Louisiana"),
    ("Maine", "Maine"),
    ("Maryland", "Maryland"),
    ("Massachusetts", "Massachusetts"),
    ("Michigan", "Michigan"),
    ("Minnesota", "Minnesota"),
    ("Mississippi", "Mississippi"),
    ("Missouri", "Missouri"),
    ("Montana", "Montana"),
    ("Nebraska", "Nebraska"),
    ("Nevada", "Nevada"),
    ("New Hampshire", "New Hampshire"),
    ("New Jersey", "New Jersey"),
    ("New Mexico", "New Mexico"),
    ("New York", "New York"),
    ("North Carolina", "North Carolina"),
    ("North Dakota", "North Dakota"),
    ("Ohio", "Ohio"),
    ("Oklahoma", "Oklahoma"),
    ("Oregon", "Oregon"),
    ("Pennsylvania", "Pennsylvania"),
    ("Rhode Island", "Rhode Island"),
    ("South Carolina", "South Carolina"),
    ("South Dakota", "South Dakota"),
    ("Tennessee", "Tennessee"),
    ("Texas", "Texas"),
    ("Utah", "Utah"),
    ("Vermont", "Vermont"),
    ("Virginia", "Virginia"),
    ("Washington", "Washington"),
    ("West Virginia", "West Virginia"),
    ("Wisconsin", "Wisconsin"),
    ("Wyoming", "Wyoming"),
    ("District of Columbia", "District of Columbia"),
]

_CSBG_ASSURANCES_NARRATIVE = (
    "As a part of the annual or biannual application and plan required by subsection 676 of "
    "the Community Services Block Grant Act, as amended, (42 U.S.C. 9901 et seq.) (the Act), "
    "the Tribe or Tribal Organization agrees to the Assurances in Section 676 of the Act "
    "(summarized below).\n\n"
    "Programmatic Assurances\n"
    "1. An assurance that funds made available through the grant or allotment will be used for "
    "at least one of the following purposes [per 676(b)(1)]:\n"
    "a. To support activities that are designed to assist low-income families and individuals, "
    "including families and individuals receiving assistance under part A of title IV of the "
    "Social Security Act (42 U.S.C. 601 et seq.), homeless families and individuals, migrant or "
    "seasonal farm workers, and elderly low-income individuals and families so that they may:\n"
    "i. Remove obstacles and solve problems that block the achievement of self-sufficiency.\n"
    "ii. Secure and retain meaningful employment.\n"
    "iii. Attain an adequate education, including family literacy initiatives.\n"
    "iv. Make better use of available income.\n"
    "v. Obtain and maintain adequate housing and a suitable living environment.\n"
    "vi. Obtain emergency assistance through loans, grants, or other means to meet immediate "
    "and urgent individual and family needs.\n"
    "vii. Achieve greater participation in community affairs.\n"
    "b. Address the needs of youth in low-income communities through youth development programs.\n"
    "c. Make more effective use of, and coordinate with, other programs related to the "
    "purposes of this subtitle.\n\n"
    "2. An assurance that information provided by the Tribe will contain the following "
    "[per 676(b)(3)]:\n"
    "a. A description of the service delivery system for services provided or coordinated with "
    "funds under section 675C(a), targeted to low-income individuals and families.\n"
    "b. A description of how linkages will be developed to fill identified service gaps through "
    "information, referrals, case management, and follow-up consultations.\n"
    "c. A description of how funds made available under section 675C(a) will be coordinated with "
    "other public and private resources.\n"
    "d. A description of how funds will support innovative initiatives, including fatherhood and "
    "other family-strengthening initiatives.\n\n"
    "3. An assurance that the Tribe will provide, on an emergency basis, supplies and services, "
    "nutritious food, and related services necessary to counteract starvation and malnutrition "
    "among low-income individuals [per 676(b)(4)].\n\n"
    "4. An assurance that the Tribe will ensure coordination between anti-poverty programs in "
    "each community and, where appropriate, emergency energy crisis intervention programs under "
    "title XXVI [per 676(b)(6)].\n\n"
    "5. An assurance that the Tribe will permit and cooperate with Federal investigations "
    "undertaken in accordance with section 678D [per 676(b)(7)].\n\n"
    "6. An assurance that the Tribe will participate in the performance measurement system "
    "(for example, ROMA) or another acceptable system and describe outcome measures used to "
    "measure performance in promoting self-sufficiency, family stability, and community "
    "revitalization [per 676(b)(13)].\n\n"
    "Administrative and Financial Assurances\n"
    "The Tribe further agrees to the following administrative assurances under the Community "
    "Services Block Grant Act:\n"
    "1. Administrative expenses will not exceed the greater of 5% of the allotment or the "
    "percentage represented by the ratio of $55,000 to the smallest State allotment for the "
    "fiscal year [Section 675C(b)(2)].\n"
    "2. Fiscal control and fund accounting procedures will be established to assure proper "
    "disbursal and accounting of Federal funds and monitoring of assistance under this subtitle "
    "[678D(a)(1)(A)].\n"
    "3. Each Tribe that expends $750,000 or more (during the fiscal year) in all types of "
    "Federal financial assistance will conduct an audit under the Single Audit Act and "
    "applicable OMB guidance [678D(2)(B)].\n"
    "4. Each CSBG Tribal Plan (or revised plan) will be made available for public inspection in "
    "a way that facilitates public review and comment [676(a)(2)(B) and 676(e)(2)].\n\n"
    "Other Administrative Certifications\n"
    "The Tribe also certifies:\n"
    "1. Cost and accounting standards of the Office of Management and Budget apply to recipients "
    "of Community Services Block Grant funds [678D(a)(1)(B), 2 CFR 200, and 45 CFR 75]."
)

_ASSURANCES_NARRATIVE_TOPICS = (
    "As applicable, include the following topics in your description: CSBG service delivery "
    "system; geographical areas and categories of individuals to be served; criteria and method "
    "used for distribution of CSBG funds; purpose of funds, including activities to be supported; "
    "linkages to fill identified gaps in services; coordination with other public and private "
    "resources; and innovative community and neighborhood-based initiatives."
)

_LOBBYING_CERTIFICATION_TEXT = (
    "Certification for Contracts, Grants, Loans, and Cooperative Agreements\n"
    "The undersigned certifies, to the best of his or her knowledge and belief, that:\n"
    "1. No Federal appropriated funds have been paid or will be paid, by or on behalf of the "
    "undersigned, to any person for influencing or attempting to influence an officer or employee "
    "of an agency, a Member of Congress, an officer or employee of Congress, or an employee of a "
    "Member of Congress in connection with the awarding of any Federal contract, the making of any "
    "Federal grant, the making of any Federal loan, the entering into of any cooperative agreement, "
    "and the extension, continuation, renewal, amendment, or modification of any Federal contract, "
    "grant, loan, or cooperative agreement.\n"
    "2. If any funds other than Federal appropriated funds have been paid or will be paid to any "
    "person for influencing or attempting to influence an officer or employee of any agency, a Member "
    "of Congress, an officer or employee of Congress, or an employee of a Member of Congress in "
    "connection with this Federal contract, grant, loan, or cooperative agreement, the undersigned "
    "shall complete and submit Standard Form-LLL, \"Disclosure Form to Report Lobbying,\" in "
    "accordance with its instructions.\n"
    "3. The undersigned shall require that the language of this certification be included in the award "
    "documents for all subawards at all tiers (including subcontracts, subgrants, and contracts under "
    "grants, loans, and cooperative agreements) and that all subrecipients shall certify and disclose "
    "accordingly. This certification is a material representation of fact upon which reliance was placed "
    "when this transaction was made or entered into. Submission of this certification is a prerequisite "
    "for making or entering into this transaction imposed by section 1352, title 31, U.S. Code. Any "
    "person who fails to file the required certification shall be subject to a civil penalty of not less "
    "than $10,000 and not more than $100,000 for each such failure.\n\n"
    "Statement for Loan Guarantees and Loan Insurance\n"
    "The undersigned states, to the best of his or her knowledge and belief, that if any funds have been "
    "paid or will be paid to any person for influencing or attempting to influence an officer or employee "
    "of any agency, a Member of Congress, an officer or employee of Congress, or an employee of a Member "
    "of Congress in connection with this commitment providing for the United States to insure or guarantee "
    "a loan, the undersigned shall complete and submit Standard Form-LLL, \"Disclosure Form to Report "
    "Lobbying,\" in accordance with its instructions. Submission of this statement is a prerequisite for "
    "making or entering into this transaction imposed by section 1352, title 31, U.S. Code. Any person "
    "who fails to file the required statement shall be subject to a civil penalty of not less than "
    "$10,000 and not more than $100,000 for each such failure."
)

_DRUG_FREE_WORKPLACE_CERTIFICATION_TEXT = (
    "Instructions for Certifications\n"
    "1. By signing and/or submitting this application or grant agreement, the grant recipient is "
    "providing the certification set out below.\n"
    "2. The certification set out below is a material representation of fact upon which reliance is "
    "placed when the agency awards the grant. If it is later determined that the grant recipient "
    "knowingly rendered a false certification, or otherwise violates the requirements of the Drug-Free "
    "Workplace Act, the agency, in addition to any other remedies available to the Federal Government, "
    "may take action authorized under the Drug-Free Workplace Act.\n"
    "3. For grant recipients other than individuals, Alternate I applies.\n"
    "4. For grant recipients who are individuals, Alternate II applies.\n"
    "5. Workplaces under grants, for grant recipients other than individuals, need to be identified on "
    "the certification. If known, they may be identified in the grant application. If the grant recipient "
    "does not identify the workplaces at the time of application, or upon award if there is no "
    "application, the grant recipient must keep the identity of the workplace(s) on file in its office "
    "and make the information available for Federal inspection. Failure to identify all known workplaces "
    "constitutes a violation of the grant recipient's drug-free workplace requirements.\n"
    "6. Workplace identifications must include the actual address of buildings (or parts of buildings) "
    "or other sites where work under the grant takes place. Categorical descriptions may be used "
    "(for example, all vehicles of a transit authority while in operation).\n"
    "7. If the workplace identified to the agency changes during the performance of the grant, the grant "
    "recipient shall inform the agency of the change(s), if it previously identified the workplaces in "
    "question.\n"
    "8. Definitions of terms in the Nonprocurement Suspension and Debarment common rule and Drug-Free "
    "Workplace common rule apply to this certification.\n\n"
    "Alternate I. (Grant Recipients Other Than Individuals)\n"
    "The grant recipient certifies that it will or will continue to provide a drug-free workplace by:\n"
    "(a) Publishing a statement notifying employees that the unlawful manufacture, distribution, "
    "dispensing, possession, or use of a controlled substance is prohibited in the grant recipient's "
    "workplace and specifying the actions that will be taken against employees for violation of such "
    "prohibition.\n"
    "(b) Establishing an ongoing drug-free awareness program to inform employees about the dangers of "
    "drug abuse in the workplace; the grant recipient's policy of maintaining a drug-free workplace; any "
    "available drug counseling, rehabilitation, and employee assistance programs; and the penalties that "
    "may be imposed upon employees for drug abuse violations occurring in the workplace.\n"
    "(c) Making it a requirement that each employee to be engaged in the performance of the grant be given "
    "a copy of the statement required by paragraph (a).\n"
    "(d) Notifying the employee in the statement required by paragraph (a) that, as a condition of "
    "employment under the grant, the employee will abide by the terms of the statement and notify the "
    "employer in writing of his or her conviction for a violation of a criminal drug statute occurring in "
    "the workplace no later than five calendar days after such conviction.\n"
    "(e) Notifying the agency in writing, within 10 calendar days after receiving notice under paragraph "
    "(d)(2) from an employee or otherwise receiving actual notice of such conviction.\n"
    "(f) Taking one of the following actions, within 30 calendar days of receiving notice under paragraph "
    "(d)(2), with respect to any employee who is so convicted: 1) taking appropriate personnel action, up "
    "to and including termination; or 2) requiring such employee to participate satisfactorily in a drug "
    "abuse assistance or rehabilitation program approved for such purposes by a Federal, State, or local "
    "health, law enforcement, or other appropriate agency.\n"
    "(g) Making a good faith effort to continue to maintain a drug-free workplace through implementation of "
    "paragraphs (a), (b), (c), (d), (e), and (f).\n\n"
    "Alternate II. (Grant Recipients Who Are Individuals)\n"
    "(a) The grant recipient certifies that, as a condition of the grant, he or she will not engage in the "
    "unlawful manufacture, distribution, dispensing, possession, or use of a controlled substance in "
    "conducting any activity with the grant.\n"
    "(b) If convicted of a criminal drug offense resulting from a violation occurring during the conduct of "
    "any grant activity, he or she will report the conviction, in writing, within 10 calendar days of the "
    "conviction, to every grant officer or other designee, unless the Federal agency designates a central "
    "point for the receipt of such notices."
)

_DEBARMENT_PRIMARY_INSTRUCTIONS_TEXT = (
    "1. By signing and submitting this proposal, the prospective primary participant is providing the "
    "certification set out below.\n"
    "2. The inability of a person to provide the certification required below will not necessarily result "
    "in denial of participation in this covered transaction.\n"
    "3. The certification in this clause is a material representation of fact.\n"
    "4. The prospective primary participant shall provide immediate written notice if any certification "
    "becomes erroneous by reason of changed circumstances.\n"
    "5. Definitions in the applicable debarment rules apply to this certification.\n"
    "6. The prospective primary participant agrees not to knowingly enter into lower tier covered "
    "transactions with excluded persons, unless authorized.\n"
    "7. The prospective primary participant agrees to include the required lower-tier certification clause "
    "in subtransactions.\n"
    "8. A participant may rely on a lower-tier certification unless it knows it is erroneous.\n"
    "9. Nothing in these instructions requires creating a separate system of records.\n"
    "10. If a participant knowingly enters into a lower tier transaction with an excluded person, the "
    "department or agency may terminate for cause or default."
)

_DEBARMENT_LOWER_TIER_INSTRUCTIONS_TEXT = (
    "1. By signing and submitting this proposal, the prospective lower tier participant is providing the "
    "certification set out below.\n"
    "2. This certification is a material representation of fact upon which reliance is placed.\n"
    "3. The prospective lower tier participant shall provide immediate written notice if its certification "
    "was erroneous when submitted or becomes erroneous.\n"
    "4. Definitions in the applicable debarment rules apply to this certification.\n"
    "5. The prospective lower tier participant agrees not to knowingly enter into lower tier covered "
    "transactions with excluded persons, unless authorized.\n"
    "6. The prospective lower tier participant agrees to include this clause in all lower tier covered "
    "transactions and solicitations.\n"
    "7. A participant may rely on a certification unless it knows it is erroneous.\n"
    "8. Nothing in these instructions requires creating a separate system of records.\n"
    "9. If a participant knowingly enters into a lower tier transaction with an excluded person, the "
    "department or agency may pursue remedies, including suspension and/or debarment."
)

_DEBARMENT_CERTIFICATION_TEXT = (
    "Primary Covered Transactions\n"
    "1. The prospective primary participant certifies to the best of its knowledge and belief, that it and "
    "its principals are not presently debarred, suspended, proposed for debarment, declared ineligible, or "
    "voluntarily excluded by any Federal department or agency; have not within a three-year period "
    "preceding this proposal been convicted of or had a civil judgment rendered against them for commission "
    "of fraud or a criminal offense in connection with obtaining, attempting to obtain, or performing a "
    "public transaction or contract under a public transaction; and are not presently indicted for or "
    "otherwise criminally or civilly charged by a governmental entity with commission of the enumerated "
    "offenses.\n"
    "2. Where the prospective primary participant is unable to certify to any of the statements in this "
    "certification, such prospective participant shall attach an explanation to this proposal.\n\n"
    "Lower Tier Covered Transactions\n"
    "1. The prospective lower tier participant certifies, by submission of this proposal, that neither it "
    "nor its principals is presently debarred, suspended, proposed for debarment, declared ineligible, or "
    "voluntarily excluded from participation in this transaction by any Federal department or agency.\n"
    "2. Where the prospective lower tier participant is unable to certify to any of the statements in this "
    "certification, such prospective participant shall attach an explanation to this proposal."
)

_TOBACCO_SMOKE_CERTIFICATION_TEXT = (
    "Public Law 103-227, Part C, Environmental Tobacco Smoke, also known as the Pro-Children Act of 1994, "
    "requires that smoking not be permitted in any portion of any indoor facility owned, leased, or "
    "contracted for and used routinely or regularly for the provision of health, day care, education, or "
    "library services to children under 18 years of age, if the services are funded by Federal programs "
    "either directly or through State or local governments by Federal grant, contract, loan, or loan "
    "guarantee.\n\n"
    "The law does not apply to children's services provided in private residences, facilities funded solely "
    "by Medicare or Medicaid funds, and portions of facilities used for inpatient drug or alcohol treatment."
    "\n\n"
    "Failure to comply with these requirements may result in the imposition of a civil monetary penalty and "
    "possible administrative compliance action."
)


def _fiscal_year_choices() -> list[tuple[str, str]]:
    """Return the upcoming 3 fiscal year choices from the current date.

    The fiscal year runs October 1 – September 30. This list is computed once at
    module load time. Kayla confirmed "next 2 fiscal years continuously" is the
    desired range; 3 are included here as a small buffer.
    """
    today = date.today()
    # Before October: the current calendar year is the ending year of the current FY.
    start_fy = today.year + 1 if today.month >= 10 else today.year
    choices: list[tuple[str, str]] = [("", "Select a fiscal year")]
    for i in range(3):
        fy = start_fy + i
        choices.append((f"fy_{fy}", f"FY {fy} (October 1, {fy - 1} – September 30, {fy})"))
    return choices


_FISCAL_YEAR_CHOICES = _fiscal_year_choices()

_Y1_ALLOCATION_FIELDS = [
    "alloc_admin_y1",
    "alloc_employment_y1",
    "alloc_education_y1",
    "alloc_income_y1",
    "alloc_housing_y1",
    "alloc_health_y1",
    "alloc_civic_y1",
    "alloc_transportation_y1",
    "alloc_partnerships_y1",
]

_Y2_ALLOCATION_FIELDS = [
    "alloc_admin_y2",
    "alloc_employment_y2",
    "alloc_education_y2",
    "alloc_income_y2",
    "alloc_housing_y2",
    "alloc_health_y2",
    "alloc_civic_y2",
    "alloc_transportation_y2",
    "alloc_partnerships_y2",
]


class TribalPlanFormFields(BaseFields):

    # region Section 1 — CSBG Tribal Administrative Information

    # 1.1 Plan Coverage
    plan_coverage = acf_fields.ChoiceField(
        title="Plan Coverage",
        choices=[("one_year", "One year"), ("two_year", "Two year")],
        widget=forms.RadioSelect(attrs={"radio_type": "tile"}),
    )

    # 1.1a Fiscal Years
    fiscal_year_y1 = acf_fields.ChoiceField(
        title="Fiscal Year (Year One)",
        choices=_FISCAL_YEAR_CHOICES,
    )
    fiscal_year_y2 = acf_fields.ChoiceField(
        title="Fiscal Year (Year Two)",
        description="Required only if a two-year plan is selected above.",
        choices=_FISCAL_YEAR_CHOICES,
        required=False,
    )

    # Tribal Organization
    tribal_lead_agency_name = acf_fields.CharField(
        title="Name of Tribal Lead Agency",
        max_length=200,
    )

    # 1.2a
    org_name = acf_fields.CharField(
        title="Name of Tribe or Tribal Organization",
        max_length=200,
    )

    # 1.2b Multi-tribe representation
    is_multi_tribe = acf_fields.ChoiceField(
        title="Are you representing more than one Tribe, Village, Community or Jurisdiction?",
        choices=[("yes", "Yes"), ("no", "No")],
        widget=forms.RadioSelect(attrs={"radio_type": "tile"}),
    )
    multi_tribe_names = acf_fields.TextareaField(
        title="Names of all Tribes/Villages/Communities/Jurisdictions represented",
        description="Required if representing more than one tribe. Maximum 1,000 characters.",
        max_length=1000,
        required=False,
    )
    # NOTE: Per CSV decisions (3/24 PO Notes), tribal resolution upload was moved here
    # from Section 2.1 to be adjacent to the multi-tribe question at 1.2b.
    # TODO: Final allowed file types and max size pending confirmation from ACF.
    tribal_resolution_upload = acf_fields.FileField(
        title="Tribal Resolution(s)",
        description=(
            "Upload tribal resolution documentation. Required if representing more than one tribe. "
            "Allowed types: PDF, PNG, JPG, JPEG. Maximum size: 10 MB."
        ),
        required=False,
    )

    # 1.3 Authorized Tribal Official
    authorized_official_name = acf_fields.CharField(title="Full name", max_length=200)
    authorized_official_title = acf_fields.CharField(title="Title", max_length=200)
    authorized_official_street = acf_fields.CharField(title="Street address", max_length=200)
    authorized_official_city = acf_fields.CharField(title="City", max_length=100)
    authorized_official_state = acf_fields.ChoiceField(title="State", choices=_US_STATES)
    authorized_official_zip = acf_fields.CharField(
        title="ZIP code",
        max_length=5,
        min_length=5,
    )
    authorized_official_phone = acf_fields.CharField(
        title="Phone number",
        widget=forms.TelInput,  # type: ignore
    )
    authorized_official_extension = acf_fields.CharField(
        title="Extension (Optional)",
        required=False,
        max_length=10,
    )
    authorized_official_fax = acf_fields.CharField(
        title="Fax number (Optional)",
        widget=forms.TelInput,  # type: ignore
        required=False,
    )
    authorized_official_email = acf_fields.CharField(
        title="Email address",
        widget=forms.EmailInput,
    )
    authorized_official_website = acf_fields.CharField(
        title="Website (Optional)",
        required=False,
        max_length=200,
    )

    # 1.4 Tribal CSBG Point of Contact
    contact_name = acf_fields.CharField(title="Full name", max_length=200)
    contact_title = acf_fields.CharField(title="Title", max_length=200)
    contact_street = acf_fields.CharField(title="Street address", max_length=200)
    contact_city = acf_fields.CharField(title="City", max_length=100)
    contact_state = acf_fields.ChoiceField(title="State", choices=_US_STATES)
    contact_zip = acf_fields.CharField(title="ZIP code", max_length=5, min_length=5)
    contact_phone = acf_fields.CharField(
        title="Phone number",
        widget=forms.TelInput,  # type: ignore
    )
    contact_extension = acf_fields.CharField(
        title="Extension (Optional)",
        required=False,
        max_length=10,
    )
    contact_fax = acf_fields.CharField(
        title="Fax number (Optional)",
        widget=forms.TelInput,  # type: ignore
        required=False,
    )
    contact_email = acf_fields.CharField(
        title="Email address",
        widget=forms.EmailInput,
        max_length=150,
    )

    # 1.5 Delegation of Authority
    has_delegation = acf_fields.ChoiceField(
        title="Is signature authority being delegated?",
        description="If No, proceed to Section 2.",
        choices=[("yes", "Yes"), ("no", "No")],
        widget=forms.RadioSelect(attrs={"radio_type": "tile"}),
    )
    # 1.5b Additional Authorized Official (conditional on has_delegation = yes)
    delegation_name = acf_fields.CharField(title="Full name", required=False, max_length=200)
    delegation_title = acf_fields.CharField(title="Title", required=False, max_length=200)
    delegation_phone = acf_fields.CharField(
        title="Phone number",
        widget=forms.TelInput,  # type: ignore
        required=False,
    )
    delegation_extension = acf_fields.CharField(
        title="Extension (Optional)",
        required=False,
        max_length=10,
    )
    delegation_email = acf_fields.CharField(
        title="Email address",
        widget=forms.EmailInput,
        required=False,
        max_length=100,
    )

    # endregion

    # region Section 2 — Tribal Resolution and Recognition
    # NOTE: Section 2.1 (standalone "Is the applicant representing more than one Tribe?")
    # has been removed per 3/24 PO Notes. The question and associated upload have been
    # consolidated into Section 1 at field 1.2b. See tribal_resolution_upload above.

    # 2.2a
    has_recognition = acf_fields.ChoiceField(
        title="Do all Tribes/Villages/Communities/Jurisdictions served have state or federal recognition?",
        choices=[("yes", "Yes"), ("no", "No")],
        widget=forms.RadioSelect(attrs={"radio_type": "tile"}),
    )
    # 2.2b Recognition citation and upload (conditional on has_recognition = yes)
    recognition_citation = acf_fields.CharField(
        title="State or federal recognition citation",
        description="Required if recognition exists. Provide the citation for the recognition.",
        max_length=500,
        required=False,
    )
    recognition_upload = acf_fields.FileField(
        title="Recognition documentation",
        description=(
            "Upload supporting recognition documentation. Required if recognition exists. "
            "Allowed types: PDF, PNG, JPG, JPEG. Maximum size: 10 MB."
        ),
        required=False,
    )
    # NOTE: 2.2b-no (explanation for lack of recognition) has been removed per 3/24 PO Notes.
    # POs confirmed: "Tribes don't need to explain. There does not need to be a pop-up if a tribe selects No."

    # endregion

    # region Section 3 — CSBG Tribal Plan Goals and Objectives

    # 3.1
    goals_and_objectives = acf_fields.TextareaField(
        title="CSBG Goals, Objectives, and Strategies",
        description="Maximum 5,000 characters.",
        max_length=5000,
    )

    # endregion

    # region Section 4 — CSBG Community-Based Feedback

    # 4.1a/b
    community_feedback = acf_fields.YesNoDisplayField(
        title="Did the Tribe solicit feedback from Tribal members served?",
        fields=[
            acf_fields.TextareaField(
                title="Describe how feedback was solicited",
                description="Maximum 5,000 characters.",
                max_length=5000,
                required=False,
            )
        ],
        validators=[],
    )

    # endregion

    # region Section 5 — Use of Funds and Fiscal Controls

    # 5.1 Year 1 Allocations (must total 100%)
    alloc_admin_y1 = acf_fields.DecimalField(
        title="Administrative Funds",
        review_title="Administrative Funds (Year 1 %)",
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
    )
    alloc_employment_y1 = acf_fields.DecimalField(
        title="Employment",
        review_title="Employment (Year 1 %)",
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
    )
    alloc_education_y1 = acf_fields.DecimalField(
        title="Childcare, Early Childhood, Youth Development, and Adult Education",
        review_title="Education and Youth Development (Year 1 %)",
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
    )
    alloc_income_y1 = acf_fields.DecimalField(
        title="Income and Asset Building",
        review_title="Income and Asset Building (Year 1 %)",
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
    )
    alloc_housing_y1 = acf_fields.DecimalField(
        title="Housing",
        review_title="Housing (Year 1 %)",
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
    )
    alloc_health_y1 = acf_fields.DecimalField(
        title="Health and Nutrition",
        review_title="Health and Nutrition (Year 1 %)",
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
    )
    alloc_civic_y1 = acf_fields.DecimalField(
        title="Civic Engagement and Community Involvement",
        review_title="Civic Engagement and Community Involvement (Year 1 %)",
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
    )
    alloc_transportation_y1 = acf_fields.DecimalField(
        title="Transportation",
        review_title="Transportation (Year 1 %)",
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
    )
    alloc_partnerships_y1 = acf_fields.DecimalField(
        title="Partnerships, Linkages, and Service Coordination",
        review_title="Partnerships, Linkages, and Service Coordination (Year 1 %)",
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
    )
    alloc_total_y1 = acf_fields.CalculatedDecimalField(
        title="Year 1 Total",
        review_title="Year 1 Total (%)",
        fields=_Y1_ALLOCATION_FIELDS,
        max_digits=5,
        decimal_places=2,
    )

    # 5.1 Year 2 Allocations (conditional on two-year plan; must total 100%)
    alloc_admin_y2 = acf_fields.DecimalField(
        title="Administrative Funds",
        review_title="Administrative Funds (Year 2 %)",
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
        required=False,
    )
    alloc_employment_y2 = acf_fields.DecimalField(
        title="Employment",
        review_title="Employment (Year 2 %)",
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
        required=False,
    )
    alloc_education_y2 = acf_fields.DecimalField(
        title="Childcare, Early Childhood, Youth Development, and Adult Education",
        review_title="Education and Youth Development (Year 2 %)",
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
        required=False,
    )
    alloc_income_y2 = acf_fields.DecimalField(
        title="Income and Asset Building",
        review_title="Income and Asset Building (Year 2 %)",
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
        required=False,
    )
    alloc_housing_y2 = acf_fields.DecimalField(
        title="Housing",
        review_title="Housing (Year 2 %)",
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
        required=False,
    )
    alloc_health_y2 = acf_fields.DecimalField(
        title="Health and Nutrition",
        review_title="Health and Nutrition (Year 2 %)",
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
        required=False,
    )
    alloc_civic_y2 = acf_fields.DecimalField(
        title="Civic Engagement and Community Involvement",
        review_title="Civic Engagement and Community Involvement (Year 2 %)",
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
        required=False,
    )
    alloc_transportation_y2 = acf_fields.DecimalField(
        title="Transportation",
        review_title="Transportation (Year 2 %)",
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
        required=False,
    )
    alloc_partnerships_y2 = acf_fields.DecimalField(
        title="Partnerships, Linkages, and Service Coordination",
        review_title="Partnerships, Linkages, and Service Coordination (Year 2 %)",
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
        required=False,
    )
    alloc_total_y2 = acf_fields.CalculatedDecimalField(
        title="Year 2 Total",
        review_title="Year 2 Total (%)",
        fields=_Y2_ALLOCATION_FIELDS,
        max_digits=5,
        decimal_places=2,
    )

    # 5.2 Limitation on Use of Funds - Acknowledgment
    use_of_funds_acknowledgment = acf_fields.BooleanField(
        title="I acknowledge the limitation on use of CSBG funds as described above.",
    )

    # 5.3 Single Audit Review
    audit_date = acf_fields.DateField(
        title="Date of most recent audit",
        description="Enter as mm/dd/yyyy.",
        required=False,
    )
    # NOTE: Fiscal year covered is implemented as free text per 3/24 PO Notes.
    # PDE/PS teams will provide guidance on final instruction language.
    audit_fiscal_period = acf_fields.CharField(
        title="Fiscal year covered by most recent audit",
        description=(
            "Enter the fiscal period as mm/dd/yyyy – mm/dd/yyyy. "
            "If you received less than $750,000 in total federal funds, this question is optional."
        ),
        required=False,
        max_length=50,
    )

    # endregion

    # region Section 6 — Individual Eligibility and Targeted Community Eligibility

    # 6.1
    individual_eligibility = acf_fields.TextareaField(
        title="Individual Eligibility",
        description=(
            "Describe your policies and procedures for determining individual eligibility. "
            "Maximum 5,000 characters."
        ),
        max_length=5000,
    )

    # 6.2
    targeted_community_eligibility = acf_fields.TextareaField(
        title="Targeted Community Eligibility",
        description=(
            "Describe how your services target and benefit low-income communities. "
            "Maximum 5,000 characters."
        ),
        max_length=5000,
    )

    # endregion

    # region Section 7 — CSBG Statement of Assurances

    # 7.1 Assurances Narrative
    assurance_narrative = acf_fields.TextareaField(
        title="Description",
        description="Maximum 5,000 characters.",
        max_length=5000,
    )

    # 7.2 Attestation and typed signature
    assurance_attestation = acf_fields.BooleanField(
        title=(
            "By checking this box, the Tribal CSBG authorized official is certifying "
            "the assurances set out above."
        ),
    )
    assurance_signature = acf_fields.CharField(
        title="Authorized Tribal Official Signature",
        description="Type your full name to sign.",
        max_length=200,
    )

    # endregion

    # region Section 8 — Federal Certifications

    # 8.1 Lobbying Certification
    lobbying_attestation = acf_fields.BooleanField(
        title=(
            "I have reviewed this certification and affirm that the Tribe or Tribal "
            "Organization will ensure compliance with it"
        ),
    )
    lobbying_signature = acf_fields.CharField(
        title="Authorized Tribal Official Signature",
        description="Type your full name to sign.",
        max_length=200,
    )

    # 8.2 Drug-Free Workplace Certification
    drug_free_attestation = acf_fields.BooleanField(
        title=(
            "I have reviewed this certification and affirm that the Tribe or Tribal "
            "Organization will ensure compliance with it"
        ),
    )
    drug_free_place_of_performance = acf_fields.CharField(
        title="Place of Performance (street, city, county, state, ZIP code)",
        description=(
            "Provide the address or location where CSBG-funded activities will be performed."
        ),
        max_length=500,
    )
    # TODO: Exact question wording and behavior for "unidentified workplaces" is pending
    # guidance from ACF legal team (Kayla and Melanie following up with program specialists).
    drug_free_unidentified_workplaces = acf_fields.YesNoDisplayField(
        title="Are there additional locations where CSBG-funded work is performed?",
        fields=[
            acf_fields.TextareaField(
                title="List additional workplace location(s)",
                description="500 characters allowed.",
                max_length=500,
                required=False,
            )
        ],
        validators=[],
    )
    drug_free_signature = acf_fields.CharField(
        title="Authorized Tribal Official Signature",
        description="Type your full name to sign.",
        max_length=200,
    )

    # 8.3 Debarment, Suspension Certification
    debarment_attestation = acf_fields.BooleanField(
        title=(
            "I have reviewed this certification and affirm that the Tribe or Tribal "
            "Organization will ensure compliance with it"
        ),
    )
    debarment_signature = acf_fields.CharField(
        title="Authorized Tribal Official Signature",
        description="Type your full name to sign.",
        max_length=200,
    )

    # 8.4 Tobacco Smoke Certification
    tobacco_attestation = acf_fields.BooleanField(
        title=(
            "I have reviewed this certification and affirm that the Tribe or Tribal "
            "Organization will ensure compliance with it"
        ),
    )
    tobacco_signature = acf_fields.CharField(
        title="Authorized Tribal Official Signature",
        description="Type your full name to sign.",
        max_length=200,
    )

    # endregion

    # region Additional Documents

    # TODO: Final file upload constraints (allowed types, count, size) pending confirmation from ACF.
    additional_documents = acf_fields.FileField(
        title="Additional Documents (Optional)",
        description=(
            "Upload any additional supporting documents. "
            "Allowed types: PDF, PNG, JPG, JPEG. Maximum size: 10 MB."
        ),
        required=False,
    )

    # endregion

    def clean(self):
        cleaned_data = super().clean()

        plan_coverage = cleaned_data.get("plan_coverage")
        is_multi_tribe = cleaned_data.get("is_multi_tribe")
        has_delegation = cleaned_data.get("has_delegation")
        has_recognition = cleaned_data.get("has_recognition")

        # 1.2b: Multi-tribe names and tribal resolution upload are required when
        # representing more than one tribe.
        if is_multi_tribe == "yes":
            if not cleaned_data.get("multi_tribe_names"):
                self.add_error(
                    "multi_tribe_names",
                    "Names of all represented tribes are required when representing more than one tribe.",
                )
            if not cleaned_data.get("tribal_resolution_upload"):
                self.add_error(
                    "tribal_resolution_upload",
                    "Tribal resolution documentation is required when representing more than one tribe.",
                )

        # 1.5: Additional Authorized Official fields are required when delegating authority.
        if has_delegation == "yes":
            for field_name, label in [
                ("delegation_name", "Full name"),
                ("delegation_title", "Title"),
                ("delegation_phone", "Phone number"),
                ("delegation_email", "Email address"),
            ]:
                if not cleaned_data.get(field_name):
                    self.add_error(
                        field_name,
                        f"{label} is required when delegating signature authority.",
                    )

        # 2.2b: At least one of citation or upload is required when tribes have recognition.
        if has_recognition == "yes":
            if not cleaned_data.get("recognition_citation") and not cleaned_data.get(
                "recognition_upload"
            ):
                self.add_error(
                    "recognition_citation",
                    "Provide a recognition citation or upload supporting documentation.",
                )

        # 1.1a-Y2 and Year 2 allocations: required when a two-year plan is selected.
        if plan_coverage == "two_year":
            if not cleaned_data.get("fiscal_year_y2"):
                self.add_error(
                    "fiscal_year_y2",
                    "Fiscal year for Year Two is required for a two-year plan.",
                )
            for field_name in _Y2_ALLOCATION_FIELDS:
                if cleaned_data.get(field_name) is None:
                    self.add_error(field_name, "This allocation is required for a two-year plan.")

        # 5.1: Year 1 allocation total must equal 100%.
        y1_values = [cleaned_data.get(f) for f in _Y1_ALLOCATION_FIELDS]
        if all(v is not None for v in y1_values):
            y1_total = sum(Decimal(str(v)) for v in y1_values)
            if y1_total != Decimal("100"):
                raise forms.ValidationError(
                    f"Year 1 allocation percentages must total 100%. Current total: {y1_total}%."
                )

        # 5.1: Year 2 allocation total must equal 100% when a two-year plan is selected.
        if plan_coverage == "two_year":
            y2_values = [cleaned_data.get(f) for f in _Y2_ALLOCATION_FIELDS]
            if all(v is not None for v in y2_values):
                y2_total = sum(Decimal(str(v)) for v in y2_values)
                if y2_total != Decimal("100"):
                    raise forms.ValidationError(
                        f"Year 2 allocation percentages must total 100%. Current total: {y2_total}%."
                    )

        return cleaned_data


class TribalPlanForm(BaseFormSchema):
    family: FormFamilies = Field(FormFamilies.CSBG_TRIBAL_PLAN_APPLICATION, frozen=True)
    name: AllFormNames = Field(CSBGTribalPlanApplicationForms.CSBG_TRIBAL_PLAN, frozen=True)
    variant: SemanticVersion = Field(SemanticVersion(1, 0, 0), frozen=True)
    form_fields: TribalPlanFormFields  # type: ignore
    ui: UIDefinition = Field(
        frozen=True,
        default=[
            # Step 1: Section 1 — Tribal Administrative Information
            StepBlock(
                title="Tribal Administrative Information",
                children=[
                    PermanentPageBlock(
                        title="Plan Coverage",
                        children=[
                            SectionBlock(
                                title="Plan Coverage",
                                children=[
                                    ReviewSubheadingBlock(title="Plan Coverage"),
                                    FieldBlock(field_name="plan_coverage"),
                                    FieldBlock(field_name="fiscal_year_y1"),
                                    FieldBlock(field_name="fiscal_year_y2"),
                                ],
                            ),
                        ],
                    ),
                    PermanentPageBlock(
                        title="Tribal Information",
                        children=[
                            SectionBlock(
                                title="Tribal Information",
                                children=[
                                    ReviewSubheadingBlock(title="Tribal Information"),
                                    FieldBlock(field_name="tribal_lead_agency_name"),
                                    FieldBlock(field_name="org_name"),
                                ],
                            ),
                            SectionBlock(
                                title="Tribal Representation",
                                children=[
                                    ReviewSubheadingBlock(title="Tribal Representation"),
                                    FieldBlock(field_name="is_multi_tribe"),
                                    FieldBlock(field_name="multi_tribe_names"),
                                    FieldBlock(field_name="tribal_resolution_upload"),
                                ],
                            ),
                        ],
                    ),
                    PermanentPageBlock(
                        title="Authorized Tribal Official",
                        children=[
                            SectionBlock(
                                title="Authorized Tribal Official",
                                children=[
                                    ReviewSubheadingBlock(title="Authorized Tribal Official"),
                                    FieldBlock(field_name="authorized_official_name"),
                                    FieldBlock(field_name="authorized_official_title"),
                                    FieldBlock(field_name="authorized_official_street"),
                                    FieldBlock(field_name="authorized_official_city"),
                                    FieldBlock(field_name="authorized_official_state"),
                                    FieldBlock(field_name="authorized_official_zip"),
                                    FieldBlock(field_name="authorized_official_phone"),
                                    FieldBlock(field_name="authorized_official_extension"),
                                    FieldBlock(field_name="authorized_official_fax"),
                                    FieldBlock(field_name="authorized_official_email"),
                                    FieldBlock(field_name="authorized_official_website"),
                                ],
                            ),
                        ],
                    ),
                    PermanentPageBlock(
                        title="Tribal Program Contact",
                        children=[
                            SectionBlock(
                                title="Tribal Program Contact",
                                children=[
                                    ReviewSubheadingBlock(title="Tribal Program Contact"),
                                    FieldBlock(field_name="contact_name"),
                                    FieldBlock(field_name="contact_title"),
                                    FieldBlock(field_name="contact_street"),
                                    FieldBlock(field_name="contact_city"),
                                    FieldBlock(field_name="contact_state"),
                                    FieldBlock(field_name="contact_zip"),
                                    FieldBlock(field_name="contact_phone"),
                                    FieldBlock(field_name="contact_extension"),
                                    FieldBlock(field_name="contact_fax"),
                                    FieldBlock(field_name="contact_email"),
                                ],
                            ),
                        ],
                    ),
                    PermanentPageBlock(
                        title="Delegation of Authority",
                        subtitle=(
                            "If signature authority is being delegated, complete the "
                            "Additional Authorized Official fields below."
                        ),
                        children=[
                            SectionBlock(
                                title="Delegation of Authority",
                                children=[
                                    ReviewSubheadingBlock(title="Delegation of Authority"),
                                    FieldBlock(field_name="has_delegation"),
                                ],
                            ),
                            SectionBlock(
                                title="Additional Authorized Official",
                                description="Complete only if signature authority is being delegated.",
                                children=[
                                    ReviewSubheadingBlock(title="Additional Authorized Official"),
                                    FieldBlock(field_name="delegation_name"),
                                    FieldBlock(field_name="delegation_title"),
                                    FieldBlock(field_name="delegation_phone"),
                                    FieldBlock(field_name="delegation_extension"),
                                    FieldBlock(field_name="delegation_email"),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            # Step 2: Section 2 — Tribal Recognition
            StepBlock(
                title="Tribal Recognition",
                children=[
                    PermanentPageBlock(
                        title="Tribal Recognition",
                        children=[
                            SectionBlock(
                                title="Tribal Recognition",
                                children=[
                                    ReviewSubheadingBlock(title="Tribal Recognition"),
                                    FieldBlock(field_name="has_recognition"),
                                    FieldBlock(field_name="recognition_citation"),
                                    FieldBlock(field_name="recognition_upload"),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            # Step 3: Section 3 — Goals and Objectives
            StepBlock(
                title="Goals and Objectives",
                children=[
                    PermanentPageBlock(
                        title="Goals and Objectives",
                        subtitle=(
                            "Briefly describe the Tribe or Tribal Organization's CSBG-specific goals "
                            "and objectives for the Community Services Block Grant funding, as applicable."
                        ),
                        children=[
                            SectionBlock(
                                children=[
                                    ReviewSubheadingBlock(title="Goals and Objectives"),
                                    FieldBlock(field_name="goals_and_objectives"),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            # Step 4: Section 4 — Community-Based Feedback
            StepBlock(
                title="Community-Based Feedback",
                children=[
                    PermanentPageBlock(
                        title="Community-Based Feedback",
                        children=[
                            SectionBlock(
                                children=[
                                    ReviewSubheadingBlock(title="Community-Based Feedback"),
                                    FieldBlock(
                                        field_name="community_feedback",
                                        review_template_name="form_manager/forms/yes_no_display_review.html",
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            # Step 5: Section 5 — Use of Funds & Fiscal Controls
            StepBlock(
                title="Use of Funds & Fiscal Controls",
                children=[
                    PermanentPageBlock(
                        title="Planned Allocation of Funds",
                        subtitle=(
                            "For program funds, enter the percentage allocated to each CSBG service "
                            "area. The total must equal 100%."
                        ),
                        children=[
                            AlertBoxBlock(
                                alert_type="info",
                                heading="Allocation requirements for CSBG funds",
                                message=(
                                    "According to the CSBG Act: no more than 5% of funds may be used "
                                    "for administrative costs, and at least 95% must be allocated to "
                                    "program services."
                                ),
                            ),
                            FieldGroupBlock(
                                description=(
                                    "Year One allocations: enter percentages (0–100). "
                                    "The total must equal 100%."
                                ),
                                children=[
                                    ReviewSubheadingBlock(title="Year One"),
                                    FieldBlock(field_name="alloc_admin_y1"),
                                    FieldBlock(field_name="alloc_employment_y1"),
                                    FieldBlock(field_name="alloc_education_y1"),
                                    FieldBlock(field_name="alloc_income_y1"),
                                    FieldBlock(field_name="alloc_housing_y1"),
                                    FieldBlock(field_name="alloc_health_y1"),
                                    FieldBlock(field_name="alloc_civic_y1"),
                                    FieldBlock(field_name="alloc_transportation_y1"),
                                    FieldBlock(field_name="alloc_partnerships_y1"),
                                    FieldBlock(field_name="alloc_total_y1"),
                                ],
                            ),
                            AlertBoxBlock(
                                alert_type="info",
                                heading="Two-Year Plan Only",
                                message=(
                                    "Complete Year Two allocations only if you selected a two-year "
                                    "plan in Section 1 (Plan Coverage)."
                                ),
                            ),
                            FieldGroupBlock(
                                description=(
                                    "Year Two allocations: enter percentages (0–100). "
                                    "The total must equal 100%."
                                ),
                                children=[
                                    ReviewSubheadingBlock(title="Year Two"),
                                    FieldBlock(field_name="alloc_admin_y2"),
                                    FieldBlock(field_name="alloc_employment_y2"),
                                    FieldBlock(field_name="alloc_education_y2"),
                                    FieldBlock(field_name="alloc_income_y2"),
                                    FieldBlock(field_name="alloc_housing_y2"),
                                    FieldBlock(field_name="alloc_health_y2"),
                                    FieldBlock(field_name="alloc_civic_y2"),
                                    FieldBlock(field_name="alloc_transportation_y2"),
                                    FieldBlock(field_name="alloc_partnerships_y2"),
                                    FieldBlock(field_name="alloc_total_y2"),
                                ],
                            ),
                        ],
                    ),
                    PermanentPageBlock(
                        title="Limitation on Use of Funds",
                        children=[
                            SectionBlock(
                                title="Limitation on Use of Funds",
                                children=[
                                    ReviewSubheadingBlock(title="Limitation on Use of Funds"),
                                    FieldBlock(field_name="use_of_funds_acknowledgment"),
                                ],
                            ),
                            SectionBlock(
                                title="Single Audit Review",
                                children=[
                                    ReviewSubheadingBlock(title="Single Audit Review"),
                                    FieldBlock(field_name="audit_date"),
                                    FieldBlock(field_name="audit_fiscal_period"),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            # Step 6: Section 6 — Individual & Targeted Community Eligibility
            StepBlock(
                title="Individual & Targeted Community Eligibility",
                children=[
                    PermanentPageBlock(
                        title="Individual Eligibility",
                        subtitle=(
                            "Describe your tribe's policies and procedures for determining "
                            "individual eligibility for CSBG services."
                        ),
                        children=[
                            SectionBlock(
                                children=[
                                    ReviewSubheadingBlock(title="Individual Eligibility"),
                                    FieldBlock(field_name="individual_eligibility"),
                                ],
                            ),
                        ],
                    ),
                    PermanentPageBlock(
                        title="Targeted Community",
                        subtitle=(
                            "Describe how your tribe's services target and benefit "
                            "low-income communities."
                        ),
                        children=[
                            SectionBlock(
                                children=[
                                    ReviewSubheadingBlock(title="Targeted Community"),
                                    FieldBlock(field_name="targeted_community_eligibility"),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            # Step 7: Section 7 — Statement of Assurances
            StepBlock(
                title="Statement of Assurances",
                children=[
                    PermanentPageBlock(
                        title="Assurances Narrative",
                        subtitle=(
                            "Provide a narrative description of how the tribe or tribal organization "
                            "will carry out the required programmatic assurances."
                        ),
                        children=[
                            AlertBoxBlock(
                                alert_type="info",
                                heading="Programmatic assurances topics",
                                message=_ASSURANCES_NARRATIVE_TOPICS,
                            ),
                            SectionBlock(
                                children=[
                                    ReviewSubheadingBlock(title="Assurances Narrative"),
                                    FieldBlock(field_name="assurance_narrative"),
                                ],
                            ),
                        ],
                    ),
                    PermanentPageBlock(
                        title="Statement of Assurances",
                        subtitle=(
                            "Review the certification below and sign at the bottom of this page to "
                            "affirm compliance. Full legislation: Community Services Block Grant "
                            "Reauthorization Act of 1998 (P.L. 105-285)."
                        ),
                        children=[
                            TextBlock(
                                bordered=True,
                                heading="Statement of CSBG Assurances",
                                text=_CSBG_ASSURANCES_NARRATIVE,
                            ),
                            SectionBlock(
                                children=[
                                    ReviewSubheadingBlock(title="Statement of Assurances"),
                                    FieldBlock(field_name="assurance_attestation"),
                                    FieldBlock(field_name="assurance_signature"),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            # Step 8: Section 8 — Federal Certifications
            StepBlock(
                title="Federal Certifications",
                children=[
                    PermanentPageBlock(
                        title="Regarding Lobbying",
                        subtitle=(
                            "Review the certification below and sign at the bottom of this page to "
                            "affirm compliance."
                        ),
                        children=[
                            TextBlock(
                                bordered=True,
                                heading="Certification Regarding Lobbying",
                                text=_LOBBYING_CERTIFICATION_TEXT,
                            ),
                            SectionBlock(
                                children=[
                                    ReviewSubheadingBlock(title="Regarding Lobbying"),
                                    FieldBlock(field_name="lobbying_attestation"),
                                    FieldBlock(field_name="lobbying_signature"),
                                ],
                            ),
                        ],
                    ),
                    PermanentPageBlock(
                        title="Drug-Free Workplace Requirements",
                        subtitle=(
                            "Review the certification below and sign at the bottom of this page to "
                            "affirm compliance."
                        ),
                        children=[
                            AccordionBlock(
                                items=[
                                    AccordionItem(
                                        heading="Instructions for Certifications",
                                        text=_DRUG_FREE_WORKPLACE_CERTIFICATION_TEXT,
                                        is_expanded=False,
                                    )
                                ]
                            ),
                            SectionBlock(
                                children=[
                                    ReviewSubheadingBlock(title="Drug-Free Workplace Requirements"),
                                    FieldBlock(field_name="drug_free_attestation"),
                                    FieldBlock(field_name="drug_free_place_of_performance"),
                                    FieldBlock(
                                        field_name="drug_free_unidentified_workplaces",
                                        review_template_name="form_manager/forms/yes_no_display_review.html",
                                    ),
                                    FieldBlock(field_name="drug_free_signature"),
                                ],
                            ),
                        ],
                    ),
                    PermanentPageBlock(
                        title="Debarment, Suspension and Other Responsibility Matters",
                        subtitle=(
                            "Review the certification below and sign at the bottom of this page to "
                            "affirm compliance."
                        ),
                        children=[
                            AccordionBlock(
                                items=[
                                    AccordionItem(
                                        heading=(
                                            "Instructions for Certifications - Primary Covered Transactions"
                                        ),
                                        text=_DEBARMENT_PRIMARY_INSTRUCTIONS_TEXT,
                                        is_expanded=False,
                                    ),
                                    AccordionItem(
                                        heading=(
                                            "Instructions for Certifications - Lower Tier Covered Transactions"
                                        ),
                                        text=_DEBARMENT_LOWER_TIER_INSTRUCTIONS_TEXT,
                                        is_expanded=False,
                                    ),
                                ]
                            ),
                            TextBlock(
                                bordered=False,
                                text=_DEBARMENT_CERTIFICATION_TEXT,
                            ),
                            SectionBlock(
                                children=[
                                    ReviewSubheadingBlock(
                                        title="Debarment, Suspension and Other Responsibility Matters"
                                    ),
                                    FieldBlock(field_name="debarment_attestation"),
                                    FieldBlock(field_name="debarment_signature"),
                                ],
                            ),
                        ],
                    ),
                    PermanentPageBlock(
                        title="Environmental Tobacco Smoke",
                        subtitle=(
                            "Review the certification below and sign at the bottom of this page to "
                            "affirm compliance."
                        ),
                        children=[
                            TextBlock(
                                bordered=True,
                                heading="Certification Regarding Environmental Tobacco Smoke",
                                text=_TOBACCO_SMOKE_CERTIFICATION_TEXT,
                            ),
                            SectionBlock(
                                children=[
                                    ReviewSubheadingBlock(title="Environmental Tobacco Smoke"),
                                    FieldBlock(field_name="tobacco_attestation"),
                                    FieldBlock(field_name="tobacco_signature"),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )

    model_config = ConfigDict(use_enum_values=True)
