class WeightAdapter:

    def __init__(self, weights):
        self.weights = weights

    def update(self, feedbacks):

        for fb in feedbacks:

            topic = fb.get("topic", "")
            success = fb.get("success", False)

            for key in self.weights:

                if key in topic.lower():

                    if success:
                        self.weights[key] += 0.1
                    else:
                        self.weights[key] -= 0.05

                    # sınır koy
                    self.weights[key] = max(0.5, min(self.weights[key], 5))

        return self.weights
