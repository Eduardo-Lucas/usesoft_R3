from django.http import HttpResponse
from django.shortcuts import render

from .resources import UfResource

from tablib import Dataset


def export(request):
    uf_resource = UfResource()
    dataset = uf_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="uf.csv"'


def simple_upload(request):
    if request.method == 'POST':
        uf_resource = UfResource()
        dataset = Dataset()
        new_ufs = request.FILES['myfile']

        imported_data = dataset.load(new_ufs.read())
        result = uf_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            uf_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'core/simple_upload.html')
