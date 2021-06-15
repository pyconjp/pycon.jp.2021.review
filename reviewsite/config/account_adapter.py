from allauth.account.adapter import DefaultAccountAdapter


class NoNewUsersAccountAdapter(DefaultAccountAdapter):
    # ref: https://stackoverflow.com/a/29799664
    def is_open_for_signup(self, request):
        return False
