from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ReviewForm
from .models import Proposal


@login_required
def list_proposals(request):
    proposals = Proposal.objects.order_by("sessionize_id")
    context = {"page_obj": proposals, "proposals_count": len(proposals)}
    return render(request, "review/list_proposals.html", context)


@login_required
def detail_proposal(request, sessionize_id):
    proposal = get_object_or_404(Proposal, sessionize_id=sessionize_id)
    review_by_user = proposal.reviews.filter(reviewer=request.user).first()

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review_by_user)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.proposal = proposal
            review.save()

            return redirect(
                "review:detail_proposal", sessionize_id=proposal.sessionize_id
            )
    else:
        form = ReviewForm(instance=review_by_user)

    context = {"proposal": proposal, "form": form}
    return render(request, "review/detail_proposal.html", context=context)
