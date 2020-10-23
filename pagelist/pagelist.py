
def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

class PageRange():

    def __init__(self, start, number, form, length):
        self.start = start
        self.end = start + length - 1
        self.number = number
        self.form = form

    def to_str(self):

        if self.form == "numeric":
            return "{}={}".format(self.start, self.number)
        elif self.form in ["roman", "highroman"]:
            s = "{}={}".format(self.start, self.number)

            if self.start == self.end:
                s += "\n{}={}".format(self.start, self.form)
            else:
                s += "\n{}to{}={}".format(self.start, self.end, self.form)
            return s
        else:
            if self.start == self.end:
                return "{}=\"{}\"".format(self.start, self.number)

            return "{}to{}=\"{}\"".format(self.start, self.end, self.number)


class PageList():

    def __init__(self):
        self.ranges = []
        self.page = 0
        self.title_index = None

    @staticmethod
    def _roman_to_int(s):

        try:
            rom_val = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
            int_val = 0
            for i in range(len(s)):
                if i > 0 and rom_val[s[i]] > rom_val[s[i - 1]]:
                    int_val += rom_val[s[i]] - 2 * rom_val[s[i - 1]]
                else:
                    int_val += rom_val[s[i]]
            return int_val
        except KeyError:
            pass

        return None

    def to_pagelist_tag(self):

        s = "<pagelist\n"
        s += "\n".join(r.to_str() for r in self.ranges)
        s += "\n/>"
        return s

    def append(self, number):

        self.page += 1

        form = "numeric"

        from_rom = self._roman_to_int(number.upper())

        if from_rom is not None:
            form = "roman"
            number = from_rom
        elif RepresentsInt(number):
            form = "numeric"
        else:
            form = "string"

        if number == "Title":
            self.title_index = self.page

        if not self.ranges:
            self.ranges.append(PageRange(self.page, number, form, 1))

        else:

            last_range = self.ranges[-1]

            # a new int, see if we can slot it in
            if (last_range.form == form and
                    RepresentsInt(number) and RepresentsInt(last_range.number)):

                last = int(last_range.number) + (last_range.end - last_range.start)
                this = int(number)

                if this == last + 1:
                    # extend
                    last_range.end += 1
                else:
                    # discontinuous
                    self.ranges.append(PageRange(self.page, number, form, 1))
            else:
                # not an int
                if last_range.form == form and last_range.number == number:
                    # extend
                    last_range.end += 1
                else:
                    # start a new range
                    self.ranges.append(PageRange(self.page, number, form, 1))