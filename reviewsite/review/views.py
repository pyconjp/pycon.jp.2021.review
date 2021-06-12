from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Proposal


@login_required
def list_proposals(request):
    proposals = Proposal.objects.order_by("sessionize_id")
    context = {"page_obj": proposals, "proposals_count": len(proposals)}
    return render(request, "review/list_proposals.html", context)
