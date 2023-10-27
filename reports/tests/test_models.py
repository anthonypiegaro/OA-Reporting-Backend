from decimal import getcontext, Decimal
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase
from django.utils import timezone

from reports.models import (
    Report,
    ReportTemplate,
    Assessment,
    QualitativeAssessment,
    QuantitativeAssessment,
    QualitativeAssessmentScore,
    QuantitativeAssessmentScore,
    QualitativeAssessmentChoices,
    Drill
)

# Set the precision for Decimal instances
getcontext().prec = 5

class AssessmentCreationTest(TestCase):

    def setUp(self):
        data_quant = {
            "name": "assessment_quant",
            "assessment_type": "quantitative",
            "description": "Example description for a quant assessment",
            "unit": "pounds"
        }
        self.assessment_quant = Assessment.objects.create(**data_quant) 

        data_qual = {
            "name": "assessment_qual",
            "assessment_type": "qualitative",
            "description": "Example description for a quanl assessment",
            "unit": None
        }
        self.assessment_quanl = Assessment.objects.create(**data_qual) 

    def test_valid_name(self):
        name = "test"
        valid_assessment = Assessment.objects.create(
            name=name,
            assessment_type="quantitative",
            description="Test assessment description",
            unit="reps"
        )
        valid_assessment.full_clean()
        self.assertEqual(valid_assessment.name, name)
    
    def test_invalid_name(self):
        name = "A" * 101
        valid_assessment = Assessment.objects.create(
            name=name,
            assessment_type="quantitative",
            description="Test assessment description",
            unit="reps"
        )
        with self.assertRaises(ValidationError):
            valid_assessment.full_clean()
    
    def test_valid_assessment_type(self):
        quant_type = "quantitative"
        qual_type = "qualitative"

        valid_assessment_one = Assessment.objects.create(
            name="assess_one",
            assessment_type=quant_type,
            description="Test assessment description",
            unit="reps"
        )
        valid_assessment_two = Assessment.objects.create(
            name="assess_two",
            assessment_type=qual_type,
            description="Test assessment description",
            unit="reps"
        )
        valid_assessment_one.full_clean()
        valid_assessment_two.full_clean()

        self.assertEqual(valid_assessment_one.assessment_type, quant_type)
        self.assertEqual(valid_assessment_two.assessment_type, qual_type)

    def test_invalid_assessment_type(self):
        invalid_assessment = Assessment.objects.create(
            name="assess_one",
            assessment_type="",
            description="Test assessment description",
            unit="reps"
        )
        with self.assertRaises(ValidationError):
            invalid_assessment.full_clean()
        
    def test_str_method(self):
        exp_str = "assessment_qual assessment"
        self.assertEqual(str(self.assessment_quanl), exp_str)


class ReportTemplateCreationTest(TestCase):

    def setUp(self):
        assessment_one = Assessment.objects.create(
            name="assessment one",
            assessment_type="quantitative",
            description="Description testing example",
            unit="reps"
        )
        assessment_two = Assessment.objects.create(
            name="assessment two",
            assessment_type="quantitative",
            description="Description testing example",
            unit="m/s"
        )
        assessment_three = Assessment.objects.create(
            name="assessment one",
            assessment_type="qualitative",
            description="Description testing example",
            unit=None
        )

        self.report_template = ReportTemplate.objects.create(name="Report Template Example")

        self.report_template.assessments.set([
                assessment_one,
                assessment_two,
                assessment_three
        ])
    
    def test_valid_name(self):
        name = "Report Template Unique"
        template = ReportTemplate.objects.create(name=name)
        template.full_clean()
        self.assertEqual(template.name, name)

    def test_invalid_name(self):
        name = "A"*110
        template = ReportTemplate.objects.create(name=name)
        with self.assertRaises(ValidationError):
            template.full_clean()

    def test_non_unique_name_raises_error(self):
        with self.assertRaises(IntegrityError):
            template = ReportTemplate.objects.create(name="Report Template Example")
    
    def test_str_method(self):
        exp_str = "Report Template Example report template"
        self.assertEqual(str(self.report_template), exp_str)

class ReportCreationTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="testUser@test.com", 
            password="1jy3bHJGBYUGk687b!",
            first_name="Test",
            last_name="Tester"
        )

        assessment_one = Assessment.objects.create(
            name="assessment one",
            assessment_type="quantitative",
            description="Description testing example",
            unit="reps"
        )
        assessment_two = Assessment.objects.create(
            name="assessment two",
            assessment_type="quantitative",
            description="Description testing example",
            unit="m/s"
        )
        assessment_three = Assessment.objects.create(
            name="assessment one",
            assessment_type="qualitative",
            description="Description testing example",
            unit=None
        )

        self.report_template = ReportTemplate.objects.create(name="Report Template Example")

        self.report_template.assessments.set([
                assessment_one,
                assessment_two,
                assessment_three
        ])

        self.report_one = Report.objects.create(
            user=self.user,
            template=self.report_template,
        )

        self.report_one.assessments.set(
            self.report_template.assessments.all()
        )

    def test_valid_user(self):
        report = Report.objects.create(
            user=self.user,
            template=self.report_template,
        )
        report.full_clean()
        self.assertEqual(report.user, self.user)
    
    def test_invalid_user_raises_error(self):

        with self.assertRaises(ValueError):
            report = Report.objects.create(
                user="invalid user",
                template=self.report_template,
            )

    def test_valid_template(self):
        report = Report.objects.create(
            user=self.user,
            template=self.report_template,
        )
        report.full_clean()
        self.assertEqual(report.template, self.report_template)
    
    def test_invalid_template(self):
        with self.assertRaises(ValueError):
            report = Report.objects.create(
                user=self.user,
                template="Invalid template",
            )

    def test_creation_date(self):
        report = Report.objects.create(
            user=self.user,
            template=self.report_template,
        )
        report.full_clean()
        self.assertEqual(report.creation_date, timezone.localtime(timezone.now()).date())
    
    def test_str_method(self):
        exp_str = "Report for Test Tester made from Report Template Example"
        self.assertEqual(str(self.report_one), exp_str)

class QuantitativeAssessmentCreationTest(TestCase):

    def setUp(self):
        data_quant = {
            "name": "assessment_quant",
            "assessment_type": "quantitative",
            "description": "Example description for a quant assessment",
            "unit": "pounds"
        }
        self.assessment_quant = Assessment.objects.create(**data_quant)
        data_quant = {
            "assessment": self.assessment_quant,
            "passing_score":  Decimal("10"),
            "passing_condition": "gt"
        }
        self.quantitative_assessment = QuantitativeAssessment.objects.create(**data_quant)

        data_quant_two = {
            "name": "assessment_quant_two",
            "assessment_type": "quantitative",
            "description": "Example description for a quant assessment",
            "unit": "pounds"
        }
        self.assessment_quant_two = Assessment.objects.create(**data_quant_two)

    def test_valid_assessment(self):
        assessment = self.assessment_quant_two
        data = {
            "assessment": assessment,
            "passing_score":  Decimal("10"),
            "passing_condition": "lte",
        }
        quant_assessment = QuantitativeAssessment.objects.create(**data)
        quant_assessment.full_clean()
        self.assertEqual(quant_assessment.assessment, assessment)

    def test_invalid_assessment(self):
        assessment = "assessment"
        data = {
            "assessment": assessment,
            "passing_score":  Decimal("10"),
            "passing_condition": "lte",
        }
        with self.assertRaises(ValueError):
            quant_assessment = QuantitativeAssessment.objects.create(**data)
            
    
    def test_duplicate_assessment(self):
        assessment = self.assessment_quant
        data = {
            "assessment": assessment,
            "passing_score": Decimal("10"),
            "passing_condition": "lte",
        }
        with self.assertRaises(ValidationError):
            quant_assessment = QuantitativeAssessment.objects.create(**data)
            
    def test_valid_passing_score(self):
        passing_score = Decimal("23.1")
        data = {
            "assessment": self.assessment_quant_two,
            "passing_score": passing_score,
            "passing_condition": "eq"
        }
        quant_assessment = QuantitativeAssessment.objects.create(**data)
        quant_assessment.full_clean()
        self.assertEqual(quant_assessment.passing_score, passing_score)

    def test_invalid_passing_score(self):
        passing_score = "string"
        data = {
            "assessment": self.assessment_quant_two,
            "passing_score": passing_score,
            "passing_condition": "eq"
        }
        with self.assertRaises(ValidationError):
            quant_assessment = QuantitativeAssessment.objects.create(**data)

    def test_valid_passing_condition(self):
        passing_condition = "lte"
        data = {
            "assessment": self.assessment_quant_two,
            "passing_score": Decimal("10"),
            "passing_condition": passing_condition
        }
        quant_assessment = QuantitativeAssessment.objects.create(**data)
        quant_assessment.full_clean()
        self.assertEqual(quant_assessment.passing_condition, passing_condition)

    def test_invalid_passing_condition(self):
        passing_condition = "non-condition"
        data = {
            "assessment": self.assessment_quant_two,
            "passing_score": Decimal("10"),
            "passing_condition": passing_condition
        }

        with self.assertRaises(ValidationError):
            quant_assessment = QuantitativeAssessment.objects.create(**data)

    def test_str_method(self):
        exp_str = "Quantitative details for assessment_quant"
        self.assertEqual(str(self.quantitative_assessment), exp_str)


class QuantitativeAssessmentScoreCreationTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(
            email="test@email.com",
            password="Ajsh68dgFTyjhkg76ftr!",
            first_name="Jane",
            last_name="Doe"
        )
        self.assessment_one = Assessment.objects.create(
            name="Broad Jump",
            assessment_type="quantitative",
            description="Jump from still position",
            unit="inches"
        )
        self.assessment_two = Assessment.objects.create(
            name="10 Yard Pro Agility",
            assessment_type="quantitative",
            description="Fast as possible",
            unit="seconds"
        )
        self.assessment_three = Assessment.objects.create(
            name="1RM Squat",
            assessment_type="quantitative",
            description="Strength test",
            unit="pounds"
        )
        self.assessment_four = Assessment.objects.create(
            name="Equals One",
            assessment_type="quantitative",
            description="Arbitrary to test the equals",
            unit=None
        )
        self.assessment_five = Assessment.objects.create(
            name="Bat Time to Contact",
            assessment_type="quantitative",
            description="Time from start of swing to contact",
            unit="seconds"
        )
        self.quantitative_assessment_one = QuantitativeAssessment.objects.create(
            assessment=self.assessment_one,
            passing_score=Decimal("115"),
            passing_condition="gte"
        )
        self.quantitative_assessment_two = QuantitativeAssessment.objects.create(
            assessment=self.assessment_two,
            passing_score=Decimal("1.8"),
            passing_condition="lt"
        )
        self.quantitative_assessment_three = QuantitativeAssessment.objects.create(
            assessment=self.assessment_three,
            passing_score=Decimal("450"),
            passing_condition="gt"
        )
        self.quantitative_assessment_four = QuantitativeAssessment.objects.create(
            assessment=self.assessment_four,
            passing_score=Decimal("1"),
            passing_condition="eq"
        )
        self.quantitative_assessment_five = QuantitativeAssessment.objects.create(
            assessment=self.assessment_five,
            passing_score=Decimal("0.8"),
            passing_condition="lte"
        )
        self.report_template = ReportTemplate.objects.create(name="Physical Report")
        self.report_template.assessments.set([
            self.assessment_one, 
            self.assessment_two,
            self.assessment_three,
            self.assessment_four,
            self.assessment_five,
        ])
        self.report = Report.objects.create(
            user=self.user,
            template=self.report_template,
        )
        self.report.assessments.set(
            self.report_template.assessments.all()
        )
        self.quant_score_one = QuantitativeAssessmentScore(
            assessment=self.assessment_one,
            quantitative_assessment = self.quantitative_assessment_one,
            user=self.user,
            report=self.report,
            score=Decimal(117.52)
        )
        self.quant_score_two = QuantitativeAssessmentScore(
            assessment=self.assessment_two,
            quantitative_assessment = self.quantitative_assessment_two,
            user=self.user,
            report=self.report,
            score=Decimal(1.85)
        )
        self.quant_score_three = QuantitativeAssessmentScore(
            assessment=self.assessment_three,
            quantitative_assessment = self.quantitative_assessment_three,
            user=self.user,
            report=self.report,
            score=Decimal(315)
        )
        self.quant_score_four = QuantitativeAssessmentScore(
            assessment=self.assessment_four,
            quantitative_assessment = self.quantitative_assessment_four,
            user=self.user,
            report=self.report,
            score=Decimal(1.00)
        )
        self.quant_score_five = QuantitativeAssessmentScore(
            assessment=self.assessment_five,
            quantitative_assessment = self.quantitative_assessment_five,
            user=self.user,
            report=self.report,
            score=Decimal(0.5)
        )

    def test_valid_score(self):
        score = Decimal(1.53)
        quant_score = QuantitativeAssessmentScore(
            assessment=self.assessment_two,
            quantitative_assessment = self.quantitative_assessment_two,
            user=self.user,
            report=self.report,
            score=score
        )
        self.assertEqual(quant_score.score, score)

    def test_invalid_score(self):
        score = "Invalid Score"
        quant_score = QuantitativeAssessmentScore(
            assessment=self.assessment_two,
            quantitative_assessment = self.quantitative_assessment_two,
            user=self.user,
            report=self.report,
            score=score
        )
        with self.assertRaises(ValidationError):
            quant_score.full_clean()

    def test_passed_method(self):
        self.assertEqual(self.quant_score_one.passed(), True)
        self.assertEqual(self.quant_score_two.passed(), False)
        self.assertEqual(self.quant_score_three.passed(), False)
        self.assertEqual(self.quant_score_four.passed(), True)
        self.assertEqual(self.quant_score_five.passed(), True)
    
    def test_str_method(self):
        exp_str = "Jane Doe's score for Broad Jump assessment for report Physical Report"
        self.assertEqual(str(self.quant_score_one), exp_str)

class QualitativeAssessmentChoicesCreationTest(TestCase):
    
    def setUp(self):
        self.assessment = Assessment.objects.create(
            name="Qual Assessment",
            assessment_type="qualitative",
            description="A qualitative assessment",
            unit=None
        )
        self.choice_one = QualitativeAssessmentChoices.objects.create(
            assessment=self.assessment,
            choice="left"
        )
        self.choice_two = QualitativeAssessmentChoices.objects.create(
            assessment=self.assessment,
            choice="center"
        )
        self.choice_three = QualitativeAssessmentChoices.objects.create(
            assessment=self.assessment,
            choice="right"
        )
    
    def test_valid_assessment(self):
        assessment = self.assessment
        choice = QualitativeAssessmentChoices.objects.create(
            assessment=assessment,
            choice="below"
        )
        choice.full_clean()
        self.assertEqual(choice.assessment, assessment)
    
    def test_invalid_assessmnet(self):
        assessment = "Invalid assessment"
        with self.assertRaises(ValueError):
            choice = QualitativeAssessmentChoices.objects.create(
                assessment=assessment,
                choice="below"
            )
    
    def test_valid_choice(self):
        choice = "below"
        qual_choice = QualitativeAssessmentChoices.objects.create(
            assessment=self.assessment,
            choice=choice
        )
        qual_choice.full_clean()
        self.assertEqual(qual_choice.choice, choice)
    
    def test_invalid_choice(self):
        choice = "A"*150
        with self.assertRaises(ValidationError):
            qual_choice = QualitativeAssessmentChoices.objects.create(
                assessment=self.assessment,
                choice=choice
            )
    
    def test_str_method(self):
        exp_str = "left is a choice option for the Qual Assessment assessment"
        self.assertEqual(str(self.choice_one), exp_str)

class QualitativeAssessmentCreationTest(TestCase):

    def setUp(self):
        self.assessment = Assessment.objects.create(
            name="Taste",
            assessment_type="qualitative",
            unit=None
        )
        self.choice_one = QualitativeAssessmentChoices.objects.create(
            assessment=self.assessment,
            choice="bitter"
        )
        self.choice_two = QualitativeAssessmentChoices.objects.create(
            assessment=self.assessment,
            choice="salty"
        )
        self.choice_three = QualitativeAssessmentChoices.objects.create(
            assessment=self.assessment,
            choice="perfect"
        )
        self.qual_assessment = QualitativeAssessment.objects.create(
            assessment=self.assessment,
            passing_score=self.choice_three
        )

        self.assessment_two = Assessment.objects.create(
            name="Smell",
            assessment_type="qualitative",
            unit=None
        )
        self.assessment_two_choice_one = QualitativeAssessmentChoices.objects.create(
            assessment=self.assessment_two,
            choice="Yummy"
        )
    
    def test_valid_assessment(self):
        assessment = self.assessment_two
        qual_assessment = QualitativeAssessment.objects.create(
            assessment=assessment,
            passing_score=self.choice_three
        )
        qual_assessment.full_clean()
        self.assertEqual(qual_assessment.assessment, assessment)
    
    def test_invalid_assessment(self):
        assessment = "Invalid Assessment"
        with self.assertRaises(ValueError):
            qual_assessment = QualitativeAssessment.objects.create(
                assessment=assessment,
                passing_score=self.choice_three
            )

    def test_non_unique_assessment(self):
        assessment = self.assessment
        with self.assertRaises(ValidationError):
            qual_assessment = QualitativeAssessment.objects.create(
                assessment=assessment,
                passing_score=self.choice_three
            )

    def test_valid_passing_score(self):
        valid_score = self.assessment_two_choice_one
        qual_assessment = QualitativeAssessment.objects.create(
            assessment=self.assessment_two,
            passing_score=valid_score
        )
        qual_assessment.full_clean()
        self.assertEqual(qual_assessment.passing_score, valid_score)

    def test_invalid_passing_score(self):
            invalid_score = "Invalid Score"
            with self.assertRaises(ValueError):
                qual_assessment = QualitativeAssessment.objects.create(
                    assessment=self.assessment_two,
                    passing_score=invalid_score
                )

    def test_str_method(self):
        exp_str = "Qualitative assessment details for Taste"
        self.assertEqual(str(self.qual_assessment), exp_str)

class QualitativeAssessmentScoreCreationTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(
            email="test@test.com",
            password="hGyjghkjhgbHGB78Ghj!",
            first_name="Jane",
            last_name="Doe"
        )
        self.assessment = Assessment.objects.create(
            name="Taste",
            assessment_type="qualitative",
            unit=None
        )
        self.template = ReportTemplate.objects.create(
            name="Food",
        )
        self.template.assessments.set([self.assessment])
        self.report = Report.objects.create(
            user=self.user,
            template=self.template,
        )
        self.report.assessments.set(self.template.assessments.all())
        self.choice_one = QualitativeAssessmentChoices.objects.create(
            assessment=self.assessment,
            choice="bitter"
        )
        self.choice_two = QualitativeAssessmentChoices.objects.create(
            assessment=self.assessment,
            choice="salty"
        )
        self.choice_three = QualitativeAssessmentChoices.objects.create(
            assessment=self.assessment,
            choice="perfect"
        )
        self.qual_assessment = QualitativeAssessment.objects.create(
            assessment=self.assessment,
            passing_score=self.choice_three
        )
        self.qual_score = QualitativeAssessmentScore.objects.create(
            assessment=self.assessment,
            qualitative_assessment=self.qual_assessment,
            user=self.user,
            report=self.report,
            score=self.choice_three
        )
        self.qual_score_two = QualitativeAssessmentScore.objects.create(
            assessment=self.assessment,
            qualitative_assessment=self.qual_assessment,
            user=self.user,
            report=self.report,
            score=self.choice_one
        )
    
    def test_valid_score(self):
        score = self.choice_one
        qual_score = QualitativeAssessmentScore.objects.create(
            assessment=self.assessment,
            qualitative_assessment=self.qual_assessment,
            user=self.user,
            report=self.report,
            score=score
        )
        qual_score.full_clean()
        self.assertEqual(qual_score.score, score)
    
    def test_invalid_score(self):
        score="Invalid Score"
        with self.assertRaises(ValueError):
            qual_score = QualitativeAssessmentScore.objects.create(
            assessment=self.assessment,
            qualitative_assessment=self.qual_assessment,
            user=self.user,
            report=self.report,
            score=score
        )
    
    def test_passed_method(self):
        self.assertEqual(self.qual_score.passed(), True)
        self.assertEqual(self.qual_score_two.passed(), False)
    
    def test_str_method(self):
        exp_str = "Jane Doe's score for Taste for report Food"
        self.assertEqual(str(self.qual_score), exp_str)

class DrillCreationTest(TestCase):
    
    def setUp(self):
        self.assessment = Assessment.objects.create(
            name="Taste",
            assessment_type="qualitative",
            unit=None
        )
        self.drill_one = Drill.objects.create(
            name="Drill One",
            url="https://www.linkedin.com/in/anthony-piegaro/"
        )
        self.drill_one.assessments.add(self.assessment)
    
    def test_valid_assessment(self):
        assessment = self.assessment
        drill_two = Drill.objects.create(
            name="Drill Two",
            url="https://www.youtube.com/@anthonypiegaro"
        )
        drill_two.assessments.add(assessment)
        drill_two.full_clean()
        self.assertEqual(list(drill_two.assessments.all()), [assessment])
    
    def test_invalid_assessment(self):
        assessment = "Invalid assessment"
        drill_two = Drill.objects.create(
            name="Drill Two",
            url="https://www.youtube.com/@anthonypiegaro"
        )
        with self.assertRaises(ValueError):
            drill_two.assessments.add(assessment)
    
    def test_valid_name(self):
        name = "Drill Two"
        drill_two = Drill.objects.create(
            name=name,
            url="https://www.youtube.com/@anthonypiegaro"
        )
        drill_two.full_clean()
        self.assertEqual(drill_two.name, name)
    
    def test_invalid_name(self):
        name = "a"*300
        drill_two = Drill.objects.create(
            name=name,
            url="https://www.youtube.com/@anthonypiegaro"
        )
        with self.assertRaises(ValidationError):
            drill_two.full_clean()
    
    def test_valid_url(self):
        url = "https://www.youtube.com/@anthonypiegaro"
        drill_two = Drill.objects.create(
            name="Drill Two",
            url=url
        )
        drill_two.full_clean()
        self.assertEqual(drill_two.url, url)
    
    def test_invalid_url(self):
        url = "a"*300
        drill_two = Drill.objects.create(
            name="Drill Two",
            url=url
        )
        with self.assertRaises(ValidationError):
            drill_two.full_clean()
        
    def test_str_method(self):
        exp_str = "Drill One is recommended drill"
        self.assertEqual(str(self.drill_one), exp_str)
