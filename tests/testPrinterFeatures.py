import unittest
from src.Printer.PrinterDevice import *
from src.Printer.BufferPrinter import *

class TestLineBreaking(unittest.TestCase):
    def test_no_break(self):
        printer = Printer(40)
        short_text, remainder = printer.breakLine("short text", 20)
        self.assertEqual(short_text, "short text", "Text is too short to break")
        self.assertEqual(remainder, "", "Remainder should be empty")

    def test_word_break(self):
        printer = Printer(40)
        broken, remainder = printer.breakLine("12345678901234", 10)
        self.assertEqual(broken, "123456789-", "line should be broken at the '9'")
        self.assertEqual(remainder, "01234", "remainder should be '0' through '4'")

    def test_scentence_break(self):
        printer = Printer(40)
        broken, remainder = printer.breakLine("longer text that should break line", 20)
        self.assertEqual(list(broken.split(" "))[-1], "that", "line should break after 'that'")
        self.assertEqual(list(remainder.split(" "))[0], "should", "new line should start with 'should' (no starting spaces)")

    def test_long_word_after_shorts(self):
        printer = Printer(40)
        broken, remainder = printer.breakLine("a little ReallyLongWordThatShouldn'tBreak test", 10)
        self.assertEqual(broken, "a little")
        self.assertEqual(remainder, "ReallyLongWordThatShouldn'tBreak test")

    def test_exact_length(self):
        printer = Printer(40)
        broken, remainder = printer.breakLine("don't break!", 12)
        self.assertEqual(broken, "don't break!", "Line should not be broken")
        self.assertEqual(remainder, "", "nothing should remain")

    def test_break_at_exact_length(self):
        printer = Printer(40)
        broken, remainder = printer.breakLine("break here and no later", 10)
        self.assertEqual(broken, "break here")
        self.assertEqual(remainder, "and no later")

    def test_inline_break_super_short(self):
        printer = Printer(40)
        broken, remainder = printer.breakLine("sho\nrt", 10)
        self.assertEqual(broken, "sho", "line should be broken on the linebreak")
        self.assertEqual(remainder, "rt", "the remainder should be whatever is left after the linebreak")

    def test_inline_break_short(self):
        printer = Printer(40)
        broken, remainder = printer.breakLine("early\nbroken", 10)
        self.assertEqual(broken, "early", "line should be broken on the linebreak")
        self.assertEqual(remainder, "broken", "the remainder should be whatever is left after the linebreak")

    def test_long_inline_break_early(self):
        printer = Printer(40)
        broken, remainder = printer.breakLine("early\nbreak on a much longer line that needs to be broken", 10)
        self.assertEqual(broken, "early")
        self.assertEqual(remainder, "break on a much longer line that needs to be broken")

    def test_long_inline_break_late(self):
        printer = Printer(40)
        broken, remainder = printer.breakLine("long line that has a break\nlater on", 10)
        self.assertEqual(broken, "long line")
        self.assertEqual(remainder, "that has a break\nlater on")

class TestBlockBreaking(unittest.TestCase):
    def test_line_break(self):
        printer = Printer(40)
        long_text = printer.breakText("longer text that should break line", 20)
        self.assertEqual(len(long_text), 2, "Text should be broken into two lines")
        self.assertEqual(list(long_text[0].split(" "))[-1], "that", "line should break after 'that'")
        self.assertEqual(list(long_text[1].split(" "))[0], "should", "new line should start with 'should' (no starting spaces)")

    def test_exact_line_length(self):
        printer = Printer(40)
        exact_matching = printer.breakText("This line will stop! Exactly at the stops", 20)
        self.assertEqual(len(exact_matching), 2, "Text should be broken into three lines")
        self.assertEqual(list(exact_matching[0].split(" "))[-1], "stop!", "Text should be broken exactly at 'stop!'")
        self.assertEqual(list(exact_matching[1].split(" "))[-1], "stops", "Text should be broken exactly at 'stops'")

    def test_mid_word_break(self):
        printer = Printer(40)
        word_break = printer.breakText("123456789012345", 10)
        self.assertEqual(len(word_break), 2, "Text should be broken into two lines")
        self.assertEqual(word_break[0], "123456789-", "text should be broken at the '9'")
        self.assertEqual(word_break[1], "012345", "new line should start at '0'")

    def test_multi_word_break(self):
        printer = Printer(40)
        word_breaks = printer.breakText("123456789abcdefghi12345", 10)
        self.assertEqual(len(word_breaks), 3, "Text should be broken into three lines")
        self.assertEqual(word_breaks[0], "123456789-", "text should be broken at the '9'")
        self.assertEqual(word_breaks[1], "abcdefghi-", "new line should start at '0'")
        self.assertEqual(word_breaks[2], "12345", "remaining new line should be '12345'")

    def test_multi_line_word_break(self):
        printer = Printer(40)
        line_breaks = printer.breakText("wacky line 123456789abcd", 10)
        self.assertEqual(len(line_breaks), 3, "Text should be broken into three lines")
        self.assertEqual(line_breaks[0], "wacky line", "text should be broken at 'line'")
        self.assertEqual(line_breaks[1], "123456789-", "new line should start at the '9'")
        self.assertEqual(line_breaks[2], "abcd", "remaining new line should be 'abcd'")

class TestTextSpan(unittest.TestCase):
    def test_fitting_span_left(self):
        line_length = 15
        printer = BufferPrinter(line_length)
        remainder = printer.textSpan("left", "right")
        fitting = printer.get_buffer()[0]
        self.assertEqual(remainder, "", "Text is short enough it shouldn't break the line")
        self.assertEqual(fitting.split(" ")[0], "left", "'left' should be all the way to the left")
        self.assertEqual(fitting.split(" ")[-1], "right", "'right' should be all the way to the right")
        self.assertEqual(len(fitting), line_length, "line should have spacing in the middle")

    def test_fitting_span_Right(self):
        line_length = 15
        printer = BufferPrinter(line_length)
        remainder = printer.textSpan("left", "right", True)
        fitting = printer.get_buffer()[0]
        self.assertEqual(remainder, "", "Text is short enough it shouldn't break the line")
        self.assertEqual(fitting.split(" ")[0], "left", "'left' should be all the way to the left")
        self.assertEqual(fitting.split(" ")[-1], "right", "'right' should be all the way to the right")
        self.assertEqual(len(fitting), line_length, "line should have spacing in the middle")

    def test_breaking_span_left(self):
        line_length = 15
        printer = BufferPrinter(line_length)
        remainder = printer.textSpan("[prio]", "Right side that's too long")
        broken = printer.get_buffer()[0]
        self.assertEqual(broken.split(" ")[0], "[prio]", "'[prio]' should be all the way to the left")
        self.assertEqual(broken.split(" ")[-1], "Right", "'Right' should be all the way to the right")
        self.assertEqual(len(broken), line_length, "line should have spacing in the middle")
        self.assertEqual(remainder, "side that's too long")

    def test_breaking_span_right(self):
        line_length = 15
        printer = BufferPrinter(line_length)
        remainder = printer.textSpan("Name, EpitaphThatsTooLong", "{0}{u}", True)
        broken = printer.get_buffer()[0]
        self.assertEqual(broken.split(" ")[0], "Name,", "'Name,' should be all the way to the left")
        self.assertEqual(broken.split(" ")[-1], "{0}{u}", "'{0}{u}' should be all the way to the right")
        self.assertEqual(len(broken), line_length, "line should have spacing in the middle")
        self.assertEqual(remainder, "EpitaphThatsTooLong")

    def test_low_width_text_break(self):
        line_length = 15
        printer = BufferPrinter(line_length)  
        remainder = printer.textSpan("Test Textin", "abcd", False)
        broken = printer.get_buffer()[0]
        self.assertEqual(broken, "Test Textin ab-")
        self.assertEqual(remainder, "cd")

if __name__ == '__main__':
    unittest.main()