from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class NoNewUsersAccountAdapter(DefaultAccountAdapter):
    # ref: https://stackoverflow.com/a/29799664
    def is_open_for_signup(self, request):
        return False


class AllowSocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, sociallogin):
        # Enable to create user account by Sign in with Slack
        return True
