from manim import *

# --- Constants ---
# Colors
BLUE_LIGHT = "#5DADE2"
GREEN_LIGHT = "#52BE80"
YELLOW_LIGHT = "#F4D03F"
RED_LIGHT = "#E74C3C"
ORANGE_LIGHT = "#EB984E"
PURPLE_LIGHT = "#AF7AC5"

# Font sizes
TITLE_FONT_SIZE = 60
HEADER_FONT_SIZE = 48
TEXT_FONT_SIZE = 36
EQUATION_FONT_SIZE = 40


class SolutionAnimation(Scene):
    def construct(self):
        self.introduction()
        self.intuitive_trap()
        self.grouping_proof()
        self.integral_test_visual()
        self.common_misunderstandings()
        self.recap_and_conclusion()

    def introduction(self):
        # Title
        title = Text("The Harmonic Series Diverges", font_size=TITLE_FONT_SIZE).to_edge(UP)
        self.play(FadeIn(title, shift=UP))
        self.wait(0.5)

        # Definition of Harmonic Series
        intro_text = Text(
            "The harmonic series is the sum of reciprocals of positive integers:",
            font_size=TEXT_FONT_SIZE,
        ).next_to(title, DOWN, buff=0.7)
        self.play(Write(intro_text))
        self.wait(0.5)

        harmonic_series_eq = MathTex(
            r"\sum_{n=1}^{\infty} \frac{1}{n} =",
            r"1 + \frac{1}{2} + \frac{1}{3} + \frac{1}{4} + \dots",
            font_size=EQUATION_FONT_SIZE,
        ).next_to(intro_text, DOWN, buff=0.5)
        self.play(Write(harmonic_series_eq))
        self.wait(2)

        # Animate partial sums on a number line
        partial_sums_header = Text(
            "First few partial sums:", font_size=TEXT_FONT_SIZE
        ).next_to(harmonic_series_eq, DOWN, buff=1.0)
        self.play(FadeIn(partial_sums_header, shift=UP))

        number_line = (
            NumberLine(x_range=[0, 4, 0.5], length=10, include_numbers=True)
            .shift(DOWN * 2)
            .set_color(WHITE)
        )
        self.play(Create(number_line))
        self.wait(0.5)

        # S1 = 1
        s1_val = 1
        s1_dot = Dot(point=number_line.number_to_point(s1_val), color=BLUE_LIGHT)
        s1_label = MathTex(r"S_1 = 1").next_to(s1_dot, UP, buff=0.3)
        self.play(FadeIn(s1_dot), Write(s1_label))
        self.wait(1)

        # S2 = 1.5
        s2_val = 1 + 0.5
        s2_dot = Dot(point=number_line.number_to_point(s2_val), color=GREEN_LIGHT)
        s2_label = MathTex(r"S_2 = 1.5").next_to(s2_dot, UP, buff=0.3)
        self.play(Transform(s1_dot, s2_dot), Transform(s1_label, s2_label))
        self.wait(1)

        # S3 = 1.5 + 1/3 ~ 1.83
        s3_val = s2_val + 1 / 3
        s3_dot = Dot(point=number_line.number_to_point(s3_val), color=YELLOW_LIGHT)
        s3_label = MathTex(r"S_3 \approx 1.83").next_to(s3_dot, UP, buff=0.3)
        self.play(Transform(s1_dot, s3_dot), Transform(s1_label, s3_label))
        self.wait(1)

        # S4 = 1.83 + 1/4 ~ 2.08
        s4_val = s3_val + 1 / 4
        s4_dot = Dot(point=number_line.number_to_point(s4_val), color=RED_LIGHT)
        s4_label = MathTex(r"S_4 \approx 2.08").next_to(s4_dot, UP, buff=0.3)
        self.play(Transform(s1_dot, s4_dot), Transform(s1_label, s4_label))
        self.wait(2)

        self.play(
            FadeOut(title),
            FadeOut(intro_text),
            FadeOut(harmonic_series_eq),
            FadeOut(partial_sums_header),
            FadeOut(number_line),
            FadeOut(s1_dot),
            FadeOut(s1_label),
        )

    def intuitive_trap(self):
        # Intuitive Trap
        trap_header = Text(
            "The Intuitive Trap: Why it *seems* to converge",
            font_size=HEADER_FONT_SIZE,
            color=ORANGE_LIGHT,
        ).to_edge(UP)
        self.play(Write(trap_header))
        self.wait(1)

        lim_eq = MathTex(r"\lim_{n \to \infty} \frac{1}{n} = 0", font_size=EQUATION_FONT_SIZE)
        lim_text = Text(
            "Each term approaches zero...", font_size=TEXT_FONT_SIZE
        ).next_to(lim_eq, DOWN, buff=0.5)
        self.play(Write(lim_eq))
        self.play(Write(lim_text))
        self.wait(2)

        # Contrast with convergent geometric series
        contrast_text = Text(
            "Like the convergent geometric series:",
            font_size=TEXT_FONT_SIZE,
        ).next_to(lim_text, DOWN, buff=1.0)
        geometric_series_eq = MathTex(
            r"\sum_{n=1}^{\infty} \frac{1}{2^{n-1}} = 1 + \frac{1}{2} + \frac{1}{4} + \dots = 2",
            font_size=EQUATION_FONT_SIZE,
        ).next_to(contrast_text, DOWN, buff=0.5)
        self.play(Write(contrast_text))
        self.play(Write(geometric_series_eq))
        self.wait(2)

        warning_text = Text(
            "Terms approaching zero is NECESSARY, but NOT SUFFICIENT for convergence!",
            font_size=TEXT_FONT_SIZE,
            color=RED_LIGHT,
        ).next_to(geometric_series_eq, DOWN, buff=1.0)
        self.play(Write(warning_text))
        self.wait(3)

        self.play(
            FadeOut(trap_header),
            FadeOut(lim_eq),
            FadeOut(lim_text),
            FadeOut(contrast_text),
            FadeOut(geometric_series_eq),
            FadeOut(warning_text),
        )

    def grouping_proof(self):
        proof_header = Text(
            "The Brilliant Proof: Grouping Terms",
            font_size=HEADER_FONT_SIZE,
            color=GREEN_LIGHT,
        ).to_edge(UP)
        self.play(Write(proof_header))
        self.wait(1)

        # Display the series
        series_full = MathTex(
            r"1 + \frac{1}{2} + \frac{1}{3} + \frac{1}{4} + \frac{1}{5} + \frac{1}{6} + \frac{1}{7} + \frac{1}{8} + \dots",
            font_size=EQUATION_FONT_SIZE,
        ).shift(UP * 1.5)
        self.play(Write(series_full))
        self.wait(1)

        group_text = Text(
            "Let's strategically group the terms:",
            font_size=TEXT_FONT_SIZE,
        ).next_to(series_full, DOWN, buff=0.7)
        self.play(Write(group_text))
        self.wait(1)

        # Grouping animation
        g1 = MathTex(r"1", color=BLUE_LIGHT)
        g2 = MathTex(r"\frac{1}{2}", color=GREEN_LIGHT)
        g3 = MathTex(r"\left(\frac{1}{3} + \frac{1}{4}\right)", color=YELLOW_LIGHT)
        g4 = MathTex(
            r"\left(\frac{1}{5} + \frac{1}{6} + \frac{1}{7} + \frac{1}{8}\right)",
            color=RED_LIGHT,
        )
        g_dots = MathTex(r"+ \dots")

        grouped_series = (
            VGroup(g1, MathTex(r"+"), g2, MathTex(r"+"), g3, MathTex(r"+"), g4, g_dots)
            .arrange(RIGHT, buff=0.2)
            .next_to(group_text, DOWN, buff=0.5)
        )

        self.play(Transform(series_full, grouped_series[0]))  # 1
        self.play(FadeIn(grouped_series[1]))  # +
        self.play(Transform(series_full[2], grouped_series[2]))  # 1/2
        self.play(FadeIn(grouped_series[3]))  # +
        self.play(
            Transform(series_full[4], grouped_series[4][0]),  # (
            Transform(series_full[6], grouped_series[4][1]),  # 1/3
            Transform(series_full[8], grouped_series[4][2]),  # +
            Transform(series_full[10], grouped_series[4][3]),  # 1/4
            Transform(series_full[12], grouped_series[4][4]),  # )
        )
        self.play(FadeIn(grouped_series[5]))  # +
        self.play(
            Transform(series_full[14], grouped_series[6][0]),  # (
            Transform(series_full[16], grouped_series[6][1]),  # 1/5
            Transform(series_full[18], grouped_series[6][2]),  # +
            Transform(series_full[20], grouped_series[6][3]),  # 1/6
            Transform(series_full[22], grouped_series[6][4]),  # +
            Transform(series_full[24], grouped_series[6][5]),  # 1/7
            Transform(series_full[26], grouped_series[6][6]),  # +
            Transform(series_full[28], grouped_series[6][7]),  # 1/8
            Transform(series_full[30], grouped_series[6][8]),  # )
        )
        self.play(FadeIn(grouped_series[7]))  # ...

        # Re-arrange to the official grouped series MathTex object for easier manipulation
        grouped_series_final = MathTex(
            r"1 + \frac{1}{2} + \left(\frac{1}{3} + \frac{1}{4}\right) + \left(\frac{1}{5} + \frac{1}{6} + \frac{1}{7} + \frac{1}{8}\right) + \dots",
            font_size=EQUATION_FONT_SIZE,
        ).move_to(series_full.get_center())
        # Apply colors to specific parts for clarity
        grouped_series_final[0].set_color(BLUE_LIGHT)  # 1
        grouped_series_final[2].set_color(GREEN_LIGHT)  # 1/2
        grouped_series_final[4:9].set_color(YELLOW_LIGHT)  # (1/3 + 1/4)
        grouped_series_final[10:19].set_color(RED_LIGHT)  # (1/5 + ... + 1/8)
        self.play(Transform(series_full, grouped_series_final))
        self.wait(2)

        # Analyzing the groups
        analyze_header = Text(
            "Analyzing each group's sum:", font_size=TEXT_FONT_SIZE
        ).next_to(series_full, DOWN, buff=0.7)
        self.play(Write(analyze_header))
        self.wait(1)

        # Group 1 & 2 (1 and 1/2)
        g1_eq = MathTex(r"1 = 1", font_size=EQUATION_FONT_SIZE).shift(DOWN * 0.5 + LEFT * 4)
        g2_eq = MathTex(r"\frac{1}{2} = \frac{1}{2}", font_size=EQUATION_FONT_SIZE).next_to(g1_eq, RIGHT, buff=1.0)
        self.play(Write(g1_eq), Write(g2_eq))
        self.wait(1)

        # Group (1/3 + 1/4)
        g3_comparison = MathTex(
            r"\frac{1}{3} + \frac{1}{4} > \frac{1}{4} + \frac{1}{4} = \frac{2}{4} = \frac{1}{2}",
            font_size=EQUATION_FONT_SIZE,
            color=YELLOW_LIGHT,
        ).next_to(analyze_header, DOWN, buff=0.5)
        self.play(
            TransformFromCopy(grouped_series_final[4:9], g3_comparison),
            FadeOut(g1_eq), FadeOut(g2_eq),
        )
        self.wait(2)

        # Group (1/5 + ... + 1/8)
        g4_comparison = MathTex(
            r"\frac{1}{5} + \frac{1}{6} + \frac{1}{7} + \frac{1}{8} > \frac{1}{8} + \frac{1}{8} + \frac{1}{8} + \frac{1}{8} = \frac{4}{8} = \frac{1}{2}",
            font_size=EQUATION_FONT_SIZE,
            color=RED_LIGHT,
        ).next_to(g3_comparison, DOWN, buff=0.5)
        self.play(
            TransformFromCopy(grouped_series_final[10:19], g4_comparison)
        )
        self.wait(2)

        # Generalization
        generalize_text = Text(
            "Each group of $2^{k-1}$ terms sums to $ > \frac{1}{2}$",
            font_size=TEXT_FONT_SIZE,
        ).next_to(g4_comparison, DOWN, buff=1.0)
        self.play(Write(generalize_text))
        self.wait(1.5)

        general_group_eq = MathTex(
            r"\sum_{j=2^{k-1}+1}^{2^k} \frac{1}{j} > \sum_{j=2^{k-1}+1}^{2^k} \frac{1}{2^k} = 2^{k-1} \cdot \frac{1}{2^k} = \frac{1}{2}",
            font_size=EQUATION_FONT_SIZE,
        ).next_to(generalize_text, DOWN, buff=0.5)
        self.play(Write(general_group_eq))
        self.wait(3)

        self.play(
            FadeOut(proof_header),
            FadeOut(series_full),
            FadeOut(group_text),
            FadeOut(analyze_header),
            FadeOut(g3_comparison),
            FadeOut(g4_comparison),
            FadeOut(generalize_text),
            FadeOut(general_group_eq),
        )

        # Infinite half-steps to infinity
        infinite_half_header = Text(
            "Infinite Half-Steps to Infinity",
            font_size=HEADER_FONT_SIZE,
            color=PURPLE_LIGHT,
        ).to_edge(UP)
        self.play(Write(infinite_half_header))
        self.wait(1)

        partial_sum_N = MathTex(
            r"S_{2^N} = 1 + \frac{1}{2} + \left(\frac{1}{3} + \frac{1}{4}\right) + \left(\frac{1}{5} + \dots + \frac{1}{8}\right) + \dots + \left(\sum_{j=2^{N-1}+1}^{2^N} \frac{1}{j}\right)",
            font_size=EQUATION_FONT_SIZE,
        ).shift(UP * 1.5)
        self.play(Write(partial_sum_N))
        self.wait(2)

        lower_bound_text = Text(
            "By replacing each group with its lower bound of 1/2:",
            font_size=TEXT_FONT_SIZE,
        ).next_to(partial_sum_N, DOWN, buff=0.7)
        self.play(Write(lower_bound_text))
        self.wait(1)

        lower_bound_sum = MathTex(
            r"S_{2^N} > 1 + \frac{1}{2} + \frac{1}{2} + \frac{1}{2} + \dots + \frac{1}{2}",
            font_size=EQUATION_FONT_SIZE,
        ).next_to(lower_bound_text, DOWN, buff=0.5)
        brace = Brace(lower_bound_sum[4:], direction=DOWN)
        num_terms = Text("$N$ terms", font_size=TEXT_FONT_SIZE).next_to(brace, DOWN)
        self.play(Write(lower_bound_sum))
        self.play(GrowFromCenter(brace), Write(num_terms))
        self.wait(2)

        final_bound = MathTex(
            r"S_{2^N} > 1 + N \cdot \frac{1}{2} = 1 + \frac{N}{2}",
            font_size=EQUATION_FONT_SIZE,
        ).next_to(lower_bound_sum, DOWN, buff=0.7)
        self.play(Write(final_bound))
        self.wait(2)

        conclusion_text = Text(
            "As N approaches infinity, $1 + N/2$ approaches infinity.",
            font_size=TEXT_FONT_SIZE,
            color=RED_LIGHT,
        ).next_to(final_bound, DOWN, buff=1.0)
        conclusion_diverges = Text(
            "Thus, the Harmonic Series DIVERGES!",
            font_size=HEADER_FONT_SIZE,
            color=RED_LIGHT,
        ).next_to(conclusion_text, DOWN, buff=0.5)
        self.play(Write(conclusion_text))
        self.play(Write(conclusion_diverges))
        self.wait(3)

        self.play(
            FadeOut(infinite_half_header),
            FadeOut(partial_sum_N),
            FadeOut(lower_bound_text),
            FadeOut(lower_bound_sum),
            FadeOut(brace),
            FadeOut(num_terms),
            FadeOut(final_bound),
            FadeOut(conclusion_text),
            FadeOut(conclusion_diverges),
        )

    def integral_test_visual(self):
        integral_header = Text(
            "The Integral Test: A Visual Analogy",
            font_size=HEADER_FONT_SIZE,
            color=YELLOW_LIGHT,
        ).to_edge(UP)
        self.play(Write(integral_header))
        self.wait(1)

        axes = Axes(
            x_range=[0.5, 6.5, 1],
            y_range=[0, 1.2, 0.2],
            x_length=8,
            y_length=5,
            axis_config={"include_numbers": True},
        ).shift(DOWN * 0.5)
        labels = axes.get_axis_labels(x_label="x", y_label="1/x")
        self.play(Create(axes), Write(labels))
        self.wait(1)

        # Plot 1/x
        graph = axes.plot(lambda x: 1 / x, x_range=[1, 6.5], color=BLUE)
        graph_label = axes.get_graph_label(graph, label="f(x) = \\frac{1}{x}", x_val=5.5).shift(UP*0.5)
        self.play(Create(graph), FadeIn(graph_label))
        self.wait(1)

        # Draw rectangles for the series terms
        rects = VGroup()
        for i in range(1, 6):
            rect = axes.get_rectangle_rise_and_run(
                x_values=[i, i + 1],
                graph=graph,
                dx=0.01,
                stroke_width=0,
                fill_opacity=0.4,
                fill_color=GREEN_LIGHT,
            )
            rects.add(rect)

        series_sum_label = MathTex(
            r"\sum_{n=1}^{\infty} \frac{1}{n}", color=GREEN_LIGHT, font_size=EQUATION_FONT_SIZE
        ).shift(UP * 2.5 + LEFT * 4.5)
        integral_label = MathTex(
            r"\int_1^{\infty} \frac{1}{x} dx", color=BLUE, font_size=EQUATION_FONT_SIZE
        ).next_to(series_sum_label, RIGHT, buff=1.0)
        
        self.play(Create(rects), Write(series_sum_label))
        self.wait(1)
        self.play(Write(integral_label))
        self.wait(1)

        # Visually show that the sum of areas of rectangles is greater than the area under the curve
        comparison_text = Text(
            "Area of rectangles > Area under curve", font_size=TEXT_FONT_SIZE
        ).next_to(integral_label, RIGHT, buff=0.5)
        self.play(Write(comparison_text))
        self.wait(1)

        # Integral calculation
        integral_calc = MathTex(
            r"\int_1^{\infty} \frac{1}{x} dx &= \lim_{M \to \infty} \int_1^M \frac{1}{x} dx \\",
            r"&= \lim_{M \to \infty} [\ln|x|]_1^M \\",
            r"&= \lim_{M \to \infty} (\ln M - \ln 1) \\",
            r"&= \lim_{M \to \infty} \ln M = \infty",
            font_size=EQUATION_FONT_SIZE - 5,
        ).next_to(axes, DOWN, buff=0.7)
        integral_calc.shift(LEFT * 1.5)

        self.play(FadeOut(rects), FadeOut(series_sum_label), FadeOut(integral_label), FadeOut(comparison_text))
        self.play(Write(integral_calc[0]))
        self.wait(1.5)
        self.play(Write(integral_calc[1]))
        self.wait(1.5)
        self.play(Write(integral_calc[2]))
        self.wait(1.5)
        self.play(Write(integral_calc[3]))
        self.wait(2)

        integral_conclusion = Text(
            "Since the integral diverges, the series must also diverge!",
            font_size=TEXT_FONT_SIZE,
            color=RED_LIGHT,
        ).next_to(integral_calc, DOWN, buff=0.7)
        self.play(Write(integral_conclusion))
        self.wait(2.5)

        self.play(
            FadeOut(integral_header),
            FadeOut(axes),
            FadeOut(labels),
            FadeOut(graph),
            FadeOut(graph_label),
            FadeOut(integral_calc),
            FadeOut(integral_conclusion),
        )

    def common_misunderstandings(self):
        misconceptions_header = Text(
            "Common Misunderstandings",
            font_size=HEADER_FONT_SIZE,
            color=ORANGE_LIGHT,
        ).to_edge(UP)
        self.play(Write(misconceptions_header))
        self.wait(1)

        # Misconception 1
        miscon_1_title = Text(
            "Misconception 1:", font_size=TEXT_FONT_SIZE, color=RED_LIGHT
        ).shift(UP * 1.5 + LEFT * 3.5)
        miscon_1_text = Text(
            "\"If terms approach zero, the series must converge.\"",
            font_size=TEXT_FONT_SIZE - 5,
        ).next_to(miscon_1_title, RIGHT, buff=0.2)
        self.play(Write(miscon_1_title), Write(miscon_1_text))
        self.wait(1)

        corr_1_title = Text(
            "Correction:", font_size=TEXT_FONT_SIZE, color=GREEN_LIGHT
        ).next_to(miscon_1_title, DOWN, buff=0.5, aligned_edge=LEFT)
        corr_1_text = Text(
            "False! Terms must approach zero *fast enough*. Harmonic series is the classic counterexample.",
            font_size=TEXT_FONT_SIZE - 5,
            line_spacing=0.8,
        ).next_to(corr_1_title, RIGHT, buff=0.2)
        self.play(Write(corr_1_title), Write(corr_1_text))
        self.wait(3)

        # Misconception 2
        miscon_2_title = Text(
            "Misconception 2:", font_size=TEXT_FONT_SIZE, color=RED_LIGHT
        ).next_to(corr_1_title, DOWN, buff=1.0, aligned_edge=LEFT)
        miscon_2_text = Text(
            "\"The harmonic series converges, but just incredibly slowly.\"",
            font_size=TEXT_FONT_SIZE - 5,
        ).next_to(miscon_2_title, RIGHT, buff=0.2)
        self.play(Write(miscon_2_title), Write(miscon_2_text))
        self.wait(1)

        corr_2_title = Text(
            "Correction:", font_size=TEXT_FONT_SIZE, color=GREEN_LIGHT
        ).next_to(miscon_2_title, DOWN, buff=0.5, aligned_edge=LEFT)
        corr_2_text = Text(
            "It truly grows infinitely large. Its growth is logarithmic (slow), but unbounded.",
            font_size=TEXT_FONT_SIZE - 5,
            line_spacing=0.8,
        ).next_to(corr_2_title, RIGHT, buff=0.2)
        self.play(Write(corr_2_title), Write(corr_2_text))
        self.wait(3)

        self.play(
            FadeOut(misconceptions_header),
            FadeOut(miscon_1_title),
            FadeOut(miscon_1_text),
            FadeOut(corr_1_title),
            FadeOut(corr_1_text),
            FadeOut(miscon_2_title),
            FadeOut(miscon_2_text),
            FadeOut(corr_2_title),
            FadeOut(corr_2_text),
        )

    def recap_and_conclusion(self):
        recap_header = Text(
            "Recap: Why It Diverges", font_size=HEADER_FONT_SIZE
        ).to_edge(UP)
        self.play(Write(recap_header))
        self.wait(1)

        summary_points = VGroup(
            Text(
                "1. Harmonic Series: $\\sum_{n=1}^{\\infty} \\frac{1}{n}$",
                font_size=TEXT_FONT_SIZE,
                color=BLUE_LIGHT,
            ),
            Text(
                "2. Terms approach zero, but NOT fast enough for convergence.",
                font_size=TEXT_FONT_SIZE,
                color=ORANGE_LIGHT,
            ),
            Text(
                "3. Grouping Proof: Each group of terms adds at least $1/2$.",
                font_size=TEXT_FONT_SIZE,
                color=GREEN_LIGHT,
            ),
            Text(
                "4. Integral Test: $\\int_1^{\\infty} \\frac{1}{x} dx = \\infty$, confirming divergence.",
                font_size=TEXT_FONT_SIZE,
                color=YELLOW_LIGHT,
            ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.7).shift(UP * 0.5)

        for point in summary_points:
            self.play(FadeIn(point, shift=UP))
            self.wait(1.5)
        self.wait(1)

        closing_statement = Text(
            "The harmonic series is a classic example of infinite sums behaving counter-intuitively!",
            font_size=TEXT_FONT_SIZE,
            color=WHITE,
            line_spacing=1.2,
        ).next_to(summary_points, DOWN, buff=1.0)
        self.play(Write(closing_statement))
        self.wait(3)

        call_to_action = Text(
            "Explore more fascinating series!", font_size=TEXT_FONT_SIZE, color=PURPLE_LIGHT
        ).next_to(closing_statement, DOWN, buff=0.7)
        self.play(FadeIn(call_to_action, shift=UP))
        self.wait(2)

        self.play(
            FadeOut(recap_header),
            FadeOut(summary_points),
            FadeOut(closing_statement),
            FadeOut(call_to_action),
        )
