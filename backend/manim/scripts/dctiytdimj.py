from manim import *

# === Constants for Styling ===
# Colors
BLUE_COLOR = BLUE_C
GREEN_COLOR = GREEN_C
RED_COLOR = RED_C
YELLOW_COLOR = YELLOW_C
TEXT_COLOR = WHITE

# Font Sizes
TITLE_FONT_SIZE = 48
EQUATION_FONT_SIZE = 96
LABEL_FONT_SIZE = 36
RECAP_FONT_SIZE = 42

class LinearEquationScene(Scene):
    """
    An animation explaining the components of the linear equation y = mx + b.
    This scene follows a step-by-step visual explanation, breaking down
    the y-intercept, slope, and how they combine to form a line.
    """
    def construct(self):
        # Set a slightly darker background for better contrast
        self.camera.background_color = "#1E1E1E"

        # --- Scene 1: Introduction & Hook ---
        self.show_intro()

        # --- Scene 2: The Core Idea ---
        self.show_core_idea()

        # --- Scene 3: 'b' - The Y-Intercept ---
        self.explain_y_intercept()

        # --- Scene 4: 'm' - The Slope ---
        self.explain_slope()

        # --- Scene 5: Putting It All Together ---
        self.show_full_example()

        # --- Scene 6: Recap ---
        self.show_recap()

        # Hold the final scene
        self.wait(3)

    def show_intro(self):
        """
        Displays the title and the main equation y = mx + b.
        """
        # Create title
        title = Text(
            "The Secret to Straight Lines: Understanding y = mx + b",
            font_size=TITLE_FONT_SIZE
        )
        self.play(Write(title))
        self.wait(1.5)

        # Create the main equation
        self.main_equation = MathTex(
            "y", "=", "m", "x", "+", "b",
            font_size=EQUATION_FONT_SIZE
        ).scale(1.2)
        
        self.play(Transform(title, self.main_equation))
        self.main_equation.to_edge(UP, buff=1)
        self.play(Write(self.main_equation[1:])) # Write rest of equation
        self.title_placeholder = title # Keep a reference to the title mobject for later transforms
        self.wait(2)

    def show_core_idea(self):
        """
        Labels the independent (x) and dependent (y) variables.
        Introduces the Cartesian coordinate system.
        """
        # Isolate x and y parts of the equation
        y_part = self.main_equation.get_part_by_tex("y")
        x_part = self.main_equation.get_part_by_tex("x")

        # Create labels
        y_label = Text("Dependent Variable (Output)", font_size=LABEL_FONT_SIZE).next_to(y_part, DOWN, buff=1.5)
        x_label = Text("Independent Variable (Input)", font_size=LABEL_FONT_SIZE).next_to(x_part, DOWN, buff=1.5)

        # Create arrows pointing to labels
        y_arrow = Arrow(y_part.get_bottom(), y_label.get_top(), buff=0.2, color=BLUE_COLOR)
        x_arrow = Arrow(x_part.get_bottom(), x_label.get_top(), buff=0.2, color=GREEN_COLOR)

        self.play(
            LaggedStart(
                Write(y_label),
                Create(y_arrow),
                Write(x_label),
                Create(x_arrow),
                lag_ratio=0.5
            )
        )
        self.wait(3)

        # Clean up labels and arrows
        labels_group = VGroup(y_label, x_label, y_arrow, x_arrow)
        self.play(FadeOut(labels_group))
        self.wait(1)

        # Create the coordinate plane
        self.axes = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-2, 8, 1],
            x_length=10,
            y_length=6.5,
            axis_config={"include_tip": True, "numbers_to_exclude": [0]},
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 2,
                "stroke_opacity": 0.3
            }
        ).to_edge(DOWN, buff=0.5)
        
        self.play(Create(self.axes))
        self.wait(1)

    def explain_y_intercept(self):
        """
        Explains 'b' as the y-intercept or starting point.
        """
        b_part = self.main_equation.get_part_by_tex("b")

        # Highlight 'b'
        self.play(b_part.animate.set_color(BLUE_COLOR).scale(1.2))
        self.wait(0.5)

        # Show example equation
        self.example_eq = MathTex("y = 2x + 1", font_size=LABEL_FONT_SIZE+10).next_to(self.main_equation, DOWN, buff=0.5)
        self.play(Write(self.example_eq))
        
        b_example_part = self.example_eq.get_part_by_tex("1")
        self.play(b_example_part.animate.set_color(BLUE_COLOR))

        # Plot the y-intercept point
        y_intercept_point = self.axes.c2p(0, 1)
        b_dot = Dot(y_intercept_point, color=BLUE_COLOR, radius=0.12)
        b_dot_label = MathTex("(0, 1)", font_size=LABEL_FONT_SIZE).next_to(b_dot, RIGHT, buff=0.2)
        
        self.play(GrowFromCenter(b_dot))
        self.play(Write(b_dot_label))
        self.wait(3)

        # Revert 'b' highlighting
        self.play(
            b_part.animate.set_color(TEXT_COLOR).scale(1/1.2),
            b_example_part.animate.set_color(TEXT_COLOR)
        )
        self.b_dot = b_dot # Save for later use
        self.b_dot_label = b_dot_label

    def explain_slope(self):
        """
        Explains 'm' as the slope, demonstrating positive, negative, and zero slopes.
        """
        m_part = self.main_equation.get_part_by_tex("m")
        m_example_part = self.example_eq.get_part_by_tex("2")
        
        # Highlight 'm'
        self.play(
            m_part.animate.set_color(GREEN_COLOR).scale(1.2),
            m_example_part.animate.set_color(GREEN_COLOR)
        )

        # Show slope formula
        slope_formula = MathTex(
            "\\text{Slope } (m) = \\frac{\\text{Rise}}{\\text{Run}}", 
            font_size=LABEL_FONT_SIZE
        ).next_to(self.axes, UP, buff=0.25).to_edge(LEFT)
        self.play(Write(slope_formula))
        self.wait(2)

        # Animate different slopes
        slope_tracker = ValueTracker(0.01) # Start with a small non-zero value
        line = always_redraw(
            lambda: self.axes.get_graph(
                lambda x: slope_tracker.get_value() * x + 1, 
                color=YELLOW_COLOR
            )
        )
        
        slope_value_text = always_redraw(
            lambda: MathTex(f"m = {slope_tracker.get_value():.2f}", font_size=LABEL_FONT_SIZE)
                .next_to(slope_formula, DOWN, aligned_edge=LEFT)
        )

        self.play(FadeOut(self.b_dot, self.b_dot_label)) # Temporarily hide intercept dot
        self.add(line, slope_value_text)
        
        # Positive slope
        self.play(slope_tracker.animate.set_value(2), run_time=2)
        self.wait(1)
        # Negative slope
        self.play(slope_tracker.animate.set_value(-1), run_time=2)
        self.wait(1)
        # Zero slope
        self.play(slope_tracker.animate.set_value(0), run_time=2)
        self.wait(1)

        # Cleanup
        self.play(
            FadeOut(line, slope_value_text, slope_formula),
            m_part.animate.set_color(TEXT_COLOR).scale(1/1.2) # Revert 'm' highlight
        )
        self.remove(line, slope_value_text) # Remove updaters

    def show_full_example(self):
        """
        Builds the line y = 2x + 1 step-by-step using rise over run.
        """
        # Re-introduce the y-intercept dot
        self.play(FadeIn(self.b_dot, self.b_dot_label))

        # Show slope as rise/run
        slope_as_fraction = MathTex(
            "m = 2 = \\frac{2 \\, (\\text{Rise})}{1 \\, (\\text{Run})}",
            font_size=LABEL_FONT_SIZE
        ).next_to(self.axes, UP, buff=0.25).to_edge(RIGHT)
        self.play(Write(slope_as_fraction))
        self.wait(1)
        
        # --- First step: (0, 1) to (1, 3) ---
        p1 = self.axes.c2p(0, 1)
        p2 = self.axes.c2p(1, 3)
        
        run1_line = DashedLine(p1, self.axes.c2p(1, 1), color=RED_COLOR)
        run1_label = MathTex("1", color=RED_COLOR).next_to(run1_line, DOWN)
        self.play(Create(run1_line), Write(run1_label))
        self.wait(0.5)

        rise1_line = DashedLine(self.axes.c2p(1, 1), p2, color=GREEN_COLOR)
        rise1_label = MathTex("2", color=GREEN_COLOR).next_to(rise1_line, RIGHT)
        self.play(Create(rise1_line), Write(rise1_label))
        self.wait(0.5)

        p2_dot = Dot(p2, color=WHITE, radius=0.1)
        self.play(FadeIn(p2_dot))
        self.wait(1)

        # --- Second step: (1, 3) to (2, 5) ---
        p3 = self.axes.c2p(2, 5)

        run2_line = DashedLine(p2, self.axes.c2p(2, 3), color=RED_COLOR)
        run2_label = MathTex("1", color=RED_COLOR).next_to(run2_line, DOWN)
        self.play(Create(run2_line), Write(run2_label))
        self.wait(0.5)

        rise2_line = DashedLine(self.axes.c2p(2, 3), p3, color=GREEN_COLOR)
        rise2_label = MathTex("2", color=GREEN_COLOR).next_to(rise2_line, RIGHT)
        self.play(Create(rise2_line), Write(rise2_label))
        self.wait(0.5)
        
        p3_dot = Dot(p3, color=WHITE, radius=0.1)
        self.play(FadeIn(p3_dot))
        self.wait(1)

        # Draw the final line
        final_line = self.axes.get_graph(
            lambda x: 2 * x + 1, 
            color=YELLOW_COLOR,
            x_range=[-2, 3]
        )
        self.play(Create(final_line, run_time=2))
        self.wait(3)

        # Group all example elements for cleanup
        self.example_elements = VGroup(
            self.axes, self.example_eq, slope_as_fraction,
            self.b_dot, self.b_dot_label, p2_dot, p3_dot,
            run1_line, run1_label, rise1_line, rise1_label,
            run2_line, run2_label, rise2_line, rise2_label,
            final_line
        )

    def show_recap(self):
        """
        Displays a final summary of all components.
        """
        # Fade out everything except the main equation
        self.play(FadeOut(self.example_elements))
        self.play(self.main_equation.animate.center().scale(1.2))
        self.wait(1)

        # Isolate parts for recap
        y_part = self.main_equation.get_part_by_tex("y")
        x_part = self.main_equation.get_part_by_tex("x")
        m_part = self.main_equation.get_part_by_tex("m")
        b_part = self.main_equation.get_part_by_tex("b")
        
        # Create recap labels
        b_label = Text("Y-Intercept (Start Point)", font_size=RECAP_FONT_SIZE).next_to(b_part, DOWN, buff=1.5)
        m_label = Text("Slope (Steepness)", font_size=RECAP_FONT_SIZE).next_to(m_part, DOWN, buff=1.5)
        xy_label = Text("Any point (x, y) on the line", font_size=RECAP_FONT_SIZE).next_to(self.main_equation, UP, buff=1.5)
        
        # Create arrows
        b_arrow = Arrow(b_part.get_bottom(), b_label.get_top(), buff=0.2, color=BLUE_COLOR)
        m_arrow = Arrow(m_part.get_bottom(), m_label.get_top(), buff=0.2, color=GREEN_COLOR)
        xy_arrow_start = VGroup(y_part, x_part).get_center()
        xy_arrow = Arrow(xy_arrow_start + UP*0.5, xy_label.get_bottom(), buff=0.2, color=YELLOW_COLOR)

        # Animate recap
        self.play(
            LaggedStart(
                b_part.animate.set_color(BLUE_COLOR),
                Write(b_label),
                Create(b_arrow),
                lag_ratio=0.5
            )
        )
        self.wait(1)
        self.play(
            LaggedStart(
                m_part.animate.set_color(GREEN_COLOR),
                Write(m_label),
                Create(m_arrow),
                lag_ratio=0.5
            )
        )
        self.wait(1)
        self.play(
            LaggedStart(
                VGroup(y_part, x_part).animate.set_color(YELLOW_COLOR),
                Write(xy_label),
                Create(xy_arrow),
                lag_ratio=0.5
            )
        )
