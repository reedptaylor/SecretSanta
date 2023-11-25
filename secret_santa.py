from abc import ABC, abstractmethod

class SantaBase(ABC):
    def __init__(self, participant_couples: list[list[str]], count: int):
        self.participant_couples = participant_couples
        self.count = count
        self.assignments : dict[str, list[str]] = {}

    @abstractmethod
    def _get_possible_assignment(self):
        pass

    def generate_assignments(self) -> None:
        """Generates and print the assignments to the console.

        Args:
            assignments (dict): The assignments to print.
        """

        self._get_possible_assignment()

        for participant, participant_assignments in self.assignments.items():
            print(participant + ':')
            for assignment in participant_assignments:
                print('- ' + assignment)
            print()

    def _get_possible_assignments(self, participant: str, assignments: dict[str, list[str]]) -> list[str]:
        all_participants = [item for sublist in self.participant_couples for item in sublist]

        return [item for item in all_participants if item not in self._get_disallowed_assignments(participant, assignments)]


    def _get_disallowed_assignments(self, participant: str, assignments: dict[str, list[str]]) -> set[str]:
        from collections import Counter

        current_couple = [x for x in self.participant_couples if participant in x][0]
        all_assignments = [item for sublist in assignments.values() for item in sublist]
        current_assignments = assignments.get(participant) or []

        disallowed_assignments = current_couple.copy()
        counts = Counter(all_assignments)
        disallowed_assignments.extend([a for a, c in counts.items() if c == self.count])
        disallowed_assignments.extend(current_assignments)

        return set(disallowed_assignments)


class BruteForceSanta(SantaBase):
    def __init__(self, participant_couples: list[list[str]], count: int):
        super().__init__(participant_couples, count)

    def _get_possible_assignment(self):
        iter = 0
        attempt = 0

        while True:
            if (iter >= self.count):
                break
            if (attempt >= 20):
                print('Failed to find a solution.')
                break

            if self._attempt_assign():
                iter += 1
            else:
                iter = 0
                attempt += 1
                self.assignments.clear()
                print('Failed to assign secret santas. Trying again...')

    def _attempt_assign(self) -> bool:
        from random import seed
        from random import randint
        seed()

        for couple in self.participant_couples:
            for participant in couple:
                possible_assignments = self._get_possible_assignments(participant, self.assignments)

                if len(possible_assignments) == 0:
                    return False

                newAssignment = possible_assignments[randint(0, len(possible_assignments) - 1)]

                if self.assignments.get(participant) is None:
                    self.assignments[participant] = [newAssignment]
                else:
                    self.assignments[participant].append(newAssignment)

        return True


class CompleteSanta(SantaBase):
    def __init__(self, participant_couples: list[list[str]], count: int):
        super().__init__(participant_couples, count)

    def _get_possible_assignment(self):
        from random import seed
        from random import randint
        seed()

        all_possible = self._get_all_possible_assignments()
        self.assignments = all_possible[randint(0, len(all_possible) - 1)]

    def _get_all_possible_assignments(self) -> list[dict[str, list[str]]]:
        all_possible = []

        # TODO

        return all_possible


# Run
couples = [['Reed', 'Brooke'], ['Lacey', 'Bryce'], ['Darcy', 'Jon']]
count = 2
use_brute_force = True

santa_assigner : SantaBase = BruteForceSanta(couples, count) if use_brute_force else CompleteSanta(couples, count)
santa_assigner.generate_assignments()