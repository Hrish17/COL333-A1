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
        n = len(words)
        for i in range(n):
            word = words[i]
            changed = []
            while True:
                # neighbors = []
                state_updated = False
                for phoneme, substitutes in self.subsitutions.items():
                    phoneme_pos = [j for j in range(
                        len(word)) if word.startswith(phoneme, j) and j not in changed]
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
                                    state_updated = True
                                    words[i] = new_word
                                    word = new_word
                                    print("Current state:", state)
                                    if (len(phoneme) == len(substitute)):
                                        changed.append(pos)
                                    elif (len(phoneme) > len(substitute)):
                                        m = len(changed)
                                        for j in range(m):
                                            if changed[j] > pos:
                                                changed[j] += len(substitute) - \
                                                    len(phoneme)
                                        changed.append(pos)
                                    else:
                                        m = len(changed)
                                        for j in range(m):
                                            if changed[j] > pos:
                                                changed[j] += len(substitute) - \
                                                    len(phoneme)
                                        changed.append(pos)
                                        changed.append(pos+1)
                                    break
                                elif time.time() - start_time > 240:
                                    return state, current_cost
                            if state_updated:
                                break
                        if state_updated:
                            break
                    if state_updated:
                        break
                if not state_updated:
                    break

        return state, current_cost

    def generate_neighbor2(self, state, environment, start_time, current_cost):
        if (time.time() - start_time > 240):
            return state, current_cost

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
