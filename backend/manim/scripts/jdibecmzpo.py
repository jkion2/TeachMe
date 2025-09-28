# To run this code, save it as a .py file (e.g., linear_equation.py)
# and run `manim -pql linear_equation.py EquationOfALine` in your terminal.
# The command below will render all scenes in the file in order.
# manim -pql linear_equation.py

from manim import (
    Scene,
    Text,
    MathTex,
    VGroup,
    Axes,
    Dot,
    Line,
    Arrow,
    SurroundingRectangle,
    Create,
    Write,
    FadeIn,
    FadeOut,
    Transform,
    Indicate,
    Circumscribe,
    ValueTracker,
    always_redraw,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    BLUE,
    GREEN,
    YELLOW,
    RED,
    WHITE,
)

# Constants for styling
TEXT_COLOR = WHITE
EQUATION_COLOR = WHITE
SLOPE_COLOR = YELLOW
INTERCEPT_COLOR = BLUE
LINE_COLOR = GREEN
HIGHLIGHT_COLOR = RED


class EquationOfALine(Scene):
    """
    This class combines all scenes into one for a continuous video flow.
    """
    def construct(self):
        self.intro_scene()
        self.y_intercept_scene()
        self.slope_scene()
        self.graphing_scene()
        self.slope_exploration_scene()
        self.summary_scene()

    def intro_scene(self):
        """Scene 1: Introduction"""
        # Title
        title = Text("The Equation of a Line", font_size=48)
        self.play(Write(title))
        self.wait(1)

        # Equation
        equation = MathTex("y", "=", "m", "x", "+", "b", font_size=96).next_to(title, DOWN, buff=1)
        self.play(Transform(title, equation))
        self.wait(1)

        # Highlight components
        self.play(Indicate(equation.get_part_by_tex("y"), color=HIGHLIGHT_COLOR))
        self.wait(0.5)
        self.play(Indicate(equation.get_part_by_tex("m"), color=SLOPE_COLOR))
        self.wait(0.5)
        self.play(Indicate(equation.get_part_by_tex("x"), color=HIGHLIGHT_COLOR))
        self.wait(0.5)
        self.play(Indicate(equation.get_part_by_tex("b"), color=INTERCEPT_COLOR))
        self.wait(2)
        
        # Prepare for next scene
        self.play(FadeOut(title), equation.animate.to_edge(UP).scale(0.7))
        self.equation = equation

    def y_intercept_scene(self):
        """Scene 2: The Components - Y-Intercept 'b'"""
        # Create coordinate plane
        self.axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            axis_config={"color": BLUE},
            x_axis_config={"numbers_to_include": range(-4, 5, 2)},
            y_axis_config={"numbers_to_include": range(-4, 5, 2)},
        )
        self.play(Create(self.axes))
        self.wait(1)

        # Isolate 'b'
        b_part = self.equation.get_part_by_tex("b")
        b_highlight = SurroundingRectangle(b_part, color=INTERCEPT_COLOR)
        b_text = Text("'b' is the y-intercept", font_size=36).next_to(self.equation, DOWN)
        b_text.set_color(INTERCEPT_COLOR)
        
        self.play(Create(b_highlight), Write(b_text))
        self.wait(1)

        # Explain 'starting point'
        starting_point_text = Text("It's the 'starting point' on the y-axis.", font_size=32).next_to(b_text, DOWN)
        self.play(Write(starting_point_text))
        self.wait(2)

        # Show substitution x=0
        explanation_group = VGroup()
        when_x_is_0 = MathTex("When ", "x=0", ":").next_to(self.axes, DOWN, buff=0.5).to_edge(LEFT, buff=0.5)
        y_eq_0 = MathTex("y", "=", "m", "(0)", "+", "b").next_to(when_x_is_0, RIGHT)
        y_eq_b = MathTex("y", "=", "b").next_to(y_eq_0, RIGHT, buff=1)

        explanation_group.add(when_x_is_0, y_eq_0)
        self.play(Write(explanation_group))
        self.wait(1.5)
        self.play(Transform(y_eq_0.copy(), y_eq_b))
        explanation_group.add(y_eq_b)
        self.wait(2)

        # Animate the y-intercept point
        # Let's use b=1 for our example
        b_val = 1
        y_intercept_dot = Dot(self.axes.c2p(0, b_val), color=INTERCEPT_COLOR, radius=0.1)
        y_intercept_label = MathTex("(0, b)").next_to(y_intercept_dot, RIGHT)
        
        self.play(Create(y_intercept_dot), Write(y_intercept_label))
        self.wait(2)
        
        # Cleanup for next scene
        self.play(
            FadeOut(b_text), 
            FadeOut(starting_point_text), 
            FadeOut(explanation_group), 
            FadeOut(y_intercept_label)
        )
        self.b_highlight = b_highlight
        self.y_intercept_dot = y_intercept_dot

    def slope_scene(self):
        """Scene 3: The Components - Slope 'm'"""
        # Isolate 'm'
        m_part = self.equation.get_part_by_tex("m")
        m_highlight = SurroundingRectangle(m_part, color=SLOPE_COLOR)
        m_text = Text("'m' is the slope", font_size=36).next_to(self.equation, DOWN)
        m_text.set_color(SLOPE_COLOR)

        self.play(Transform(self.b_highlight, m_highlight), Write(m_text))
        self.wait(1)

        # Explain slope
        steepness_text = Text("It's the 'rate of change' or 'steepness'.", font_size=32).next_to(m_text, DOWN)
        self.play(Write(steepness_text))
        self.wait(2)

        # Rise over run formula
        rise_run_formula = MathTex(
            "m = \\frac{\\text{rise}}{\\text{run}} = \\frac{\\Delta y}{\\Delta x}",
            font_size=48
        ).next_to(self.axes, DOWN, buff=0.5)
        
        self.play(Write(rise_run_formula))
        self.wait(2)

        # Introduce example: y = 2x + 1
        example_equation = MathTex("y", "=", "2", "x", "+", "1", font_size=80)
        example_equation.move_to(self.equation).to_edge(UP)
        
        self.play(Transform(self.equation, example_equation), FadeOut(self.b_highlight))
        self.wait(1)
        
        # Highlight m=2 and b=1
        m_example = VGroup(
            Text("m = 2", font_size=36).next_to(m_text, DOWN, buff=0.75),
            Text("b = 1", font_size=36)
        )
        m_example[1].next_to(m_example[0], RIGHT, buff=1)
        m_example[0].set_color(SLOPE_COLOR)
        m_example[1].set_color(INTERCEPT_COLOR)

        self.play(FadeOut(steepness_text), Write(m_example))
        self.wait(1)
        
        # Explain m = 2/1
        slope_fraction = MathTex("m = 2 = \\frac{2}{1}").next_to(rise_run_formula, DOWN)
        slope_fraction[0][2].set_color(SLOPE_COLOR)
        slope_fraction[0][4].set_color(RED)  # rise
        slope_fraction[0][6].set_color(YELLOW) # run

        self.play(Write(slope_fraction))
        self.wait(2)

        # Cleanup
        self.play(FadeOut(m_text), FadeOut(rise_run_formula), FadeOut(m_example), FadeOut(slope_fraction))

    def graphing_scene(self):
        """Scene 4: Graphing the Line"""
        b_val = 1
        m_val = 2
        
        # Animate run
        run_arrow = Arrow(
            start=self.axes.c2p(0, b_val),
            end=self.axes.c2p(1, b_val),
            buff=0,
            color=YELLOW,
        )
        run_label = MathTex("\\text{run} = 1", font_size=36, color=YELLOW).next_to(run_arrow, DOWN)
        
        self.play(Create(run_arrow), Write(run_label))
        self.wait(1)

        # Animate rise
        rise_arrow = Arrow(
            start=self.axes.c2p(1, b_val),
            end=self.axes.c2p(1, b_val + m_val),
            buff=0,
            color=RED,
        )
        rise_label = MathTex("\\text{rise} = 2", font_size=36, color=RED).next_to(rise_arrow, RIGHT)

        self.play(Create(rise_arrow), Write(rise_label))
        self.wait(1)
        
        # Place new dot
        new_dot = Dot(self.axes.c2p(1, b_val + m_val), color=INTERCEPT_COLOR, radius=0.1)
        self.play(Create(new_dot))
        self.wait(1)

        # Draw the line
        self.line = self.axes.get_graph(lambda x: m_val * x + b_val, color=LINE_COLOR)
        line_label = self.axes.get_graph_label(self.line, "y = 2x + 1", x_val=2)
        self.play(Create(self.line), Write(line_label))
        self.wait(2)
        
        # Store objects for next scene
        self.graphing_elements = VGroup(
            self.y_intercept_dot, new_dot, run_arrow, run_label, rise_arrow, rise_label, line_label
        )

    def slope_exploration_scene(self):
        """Scene 5: Exploring Different Slopes"""
        self.play(FadeOut(self.graphing_elements))

        m_tracker = ValueTracker(2)
        
        # Redrawable line and its label
        line_graph = always_redraw(
            lambda: self.axes.get_graph(
                lambda x: m_tracker.get_value() * x + 1, color=LINE_COLOR
            )
        )
        line_eq_label = always_redraw(
            lambda: MathTex(
                f"y = {m_tracker.get_value():.1f}x + 1",
                font_size=40
            ).next_to(line_graph, UP, buff=0.5, aligned_edge=RIGHT)
        )
        
        self.play(FadeOut(self.line), FadeIn(line_graph), FadeIn(line_eq_label))
        self.wait(1)

        # Animate to negative slope
        neg_slope_text = Text("Negative slope (m < 0) goes down", font_size=36).to_edge(DOWN)
        self.play(Write(neg_slope_text))
        self.play(m_tracker.animate.set_value(-1), run_time=3)
        self.wait(2)
        self.play(FadeOut(neg_slope_text))
        
        # Animate to zero slope
        zero_slope_text = Text("Zero slope (m = 0) is flat", font_size=36).to_edge(DOWN)
        self.play(Write(zero_slope_text))
        self.play(m_tracker.animate.set_value(0), run_time=3)
        self.wait(2)
        self.play(FadeOut(zero_slope_text))
        
        # Animate to a steeper slope
        steeper_slope_text = Text("Larger slope means a steeper line", font_size=36).to_edge(DOWN)
        self.play(Write(steeper_slope_text))
        self.play(m_tracker.animate.set_value(4), run_time=3)
        self.wait(2)
        self.play(FadeOut(steeper_slope_text))
        
        # Cleanup
        self.play(FadeOut(self.axes), FadeOut(line_graph), FadeOut(line_eq_label), FadeOut(self.equation))

    def summary_scene(self):
        """Scene 6: Summary"""
        final_equation = MathTex("y", "=", "m", "x", "+", "b", font_size=96)
        self.play(Write(final_equation))
        self.wait(1)

        # Highlight 'b'
        b_part = final_equation.get_part_by_tex("b")
        b_box = SurroundingRectangle(b_part, color=INTERCEPT_COLOR)
        b_summary = Text("y-intercept: Where the line starts", font_size=36).next_to(b_box, DOWN, buff=0.5)
        b_summary.set_color(INTERCEPT_COLOR)
        
        self.play(Create(b_box))
        self.play(Write(b_summary))
        self.wait(2)

        # Highlight 'm'
        m_part = final_equation.get_part_by_tex("m")
        m_box = SurroundingRectangle(m_part, color=SLOPE_COLOR)
        m_summary = Text("Slope: How the line moves", font_size=36).next_to(m_box, UP, buff=0.5)
        m_summary.set_color(SLOPE_COLOR)

        self.play(Create(m_box))
        self.play(Write(m_summary))
        self.wait(3)

        # Fade out everything
        self.play(
            FadeOut(final_equation),
            FadeOut(b_box),
            FadeOut(b_summary),
            FadeOut(m_box),
            FadeOut(m_summary),
        )
        self.wait(1)
