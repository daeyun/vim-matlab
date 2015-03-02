__author__ = 'Daeyun Shin'

vim = None


class PythonVimUtils(object):
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
    def get_selection():
        buf = vim.current.buffer
        row1, col1 = buf.mark('<')
        row2, col2 = buf.mark('>')
        lines = buf[row1 - 1:row2]
        if len(lines) == 1:
            lines[0] = lines[0][col1:col2+1]
        else:
            lines[0] = lines[0][col1:]
            lines[-1] = lines[-1][:col2+1]
        return lines

    @staticmethod
    def get_text_selection():
        pass

    @staticmethod
    def is_current_buffer_modified():
        return vim.eval('&modified') == 1

    @staticmethod
    def echo_text(string):
        vim.command("echo '{}'".format(string.replace("'", r"\'")))
