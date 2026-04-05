from .feedback_engine import FeedbackEngine
from .decay_engine import DecayEngine
from .weight_adapter import WeightAdapter
from .reinforcement_engine import ReinforcementEngine


class LearningPipeline:

    def __init__(self, weights):

        self.feedback_engine = FeedbackEngine()
        self.decay_engine = DecayEngine()
        self.weight_adapter = WeightAdapter(weights)
        self.reinforcement_engine = ReinforcementEngine()

    def run(self, items):

        # 1. decay uygula
        items = self.decay_engine.apply(items)

        # 2. feedback al
        feedbacks = self.feedback_engine.ingest(items)

        # 3. weight güncelle
        self.weight_adapter.update(feedbacks)

        # 4. reinforce et
        items = self.reinforcement_engine.reinforce(items, feedbacks)

        return items
