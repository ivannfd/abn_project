import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView

from abn.a_posteriori_propagation import get_a_posteriori_estimates


class Interface(TemplateView):
    template_name = 'index.html'

    def get(self, request):
        ctx = {}
        return render(request, self.template_name, ctx)


class ABNChecker(TemplateView):
    def post(self, request):
        json_data = json.loads(request.body)['body']
        print(json_data)
        conjuncts_count = int(json_data['conjuncts_count'])
        evidence_data = json_data['evidence_data']
        conjuncts_data = [float(element) for element in json_data['conjuncts_data']]
        new_estimates = get_a_posteriori_estimates(conjuncts_count, conjuncts_data, evidence_data)
        return JsonResponse({"conjuncts_data": new_estimates.tolist()})
