from collections import defaultdict

referrals = defaultdict(int)
creator_scores = defaultdict(float)

def record_referral(inviter_id):
    referrals[inviter_id] += 1
    creator_scores[inviter_id] += 0.5

def record_engagement(user_id):
    if not user_id:
        return
    creator_scores[user_id] += 0.1

def get_creator_score(user_id):
    return creator_scores[user_id]
