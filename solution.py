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

    def generate_neighbor(self, state, environment, start_time, current_cost):
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
                                return new_state, new_cost
                            elif time.time() - start_time > 240:
                                return state, current_cost

        for word in self.vocabulary:
            new_state = word + ' ' + state
            new_cost = environment.compute_cost(new_state)
            if new_cost < current_cost:
                return new_state, new_cost
            elif time.time() - start_time > 240:
                return state, current_cost

            new_state = state + ' ' + word
            new_cost = environment.compute_cost(new_state)
            if new_cost < current_cost:
                return new_state, new_cost
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

        while True:
            if (time.time() - start_time > 240):
                break
            current_state, current_cost = self.generate_neighbor(
                current_state, environment, start_time, current_cost)
            if current_state == self.best_state:
                break
            self.best_state = current_state

        print("Initial state:", environment.init_state)
        print("Best state:", self.best_state)
        print("Time taken in seconds:", time.time() - start_time)

        # while True:
        #     # Hill climbing to find local optimum
        #     print("Current state:", current_state)
        #     neighbors = self.generate_neighbors(current_state)
        #     # print(neighbors)
        #     neighbor_costs = [(neighbor, environment.compute_cost(
        #         neighbor)) for neighbor in neighbors]
        #     neighbor_costs.sort(key=lambda x: x[1])  # Sort neighbors by cost
        #     print(neighbor_costs)

        #     best_neighbor, best_cost = neighbor_costs[0]

        #     if best_cost < current_cost:
        #         current_state = best_neighbor
        #         current_cost = best_cost
        #         self.best_state = current_state
        #         # print(self.best_state)
        #     else:
        #         # If no improvement, perform BFS from the local optimum
        #         frontier = [current_state]
        #         explored = set()

        #         while frontier:
        #             state = frontier.pop(0)
        #             if state not in explored:
        #                 explored.add(state)
        #                 neighbors = self.generate_neighbors(state)
        #                 for neighbor in neighbors:
        #                     if neighbor not in explored:
        #                         frontier.append(neighbor)
        #                         neighbor_cost = environment.compute_cost(
        #                             neighbor)
        #                         if neighbor_cost < current_cost:
        #                             self.best_state = neighbor
        #                             # print(self.best_state)
        #                             return  # Stop once we find a better state

        #         break
