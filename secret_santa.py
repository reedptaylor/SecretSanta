from abc import ABC, abstractmethod

class SantaBase(ABC):
    def __init__(self, participant_couples: list[list[str]], assignments_per_person: int):
        import random
        self.random = random
        self.random.seed()

        self.participant_couples = participant_couples
        self.assignments_per_person = assignments_per_person
        self.all_participants = [item for sublist in self.participant_couples for item in sublist]
        self.assignments : dict[str, list[str]] = {}

    @abstractmethod
    def _get_possible_assignment(self):
        pass # implement this method in the child class; should set self.assignments

    def generate_assignments(self) -> None:
        """Generates the assignments.
        """

        self._get_possible_assignment()

    def _get_possible_assignments(self, participant: str) -> list[str]:
        """Gets the possible assignments for the specified participant.

        Args:
            participant (str): The participant to get the possible assignments for.
        """
        return [item for item in self.all_participants if item not in self._get_disallowed_assignments(participant)]

    def _get_disallowed_assignments(self, participant: str) -> set[str]:
        """Gets the disallowed assignments for the specified participant.
        Disallowed assignments include the participant's couple,
        participants who have already been assigned the maximum number of assignments,
        and participants who have already been assigned to the specified participant.

        Args:
            participant (str): The participant to get the disallowed assignments for.
        """
        from collections import Counter

        current_couple = [x for x in self.participant_couples if participant in x][0]
        all_assignments = [item for sublist in self.assignments.values() for item in sublist]
        current_assignments = self.assignments.get(participant) or []

        disallowed_assignments = current_couple.copy()
        counts = Counter(all_assignments)
        disallowed_assignments.extend([a for a, c in counts.items() if c == self.assignments_per_person])
        disallowed_assignments.extend(current_assignments)

        return set(disallowed_assignments)
    
    def print_assignments(self) -> None:
        """Prints the assignments to the console.
        """
        for participant, participant_assignments in self.assignments.items():
            print(participant + ':')
            # print assignments as list
            for assignment in participant_assignments:
                print('- ' + assignment)
            print()

# Secret santa assigner that uses brute force (retries) to find a solution
class BruteForceSanta(SantaBase):
    def __init__(self, participant_couples: list[list[str]], assignments_per_person: int):
        super().__init__(participant_couples, assignments_per_person)

    def _get_possible_assignment(self):
        iter = 0
        attempt = 0

        while True:
            # find the specified number of assignments per person
            if (iter >= self.assignments_per_person):
                break
            # if we've tried too many times, give up
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
        for couple in self.participant_couples:
            for participant in couple:
                possible_assignments = self._get_possible_assignments(participant)

                if len(possible_assignments) == 0:
                    return False

                # get random assignment
                newAssignment = possible_assignments[self.random.randint(0, len(possible_assignments) - 1)]

                if self.assignments.get(participant) is None:
                    self.assignments[participant] = [newAssignment]
                else:
                    self.assignments[participant].append(newAssignment)

        return True

class BacktrackingSanta(SantaBase):
    def __init__(self, participant_couples: list[list[str]], count: int):
        super().__init__(participant_couples, count)

    def _get_possible_assignment(self):
        participants : list[str] = []

        for _ in range(self.assignments_per_person):
            participants.extend(self.all_participants.copy())

        self.random.shuffle(participants)

        if not self._recursive_solve(participants):
            print('Failed to find a solution.')

    def _recursive_solve(self, remaining_participants: list[str]) -> bool:
        if len(remaining_participants) == 0:
            return True

        # get the next participant in the list
        participant = remaining_participants[0]
        possible_assignments = self._get_possible_assignments(participant)

        if len(possible_assignments) == 0:
            return False

        self.random.shuffle(possible_assignments)

        for assignment in possible_assignments:
            if self.assignments.get(participant) is None:
                self.assignments[participant] = [assignment]
            else:
                self.assignments[participant].append(assignment)

            # if we can solve the rest of the assignments, we're done
            if self._recursive_solve(remaining_participants[1:]):
                return True

            # unassign so we can try again on the next iteration (or return False)
            if len(self.assignments[participant]) == 1:
                del self.assignments[participant]
            else:
                self.assignments[participant].remove(assignment)

        return False

# Run
# couples = [['Mike', 'Lorie'], ['Reed', 'Brooke'], ['Lacey', 'Bryce'], ['Darcy', 'Jon']]
# assignments_per_person = 2
# use_brute_force = True

# santa_assigner : SantaBase = BruteForceSanta(couples, assignments_per_person) if use_brute_force else BacktrackingSanta(couples, assignments_per_person)
# santa_assigner.generate_assignments()
# santa_assigner.print_assignments()