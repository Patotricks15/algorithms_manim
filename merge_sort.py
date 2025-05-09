from manim import *

class MergeSortScene(Scene):
    def construct(self):
        arr = [3, 7, 6, -10, 15, 23.5, 55, -13]
        elements = VGroup(*[self.create_box(str(x)) for x in arr])
        elements.arrange(RIGHT, buff=0.6)
        elements.move_to(ORIGIN)
        self.play(FadeIn(elements))
        self.wait(0.5)

        self.visualize_merge_sort(arr, elements, y_offset=0, x_offset=0, depth=0)

    def create_box(self, value):
        """
        Creates a box with given value.

        Args:
            value (str): The string to show inside the box.

        Returns:
            VGroup: A VGroup containing the box and the text.
        """
        box = Rectangle(width=0.8, height=0.8, color=BLUE)
        text = Text(value, font_size=20).move_to(box.get_center())
        return VGroup(box, text)

    def create_highlight(self, group):
        """
        Creates a yellow highlight box around a given group of mobjects.

        Args:
            group (VGroup): The VGroup to highlight.

        Returns:
            SurroundingRectangle: A yellow highlight box.
        """
        box = SurroundingRectangle(group, color=YELLOW, fill_opacity=0.2)
        return box

    def display_text(self, content, position=0):
        """
        Displays a text message on the scene at a specified vertical position.

        Args:
            content (str): The text content to be displayed.
            position (int, optional): The vertical position offset from the top-left corner. Defaults to 0.

        This method fades in the text at the specified position, waits briefly, and then fades it out.
        """

        txt = Text(content, font_size=20).to_corner(UL).shift(DOWN * position)
        self.play(FadeIn(txt))
        self.wait(0.5)
        self.play(FadeOut(txt))

    def visualize_merge_sort(self, arr, elements, y_offset, x_offset, depth):
        """
        Visualize the merge sort algorithm.

        Args:
            arr (list): The input list to be sorted.
            elements (VGroup): The VGroup of boxes to be animated.
            y_offset (int): The vertical offset from the top of the screen.
            x_offset (int): The horizontal offset from the left of the screen.
            depth (int): The recursion depth of the merge sort algorithm.
        """
        indent = '  ' * depth
        self.display_text(f"{indent}mergeSort called on {arr}", position=0)

        if len(arr) <= 1:
            self.display_text(f"{indent}return (base case) {arr}", position=0)
            return

        mid = len(arr) // 2
        left_arr, right_arr = arr[:mid], arr[mid:]
        self.display_text(f"{indent}Split into {left_arr} and {right_arr}", position=0)

        left_elems = VGroup(*elements[:mid])
        right_elems = VGroup(*elements[mid:])

        # Rectangles to highlight the groups
        left_highlight = self.create_highlight(left_elems)
        right_highlight = self.create_highlight(right_elems)
        self.play(FadeIn(left_highlight), FadeIn(right_highlight))
        self.wait(0.2)

        vertical_shift = 0.4
        horizontal_shift = 0.2 + x_offset

        self.play(
            left_elems.animate.shift(UP * vertical_shift + LEFT * horizontal_shift),
            right_elems.animate.shift(UP * vertical_shift + RIGHT * horizontal_shift),
            left_highlight.animate.shift(UP * vertical_shift + LEFT * horizontal_shift),
            right_highlight.animate.shift(UP * vertical_shift + RIGHT * horizontal_shift)
        )
        self.wait(0.2)

        self.visualize_merge_sort(left_arr, left_elems, y_offset + 1, x_offset, depth + 1)
        self.visualize_merge_sort(right_arr, right_elems, y_offset + 1, x_offset, depth + 1)

        # Comparing i < j
        left_sorted = sorted(left_arr)
        right_sorted = sorted(right_arr)
        merged_list = []
        i = j = 0

        self.display_text(f"{indent}merge called on {left_sorted} and {right_sorted}", position=1)

        while i < len(left_sorted) and j < len(right_sorted):
            i_val = left_sorted[i]
            j_val = right_sorted[j]
            i_box = self.create_box(str(i_val)).move_to(LEFT * 2 + DOWN * (y_offset + 1))
            j_box = self.create_box(str(j_val)).move_to(RIGHT * 2 + DOWN * (y_offset + 1))
            compare_text = Text(f"Comparing {i_val} < {j_val}", font_size=20).next_to(i_box, UP)
            self.play(FadeIn(i_box), FadeIn(j_box), FadeIn(compare_text))
            self.wait(0.5)
            if i_val < j_val:
                merged_list.append(i_val)
                i += 1
            else:
                merged_list.append(j_val)
                j += 1
            self.play(FadeOut(i_box), FadeOut(j_box), FadeOut(compare_text))

        if i < len(left_sorted):
            self.display_text(f"{indent}Appending remaining from left: {left_sorted[i:]}", position=2)
            merged_list.extend(left_sorted[i:])
        if j < len(right_sorted):
            self.display_text(f"{indent}Appending remaining from right: {right_sorted[j:]}", position=2)
            merged_list.extend(right_sorted[j:])

        self.display_text(f"{indent}Result of merge: {merged_list}", position=3)
        self.display_text(f"{indent}Merged {left_sorted} and {right_sorted} into {merged_list}", position=4)

        merged = VGroup(*[self.create_box(str(x)) for x in merged_list])
        merged.arrange(RIGHT, buff=0.6)
        merged.move_to(DOWN * (y_offset + 0.5) + RIGHT * x_offset)

        self.play(Transform(elements, merged))
        self.wait(0.5)
