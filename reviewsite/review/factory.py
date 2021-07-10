"""
$ python reviewsite/manage.py shell

>>> from review.factory import RandomProposalFactory
>>> RandomProposalFactory.create_batch(15)
"""

import factory
import factory.fuzzy
from faker import Faker

from .models import Proposal

Faker.seed(0)

fake = Faker()


class RandomProposalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Proposal

    sessionize_id = factory.Faker("pyint", min_value=210001, max_value=220000)

    title = factory.Faker("sentence")
    description = factory.LazyFunction(lambda: "\n\n".join(fake.paragraphs()))
    elevator_pitch = factory.Faker("paragraph")
    track = factory.fuzzy.FuzzyChoice(Proposal.SessionTrack.values)
    audience_python_level = factory.fuzzy.FuzzyChoice(
        Proposal.AudiencePythonKnowledge
    )
    audience_prior_knowledge = factory.LazyFunction(
        lambda: "\n".join(fake.sentences())
    )
    audience_take_away = factory.LazyFunction(
        lambda: "\n".join(fake.sentences())
    )
    motivation_and_why = factory.Faker("paragraph")
    # materials_url は一律で None とする
    speaking_language = factory.fuzzy.FuzzyChoice(
        Proposal.SpeakingLanguage.values
    )
    slide_language = factory.fuzzy.FuzzyChoice(Proposal.SlideLanguage.values)

    # reviewer_not_displayed_to は一律で None とする
    submit_user_id = factory.Faker("uuid4")
