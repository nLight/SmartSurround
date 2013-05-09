import sublime, sublime_plugin

COMMON_SURROUNDERS = {
    '(' : '\)',
    '{' : '\}',
    '[' : ']',
    '|' : '\|',
    '<' : '>',
    '"' : '"',
    "'" : "'"
}


class SmartSurroundCommand(sublime_plugin.TextCommand):
    """
    Single quotes to double quotes for now 'only'
    """

    def get_begin_end(self):
        begin = self.find_opening(r'(\||\(|\[|\"|\'|\{|<)')
        if begin and self.view.substr(begin) in COMMON_SURROUNDERS:
            end = self.find_closing(COMMON_SURROUNDERS.get(self.view.substr(begin)))
            return begin, end
        else:
            return None

    def find_closing(self, what):
        return self.view.find(what, self.cursor_pos())

    def find_opening(self, what):
        new_regions = (r for r in reversed(self.view.find_all(what)) if r.begin() < self.cursor_pos())
        try:
            new_region = new_regions.next()
        except StopIteration:
            pass

        if new_region:
            return new_region


    def cur_line(self):
        return self.view.line(self.cursor_pos())

    def cursor_pos(self):
        return self.view.sel()[0].begin()


class SmartSurroundSelectCommand(SmartSurroundCommand):
    def run(self, edit):
        begin, end = self.get_begin_end()
        if begin and end:
            self.view.sel().clear()
            self.view.sel().add(begin)
            self.view.sel().add(end)


class SmartSurroundDeleteCommand(SmartSurroundCommand):
    def run(self, edit):
        begin, end = self.get_begin_end()
        if begin and end:
            self.view.replace(edit, begin, "")
            new_end = sublime.Region(end.a - 1, end.b - 1)
            self.view.replace(edit, new_end, "")


class SmartSurroundChangeCommand(SmartSurroundCommand):
    def run(self, edit):
        begin, end = self.get_begin_end()
        if begin and end:
            self.view.replace(edit, begin, "")
            new_end = sublime.Region(end.a - 1, end.b - 1)
            self.view.replace(edit, new_end, "")
            selection = sublime.Region(begin.begin(), new_end.end() - 1)
            self.view.sel().add(selection)
