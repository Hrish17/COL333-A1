import time
import json


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

    # def local_beam_search(self, beam, start_time, current_cos):
    #     pass

    def generate_neighbor1(self, state, environment, start_time, current_cost):
        words = state.split()
        n = len(words)
        for i in range(n):
            word = words[i]
            changed = []
            while True:
                neighbor_state = ""
                neighbor_cost = 0
                neighbor_pos = 0
                neighbor_word = ""
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
                                    if (neighbor_state == "" or new_cost < neighbor_cost):
                                        neighbor_state = new_state
                                        neighbor_cost = new_cost
                                        neighbor_pos = pos
                                        neighbor_word = new_word
                                elif time.time() - start_time > 240:
                                    return state, current_cost
                if neighbor_state == "" or len(changed) == len(word):
                    break
                if neighbor_state != "":
                    if (len(word) == len(neighbor_word)):
                        changed.append(neighbor_pos)
                    elif (len(word) > len(neighbor_word)):
                        m = len(changed)
                        for j in range(m):
                            if changed[j] > neighbor_pos:
                                changed[j] += len(neighbor_word) - \
                                    len(word)
                        changed.append(neighbor_pos)
                    else:
                        m = len(changed)
                        for j in range(m):
                            if changed[j] > neighbor_pos:
                                changed[j] += len(neighbor_word) - \
                                    len(word)
                        changed.append(neighbor_pos)
                        changed.append(neighbor_pos+1)
                    state = neighbor_state
                    current_cost = neighbor_cost
                    words[i] = neighbor_word
                    word = neighbor_word
                    print("Current state:", state)

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
