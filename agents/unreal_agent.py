class UnrealAgent:
    def __init__(self):
        self.name = "Unreal Agent"

    def send_spec(self, spec):
        print("Spec sent to Unreal Engine:", spec)
        return True

    def receive_feedback(self, feedback):
        print("Feedback received from Unreal Engine:", feedback)
        return True
