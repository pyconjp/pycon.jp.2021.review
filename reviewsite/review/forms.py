from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("score", "comment")

    def clean(self):
        score = self.cleaned_data["score"]
        comment = self.cleaned_data["comment"]
        if score == Review.ReviewScore.NO and not comment:
            raise forms.ValidationError("スコアがNOの場合は、コメントを必ず入力してください")
