from manim import *

# Define constants for consistency and easy modification
TEXT_COLOR = WHITE
EQUATION_COLOR = BLUE
HIGHLIGHT_COLOR = YELLOW
SUBTLE_COLOR = GRAY
TERM_COLOR = GREEN
GROUP_COLOR = RED

class SolutionAnimation(Scene):
    def construct(self):
        self.intro_harmonic_series()
        self.intuition_trap()
        self.grouping_proof()
        self.integral_test_proof()
        self.common_misunderstandings()
        self.recap_summary()

    def intro_harmonic_series(self):
        # Title
        title = Text("The Harmonic Series: An Infinite Sum That Diverges", font_size=40).to_edge(UP)
        self.play(FadeIn(title))
        self.wait(0.5)

        # Definition of Harmonic Series
        harmonic_title = Text("What is the Harmonic Series?", font_size=36, color=HIGHLIGHT_COLOR).next_to(title, DOWN, buff=0.8)
        self.play(Write(harmonic_title))
        self.wait(0.5)

        equation_sigma = MathTex(
            r"\sum_{n=1}^{\infty} \frac{1}{n}",
            color=EQUATION_COLOR,
            font_size=60
        ).next_to(harmonic_title, DOWN, buff=0.5)
        self.play(Write(equation_sigma))
        self.wait()

        expanded_series = MathTex(
            r"= 1 + \frac{1}{2} + \frac{1}{3} + \frac{1}{4} + \frac{1}{5} + \ldots",
            color=EQUATION_COLOR,
            font_size=60
        ).next_to(equation_sigma, RIGHT, buff=0.5).shift(0.5*LEFT)
        self.play(Write(expanded_series))
        self.wait(2)

        # Explain partial sums
        partial_sum_text = Text(
            "The k-th partial sum is:", font_size=30
        ).next_to(expanded_series, DOWN, buff=0.8, aligned_edge=LEFT)
        partial_sum_eq = MathTex(
            r"H_k = \sum_{n=1}^k \frac{1}{n} = 1 + \frac{1}{2} + \dots + \frac{1}{k}",
            font_size=45, color=EQUATION_COLOR
        ).next_to(partial_sum_text, DOWN, aligned_edge=LEFT)
        self.play(Write(partial_sum_text), Write(partial_sum_eq))
        self.wait(1)

        # Demonstrate partial sums
        h1 = MathTex(r"H_1 = 1").next_to(partial_sum_eq, DOWN, aligned_edge=LEFT).shift(0.5*RIGHT)
        h2 = MathTex(r"H_2 = 1 + \frac{1}{2} = 1.5").next_to(h1, DOWN, aligned_edge=LEFT)
        h3 = MathTex(r"H_3 = 1 + \frac{1}{2} + \frac{1}{3} \approx 1.83").next_to(h2, DOWN, aligned_edge=LEFT)
        h4 = MathTex(r"H_4 = 1 + \frac{1}{2} + \frac{1}{3} + \frac{1}{4} \approx 2.08").next_to(h3, DOWN, aligned_edge=LEFT)

        partial_sums = VGroup(h1, h2, h3, h4)
        self.play(FadeIn(h1))
        self.wait(0.5)
        self.play(FadeIn(h2))
        self.wait(0.5)
        self.play(FadeIn(h3))
        self.wait(0.5)
        self.play(FadeIn(h4))
        self.wait(2)

        self.play(
            FadeOut(title),
            FadeOut(harmonic_title),
            FadeOut(equation_sigma),
            FadeOut(expanded_series),
            FadeOut(partial_sum_text),
            FadeOut(partial_sum_eq),
            FadeOut(partial_sums),
        )

    def intuition_trap(self):
        # Intuition Trap section
        intuition_trap_title = Text("The Intuition Trap", font_size=40, color=HIGHLIGHT_COLOR).to_edge(UP)
        self.play(Write(intuition_trap_title))
        self.wait(0.5)

        trap_text = Text(
            "If individual terms approach zero, shouldn't the sum converge?",
            font_size=32, text_align="center"
        ).next_to(intuition_trap_title, DOWN, buff=0.5)
        self.play(Write(trap_text))
        self.wait(2)

        # Geometric series comparison
        geometric_series_text = Text("Consider a Convergent Series: Geometric Series", font_size=30, color=TERM_COLOR).next_to(trap_text, DOWN, buff=0.8)
        geo_eq = MathTex(
            r"\sum_{n=0}^{\infty} \left(\frac{1}{2}\right)^n = 1 + \frac{1}{2} + \frac{1}{4} + \frac{1}{8} + \ldots = 2",
            font_size=45, color=EQUATION_COLOR
        ).next_to(geometric_series_text, DOWN)
        self.play(Write(geometric_series_text), Write(geo_eq))
        self.wait(3)

        # Emphasize "necessary but not sufficient"
        condition_text = Text(
            r"Condition: $\lim_{n \to \infty} a_n = 0$ is NECESSARY for convergence,",
            font_size=30
        ).next_to(geo_eq, DOWN, buff=0.8, aligned_edge=LEFT).set_color(SUBTLE_COLOR)
        condition_text2 = Text(
            r"but NOT SUFFICIENT. The harmonic series is the counterexample.",
            font_size=30
        ).next_to(condition_text, DOWN, aligned_edge=LEFT).set_color(SUBTLE_COLOR)

        self.play(Write(condition_text))
        self.play(Write(condition_text2))
        self.wait(3)

        # Visual comparison of term shrinkage
        self.play(
            FadeOut(geometric_series_text),
            FadeOut(geo_eq),
            FadeOut(condition_text),
            FadeOut(condition_text2)
        )

        axes = Axes(
            x_range=[0, 8, 1],
            y_range=[0, 1.2, 0.2],
            x_length=8,
            y_length=5,
            axis_config={"color": GRAY, "numbers_to_exclude": [0]},
            x_axis_config={"numbers_with_elongated_ticks": [1,2,3,4,5,6,7,8]},
            y_axis_config={"numbers_with_elongated_ticks": [0,0.2,0.4,0.6,0.8,1.0,1.2]}
        ).to_edge(DOWN).shift(LEFT)
        labels = axes.get_axis_labels(x_label="n", y_label="a_n")

        harmonic_func = axes.get_graph(lambda x: 1/x, x_range=[1, 8], color=BLUE)
        geometric_func = axes.get_graph(lambda x: (1/2)**(x-1), x_range=[1, 8], color=GREEN)

        harmonic_label = MathTex(r"a_n = \frac{1}{n}", color=BLUE).next_to(harmonic_func, UP)
        geometric_label = MathTex(r"a_n = \left(\frac{1}{2}\right)^{n-1}", color=GREEN).next_to(geometric_func, UP)

        self.play(Create(axes), Write(labels))
        self.play(Create(harmonic_func), Write(harmonic_label))
        self.wait(1)
        self.play(Create(geometric_func), Write(geometric_label))
        self.wait(2)

        shrink_text = Text("Terms of 1/n shrink slower than 1/2^(n-1)", font_size=28).next_to(axes, RIGHT)
        arrow = Arrow(shrink_text.get_left(), axes.get_center(), buff=0.1)
        self.play(Write(shrink_text), GrowArrow(arrow))
        self.wait(2)

        self.play(
            FadeOut(intuition_trap_title),
            FadeOut(trap_text),
            FadeOut(axes),
            FadeOut(labels),
            FadeOut(harmonic_func),
            FadeOut(harmonic_label),
            FadeOut(geometric_func),
            FadeOut(geometric_label),
            FadeOut(shrink_text),
            FadeOut(arrow)
        )

    def grouping_proof(self):
        # Grouping Proof section
        grouping_title = Text("Oresme's Grouping Proof for Divergence", font_size=40, color=HIGHLIGHT_COLOR).to_edge(UP)
        self.play(Write(grouping_title))
        self.wait(0.5)

        series_init = MathTex(
            r"S = 1 + \frac{1}{2} + \frac{1}{3} + \frac{1}{4} + \frac{1}{5} + \frac{1}{6} + \frac{1}{7} + \frac{1}{8} + \ldots",
            font_size=40, color=EQUATION_COLOR
        ).next_to(grouping_title, DOWN, buff=0.5)
        self.play(Write(series_init))
        self.wait(1)

        step1 = Text("Step 1: Strategically group terms.", font_size=30).next_to(series_init, DOWN, buff=0.8, aligned_edge=LEFT).set_color(SUBTLE_COLOR)
        self.play(Write(step1))
        self.wait(1)

        # Grouping demonstration
        series_groups = MathTex(
            r"S = 1 + \frac{1}{2} + \left(\frac{1}{3} + \frac{1}{4}\right) + \left(\frac{1}{5} + \frac{1}{6} + \frac{1}{7} + \frac{1}{8}\right) + \ldots",
            font_size=40, color=EQUATION_COLOR
        ).move_to(series_init)
        series_groups.next_to(grouping_title, DOWN, buff=0.5)

        # Highlight first group
        self.play(
            Transform(series_init, series_groups),
            FadeOut(step1)
        )
        rect1 = SurroundingRectangle(series_groups[3], color=GROUP_COLOR) # (1/3 + 1/4)
        brace1 = Brace(series_groups[3], direction=DOWN, color=GROUP_COLOR)
        text1 = Text("Group 1: 2 terms", font_size=24, color=GROUP_COLOR).next_to(brace1, DOWN)
        self.play(Create(rect1), GrowFromCenter(brace1), Write(text1))
        self.wait(1)

        # Highlight second group
        rect2 = SurroundingRectangle(series_groups[4], color=GROUP_COLOR) # (1/5 + ... + 1/8)
        brace2 = Brace(series_groups[4], direction=DOWN, color=GROUP_COLOR)
        text2 = Text("Group 2: 4 terms", font_size=24, color=GROUP_COLOR).next_to(brace2, DOWN)
        self.play(Create(rect2), GrowFromCenter(brace2), Write(text2))
        self.wait(2)

        self.play(FadeOut(rect1), FadeOut(brace1), FadeOut(text1),
                  FadeOut(rect2), FadeOut(brace2), FadeOut(text2))

        step2 = Text("Step 2: Find a lower bound for each group.", font_size=30).next_to(series_groups, DOWN, buff=0.8, aligned_edge=LEFT).set_color(SUBTLE_COLOR)
        self.play(Write(step2))
        self.wait(1)

        # Lower bound for 1/3 + 1/4
        group1_eq = MathTex(r"\left(\frac{1}{3} + \frac{1}{4}\right)", font_size=45).next_to(step2, DOWN, aligned_edge=LEFT)
        bound1_eq = MathTex(r"> \left(\frac{1}{4} + \frac{1}{4}\right) = \frac{2}{4} = \frac{1}{2}", font_size=45, color=TERM_COLOR).next_to(group1_eq, RIGHT)
        self.play(Write(group1_eq))
        self.wait(0.5)
        self.play(TransformFromCopy(group1_eq[1], bound1_eq[1]), TransformFromCopy(group1_eq[3], bound1_eq[3]))
        self.play(Write(bound1_eq[0]), Write(bound1_eq[2:]))
        self.wait(1.5)

        # Lower bound for 1/5 + 1/6 + 1/7 + 1/8
        group2_eq = MathTex(r"\left(\frac{1}{5} + \frac{1}{6} + \frac{1}{7} + \frac{1}{8}\right)", font_size=45).next_to(group1_eq, DOWN, aligned_edge=LEFT)
        bound2_eq = MathTex(r"> \left(\frac{1}{8} + \frac{1}{8} + \frac{1}{8} + \frac{1}{8}\right) = \frac{4}{8} = \frac{1}{2}", font_size=45, color=TERM_COLOR).next_to(group2_eq, RIGHT)
        self.play(Write(group2_eq))
        self.wait(0.5)
        self.play(TransformFromCopy(group2_eq[1], bound2_eq[1]),
                  TransformFromCopy(group2_eq[3], bound2_eq[3]),
                  TransformFromCopy(group2_eq[5], bound2_eq[5]),
                  TransformFromCopy(group2_eq[7], bound2_eq[7]))
        self.play(Write(bound2_eq[0]), Write(bound2_eq[2:]))
        self.wait(2)

        general_group_text = Text("In general, each group sums to at least 1/2!", font_size=30, color=HIGHLIGHT_COLOR).next_to(group2_eq, DOWN, buff=0.8)
        self.play(Write(general_group_text))
        self.wait(2)

        self.play(
            FadeOut(series_groups),
            FadeOut(step2),
            FadeOut(group1_eq),
            FadeOut(bound1_eq),
            FadeOut(group2_eq),
            FadeOut(bound2_eq),
            FadeOut(general_group_text)
        )

        step3 = Text("Step 3: Aggregate the lower bounds.", font_size=30).next_to(grouping_title, DOWN, buff=0.8, aligned_edge=LEFT).set_color(SUBTLE_COLOR)
        self.play(Write(step3))
        self.wait(1)

        sum_lower_bound = MathTex(
            r"S = 1 + \frac{1}{2} + \left(\frac{1}{3} + \frac{1}{4}\right) + \left(\frac{1}{5} + \dots + \frac{1}{8}\right) + \ldots",
            font_size=40, color=EQUATION_COLOR
        ).next_to(step3, DOWN, buff=0.5)

        sum_lower_bound_eval = MathTex(
            r"S > 1 + \frac{1}{2} + \frac{1}{2} + \frac{1}{2} + \ldots",
            font_size=45, color=TERM_COLOR
        ).next_to(sum_lower_bound, DOWN, buff=0.5).align_to(sum_lower_bound, LEFT)

        self.play(Write(sum_lower_bound))
        self.wait(1)
        self.play(TransformFromCopy(sum_lower_bound[3], sum_lower_bound_eval[2]),
                  TransformFromCopy(sum_lower_bound[4], sum_lower_bound_eval[3]))
        self.play(Write(sum_lower_bound_eval[0]), Write(sum_lower_bound_eval[1]), Write(sum_lower_bound_eval[4:]))
        self.wait(2)

        final_bound = MathTex(
            r"S > 1 + m \cdot \frac{1}{2} \quad \text{for } m \text{ groups}",
            font_size=45, color=HIGHLIGHT_COLOR
        ).next_to(sum_lower_bound_eval, DOWN, buff=0.8, aligned_edge=LEFT)
        self.play(Write(final_bound))
        self.wait(2)

        step4 = Text("Step 4: Conclude divergence.", font_size=30).next_to(final_bound, DOWN, buff=0.8, aligned_edge=LEFT).set_color(SUBTLE_COLOR)
        self.play(Write(step4))
        self.wait(1)

        lim_m = MathTex(r"\lim_{m \to \infty} \left(1 + m \cdot \frac{1}{2}\right) = \infty", font_size=50).next_to(step4, DOWN)
        self.play(Write(lim_m))
        self.wait(1.5)

        conclusion_diverges = Text("Since S > an unbounded quantity, S must diverge!",
                                   font_size=36, color=RED).next_to(lim_m, DOWN, buff=0.8)
        self.play(Write(conclusion_diverges))
        self.wait(3)

        self.play(
            FadeOut(grouping_title),
            FadeOut(step3),
            FadeOut(sum_lower_bound),
            FadeOut(sum_lower_bound_eval),
            FadeOut(final_bound),
            FadeOut(step4),
            FadeOut(lim_m),
            FadeOut(conclusion_diverges)
        )

    def integral_test_proof(self):
        # Integral Test section
        integral_title = Text("The Integral Test", font_size=40, color=HIGHLIGHT_COLOR).to_edge(UP)
        self.play(Write(integral_title))
        self.wait(0.5)

        integral_test_statement = Text(
            "For positive, continuous, decreasing function f(x):",
            font_size=30
        ).next_to(integral_title, DOWN, buff=0.5)
        integral_test_statement2 = MathTex(
            r"\sum_{n=1}^\infty f(n) \quad \text{and} \quad \int_1^\infty f(x) dx",
            font_size=45
        ).next_to(integral_test_statement, DOWN)
        integral_test_statement3 = Text(
            "either both converge or both diverge.",
            font_size=30
        ).next_to(integral_test_statement2, DOWN)

        self.play(Write(integral_test_statement))
        self.play(Write(integral_test_statement2))
        self.play(Write(integral_test_statement3))
        self.wait(3)

        self.play(
            FadeOut(integral_test_statement),
            FadeOut(integral_test_statement2),
            FadeOut(integral_test_statement3)
        )

        # Graph f(x) = 1/x and show rectangles
        axes = Axes(
            x_range=[0, 7, 1],
            y_range=[0, 1.2, 0.2],
            x_length=7,
            y_length=5,
            axis_config={"color": GRAY},
            x_axis_config={"numbers_with_elongated_ticks": [1,2,3,4,5,6]},
            y_axis_config={"numbers_with_elongated_ticks": [0,0.2,0.4,0.6,0.8,1.0,1.2]}
        ).to_edge(LEFT, buff=0.5).shift(0.5*DOWN)
        labels = axes.get_axis_labels(x_label="x", y_label="f(x)")
        func = axes.get_graph(lambda x: 1/x, x_range=[1, 6.5], color=BLUE)
        func_label = MathTex(r"f(x) = \frac{1}{x}", color=BLUE).next_to(func, UP, buff=0.1)

        self.play(Create(axes), Write(labels), Create(func), Write(func_label))
        self.wait(1)

        rects = VGroup()
        for i in range(1, 6):
            rect = axes.get_rectangle(x_range=[i, i+1], y_range=[0, 1/i], color=TERM_COLOR, fill_opacity=0.6)
            rects.add(rect)
        self.play(Create(rects))
        self.wait(1)

        series_sum_text = Text(r"$\sum_{n=1}^\infty \frac{1}{n}$ is the sum of these rectangle areas (or slightly larger)",
                               font_size=24).next_to(axes, RIGHT, buff=0.5).set_color(TERM_COLOR)
        self.play(Write(series_sum_text))
        self.wait(2)

        integral_text_formula = MathTex(
            r"\int_1^\infty \frac{1}{x} dx = [\ln|x|]_1^\infty",
            font_size=50, color=EQUATION_COLOR
        ).next_to(series_sum_text, DOWN, buff=0.8, aligned_edge=LEFT)
        self.play(Write(integral_text_formula))
        self.wait(1.5)

        integral_eval = MathTex(
            r" = \lim_{b \to \infty} (\ln b - \ln 1) = \lim_{b \to \infty} \ln b",
            font_size=50, color=EQUATION_COLOR
        ).next_to(integral_text_formula, DOWN, aligned_edge=LEFT)
        self.play(Write(integral_eval))
        self.wait(1.5)

        integral_infinity = MathTex(r"= \infty", font_size=50, color=RED).next_to(integral_eval, DOWN, aligned_edge=LEFT)
        self.play(Write(integral_infinity))
        self.wait(1.5)

        conclusion_integral = Text(
            "Since the integral diverges, the Harmonic Series also diverges!",
            font_size=36, color=RED
        ).next_to(integral_infinity, DOWN, buff=0.8)
        self.play(Write(conclusion_integral))
        self.wait(3)

        self.play(
            FadeOut(integral_title),
            FadeOut(axes),
            FadeOut(labels),
            FadeOut(func),
            FadeOut(func_label),
            FadeOut(rects),
            FadeOut(series_sum_text),
            FadeOut(integral_text_formula),
            FadeOut(integral_eval),
            FadeOut(integral_infinity),
            FadeOut(conclusion_integral)
        )

    def common_misunderstandings(self):
        # Misconceptions section
        miscon_title = Text("Common Misunderstandings", font_size=40, color=HIGHLIGHT_COLOR).to_edge(UP)
        self.play(Write(miscon_title))
        self.wait(0.5)

        miscon1_text = Text("Misconception 1: \"If terms go to zero, the series must converge.\"", font_size=30, color=RED).next_to(miscon_title, DOWN, buff=0.5)
        self.play(Write(miscon1_text))
        self.wait(0.5)

        correction1_text = Text(
            "Correction: NECESSARY but not SUFFICIENT. Terms must go to zero FAST ENOUGH.",
            font_size=28, color=GREEN
        ).next_to(miscon1_text, DOWN, aligned_edge=LEFT).shift(0.5*RIGHT)
        self.play(Write(correction1_text))
        self.wait(2)

        miscon2_text = Text("Misconception 2: \"All p-series diverge.\"", font_size=30, color=RED).next_to(correction1_text, DOWN, buff=0.8, aligned_edge=LEFT).shift(-0.5*RIGHT)
        self.play(Write(miscon2_text))
        self.wait(0.5)

        p_series_eq = MathTex(r"\sum_{n=1}^\infty \frac{1}{n^p}", font_size=40).next_to(miscon2_text, DOWN, aligned_edge=LEFT).shift(0.5*RIGHT)
        correction2_text = Text(
            "Correction: p-series diverge only when p <= 1.",
            font_size=28, color=GREEN
        ).next_to(p_series_eq, DOWN, aligned_edge=LEFT)
        example_converge = MathTex(
            r"\text{Converges if } p > 1 \text{ (e.g., } \sum \frac{1}{n^2})",
            font_size=28, color=GREEN
        ).next_to(correction2_text, DOWN, aligned_edge=LEFT)

        self.play(Write(p_series_eq), Write(correction2_text))
        self.wait(1)
        self.play(Write(example_converge))
        self.wait(3)

        self.play(
            FadeOut(miscon_title),
            FadeOut(miscon1_text),
            FadeOut(correction1_text),
            FadeOut(miscon2_text),
            FadeOut(p_series_eq),
            FadeOut(correction2_text),
            FadeOut(example_converge)
        )

    def recap_summary(self):
        # Recap section
        recap_title = Text("Recap: Why the Harmonic Series Diverges", font_size=40, color=HIGHLIGHT_COLOR).to_edge(UP)
        self.play(Write(recap_title))
        self.wait(0.5)

        summary_points = VGroup(
            Text("1. Grouping Proof: Groups of terms sum to at least 1/2, leading to an unbounded sum.", font_size=30).set_color(BLUE),
            Text("2. Integral Test: The integral of 1/x from 1 to infinity diverges to infinity.", font_size=30).set_color(GREEN),
            Text("Key Takeaway: Terms must shrink FAST ENOUGH for convergence.", font_size=32).set_color(YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.7).next_to(recap_title, DOWN, buff=0.8)

        self.play(Write(summary_points[0]))
        self.wait(2)
        self.play(Write(summary_points[1]))
        self.wait(2)
        self.play(Write(summary_points[2]))
        self.wait(3)

        closing_text = Text("Infinity is tricky! Our intuition isn't always reliable in math.",
                            font_size=30, text_align="center").next_to(summary_points, DOWN, buff=1.0)
        self.play(Write(closing_text))
        self.wait(2)

        self.play(FadeOut(VGroup(recap_title, summary_points, closing_text)))
        final_message = Text("Keep exploring the infinite!", font_size=45, color=HIGHLIGHT_COLOR)
        self.play(Write(final_message))
        self.wait(3)

        self.play(FadeOut(final_message))
