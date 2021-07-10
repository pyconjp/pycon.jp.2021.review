from django import forms

from .models import Proposal, Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("score", "comment")

    def clean(self):
        score = self.cleaned_data["score"]
        comment = self.cleaned_data["comment"]
        if score == Review.ReviewScore.NO and not comment:
            raise forms.ValidationError("スコアがNOの場合は、コメントを必ず入力してください")


def insert_initial_option(options):
    options.insert(0, ("", "選んでください"))
    return options


class ProposalSearchForm(forms.Form):
    audience_python_level = forms.ChoiceField(
        choices=insert_initial_option(
            Proposal.AudiencePythonKnowledge.choices
        ),
        required=False,
        label=Proposal.audience_python_level.field.verbose_name,
    )
    speaking_language = forms.ChoiceField(
        choices=insert_initial_option(Proposal.SpeakingLanguage.choices),
        required=False,
        label=Proposal.speaking_language.field.verbose_name,
    )
    track = forms.ChoiceField(
        choices=insert_initial_option(Proposal.SessionTrack.choices),
        required=False,
        label=Proposal.track.field.verbose_name,
    )
    query = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "次の語句を含む"}),
        required=False,
        label=Proposal.title.field.verbose_name,
    )
