from rest_framework.decorators import api_view
from rest_framework.response import Response
from projects.models import Project, Tag
from .serializers import ProjectSerializer


@api_view(['GET'])
def routes(request):
    routes = [
        {'GET': '/api/projects'},
        {'DELETE': '/api/remove-tag'},
    ]

    return Response(routes)


@api_view(['GET'])
def projects(request):
    projects = Project.objects.all()
    serialzier = ProjectSerializer(projects, many=True)
    return Response(serialzier.data)


@api_view(['DELETE'])
def remove_tag(request):
    tag_id = request.data['tag']
    project_id = request.data['project']
    print('TAG_ID', tag_id)
    print('PROJECT_ID', project_id)

    tag = Tag.objects.get(id=tag_id)
    project = Project.objects.get(id=project_id)

    project.tags.remove(tag)
