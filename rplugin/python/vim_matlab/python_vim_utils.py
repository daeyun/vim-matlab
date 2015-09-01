import re

__author__ = 'Daeyun Shin'

vim = None


class PythonVimUtils(object):
    comment_pattern = re.compile(r"(^(?:[^'%]|'[^']*')*)(%.*)$")
    cell_header_pattern = re.compile(
        r'(?:^%%(?:[^%]|$)|^[ \t]*?(?<!%)[ \t]*?(?:function|classdef)\s+)')
    ellipsis_pattern = re.compile(r'^(.*[^\s])\s*\.\.\.\s*$')
    variable_pattern = re.compile(r"\b((?:[a-zA-Z_]\w*)*\.?[a-zA-Z_]*\w*)")
    function_block_pattern = re.compile(
        r'(?:^|\n[ \t]*)(?<!%)[ \t]*(?:function|classdef)(?:.*?)[^\w]([a-zA-Z]\w*) *(?:\(|(?:%|\n|\.\.\.|$))[\s\S]*?(?=(?:\n)(?<!%)[ \t]*(?:function[^a-zA-Z]|classdef[^a-zA-Z])|$)')
    option_line_pattern = re.compile(r'%%! *vim-matlab: *(\w+) *\(([^\(]+)\)')

    @staticmethod
    def get_current_file_path():
        return vim.eval("expand('%:p')")

    @staticmethod
    def save_current_buffer():
        vim.command("w")

    @staticmethod
    def edit_file(path):
        vim.command("silent e! {}".format(path))

    @staticmethod
    def get_cursor():
        """
        :return: 1-indexed current cursor position
        """
        row, col = vim.current.window.cursor
        return row, col + 1

    @staticmethod
    def set_cursor(row_col):
        vim.current.window.cursor = (row_col[0], row_col[1] - 1)

    @staticmethod
    def get_selection(ignore_matlab_comments=True):
        buf = vim.current.buffer
        row1, col1 = buf.mark('<')
        row2, col2 = buf.mark('>')
        lines = buf[row1 - 1:row2]
        if len(lines) == 1:
            lines[0] = lines[0][col1:col2 + 1]
        else:
            lines[0] = lines[0][col1:]
            lines[-1] = lines[-1][:col2 + 1]

        if ignore_matlab_comments:
            return PythonVimUtils.trim_matlab_code(lines)
        return lines

    @staticmethod
    def get_lines():
        buf = vim.current.buffer
        return buf

    @staticmethod
    def get_text_selection():
        pass

    @staticmethod
    def is_current_buffer_modified():
        return vim.eval('&modified') == 1

    @staticmethod
    def echo_text(string):
        vim.command("echo '{}'".format(string.replace("'", r"''")))

    @staticmethod
    def get_current_matlab_cell_lines(ignore_matlab_comments=True):
        lines = PythonVimUtils.get_lines()
        crow, _ = PythonVimUtils.get_cursor()

        cell_start = crow - 1
        while cell_start > 0:
            if PythonVimUtils.cell_header_pattern.match(lines[cell_start]):
                cell_start += 1
                break
            cell_start -= 1

        cell_end = crow - 1
        while cell_end < len(lines) - 1:
            cell_end += 1
            if PythonVimUtils.cell_header_pattern.match(lines[cell_end]):
                cell_end -= 1
                break

        lines = lines[cell_start:cell_end + 1]
        if ignore_matlab_comments:
            return PythonVimUtils.trim_matlab_code(lines)
        return lines

    @staticmethod
    def trim_matlab_code(lines):
        new_lines = []
        for line in lines:
            line = PythonVimUtils.comment_pattern.sub(r"\1", line).strip()

            if PythonVimUtils.ellipsis_pattern.match(line):
                line = PythonVimUtils.ellipsis_pattern.sub(r"\1", line)
                if new_lines:
                    prev_line = new_lines.pop()
                    line = prev_line + ',' + line
            new_lines.append(line)

        return new_lines

    @staticmethod
    def get_variable_under_cursor():
        row, col = PythonVimUtils.get_cursor()
        lines = PythonVimUtils.get_lines()
        if len(lines) < row:
            return None

        for m in PythonVimUtils.variable_pattern.finditer(lines[row - 1]):
            if m.start() < col <= m.end():
                return m.group(0)

    @staticmethod
    def get_options():
        lines = vim.current.buffer[:20]
        options = {}
        for line in lines:
            m = PythonVimUtils.option_line_pattern.match(line)
            if m is None:
                break
            options[m.group(1)] = [s.strip() for s in m.group(2).split(',')]
        return options

    @staticmethod
    def get_function_blocks():
        lines = vim.current.buffer
        content = '\n'.join(lines)
        function_blocks = {}
        for m in PythonVimUtils.function_block_pattern.finditer(content):
            function_blocks[m.group(1)] = m.group(0).strip()

        return function_blocks
