from ariadne import QueryType, MutationType, load_schema_from_path, make_executable_schema
from django.forms.models import model_to_dict
from .models import *

# Load schema type definitions from graphql schema
type_defs = load_schema_from_path("schema.graphql")

query = QueryType()
mutation = MutationType()

@query.field("getAllStudentAssignments")
def resolve_get_all_student_assignments(_, info, studentID):
    try:
        scores = [{
            "assignment": score.assignment,
            "score": score.score}
            for score in Score.objects.filter(student_id=studentID)]
        payload = {
            "success": True,
            "scores": scores
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload

@mutation.field("createAssignment")
def resolve_create_assignment(_, info, input):
    try:
        assignment = Assignment.objects.create(
            title=input["title"],
            description=input["description"],
            classroom_id=input["classroom_id"]
        )
        payload = {
            "success": True,
            "assignment": assignment
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload

@mutation.field("addScore")
def resolve_add_score(_, info, input):
    try:
        student = Student.objects.get(pk=input["student_id"])
        assignment = Assignment.objects.get(pk=input["assignment_id"])
        if student.classroom.id == assignment.classroom.id:
            existing_score = Score.objects.filter(student_id=input["student_id"],
                                                  assignment_id=input["assignment_id"])
            score, created = Score.objects.update_or_create(
                student_id=input["student_id"],
                assignment_id=input["assignment_id"],
                defaults={"score": input["score"]}
            )
        else:
            raise Exception("Student not in the same class as the assignment.") 
        payload = {
            "success": True,
            "score": score
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload

@mutation.field("removeAssignment")
def resolve_remove_assignment(_, info, assignmentId):
    try:
        assignment = Assignment.objects.get(pk=assignmentId)
        assignment.delete()
        payload = {
            "success": True
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload

@mutation.field("removeScore")
def resolve_remove_score(_, info, scoreId):
    try:
        score = Score.objects.get(pk=scoreId)
        score.delete()
        payload = {
            "success": True
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload

schema = make_executable_schema(type_defs, query, mutation)