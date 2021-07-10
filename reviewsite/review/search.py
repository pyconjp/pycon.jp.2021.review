def filter_proposals(proposals, parameters):
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
    return proposals
