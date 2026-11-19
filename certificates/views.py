from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Certificate


@login_required
def my_certificates(request):
    certificates = Certificate.objects.filter(
        student=request.user
    ).select_related("course")

    return render(
        request,
        "certificates/my_certificates.html",
        {"certificates": certificates}
    )


@login_required
def view_certificate(request, certificate_id):
    certificate = get_object_or_404(
        Certificate,
        id=certificate_id,
        student=request.user
    )

    return render(
        request,
        "certificates/certificate_detail.html",
        {"certificate": certificate}
    )