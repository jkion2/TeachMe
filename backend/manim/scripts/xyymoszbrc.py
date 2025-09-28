# To run this code, save it as a Python file (e.g., linear_equation.py)
# and run the following command in your terminal:
# manim -pql linear_equation.py UnpackingYMXB

from manim import *

# Define constants for colors and font sizes for consistency
HIGHLIGHT_COLOR = YELLOW
LABEL_COLOR = BLUE
EQUATION_COLOR = WHITE
TEXT_COLOR = WHITE

class UnpackingYMXB(Scene):
    def construct(self):
        """
        This scene provides a visual explanation of the linear equation y = mx + b.
        """
        # --- Scene 1: Introduction ---
        self.scene1_introduction()

        # --- Scene 2: The Core Components - Variables x and y ---
        self.scene2_variables_xy()

        # --- Scene 3: The Starting Point - The Y-intercept 'b' ---
        self.scene3_y_intercept_b()

        # --- Scene 4: The Engine of Change - The Slope 'm' ---
        self.scene4_slope_m()

        # --- Scene 5: Putting It All Together with an Example ---
        self.scene5_example()

        # --- Scene 6: Common Pitfalls ---
        self.scene6_pitfalls()

        # --- Scene 7: Recap and Conclusion ---
        self.scene7_recap()


    def scene1_introduction(self):
        """
        Introduces the topic and the main equation y = mx + b.
        """
        title = Text("Unpacking y = mx + b", font_size=48)
        subtitle = Text("The DNA of Straight Lines", font_size=36).next_to(title, DOWN)
        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(2)

        equation = MathTex("y", "=", "m", "x", "+", "b", font_size=96)
        self.play(
            Transform(VGroup(title, subtitle), equation),
        )
        self.wait(2)
        self.clear()
        self.add(equation) # Keep equation for the next scene
        
    def scene2_variables_xy(self):
        """
        Explains the role of x and y on a Cartesian plane.
        """
        # Get equation from previous scene
        equation = self.mobjects[0]
        
        # Setup axes and graph
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            x_length=10,
            y_length=7,
            axis_config={"color": BLUE},
        ).add_coordinates()
        
        graph = axes.plot(lambda x: 0.5 * x + 1, color=GREEN)
        
        # Animate the appearance of the plane and graph
        self.play(
            equation.animate.scale(0.5).to_corner(UP + RIGHT),
            Create(axes),
        )
        self.play(Create(graph))
        self.wait(1)

        # Highlight x and y in the equation
        self.play(
            equation.get_part_by_tex("x").animate.set_color(HIGHLIGHT_COLOR),
            equation.get_part_by_tex("y").animate.set_color(HIGHLIGHT_COLOR),
        )

        # Labels for axes
        x_label = axes.get_x_axis_label(MathTex("x", "\\text{ (Independent)}")).set_color(LABEL_COLOR)
        y_label = axes.get_y_axis_label(MathTex("y", "\\text{ (Dependent)}")).set_color(LABEL_COLOR)
        self.play(Write(x_label), Write(y_label))
        
        # Create a moving dot and its coordinates
        k = ValueTracker(-4)
        moving_dot = Dot(point=axes.c2p(-4, 0.5 * (-4) + 1), color=YELLOW)
        coords = MathTex(font_size=36).add_updater(
            lambda m: m.set_value(f"(x, y) = ({k.get_value():.1f}, {axes.p2c(moving_dot.get_center())[1]:.1f})")
        ).next_to(moving_dot, UR, buff=0.2)

        moving_dot.add_updater(lambda m: m.move_to(axes.c2p(k.get_value(), 0.5 * k.get_value() + 1)))

        self.play(Create(moving_dot), Write(coords))
        self.play(k.animate.set_value(4), run_time=5, rate_func=linear)
        self.wait(1)
        
        # Clean up for next scene
        self.play(
            FadeOut(VGroup(axes, graph, moving_dot, coords, x_label, y_label)),
            equation.animate.move_to(UP*3).set_color(WHITE),
        )
        self.wait()

    def scene3_y_intercept_b(self):
        """
        Explains the y-intercept 'b'.
        """
        equation = self.mobjects[0]
        
        # Highlight 'b'
        self.play(Circumscribe(equation.get_part_by_tex("b"), color=HIGHLIGHT_COLOR))
        
        # Show substitution x=0
        equation_at_zero = MathTex("y = m(0) + b", font_size=48).next_to(equation, DOWN, buff=1)
        simplified_equation = MathTex("y = b", font_size=48).move_to(equation_at_zero)
        self.play(Write(equation_at_zero))
        self.wait(1)
        self.play(TransformMatchingTex(equation_at_zero, simplified_equation))
        self.wait(2)

        self.play(FadeOut(simplified_equation))
        
        # Visual demonstration
        axes = Axes(x_range=[-4, 4], y_range=[-4, 4], axis_config={"color": BLUE}).add_coordinates()
        self.play(Create(axes))
        
        b_tracker = ValueTracker(1)
        
        graph = axes.plot(lambda x: 0.5 * x + b_tracker.get_value(), color=GREEN)
        intercept_dot = Dot(color=YELLOW).add_updater(
            lambda d: d.move_to(axes.c2p(0, b_tracker.get_value()))
        )
        intercept_label = MathTex("b").add_updater(
            lambda m: m.next_to(intercept_dot, RIGHT)
        )
        b_value_text = MathTex("b = ").add_updater(
            lambda m: m.become(MathTex(f"b = {b_tracker.get_value():.1f}"))
        ).to_corner(DOWN + LEFT)
        
        self.play(Create(graph), Create(intercept_dot), Write(intercept_label), Write(b_value_text))
        self.wait(1)
        
        self.play(b_tracker.animate.set_value(3), run_time=2)
        self.play(b_tracker.animate.set_value(-2), run_time=3)
        self.play(b_tracker.animate.set_value(1), run_time=1.5)
        self.wait(1)
        
        # Clean up
        self.play(FadeOut(VGroup(axes, graph, intercept_dot, intercept_label, b_value_text)))
        
    def scene4_slope_m(self):
        """
        Explains the slope 'm'.
        """
        equation = self.mobjects[0]

        # Highlight 'm'
        self.play(Circumscribe(equation.get_part_by_tex("m"), color=HIGHLIGHT_COLOR))
        
        # Show slope formula
        slope_formula = MathTex("m = \\frac{\\text{Rise}}{\\text{Run}} = \\frac{\\Delta y}{\\Delta x}", font_size=48).next_to(equation, DOWN, buff=1)
        self.play(Write(slope_formula))
        self.wait(2)

        # Visual demonstration of Rise over Run
        axes = Axes(x_range=[-1, 5], y_range=[-1, 5], axis_config={"color": BLUE})
        graph = axes.plot(lambda x: 0.8 * x + 1, color=GREEN)
        
        p1 = axes.c2p(1, 0.8 * 1 + 1)
        p2 = axes.c2p(4, 0.8 * 4 + 1)
        dot1 = Dot(p1, color=YELLOW)
        dot2 = Dot(p2, color=YELLOW)
        
        # Rise and Run lines
        run_line = DashedLine(p1, [p2[0], p1[1], 0], color=RED)
        rise_line = DashedLine([p2[0], p1[1], 0], p2, color=ORANGE)
        
        # Labels
        run_label = MathTex("\\Delta x", "\\text{ (Run)}").next_to(run_line, DOWN).set_color(RED)
        rise_label = MathTex("\\Delta y", "\\text{ (Rise)}").next_to(rise_line, RIGHT).set_color(ORANGE)

        self.play(FadeOut(slope_formula), Create(axes), Create(graph))
        self.play(Create(VGroup(dot1, dot2)))
        self.play(Create(run_line), Write(run_label))
        self.play(Create(rise_line), Write(rise_label))
        self.wait(3)

        self.play(FadeOut(VGroup(dot1, dot2, run_line, rise_line, run_label, rise_label)))
        
        # Animate different slope values
        m_tracker = ValueTracker(0.8)
        graph.add_updater(lambda g: g.become(axes.plot(lambda x: m_tracker.get_value() * x + 1, color=GREEN)))
        slope_value_text = MathTex("m = ").add_updater(
            lambda m: m.become(MathTex(f"m = {m_tracker.get_value():.1f}"))
        ).to_corner(DOWN + LEFT)
        
        self.add(slope_value_text)
        
        # Positive Slope
        self.play(m_tracker.animate.set_value(2), run_time=2)
        self.wait(0.5)
        # Negative Slope
        self.play(m_tracker.animate.set_value(-1.5), run_time=3)
        self.wait(0.5)
        # Zero Slope
        self.play(m_tracker.animate.set_value(0), run_time=2)
        self.wait(1)

        # Clean up
        self.play(FadeOut(VGroup(axes, graph, slope_value_text)))
        self.remove(graph) # remove updater

    def scene5_example(self):
        """
        Walks through a concrete example: y = 2x + 1.
        """
        self.clear() # Start fresh
        
        example_eq = MathTex("y = 2x + 1", font_size=60).to_corner(UP + LEFT)
        self.play(Write(example_eq))
        
        # Extract m and b
        m_val = MathTex("m = 2", font_size=48).next_to(example_eq, DOWN, align=LEFT)
        b_val = MathTex("b = 1", font_size=48).next_to(m_val, DOWN, align=LEFT)
        self.play(FadeIn(m_val, shift=RIGHT), FadeIn(b_val, shift=RIGHT))
        self.wait(1)
        
        # Setup axes
        axes = Axes(x_range=[-2, 3], y_range=[-1, 6], axis_config={"color": BLUE}).add_coordinates()
        self.play(Create(axes))
        
        # Step 1: Plot y-intercept
        b_point = Dot(axes.c2p(0, 1), color=YELLOW, radius=0.12)
        b_label = MathTex("(0, 1)").next_to(b_point, RIGHT)
        self.play(Write(Text("Step 1: Plot y-intercept b=1", font_size=24).to_corner(DOWN)))
        self.play(Create(b_point), Write(b_label))
        self.wait(1)
        
        # Step 2: Use slope to find next point
        self.play(Write(Text("Step 2: Use slope m = 2 = 2/1", font_size=24).to_corner(DOWN)))
        
        rise_arrow = Arrow(axes.c2p(0, 1), axes.c2p(0, 3), buff=0, color=ORANGE)
        rise_label = MathTex("\\text{Rise}=2").next_to(rise_arrow, RIGHT)
        run_arrow = Arrow(axes.c2p(0, 3), axes.c2p(1, 3), buff=0, color=RED)
        run_label = MathTex("\\text{Run}=1").next_to(run_arrow, UP)

        self.play(Create(rise_arrow), Write(rise_label))
        self.wait(0.5)
        self.play(Create(run_arrow), Write(run_label))
        self.wait(1)
        
        p2_point = Dot(axes.c2p(1, 3), color=YELLOW, radius=0.12)
        p2_label = MathTex("(1, 3)").next_to(p2_point, RIGHT)
        self.play(Create(p2_point), Write(p2_label))
        self.wait(1)

        # Step 3: Draw the line
        line = axes.plot(lambda x: 2 * x + 1, color=GREEN)
        self.play(Create(line))
        self.wait(2)
        
        # Verification
        check_calc = MathTex("y = 2(1) + 1 = 3", font_size=40).to_corner(DOWN + RIGHT)
        check_mark = MathTex("\\checkmark", color=GREEN).next_to(check_calc, RIGHT)
        self.play(Write(check_calc))
        self.play(Write(check_mark))
        self.wait(3)
        
        self.clear()

    def scene6_pitfalls(self):
        """
        Explains common pitfalls like confusing m and b, and vertical lines.
        """
        # Setup
        title = Text("Common Pitfalls", font_size=40).to_edge(UP)
        self.play(Write(title))
        axes = Axes(x_range=[-4, 4], y_range=[-4, 4], axis_config={"color": BLUE})
        self.play(Create(axes))

        b_tracker = ValueTracker(1)
        m_tracker = ValueTracker(0.5)
        
        graph = axes.plot(lambda x: m_tracker.get_value() * x + b_tracker.get_value(), color=GREEN)
        
        b_text = Text("'b' shifts the line vertically", font_size=28).to_corner(DOWN)
        m_text = Text("'m' changes the steepness", font_size=28).to_corner(DOWN)
        
        # Animate 'b'
        self.play(Create(graph), Write(b_text))
        self.play(b_tracker.animate.set_value(3), run_time=1.5)
        self.play(b_tracker.animate.set_value(-2), run_time=2)
        self.play(b_tracker.animate.set_value(1), run_time=1)
        
        # Animate 'm'
        self.play(Transform(b_text, m_text))
        self.play(m_tracker.animate.set_value(2), run_time=1.5)
        self.play(m_tracker.animate.set_value(-1), run_time=2)
        self.play(m_tracker.animate.set_value(0.5), run_time=1)
        self.wait(1)
        
        # Vertical Line
        self.play(FadeOut(graph, b_text))
        
        vertical_line = axes.get_vertical_line(axes.c2p(2, 0), color=RED)
        v_line_label = MathTex("x=2").next_to(vertical_line, UP)
        undefined_slope = MathTex("m = \\frac{\\Delta y}{0} \\rightarrow \\text{Undefined}", font_size=40).to_corner(DOWN)

        self.play(Create(vertical_line), Write(v_line_label))
        self.play(Write(undefined_slope))
        self.wait(3)
        
        self.clear()
        
    def scene7_recap(self):
        """
        Summarizes the components of y = mx + b.
        """
        title = Text("Recap", font_size=48).to_edge(UP)
        self.play(Write(title))

        equation = MathTex("y", "=", "m", "x", "+", "b", font_size=80).center().shift(UP)
        self.play(Write(equation))
        self.wait(1)

        # Unpack each component with braces
        y_brace = Brace(equation.get_part_by_tex("y"), DOWN, buff=0.2)
        y_label = y_brace.get_text("Output (Dependent Variable)")
        
        x_brace = Brace(equation.get_part_by_tex("x"), DOWN, buff=0.2)
        x_label = x_brace.get_text("Input (Independent Variable)")
        
        b_brace = Brace(equation.get_part_by_tex("b"), UP, buff=0.2)
        b_label = b_brace.get_text("Y-Intercept (Starting Point)")
        
        m_brace = Brace(equation.get_part_by_tex("m"), UP, buff=0.2)
        m_label = m_brace.get_text("Slope (Rate of Change)")

        self.play(
            Create(b_brace), Write(b_label.set_color(HIGHLIGHT_COLOR)),
            run_time=1.5
        )
        self.wait(0.5)
        self.play(
            Create(m_brace), Write(m_label.set_color(HIGHLIGHT_COLOR)),
            run_time=1.5
        )
        self.wait(0.5)
        self.play(
            Create(y_brace), Write(y_label.set_color(LABEL_COLOR)),
            run_time=1.5
        )
        self.wait(0.5)
        self.play(
            Create(x_brace), Write(x_label.set_color(LABEL_COLOR)),
            run_time=1.5
        )
        self.wait(4)

        final_message = Text("The fundamental language of linear relationships.", font_size=36).to_edge(DOWN)
        self.play(Write(final_message))
        self.wait(3)
