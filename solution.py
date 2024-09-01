import time


class Agent:
    def __init__(self, phoneme_table, vocabulary):
        self.phoneme_table = phoneme_table
        self.vocabulary = vocabulary
        self.best_state = None
        self.subsitutions = {}
        for key in self.phoneme_table:
            for value in self.phoneme_table[key]:
                if value not in self.subsitutions:
                    self.subsitutions[value] = []
                self.subsitutions[value].append(key)

    def generate_neighbor1(self, state, environment, start_time, current_cost):
        words = state.split()

        for i, word in enumerate(words):
            for phoneme, substitutes in self.subsitutions.items():
                phoneme_pos = [j for j in range(
                    len(word)) if word.startswith(phoneme, j)]
                if phoneme_pos:
                    for substitute in substitutes:
                        for pos in phoneme_pos:
                            new_word = word[:pos] + \
                                substitute + word[pos+len(phoneme):]
                            new_state = ' '.join(
                                words[:i] + [new_word] + words[i+1:])

                            new_cost = environment.compute_cost(new_state)
                            if new_cost < current_cost:
                                state = new_state
                                current_cost = new_cost
                                print("Current state:", state)
                            elif time.time() - start_time > 240:
                                return state, current_cost

        return state, current_cost

    def generate_neighbor2(self, state, environment, start_time, current_cost):
        if (time.time() - start_time > 240):
            return state, current_cost

        # Beginning of the sentence
        for word in self.vocabulary:
            new_state = word + ' ' + state
            new_cost = environment.compute_cost(new_state)
            if new_cost < current_cost:
                state = new_state
                current_cost = new_cost
                print("Current state:", state)
                break
            elif time.time() - start_time > 240:
                return state, current_cost

        # End of the sentence
        for word in self.vocabulary:
            new_state = state + ' ' + word
            new_cost = environment.compute_cost(new_state)
            if new_cost < current_cost:
                state = new_state
                current_cost = new_cost
                print("Current state:", state)
                break
            elif time.time() - start_time > 240:
                return state, current_cost

        return state, current_cost

    def asr_corrector(self, environment):
        initial_state = environment.init_state
        initial_cost = environment.compute_cost(initial_state)
        current_state = initial_state
        current_cost = initial_cost
        self.best_state = current_state

        start_time = time.time()
        print("Initial state:", environment.init_state)

        current_state, current_cost = self.generate_neighbor1(
            current_state, environment, start_time, current_cost)
        print("Neighbor 1:", current_state)

        current_state, current_cost = self.generate_neighbor2(
            current_state, environment, start_time, current_cost)
        print("Neighbor 2:", current_state)
