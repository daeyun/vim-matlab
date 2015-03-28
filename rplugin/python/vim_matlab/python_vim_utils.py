import re

__author__ = 'Daeyun Shin'

vim = None


class PythonVimUtils(object):
    comment_pattern = re.compile(r'%[^\n]*$')
    cell_header_pattern = re.compile(r'^%%(?:[^%]|$)')

    @staticmethod
    def get_current_file_path():
        return vim.eval("expand('%:p')")

    @staticmethod
    def save_current_buffer():
        vim.command("w")

    @staticmethod
    def get_cursor():
        """
        :return: 1-indexed current cursor position
        """
        row, col = vim.current.window.cursor
        return row, col + 1

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
        vim.command("echo '{}'".format(string.replace("'", r"\'")))

    @staticmethod
    def get_current_matlab_cell_lines(ignore_matlab_comments=True):
        lines = PythonVimUtils.get_lines()
        crow, _ = PythonVimUtils.get_cursor()

        cell_start = crow - 1
        while cell_start > 0:
            if PythonVimUtils.cell_header_pattern.match(lines[cell_start]):
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
        lines = [PythonVimUtils.comment_pattern.sub('', line).strip() for line in lines]
        return [line for line in lines if line]
