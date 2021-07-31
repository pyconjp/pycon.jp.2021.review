def filter_proposals(proposals, parameters):
    specify_unreviewed_only = parameters.get("unreviewed")
    if specify_unreviewed_only:
        proposals = proposals.exclude(is_reviewed_already=1)
    audience_python_level = parameters.get("audience_python_level")
    if audience_python_level:
        proposals = proposals.filter(
            audience_python_level=audience_python_level
        )
    speaking_language = parameters.get("speaking_language")
    if speaking_language:
        proposals = proposals.filter(speaking_language=speaking_language)
    track = parameters.get("track")
    if track:
        proposals = proposals.filter(track=track)
    query = parameters.get("query")
    if query:
        for keyword in query.split():
            # 複数語句を入力されたらAND検索（簡単な実装に留め、複数語の完全一致は非サポート）
            proposals = proposals.filter(title__icontains=keyword)
    return proposals


def filter_reviews(reviews, parameters):
    if score := parameters.get("score"):
        reviews = reviews.filter(score=score)
    if audience_python_level := parameters.get("audience_python_level"):
        reviews = reviews.filter(proposal_python_level=audience_python_level)
    if track := parameters.get("track"):
        reviews = reviews.filter(proposal_track=track)
    if query := parameters.get("query"):
        for keyword in query.split():
            reviews = reviews.filter(proposal_title__icontains=keyword)
    return reviews
