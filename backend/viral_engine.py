from collections import defaultdict

invites = defaultdict(int)

def register_invite(inviter_id):

    invites[inviter_id] += 1

    return invites[inviter_id]


def get_invite_count(user_id):

    return invites[user_id]
