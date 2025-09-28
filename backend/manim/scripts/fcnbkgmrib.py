#
# To run this code, save it as a Python file (e.g., line_equation.py)
# and execute the following command in your terminal:
# manim -pql line_equation.py EquationOfALine
#

from manim import *

# Define constants for colors and fonts for consistency
M_COLOR = TEAL_A
B_COLOR = GOLD_A
X_COLOR = MAROON_B
Y_COLOR = BLUE_A
LINE_COLOR = WHITE
TEXT_COLOR = WHITE
FONT_SIZE_REGULAR = 36
FONT_SIZE_LARGE = 48


class EquationOfALine(Scene):
    """
    An animation to visually explain the equation of a line, y = mx + b.
    The scene is broken down into logical parts, each explaining a component
    of the equation.
    """

    def construct(self):
        # ---------------------------------------------------------------------
        # SCENE 1: INTRODUCTION
        # ---------------------------------------------------------------------
        # Display title and the core equation
        title = Text("Unlocking y = mx + b", font_size=FONT_SIZE_LARGE)
        equation = MathTex("y", "=", "m", "x", "+", "b", font_size=96)

        self.play(Write(title))
        self.wait(1)
        self.play(
            title.animate.to_edge(UP, buff=0.5),
            Write(equation)
        )
        self.wait(1)

        # Create axes for the graph
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            axis_config={"color": BLUE},
            x_axis_config={"numbers_to_include": range(-4, 5, 2)},
            y_axis_config={"numbers_to_include": range(-4, 5, 2)},
        ).add_coordinates()
        
        self.play(FadeOut(title))
        self.play(equation.animate.scale(0.7).to_edge(UP))
        self.play(Create(axes))
        self.wait(1)

        # ---------------------------------------------------------------------
        # SCENE 2: THE VARIABLES - Y and X
        # ---------------------------------------------------------------------
        # Highlight and explain the dependent (y) and independent (x) variables
        y_var, x_var = equation[0], equation[3]
        
        self.play(
            y_var.animate.set_color(Y_COLOR),
            x_var.animate.set_color(X_COLOR)
        )

        y_label = Text("Dependent Variable (Output)", font_size=FONT_SIZE_REGULAR, color=Y_COLOR)
        y_label.next_to(equation, LEFT, buff=1).shift(UP * 0.5)
        x_label = Text("Independent Variable (Input)", font_size=FONT_SIZE_REGULAR, color=X_COLOR)
        x_label.next_to(equation, RIGHT, buff=1).shift(UP * 0.5)

        self.play(
            Write(y_label),
            Write(x_label),
        )
        self.wait(2)

        # Show a point (x, y) on the graph
        dot = Dot(axes.c2p(3, 2.5), color=YELLOW)
        point_label = MathTex("(x, y)").next_to(dot, UR, buff=0.1)
        
        h_line = DashedLine(axes.c2p(0, 2.5), axes.c2p(3, 2.5), color=YELLOW)
        v_line = DashedLine(axes.c2p(3, 0), axes.c2p(3, 2.5), color=YELLOW)

        self.play(LaggedStart(
            FadeIn(dot, scale=0.5),
            Write(point_label),
            Create(h_line),
            Create(v_line),
            lag_ratio=0.75
        ))
        self.wait(2)

        # Cleanup for the next scene
        scene2_objects = VGroup(y_label, x_label, dot, point_label, h_line, v_line)
        self.play(FadeOut(scene2_objects))
        self.play(
            y_var.animate.set_color(WHITE),
            x_var.animate.set_color(WHITE)
        )
        self.wait(1)

        # ---------------------------------------------------------------------
        # SCENE 3: THE Y-INTERCEPT - B
        # ---------------------------------------------------------------------
        # Highlight and explain the y-intercept (b)
        b_var = equation[5]
        self.play(b_var.animate.set_color(B_COLOR))

        b_label = MathTex("b = \\text{y-intercept}", color=B_COLOR, font_size=FONT_SIZE_LARGE)
        b_label.to_corner(UR)
        self.play(Write(b_label))
        self.wait(1)
        
        # Animate the y-intercept changing
        b_tracker = ValueTracker(2)
        line = axes.plot(lambda x: 0.5 * x + b_tracker.get_value(), color=LINE_COLOR)
        intercept_dot = Dot(axes.c2p(0, 2), color=B_COLOR)
        intercept_label = MathTex("(0, b)").next_to(intercept_dot, RIGHT)

        # Add updaters to move the line and dot together
        line.add_updater(
            lambda l: l.become(axes.plot(lambda x: 0.5 * x + b_tracker.get_value(), color=LINE_COLOR))
        )
        intercept_dot.add_updater(
            lambda d: d.move_to(axes.c2p(0, b_tracker.get_value()))
        )
        intercept_label.add_updater(
            lambda l: l.next_to(intercept_dot, RIGHT)
        )

        self.play(Create(line), FadeIn(intercept_dot), Write(intercept_label))
        self.wait(1)
        self.play(b_tracker.animate.set_value(-1), run_time=3, rate_func=there_and_back)
        self.wait(1)
        
        # Cleanup
        line.clear_updaters()
        intercept_dot.clear_updaters()
        intercept_label.clear_updaters()
        scene3_objects = VGroup(line, intercept_dot, intercept_label, b_label)
        self.play(FadeOut(scene3_objects))
        self.play(b_var.animate.set_color(WHITE))
        self.wait(1)

        # ---------------------------------------------------------------------
        # SCENE 4: THE SLOPE - M
        # ---------------------------------------------------------------------
        # Highlight and explain the slope (m)
        m_var = equation[2]
        self.play(m_var.animate.set_color(M_COLOR))
        
        m_label = MathTex("m = \\text{slope}", color=M_COLOR, font_size=FONT_SIZE_LARGE)
        m_label.to_corner(UR)
        self.play(Write(m_label))

        # Show rise over run
        line_slope_demo = axes.plot(lambda x: 0.75 * x + 1, color=LINE_COLOR)
        p1 = axes.c2p(0, 1)
        p2 = axes.c2p(4, 4)
        
        rise_run_triangle = VGroup(
            Line(p1, axes.c2p(4, 1), color=YELLOW),
            Line(axes.c2p(4, 1), p2, color=YELLOW)
        )
        run_label = MathTex("\\text{Run} = \\Delta x", color=YELLOW).next_to(rise_run_triangle[0], DOWN)
        rise_label = MathTex("\\text{Rise} = \\Delta y", color=YELLOW).next_to(rise_run_triangle[1], RIGHT)
        slope_formula = MathTex("m = \\frac{\\text{Rise}}{\\text{Run}}", font_size=FONT_SIZE_REGULAR).next_to(m_label, DOWN, aligned_edge=RIGHT)

        self.play(Create(line_slope_demo))
        self.play(Create(rise_run_triangle))
        self.play(Write(run_label), Write(rise_label))
        self.play(Write(slope_formula))
        self.wait(2)
        
        scene4_demo_objects = VGroup(rise_run_triangle, run_label, rise_label, slope_formula)
        self.play(FadeOut(scene4_demo_objects))

        # Animate different slope values
        m_tracker = ValueTracker(0.75)
        line_slope_demo.add_updater(
            lambda l: l.become(axes.plot(lambda x: m_tracker.get_value() * x + 1, color=LINE_COLOR))
        )
        self.play(m_tracker.animate.set_value(2), run_time=2) # Positive slope
        self.wait(0.5)
        self.play(m_tracker.animate.set_value(-1), run_time=2) # Negative slope
        self.wait(0.5)
        self.play(m_tracker.animate.set_value(0), run_time=2) # Zero slope
        self.wait(1)

        # Cleanup
        self.play(FadeOut(line_slope_demo, m_label))
        self.play(m_var.animate.set_color(WHITE))
        self.wait(1)
        
        # ---------------------------------------------------------------------
        # SCENE 5: PUTTING IT ALL TOGETHER - AN EXAMPLE
        # ---------------------------------------------------------------------
        self.play(FadeOut(equation))
        example_eq = MathTex("y", "=", "2", "x", "+", "1", font_size=72).to_edge(UP)
        self.play(Write(example_eq))
        self.wait(1)

        # Step 1: Plot the y-intercept
        b_part = VGroup(example_eq[4], example_eq[5])
        self.play(Indicate(b_part, color=B_COLOR))
        intercept_dot = Dot(axes.c2p(0, 1), color=B_COLOR, radius=0.1)
        intercept_label = MathTex("(0, 1)").next_to(intercept_dot, RIGHT)
        self.play(FadeIn(intercept_dot, intercept_label))
        self.wait(1)

        # Step 2: Use the slope to find the next point
        m_part = example_eq[2]
        m_text = MathTex("m = 2 = \\frac{2}{1} \\frac{\\text{(Rise)}}{\\text{(Run)}}", color=M_COLOR).to_corner(UR)
        self.play(Indicate(m_part, color=M_COLOR))
        self.play(Write(m_text))

        # Animate rise and run
        run_arrow = Arrow(axes.c2p(0, 1), axes.c2p(1, 1), buff=0, color=YELLOW)
        run_anim_label = MathTex("1 \\text{ unit right (Run)}").next_to(run_arrow, DOWN)
        self.play(Create(run_arrow), Write(run_anim_label))
        self.wait(0.5)

        rise_arrow = Arrow(axes.c2p(1, 1), axes.c2p(1, 3), buff=0, color=YELLOW)
        rise_anim_label = MathTex("2 \\text{ units up (Rise)}").next_to(rise_arrow, RIGHT)
        self.play(Create(rise_arrow), Write(rise_anim_label))
        self.wait(0.5)

        new_dot = Dot(axes.c2p(1, 3), color=YELLOW, radius=0.1)
        new_label = MathTex("(1, 3)").next_to(new_dot, RIGHT)
        self.play(FadeIn(new_dot, new_label))
        self.wait(1)

        # Step 3: Draw the line
        final_line = axes.plot(lambda x: 2 * x + 1, color=LINE_COLOR, x_range=[-2.5, 2.5])
        self.play(Create(final_line))
        self.wait(2)
        
        # Cleanup for final scene
        example_objects = VGroup(
            m_text, run_arrow, run_anim_label, rise_arrow, rise_anim_label,
            new_dot, new_label, intercept_dot, intercept_label
        )
        self.play(FadeOut(example_objects))
        self.wait(1)

        # ---------------------------------------------------------------------
        # SCENE 6: SUMMARY
        # ---------------------------------------------------------------------
        self.play(FadeOut(final_line, axes))
        self.play(example_eq.animate.move_to(ORIGIN).scale(1.2))
        
        summary_eq = MathTex("y", "=", "m", "x", "+", "b", font_size=96)
        summary_eq.move_to(example_eq.get_center())

        self.play(TransformMatchingTex(example_eq, summary_eq))
        self.wait(1)
        
        # Add labels pointing to each part of the equation
        y, m, x, b = summary_eq[0], summary_eq[2], summary_eq[3], summary_eq[5]
        
        y.set_color(Y_COLOR)
        x.set_color(X_COLOR)
        m.set_color(M_COLOR)
        b.set_color(B_COLOR)
        
        y_label = Text("Output Value", color=Y_COLOR, font_size=FONT_SIZE_REGULAR).next_to(y, DOWN, buff=1.5)
        x_label = Text("Input Value", color=X_COLOR, font_size=FONT_SIZE_REGULAR).next_to(x, DOWN, buff=1.5)
        m_label = Text("Slope (Rate of Change)", color=M_COLOR, font_size=FONT_SIZE_REGULAR).next_to(m, UP, buff=1.5)
        b_label = Text("Y-intercept (Start Point)", color=B_COLOR, font_size=FONT_SIZE_REGULAR).next_to(b, UP, buff=1.5)
        
        y_arrow = Arrow(y_label.get_center(), y.get_bottom(), buff=0.1, color=Y_COLOR)
        x_arrow = Arrow(x_label.get_center(), x.get_bottom(), buff=0.1, color=X_COLOR)
        m_arrow = Arrow(m_label.get_center(), m.get_top(), buff=0.1, color=M_COLOR)
        b_arrow = Arrow(b_label.get_center(), b.get_top(), buff=0.1, color=B_COLOR)

        summary_group = VGroup(
            y_label, x_label, m_label, b_label,
            y_arrow, x_arrow, m_arrow, b_arrow
        )

        self.play(LaggedStart(
            *[FadeIn(obj) for obj in summary_group],
            lag_ratio=0.5
        ))
        
        self.wait(4)
