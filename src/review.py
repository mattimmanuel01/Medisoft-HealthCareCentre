class Review:
    #a class which stores the reviews of people for a health provider or health centre
    def __init__(self, patient, feedback, rating):
        self._reviewer = patient
        self._feedback = feedback
        self._rating = rating

    def get_reviewer(self):
        return self._reviewer

    def get_feedback(self):
        if not self._feedback:
            return "no feedback was left"
        return self._feedback

    def get_rating(self):
        return self._rating
