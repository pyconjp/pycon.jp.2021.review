from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Case, Count, When
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProposalSearchForm, ReviewForm
from .models import Proposal
from .search import filter_proposals


def retrieve_page(paginator, request):
    page = request.GET.get("page")
    if page:
        page_obj = paginator.page(page)
    else:
        page_obj = paginator.page(1)
    return page_obj


@login_required
def list_proposals(request):
    # レビュアー自身が提出したプロポーザルは除く
    proposals = Proposal.objects.exclude(
        reviewer_not_displayed_to=request.user
    )
    # すでにレビューしたプロポーザルにフラグを立てて区別
    proposals = proposals.annotate(
        is_reviewed_already=Count(
            Case(When(reviews__reviewer=request.user, then=1))
        )
    )
    proposals = proposals.annotate(count=Count("reviews")).order_by(
        "count", "sessionize_id"
    )
    proposals = filter_proposals(proposals, request.GET)

    paginator = Paginator(proposals, settings.PROPOSALS_PER_PAGE)
    page_obj = retrieve_page(paginator, request)

    form = ProposalSearchForm(request.GET)
    context = {
        "page_obj": page_obj,
        "proposals_count": paginator.count,
        "form": form,
    }
    return render(request, "review/list_proposals.html", context)


@login_required
def detail_proposal(request, sessionize_id):
    proposal = get_object_or_404(Proposal, sessionize_id=sessionize_id)
    if proposal.reviewer_not_displayed_to == request.user:
        raise PermissionDenied
    review_by_user = proposal.reviews.filter(reviewer=request.user).first()
    other_proposals = (
        Proposal.objects.filter(submit_user_id=proposal.submit_user_id)
        .exclude(sessionize_id=sessionize_id)
        .order_by("sessionize_id")
    )

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review_by_user)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.proposal = proposal
            review.save()

            messages.add_message(request, messages.SUCCESS, "レビューが保存されました")
            return redirect(
                "review:detail_proposal", sessionize_id=proposal.sessionize_id
            )
        messages.add_message(request, messages.ERROR, "レビューが保存できませんでした")
    else:
        form = ReviewForm(instance=review_by_user)

    context = {
        "proposal": proposal,
        "form": form,
        "review_by_user": review_by_user,
        "other_proposals": other_proposals,
    }
    return render(request, "review/detail_proposal.html", context=context)
