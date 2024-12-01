import sys
from datetime import datetime, timedelta
from AutoComplete import *


# Script by ThomasThorun. The Turbo Solver was SimonSoft (https://github.com/caporalesimone/) idea.
turbo_solver = True


class Puzzle:
    known_solutions = {3: [[2, 3, 2, 3],
                           [2, 3, 3, 2],
                           [2, 3, 4, 3, 2, 2],
                           [2, 2, 3, 3],
                           [3, 2, 2, 3],
                           [3, 2, 3, 2],
                           [3, 3, 2, 2],
                           [3, 3, 2, 1, 1, 2, 3, 3]],
                       4: [[3, 2, 2, 2, 3, 3],
                           [3, 2, 2, 1, 2, 3, 3, 3],
                           [3, 2, 3, 2, 2, 3],
                           [3, 3, 2, 1, 2, 2, 3, 3],
                           [3, 3, 2, 2, 1, 1, 2, 3, 3, 3],
                           [3, 3, 3, 2, 2, 2],
                           [2, 3, 4, 3, 2, 2, 3, 2],
                           [2, 3, 4, 3, 3, 2, 2, 2],
                           [2, 3, 2, 2, 3, 3],
                           [2, 2, 2, 3, 3, 3],
                           [2, 2, 2, 3, 4, 4, 4, 3, 2, 2, 2, 3],
                           [2, 2, 3, 2, 3, 3]],
                       5: [[3, 3, 2, 3, 2, 2, 3, 2],
                           [3, 3, 2, 2, 2, 1, 4, 4, 1, 2, 2, 2, 3, 3, 3, 3],
                           [3, 3, 3, 3, 2, 2, 2, 2],
                           [3, 2, 3, 2, 2, 3, 2, 3],
                           [3, 2, 3, 3, 3, 2, 1, 1, 1, 2, 2, 3, 3, 3],
                           [3, 2, 2, 1, 2, 2, 3, 3, 3, 3],
                           [2, 3, 4, 3, 2, 2, 3, 2, 2, 3],
                           [2, 3, 4, 3, 3, 2, 2, 1, 1, 2, 2, 3, 3, 3],
                           [2, 3, 2, 2, 3, 4, 3, 2, 2, 3],
                           [2, 2, 2, 2, 3, 3, 3, 3],
                           [2, 2, 2, 2, 3, 3, 4, 4, 3, 3, 2, 2],
                           [2, 2, 3, 2, 2, 3, 4, 4, 4, 4, 3, 3, 2, 2, 2, 2]]}

    def __init__(self, timeout=400):
        self.skill = {'start': Player.GetSkillValue('Remove Trap'),
                      'now': Player.GetSkillValue('Remove Trap'),
                      'cap': Player.GetSkillCap('Remove Trap')}
        self.check_skill()
        self.messages = {
            'success': "You successfully disarm the trap",
            'fail': "You fail to disarm the trap and reset it"}
        self.dirs = {1: ("↑", (-1, 0)),
                     2: ("→", (0, 1)),
                     3: ("↓", (1, 0)),
                     4: ("←", (0, -1))}
        self.runs = {'total': 0, 'fails': 0, 'successes': 0}
        self.bau_list = get_bau_list()
        self.bau = self.get_bau()
        self.gump, self.size = -1, -1
        self.timeout = timeout
        self.total_time = timedelta(0)
        self.start_time = self.reset_time()
        self.excluded_paths = []
        self.path, self.m_idx, self.matrix = self.reset()

    def get_bau(self):
        return next(self.bau_list)

    def reset_matrix(self):
        self.open_gump()
        self.m_idx = [1, 1]
        self.matrix = [
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1]
        ]
        if self.size < 5:
            for p in range(7):
                self.matrix[5][p] = 1
                self.matrix[p][5] = 1
        if self.size < 4:
            for p in range(7):
                self.matrix[4][p] = 1
                self.matrix[p][4] = 1
        return self.m_idx, self.matrix

    def reset(self):
        self.path = []
        self.m_idx, self.matrix = self.reset_matrix()
        return self.path, self.m_idx, self.matrix

    def reset_time(self):
        self.start_time = datetime.now()
        return self.start_time

    def open_gump(self):
        timeout = 6500
        while True:
            self.gump, self.size = get_puzzle_gump_info()
            if self.gump > 0:
                break
            Player.UseSkill('Remove Trap')
            Target.WaitForTarget(timeout, False)
            Target.TargetExecute(self.bau)
            timeout = 500

    def get_matrix_pos(self, num):
        y, x = self.dirs[num][1]
        return y + self.m_idx[0], x + self.m_idx[1]

    def set_matrix_pos(self, num):
        self.m_idx = self.get_matrix_pos(num)
        self.matrix[self.m_idx[0]][self.m_idx[1]] = 1

    def valid_position(self, num):
        _ny, _nx = self.get_matrix_pos(num)
        return self.matrix[_ny][_nx] == 0

    def check_timeout(self):
        return timedelta.total_seconds(datetime.now() - self.start_time) > self.timeout

    def check_skill(self):
        if self.skill['now'] >= self.skill['cap']:
            Misc.SendMessage("Remove Trap Skill is in it's Cap. \r\nFinishing.", 0x95)
            sys.exit()

    def change_bau(self):
        self.bau = self.get_bau()
        Misc.Pause(500)
        Gumps.CloseGump(self.gump)

    def set_run_data(self, run_status):
        self.runs['total'] += 1
        if run_status == 'Success':
            self.runs['successes'] += 1
            self.total_time = self.total_time + (datetime.now() - self.start_time)
        else:
            self.runs['fails'] += 1
        self.skill['now'] = Player.GetSkillValue('Remove Trap')

    def print_run_data(self, state, message):
        t = {'Success': ('solve', 0x45), 'Fail': ('run', 0x20)}
        try:
            average = str(self.total_time/self.runs['successes']).split(".")[0]
        except Exception:
            average = str(0)
        Misc.SendMessage('\r\n' + state + '! ' + str(self.size) + 'x' + str(self.size) + ' gump \r\n' + t[state][0] +
                         ' time: ' + str(datetime.now() - self.start_time).split(".")[0] +
                         '\r\naverage: ' + average + ('\r\n' if message else '') + message + '\r\n', t[state][1])
        Misc.SendMessage('\r\nruns: ' + str(self.runs['total']) + '\r\n' + '[successes: ' +
                         str(self.runs['successes']) + ' | fails: ' + str(self.runs['fails']) + ']\r\n', 0x95)
        Misc.SendMessage('\r\nSkill:\r\n[start: ' + str('%.1f' % self.skill['start']) +
                         ' | now: ' + str('%.1f' % self.skill['now']) +
                         ' | gain: ' + str('%.1f' % (self.skill['now'] - self.skill['start'])) + ']\r\n', 0x39)

    def get_buttons(self):
        def excluded_path():
            for p in self.excluded_paths:
                if p[0] > len(path) or path[p[0]] == p[1]:
                    return True
            return False

        for path in Puzzle.known_solutions[self.size]:
            if excluded_path():
                continue
            return path[len(self.path):]
        return []

    def finish(self, state, message):
        self.set_run_data(state)
        self.print_run_data(state, message)
        self.check_skill()
        self.excluded_paths = []
        self.reset_time()
        self.reset()


def get_bau_list():
    rank = {2: ('2nd', 'one'), 3: ('3rd', 'two')}
    while True:
        bau_list = []
        for i in range(1, 4):
            msg = 'Target a circuit trap training kit.'
            if i > 1:
                msg = ('dispute solving: Target a ' + rank[i][0] + ' option circuit trap training kit in your range.' +
                       '\r\nJust hit ESC or target anything else if just ' + rank[i][1] + ' is enough.')
            Misc.SendMessage(msg, 65)
            bau = Items.FindBySerial(Target.PromptTarget(""))
            if bau and bau.ItemID == 0xA393:
                bau_list.append(bau)
            else:
                break
        if bau_list:
            return circular(bau_list)
        else:
            Misc.SendMessage('is that a circuit trap training kit?', 28)


def circular(args):
    while True:
        for element in args:
            yield element


def get_puzzle_gump_info():
    gump = Gumps.CurrentGump()
    gump_data = Gumps.GetGumpRawData(gump)
    if '1159005' in gump_data:
        midpoints = gump_data.count("9720")
        size = 5
        if 7 < midpoints < 23:
            size = 4
        if midpoints <= 7:
            size = 3
        return gump, size
    return -1, -1


def get_puzzle_gump():
    return get_puzzle_gump_info()[0]


def handle_response(puzzle, pos):
    Journal.Clear()
    for _ in range(0, 50):
        Misc.Pause(100)
        if Journal.Search(puzzle.messages['success']):
            puzzle.finish('Success', '')
            return 1
        if Journal.Search(puzzle.messages['fail']):
            previous = puzzle.path
            puzzle.reset()
            build_path(puzzle, previous)
            return -1
        if get_puzzle_gump() > -1:
            puzzle.path.append(pos)
            puzzle.set_matrix_pos(pos)
            return 0
    puzzle.finish('Fail', '| Gump response timed out. Probably no gump')
    return 0


def build_path(puzzle, path_buttons):
    for button in path_buttons:
        Gumps.SendAction(puzzle.gump, button)
        response = handle_response(puzzle, button)
        if response != 0:
            return response
    return 0


def remove_trap():
    puzzle = Puzzle()
    while True:
        attempt_result = 0
        for num_button in puzzle.get_buttons() if turbo_solver else [2, 3, 4, 1]:
            if puzzle.check_timeout():
                puzzle.finish('Fail', '| Something went wrong - timeout')
                break

            if not puzzle.valid_position(num_button):  # pass
                attempt_result = -1
                continue

            Misc.SendMessage("path = " + "".join([puzzle.dirs[v][0] for v in puzzle.path]) +
                             " | trying " + puzzle.dirs[num_button][0], 90)

            attempt_result = build_path(puzzle, [num_button])
            if not attempt_result == (0 if turbo_solver else -1):
                if attempt_result == -1:
                    puzzle.excluded_paths.append((len(puzzle.path), num_button))
                break
        if (attempt_result == -1 and not turbo_solver) or (turbo_solver and not puzzle.get_buttons()):
            puzzle.change_bau()
            puzzle.finish('Fail',
                          '| Something is wrong. Maybe someone else is using the same box? trying the next ' +
                          str(puzzle.bau))


remove_trap()
