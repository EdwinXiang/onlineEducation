from django.shortcuts import render
from django.views.generic.base import View
from apps.organization.models import CourseOrg,CityDict

# Create your views here.
class OrgView(View):
    '''课程机构'''
    def get(self, request):

        # 取出所有的k课程机构
        all_orgs = CourseOrg.objects.all()
        org_onums = all_orgs.count()
        # 取出所有的城市
        all_citys = CityDict.objects.all()
        return render(request, 'org-list.html', {
            "all_orgs": all_orgs,
            "all_citys": all_citys,
            "org_onums": org_onums
        })

