from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from .models import Proposal


@login_required
def list_proposals(request):
    proposals = Proposal.objects.order_by("sessionize_id")
    context = {"page_obj": proposals, "proposals_count": len(proposals)}
    return render(request, "review/list_proposals.html", context)


@login_required
def detail_proposal(request, sessionize_id):
    proposal = get_object_or_404(Proposal, sessionize_id=sessionize_id)
    return render(
        request, "review/detail_proposal.html", {"proposal": proposal}
    )
