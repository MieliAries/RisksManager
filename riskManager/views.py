import base64
import io

import matplotlib.pyplot as plt
import openpyxl
from django.shortcuts import render, redirect

from riskManager.dtos import RiskDTO, ProcessDTO
from riskManager.forms import RiskForm, ProcessForm
from riskManager.models import Risk, Process


# Create your views here.


# Return all teams data
def process_list(request):
    process = list()
    for process in Process.objects():
        process.append(ProcessDTO(process.id.__str__(), process.name, process.process).__dict__)
    return render(request, "Process-list.html", {'process': process})


def process_create(request):
    if request.method == "POST":
        form = ProcessForm(request.POST)
        if form.is_valid():
            form_data = form.data
            process = Process()
            process.name = form_data.get("name")
            process.process = form_data.get("description")
            process.save()
            return redirect('process-list')
    else:
        form = ProcessForm()
    return render(request, 'process-create.html', {'form': form})


def process_update(request, process_id):
    process = Process.objects.get(id=process_id)
    form = ProcessForm(initial={'name': process.name, 'location': process.office_location})
    if request.method == "POST":
        form = ProcessForm(request.POST)
        if form.is_valid():
            form_data = form.data
            process.name = form_data.get("name")
            process.process = form_data.get("process")
            process.save()
            return redirect('process-list')
    return render(request, 'process-update.html', {'form': form})


def process_delete(request, process_id):
    Process.objects.get(id=process_id).delete()
    Risk.objects.get(process_id=process_id).delete()
    return redirect('process-list')


SALARY_BORDERS = [1500, 4000]
TENURE_BORDERS = [2, 5]


def process_view(request, process_id):
    process = Process.objects.get(id=process_id)

    quality = 1
    cost = 1
    speed = 1

    risks = list()
    for risk in Risk.objects(process_id=process_id):
        risks.append(RiskDTO(
            risk.id.__str__(),
            risk.name,
            risk.importance,
            risk.description,
        ).__dict__)

        risk_important = 0
        if risk.importance <= IMPORTANCE_BORDERS[0]:
            risk_important = 1
        elif IMPORTANCE_BORDERS[0] < risk.importance < IMPORTANCE_BORDERS[1]:
            risk_important = 2
        elif risk.importance >= IMPORTANCE_BORDERS[1]:
            risk_important = 3

        important += risk_important

    speed += risks.__len__()
    image = io.BytesIO()
    labels = 'Speed', 'Cost'
    sizes = [speed, cost]

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, shadow=True, startangle=90)
    ax1.axis('equal')
    plt.savefig(image, format='png')
    image.seek(0)
    chart_base64 = base64.b64encode(image.read()).decode("utf-8")

    return render(request, "process-view.html",
                  {
                      'risks': risks,
                      'process_id': process_id,
                      'process_name': process.name,
                      'chart_base64': chart_base64
                  })


def risk_create(request, process_id):
    if request.method == "POST":
        form = RiskForm(request.POST)
        if form.is_valid():
            form_data = form.data
            risk = Risk()
            risk.process_id = process_id
            risk.name = form_data.get("name")
            risk.importance = form_data.get("importance")
            risk.description = form_data.get("description")
            risk.save()
            return redirect('/process-view/' + process_id)
    else:
        form = RiskForm()
    return render(request, 'risk-create.html', {'form': form, 'process_id': process_id})


def risk_upload(request, process_id):
    if request.method == "POST":
        risk_list = request.FILES.get("risk_list")
        workbook = openpyxl.load_workbook(risk_list)
        worksheet = workbook["Risks"]

        for row in worksheet.iter_rows(min_row=2, values_only=True):
            risk = Risk()
            risk.process_id = process_id
            risk.name = row[0]
            risk.importance = row[1]
            risk.description = row[2]
            risk.save()

    return redirect('/process-view/' + process_id)


def risk_update(request, risk_id):
    risk = Risk.objects.get(id=risk_id)
    form = RiskForm(initial={'name': risk.name,
                                 'importance': risk.importance,
                                 'description': risk.description})
    if request.method == "POST":
        form = RiskForm(request.POST)
        if form.is_valid():
            form_data = form.data
            risk.name = form_data.get("name")
            risk.save()
            return redirect('/process-view/' + risk.process_id)
    return render(request, 'risk-update.html', {'form': form, 'process_id': risk.process_id})


def risk_delete(request, risk_id):
    risk = Risk.objects.get(id=risk_id)
    risk.delete()
    return redirect('/process-view/' + risk.process_id)
