from manim import *

# Define constants for consistent styling
TITLE_COLOR = BLUE
EQUATION_COLOR = WHITE
AXIS_COLOR = GRAY
SLOPE_COLOR = YELLOW
INTERCEPT_COLOR = GREEN
LINE_COLOR = BLUE
POINT_COLOR = RED

class UnlockingTheLine(Scene):
    """
    An animation to visually explain the slope-intercept form of a linear equation, y = mx + b.
    The animation is broken down into logical segments, each explaining a component of the equation.
    """
    def construct(self):
        """
        Main method to construct the scene by calling helper methods for each segment.
        """
        self.show_introduction()
        self.explain_variables()
        self.explain_y_intercept()
        self.explain_slope()
        self.build_example_line()
        self.show_recap()

    def show_introduction(self):
        """
        Scene 1: Introduction to the concept and the equation.
        """
        # Title
        title = Text("Unlocking the Line: Understanding y = mx + b", color=TITLE_COLOR, font_size=40)
        self.play(Write(title))
        self.wait(2)

        # Main equation
        equation = MathTex("y", "=", "m", "x", "+", "b", font_size=96, color=EQUATION_COLOR)
        self.play(ReplacementTransform(title, equation))
        self.wait(2)

        # Create coordinate plane
        self.plane = NumberPlane(
            x_range=[-8, 8, 1],
            y_range=[-5, 5, 1],
            x_length=12,
            y_length=8,
            axis_config={"color": AXIS_COLOR},
            background_line_style={"stroke_color": AXIS_COLOR, "stroke_opacity": 0.3}
        )
        axes_labels = self.plane.get_axis_labels(x_label="x", y_label="y")
        
        self.play(
            equation.animate.scale(0.5).to_edge(UP),
            Create(self.plane),
            Write(axes_labels)
        )
        self.wait(2)
        
        # Store equation for later use
        self.equation = equation

    def explain_variables(self):
        """
        Scene 2: Explain the roles of 'x' and 'y' as variables.
        """
        # Highlight x and y in the equation
        self.play(
            Indicate(self.equation.get_part_by_tex("y"), color=YELLOW),
            Indicate(self.equation.get_part_by_tex("x"), color=YELLOW),
        )
        self.wait(1)

        # Show a point on the graph
        point_coords = self.plane.c2p(3, 4)
        point = Dot(point_coords, color=POINT_COLOR)
        point_label = MathTex("(x, y)").next_to(point, UR, buff=0.1)

        # Dashed lines to axes
        h_line = DashedLine(self.plane.c2p(0, 4), point_coords)
        v_line = DashedLine(self.plane.c2p(3, 0), point_coords)
        
        self.play(Create(point), Write(point_label))
        self.play(Create(h_line), Create(v_line))
        self.wait(3)

        # Cleanup
        self.play(FadeOut(point), FadeOut(point_label), FadeOut(h_line), FadeOut(v_line))
        self.wait(1)

    def explain_y_intercept(self):
        """
        Scene 3: Explain 'b' as the y-intercept.
        """
        # Highlight 'b'
        b_part = self.equation.get_part_by_tex("b")
        self.play(Circumscribe(b_part, color=INTERCEPT_COLOR))
        self.wait(1)

        # Show substitution for x=0
        sub_eq = MathTex("y = m(0) + b", font_size=48).to_edge(UP, buff=1.5)
        final_eq = MathTex("y = b", font_size=48).move_to(sub_eq)
        
        self.play(Write(sub_eq))
        self.wait(1.5)
        self.play(Transform(sub_eq, final_eq))
        self.wait(2)
        self.play(FadeOut(sub_eq))

        # Example line y = x + 2
        line = self.plane.plot(lambda x: x + 2, color=LINE_COLOR)
        line_label = MathTex("y = x + 2").next_to(line, UR, buff=0.2)
        
        intercept_point = Dot(self.plane.c2p(0, 2), color=INTERCEPT_COLOR, radius=0.12)
        intercept_label = MathTex("(0, b)").next_to(intercept_point, RIGHT, buff=0.2)

        self.play(Create(line), Write(line_label))
        self.wait(1)
        self.play(Create(intercept_point), Write(intercept_label))
        self.wait(3)

        # Cleanup
        self.play(FadeOut(line), FadeOut(line_label), FadeOut(intercept_point), FadeOut(intercept_label))
        self.wait(1)
        
    def explain_slope(self):
        """
        Scene 4: Explain 'm' as the slope.
        """
        # Highlight 'm'
        m_part = self.equation.get_part_by_tex("m")
        self.play(Circumscribe(m_part, color=SLOPE_COLOR))
        self.wait(1)

        # Slope formula
        slope_formula1 = MathTex("m = \\frac{\\text{rise}}{\\text{run}} = \\frac{\\text{change in } y}{\\text{change in } x}", font_size=42).next_to(self.equation, DOWN, buff=0.5)
        slope_formula2 = MathTex("m = \\frac{y_2 - y_1}{x_2 - x_1}", font_size=48).move_to(slope_formula1)
        self.play(Write(slope_formula1))
        self.wait(2)
        self.play(Transform(slope_formula1, slope_formula2))
        self.wait(2)

        # Visual demonstration of rise over run
        line = self.plane.plot(lambda x: 0.5 * x + 1, color=LINE_COLOR)
        p1 = self.plane.c2p(1, 1.5)
        p2 = self.plane.c2p(5, 3.5)
        
        dot1 = Dot(p1, color=POINT_COLOR)
        dot2 = Dot(p2, color=POINT_COLOR)
        
        run_line = DashedLine(p1, self.plane.c2p(5, 1.5), color=SLOPE_COLOR)
        rise_line = DashedLine(self.plane.c2p(5, 1.5), p2, color=SLOPE_COLOR)

        run_brace = Brace(run_line, DOWN, buff=0.1)
        rise_brace = Brace(rise_line, RIGHT, buff=0.1)
        run_text = run_brace.get_tex("\\text{run} (\\Delta x)")
        rise_text = rise_brace.get_tex("\\text{rise} (\\Delta y)")

        self.play(FadeOut(slope_formula1))
        self.play(Create(line))
        self.play(Create(dot1), Create(dot2))
        self.play(Create(run_line), Create(rise_line))
        self.play(Create(run_brace), Write(run_text))
        self.play(Create(rise_brace), Write(rise_text))
        self.wait(3)
        
        slope_demo_group = VGroup(line, dot1, dot2, run_line, rise_line, run_brace, run_text, rise_brace, rise_text)
        self.play(FadeOut(slope_demo_group))

        # Show different slope types
        pos_slope = self.plane.plot(lambda x: 2 * x - 1, color=GREEN)
        pos_text = Text("Positive Slope (m > 0)", font_size=32).to_edge(DOWN)
        self.play(Create(pos_slope), Write(pos_text))
        self.wait(2)

        neg_slope = self.plane.plot(lambda x: -1.5 * x + 2, color=RED)
        neg_text = Text("Negative Slope (m < 0)", font_size=32).to_edge(DOWN)
        self.play(ReplacementTransform(pos_slope, neg_slope), ReplacementTransform(pos_text, neg_text))
        self.wait(2)

        zero_slope = self.plane.plot(lambda x: 3, color=YELLOW)
        zero_text = Text("Zero Slope (m = 0)", font_size=32).to_edge(DOWN)
        self.play(ReplacementTransform(neg_slope, zero_slope), ReplacementTransform(neg_text, zero_text))
        self.wait(2)

        # Cleanup
        self.play(FadeOut(zero_slope), FadeOut(zero_text))
        self.wait(1)

    def build_example_line(self):
        """
        Scene 5: Putting it all together with the example y = 2x - 3.
        """
        # Display example equation
        example_eq = MathTex("y = 2x - 3", font_size=48).to_edge(UP)
        self.play(ReplacementTransform(self.equation, example_eq))
        self.wait(1)

        # Step 1: Find y-intercept 'b'
        self.play(Indicate(example_eq.get_part_by_tex("-3"), color=INTERCEPT_COLOR))
        p0 = self.plane.c2p(0, -3)
        dot0 = Dot(p0, color=INTERCEPT_COLOR, radius=0.12)
        label0 = MathTex("(0, -3)").next_to(dot0, LEFT)
        self.play(Create(dot0), Write(label0))
        self.wait(2)

        # Step 2: Use slope 'm' to find next point
        self.play(Indicate(example_eq.get_part_by_tex("2"), color=SLOPE_COLOR))
        
        # Animate run=1, rise=2 from (0, -3)
        run1 = Line(p0, self.plane.c2p(1, -3), color=SLOPE_COLOR)
        rise1 = Line(self.plane.c2p(1, -3), self.plane.c2p(1, -1), color=SLOPE_COLOR)
        run1_label = MathTex("1").next_to(run1, DOWN, buff=0.1)
        rise1_label = MathTex("2").next_to(rise1, RIGHT, buff=0.1)
        
        p1 = self.plane.c2p(1, -1)
        dot1 = Dot(p1, color=POINT_COLOR)
        label1 = MathTex("(1, -1)").next_to(dot1, RIGHT)

        self.play(Create(run1), Write(run1_label))
        self.play(Create(rise1), Write(rise1_label))
        self.play(Create(dot1), Write(label1))
        self.wait(2)

        # Animate again from (1, -1)
        run2 = Line(p1, self.plane.c2p(2, -1), color=SLOPE_COLOR)
        rise2 = Line(self.plane.c2p(2, -1), self.plane.c2p(2, 1), color=SLOPE_COLOR)
        
        p2 = self.plane.c2p(2, 1)
        dot2 = Dot(p2, color=POINT_COLOR)
        label2 = MathTex("(2, 1)").next_to(dot2, RIGHT)

        self.play(Create(VGroup(run2, rise2)))
        self.play(Create(dot2), Write(label2))
        self.wait(2)

        # Step 3: Draw the line through the points
        final_line = self.plane.plot(lambda x: 2 * x - 3, color=LINE_COLOR, x_range=[-2, 4])
        self.play(Create(final_line))
        self.wait(2)
        
        # Store objects for recap
        self.example_eq = example_eq
        self.final_line = final_line
        self.plot_elements = VGroup(dot0, label0, run1, rise1, run1_label, rise1_label, dot1, label1, run2, rise2, dot2, label2)
        
    def show_recap(self):
        """
        Scene 6: Recap the roles of 'm' and 'b'.
        """
        # Fade out intermediate steps
        self.play(FadeOut(self.plot_elements[2:])) # Keep initial dot and label

        # Bring back general equation
        recap_eq = MathTex("y = m x + b", font_size=60).to_edge(UP)
        self.play(ReplacementTransform(self.example_eq, recap_eq))
        self.wait(1)

        # Point to 'b' and the intercept
        b_part = recap_eq.get_part_by_tex("b")
        b_arrow = Arrow(start=b_part.get_bottom(), end=self.plane.c2p(0, -3), buff=0.2, color=INTERCEPT_COLOR)
        b_text = Text("'b' is the y-intercept", font_size=28, color=INTERCEPT_COLOR).next_to(b_arrow.get_start(), LEFT, buff=0.2)
        
        self.play(GrowArrow(b_arrow), Write(b_text))
        self.wait(2)

        # Point to 'm' and the slope
        m_part = recap_eq.get_part_by_tex("m")
        slope_triangle = VGroup(
            Line(self.plane.c2p(1,-1), self.plane.c2p(2,-1), color=SLOPE_COLOR),
            Line(self.plane.c2p(2,-1), self.plane.c2p(2,1), color=SLOPE_COLOR)
        )
        self.play(Create(slope_triangle))
        
        m_arrow = Arrow(start=m_part.get_bottom(), end=slope_triangle.get_center(), buff=0.2, color=SLOPE_COLOR)
        m_text = Text("'m' is the slope", font_size=28, color=SLOPE_COLOR).next_to(m_arrow.get_start(), RIGHT, buff=0.2)
        
        self.play(GrowArrow(m_arrow), Write(m_text))
        self.wait(4)

        # Final fade out
        self.play(
            FadeOut(*self.mobjects)
        )
        self.wait(1)