class Perturbation:
    def __init__(self, magnitude, type):
        self.magnitude = magnitude
        self.type = type

    def apply(self, data):
        if self.type == 'adversarial':
            return self._apply_adversarial(data)
        elif self.type == 'data_poisoning':
            return self._apply_data_poisoning(data)
        else:
            raise ValueError("Unknown perturbation type")

    def _apply_adversarial(self, data):
        # Implement adversarial perturbation logic here
        return data + self.magnitude  # Placeholder logic

    def _apply_data_poisoning(self, data):
        # Implement data poisoning logic here
        return data - self.magnitude  # Placeholder logic

def generate_perturbations(data, perturbation_configs):
    perturbed_data = data.copy()
    for config in perturbation_configs:
        perturbation = Perturbation(config['magnitude'], config['type'])
        perturbed_data = perturbation.apply(perturbed_data)
    return perturbed_data