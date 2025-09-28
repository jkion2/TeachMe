from manim import *

# --- Constants for better readability and consistency ---
COLOR_A = RED
COLOR_B = GREEN
COLOR_C = BLUE
COLOR_X = YELLOW
COLOR_FORMULA = WHITE
COLOR_DISCRIMINANT = ORANGE
COLOR_SOLUTION = TEAL
COLOR_HIGHLIGHT = YELLOW

# Standard text sizes
HEADING_SIZE = 0.8
SUBHEADING_SIZE = 0.6
EQUATION_SIZE = 0.9

class SolutionAnimation(Scene):
    def construct(self):
        # Overall animation flow
        self.introduction()
        self.what_is_quadratic()
        self.need_for_formula()
        self.unveiling_formula()
        self.projectile_motion_application()
        self.optimization_application()
        self.the_discriminant()
        self.common_misunderstandings()
        self.recap_and_conclusion()

    def introduction(self):
        """Displays the title, hook, and introductory text for the video."""
        # Title and Hook
        title = Text("The Secret Power of the Quadratic Equation", font_size=HEADING_SIZE).to_edge(UP)
        hook1 = Text("Solving Real-World Problems", font_size=SUBHEADING_SIZE).next_to(title, DOWN)
        hook2 = Text("How do engineers calculate arcs or architects design bridges?", font_size=0.45).next_to(hook1, DOWN, buff=0.5)
        hook3 = Text("A single, elegant equation holds the key!", font_size=0.5, color=COLOR_HIGHLIGHT).next_to(hook2, DOWN)

        self.play(FadeIn(title, shift=UP))
        self.play(Write(hook1))
        self.play(FadeIn(hook2, shift=UP))
        self.play(Write(hook3))
        self.wait(1.5)
        self.play(FadeOut(VGroup(title, hook1, hook2, hook3)))

        # Introduction (Context + Why It Matters)
        intro_text1 = Text("The quadratic equation, ax² + bx + c = 0,", font_size=0.5).to_edge(UP).shift(DOWN*0.5)
        intro_text2 = Text("is a fundamental tool for finding unknowns when relationships involve a squared term.", font_size=0.4).next_to(intro_text1, DOWN)
        intro_text3 = Text("It models parabolic paths, optimizes designs, and much more.", font_size=0.4).next_to(intro_text2, DOWN)

        self.play(Write(intro_text1))
        self.play(Write(intro_text2))
        self.play(Write(intro_text3))
        self.wait(2)

        # Key Idea / Intuition
        intuitive_idea_1 = Text("Imagine finding a specific point on a curved path...", font_size=0.45).next_to(intro_text3, DOWN, buff=0.7)
        intuitive_idea_2 = Text("Like the highest point of a jump or where a projectile lands.", font_size=0.45).next_to(intuitive_idea_1, DOWN)
        intuitive_idea_3 = Text("The quadratic equation provides a direct, universal method.", font_size=0.45, color=GREEN).next_to(intuitive_idea_2, DOWN)

        self.play(FadeIn(intuitive_idea_1, shift=UP))
        self.play(Write(intuitive_idea_2))
        self.play(Write(intuitive_idea_3))
        self.wait(3)
        self.play(FadeOut(VGroup(intro_text1, intro_text2, intro_text3, intuitive_idea_1, intuitive_idea_2, intuitive_idea_3)))

    def what_is_quadratic(self):
        """Explains the standard form, coefficients, and roots of a quadratic equation."""
        heading = Text("Section 1: What is a Quadratic Equation?", font_size=HEADING_SIZE, color=COLOR_HIGHLIGHT).to_edge(UP)
        self.play(Write(heading))
        self.wait(1)

        # Standard Form
        standard_form_text = Text("Standard Form:", font_size=SUBHEADING_SIZE).next_to(heading, DOWN, buff=0.5).to_edge(LEFT)
        equation = MathTex(
            "a", "x^2", " + ", "b", "x", " + ", "c", " = 0"
        ).next_to(standard_form_text, RIGHT)
        equation[0].set_color(COLOR_A) # a
        equation[3].set_color(COLOR_B) # b
        equation[6].set_color(COLOR_C) # c
        equation[1].set_color(COLOR_X) # x^2
        equation[4].set_color(COLOR_X) # x

        self.play(Write(standard_form_text))
        self.play(Write(equation))
        self.wait(1)

        # Conditions for a, b, c
        conditions_text = Text("a, b, c are real numbers", font_size=0.4).next_to(equation, DOWN, buff=0.5).align_to(equation, LEFT)
        condition_a = MathTex("a \\neq 0", font_size=0.4, color=RED).next_to(conditions_text, DOWN).align_to(conditions_text, LEFT)

        self.play(Write(conditions_text))
        self.play(Write(condition_a))
        self.wait(1)

        # Roots/Zeros explanation
        roots_text = Text("Solutions for x are called 'roots' or 'zeros'.", font_size=0.4).next_to(condition_a, DOWN, buff=0.5).align_to(condition_a, LEFT)
        graph_link_text = Text("They represent where the parabola crosses the x-axis.", font_size=0.4).next_to(roots_text, DOWN).align_to(roots_text, LEFT)
        self.play(Write(roots_text))
        self.play(Write(graph_link_text))
        self.wait(2)

        # Examples of quadratic equations
        example_header = Text("Examples:", font_size=SUBHEADING_SIZE, color=BLUE).next_to(graph_link_text, DOWN, buff=0.7).align_to(graph_link_text, LEFT)
        ex1 = MathTex("2x^2 + 3x - 5 = 0").next_to(example_header, RIGHT, buff=0.5).shift(RIGHT)
        ex2 = MathTex("x^2 - 9 = 0").next_to(ex1, DOWN, buff=0.3).align_to(ex1, LEFT)
        ex3_orig = MathTex("4x^2 = 7x").next_to(ex2, DOWN, buff=0.3).align_to(ex2, LEFT)
        ex3_rearr = MathTex("4x^2 - 7x = 0").next_to(ex3_orig, RIGHT)

        self.play(Write(example_header))
        self.play(Write(ex1))
        self.play(Write(ex2))
        self.play(Write(ex3_orig))
        self.wait(1)
        self.play(TransformMatchingTex(ex3_orig, ex3_rearr))
        self.wait(1.5)
        self.play(FadeOut(VGroup(standard_form_text, equation, conditions_text, condition_a, roots_text,
                                graph_link_text, example_header, ex1, ex2, ex3_rearr)))

        # Graph of a parabola to show x-intercepts
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 5, 1],
            x_length=7,
            y_length=6,
            axis_config={"color": GREY},
            tips=False,
        ).to_edge(DOWN).shift(RIGHT*1.5)
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")
        
        # Using y = x^2 - 1 to clearly show two x-intercepts
        parabola_two_roots = axes.get_graph(lambda x: x**2 - 1, x_range=[-2.5, 2.5], color=PURPLE, stroke_width=4)
        x_int1 = Dot(axes.c2p(-1, 0), color=GREEN, radius=0.1)
        x_int2 = Dot(axes.c2p(1, 0), color=GREEN, radius=0.1)
        x_int_label = MathTex("x_1", color=GREEN).next_to(x_int1, DOWN+LEFT)
        x_int_label2 = MathTex("x_2", color=GREEN).next_to(x_int2, DOWN+RIGHT)

        self.play(Create(axes), Write(axes_labels))
        self.play(Create(parabola_two_roots))
        self.play(FadeIn(x_int1, x_int2), Write(x_int_label), Write(x_int_label2))
        self.play(Circumscribe(VGroup(x_int1, x_int2), color=GREEN))
        self.wait(2)
        self.play(FadeOut(VGroup(heading, axes, axes_labels, parabola_two_roots, x_int1, x_int2, x_int_label, x_int_label2)))

    def need_for_formula(self):
        """Illustrates why a universal formula is needed beyond simple factoring/square roots."""
        heading = Text("Section 2: The Need for a Formula", font_size=HEADING_SIZE, color=COLOR_HIGHLIGHT).to_edge(UP)
        self.play(Write(heading))
        self.wait(1)

        simple_sol_header = Text("Beyond Simple Solutions:", font_size=SUBHEADING_SIZE).next_to(heading, DOWN, buff=0.5).to_edge(LEFT)
        self.play(Write(simple_sol_header))

        # Factoring example
        factoring_eq_orig = MathTex("x^2 + 5x + 6 = 0").next_to(simple_sol_header, RIGHT, buff=0.5)
        factoring_eq_factors = MathTex("(x+2)(x+3) = 0").next_to(factoring_eq_orig, RIGHT, buff=0.5)
        factoring_sols = MathTex("x = -2, x = -3").next_to(factoring_eq_factors, DOWN, buff=0.3).align_to(factoring_eq_factors, LEFT)

        self.play(Write(factoring_eq_orig))
        self.play(TransformMatchingTex(factoring_eq_orig.copy(), factoring_eq_factors))
        self.play(Write(factoring_sols))
        self.wait(1.5)

        # Square root example
        sq_root_eq_orig = MathTex("x^2 - 9 = 0").next_to(factoring_sols, DOWN, buff=0.5).align_to(simple_sol_header, LEFT)
        sq_root_eq_rearr = MathTex("x^2 = 9").next_to(sq_root_eq_orig, RIGHT, buff=0.5)
        sq_root_sols = MathTex("x = \\pm 3").next_to(sq_root_eq_rearr, RIGHT, buff=0.5)

        self.play(Write(sq_root_eq_orig))
        self.play(TransformMatchingTex(sq_root_eq_orig.copy(), sq_root_eq_rearr))
        self.play(Write(sq_root_sols))
        self.wait(1.5)

        # Harder example that shows the need for the formula
        hard_eq = MathTex("2x^2 + 7x + 3 = 0").next_to(sq_root_sols, DOWN, buff=0.7).align_to(simple_sol_header, LEFT).set_color(RED)
        hard_text = Text("Factoring isn't always obvious or possible!", font_size=0.4, color=COLOR_HIGHLIGHT).next_to(hard_eq, DOWN, buff=0.5).align_to(hard_eq, LEFT)

        self.play(Write(hard_eq))
        self.play(Write(hard_text))
        self.wait(2)

        formula_needed_text = Text("That's where the all-powerful Quadratic Formula comes in!", font_size=0.5, color=GREEN).next_to(hard_text, DOWN, buff=0.7)
        self.play(Write(formula_needed_text))
        self.wait(2)
        self.play(FadeOut(VGroup(heading, simple_sol_header, factoring_eq_orig, factoring_eq_factors, factoring_sols,
                                sq_root_eq_orig, sq_root_eq_rearr, sq_root_sols, hard_eq, hard_text, formula_needed_text)))

    def unveiling_formula(self):
        """Displays the quadratic formula and walks through a worked example."""
        heading = Text("Section 3: Unveiling the Quadratic Formula", font_size=HEADING_SIZE, color=COLOR_HIGHLIGHT).to_edge(UP)
        self.play(Write(heading))
        self.wait(1)

        # The Quadratic Formula
        quadratic_formula = MathTex(
            "x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}",
            font_size=EQUATION_SIZE + 0.2, color=COLOR_FORMULA
        ).center()

        self.play(Write(quadratic_formula))
        self.wait(2)

        plus_minus_expl = Text("The '±' means two solutions!", font_size=0.4, color=TEAL).next_to(quadratic_formula, DOWN, buff=0.7)
        self.play(FadeIn(plus_minus_expl, shift=UP))
        self.wait(2)
        self.play(FadeOut(plus_minus_expl))

        self.play(heading.animate.to_corner(UL).shift(DOWN*0.5),
                  quadratic_formula.animate.to_edge(UP).shift(DOWN*1.5).scale(0.8))

        # Example: Solve 2x^2 + 7x + 3 = 0
        example_header = Text("Worked Example:", font_size=SUBHEADING_SIZE, color=BLUE).next_to(heading, DOWN).align_to(heading, LEFT)
        eq_to_solve = MathTex("2x^2 + 7x + 3 = 0", font_size=0.7).next_to(example_header, DOWN, buff=0.5).align_to(example_header, LEFT)
        eq_to_solve_parts = eq_to_solve.copy()
        eq_to_solve_parts[0].set_color(COLOR_A) # 2
        eq_to_solve_parts[2].set_color(COLOR_B) # 7
        eq_to_solve_parts[4].set_color(COLOR_C) # 3

        self.play(Write(example_header))
        self.play(Write(eq_to_solve))
        self.play(Transform(eq_to_solve, eq_to_solve_parts))
        self.wait(1)

        identify_abc = MathTex("a=2", ", ", "b=7", ", ", "c=3", font_size=0.6).next_to(eq_to_solve, DOWN, buff=0.5).align_to(eq_to_solve, LEFT)
        identify_abc[0].set_color(COLOR_A)
        identify_abc[2].set_color(COLOR_B)
        identify_abc[4].set_color(COLOR_C)
        self.play(Write(identify_abc))
        self.wait(1)

        # Substitution
        sub_formula = MathTex(
            "x = \\frac{-(7) \\pm \\sqrt{(7)^2 - 4(2)(3)}}{2(2)}",
            font_size=0.6
        ).next_to(identify_abc, DOWN, buff=0.5).align_to(identify_abc, LEFT)
        self.play(TransformFromCopy(VGroup(quadratic_formula.copy(), identify_abc.copy()), sub_formula))
        self.wait(2)

        # Simplify discriminant
        step1 = MathTex("x = \\frac{-7 \\pm \\sqrt{49 - 24}}{4}", font_size=0.6).next_to(sub_formula, DOWN, buff=0.3).align_to(sub_formula, LEFT)
        self.play(TransformMatchingTex(sub_formula, step1))
        self.wait(1)

        step2 = MathTex("x = \\frac{-7 \\pm \\sqrt{25}}{4}", font_size=0.6).next_to(step1, DOWN, buff=0.3).align_to(step1, LEFT)
        self.play(TransformMatchingTex(step1, step2))
        self.wait(1)

        step3 = MathTex("x = \\frac{-7 \\pm 5}{4}", font_size=0.6).next_to(step2, DOWN, buff=0.3).align_to(step2, LEFT)
        self.play(TransformMatchingTex(step2, step3))
        self.wait(1)

        # Two solutions
        sol1 = MathTex("x_1 = \\frac{-7+5}{4} = \\frac{-2}{4} = -0.5", font_size=0.6).next_to(step3, DOWN, buff=0.5).align_to(step3, LEFT).set_color(COLOR_SOLUTION)
        sol2 = MathTex("x_2 = \\frac{-7-5}{4} = \\frac{-12}{4} = -3", font_size=0.6).next_to(sol1, DOWN, buff=0.3).align_to(sol1, LEFT).set_color(COLOR_SOLUTION)

        self.play(Write(sol1))
        self.play(Write(sol2))
        self.wait(3)
        self.play(FadeOut(VGroup(heading, quadratic_formula, example_header, eq_to_solve, identify_abc, step3, sol1, sol2))) # step3 has the content of previous steps

    def projectile_motion_application(self):
        """Demonstrates projectile motion using the quadratic formula."""
        heading = Text("Section 4: Real-World Application:", font_size=HEADING_SIZE, color=COLOR_HIGHLIGHT).to_edge(UP)
        sub_heading = Text("Projectile Motion", font_size=SUBHEADING_SIZE).next_to(heading, DOWN)
        self.play(Write(heading), Write(sub_heading))
        self.wait(1)

        # Parabolic path animation
        axes_proj = Axes(
            x_range=[0, 4.5, 1], # time
            y_range=[0, 25, 5], # height
            x_length=10,
            y_length=6,
            axis_config={"color": GREY},
            tips=False,
        ).add_coordinates().to_edge(DOWN).shift(RIGHT*0.5)
        axes_proj.x_axis.add(axes_proj.get_axis_labels(x_label="Time (s)"))
        axes_proj.y_axis.add(axes_proj.get_axis_labels(y_label="Height (m)"))

        # h(t) = -4.9t^2 + 20t + 1.5
        parabolic_path = FunctionGraph(
            lambda t: -4.9 * t**2 + 20 * t + 1.5,
            x_range=[0, 4.16, 0.01], # from t=0 to when it hits ground ~4.16s
            color=PURPLE,
            stroke_width=3
        ).set_points_as_corners([
            axes_proj.c2p(t, -4.9 * t**2 + 20 * t + 1.5) for t in np.arange(0, 4.16, 0.01)
        ])

        # Soccer ball setup
        soccer_ball = Circle(radius=0.2, color=WHITE, fill_opacity=1).set_stroke(width=2, color=BLACK)
        # Simplified soccer ball pattern
        for i in range(3):
            line = Line(soccer_ball.get_center(), soccer_ball.get_boundary_point(i * 2 * PI / 3), color=BLACK, stroke_width=1)
            soccer_ball.add(line)
        soccer_ball.move_to(axes_proj.c2p(0, 1.5)) # Initial height

        self.play(Create(axes_proj), FadeIn(axes_proj.get_axis_labels()))
        self.play(FadeIn(soccer_ball))
        self.wait(1)

        self.play(MoveAlongPath(soccer_ball, parabolic_path), rate_func=linear, run_time=4.16)
        self.wait(1)
        self.play(FadeOut(soccer_ball), FadeOut(parabolic_path), FadeOut(VGroup(axes_proj, axes_proj.get_axis_labels())))

        # Generic projectile motion equation
        generic_eq = MathTex("h(t) = -\\frac{1}{2}gt^2 + v_0t + h_0", font_size=0.7).center().shift(UP*1)
        self.play(Write(generic_eq))
        self.wait(1)

        labels_h_t = MathTex("h(t)", r" \text{= height}").next_to(generic_eq, DOWN).align_to(generic_eq, LEFT)
        labels_t = MathTex("t", r" \text{= time}").next_to(labels_h_t, DOWN).align_to(generic_eq, LEFT)
        labels_v0 = MathTex("v_0", r" \text{= initial velocity}").next_to(labels_t, DOWN).align_to(generic_eq, LEFT)
        labels_h0 = MathTex("h_0", r" \text{= initial height}").next_to(labels_v0, DOWN).align_to(generic_eq, LEFT)
        labels_g = MathTex("g", r" \text{= acceleration due to gravity (9.8 m/s}^2)").next_to(labels_h0, DOWN).align_to(generic_eq, LEFT)

        label_group = VGroup(labels_h_t, labels_t, labels_v0, labels_h0, labels_g).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        label_group.next_to(generic_eq, DOWN, buff=0.5).to_edge(LEFT, buff=0.5)
        self.play(FadeIn(label_group, shift=RIGHT))
        self.wait(2)
        self.play(FadeOut(VGroup(heading, sub_heading, generic_eq, label_group)))

        # Problem setup
        problem_text_1 = Text("Problem: A ball is thrown upwards from 1.5m with 20 m/s.", font_size=0.45).to_edge(UP).shift(DOWN*0.5)
        problem_text_2 = Text("When will it hit the ground?", font_size=0.45, color=COLOR_HIGHLIGHT).next_to(problem_text_1, DOWN)
        problem_text_3 = Text("(Use g = 9.8 m/s²)", font_size=0.35).next_to(problem_text_2, DOWN)

        self.play(Write(VGroup(problem_text_1, problem_text_2, problem_text_3)))
        self.wait(1)

        # Formulate equation
        eq_formulation_header = Text("Formulate Equation (h(t)=0):", font_size=SUBHEADING_SIZE, color=BLUE).next_to(problem_text_3, DOWN, buff=0.5).align_to(problem_text_3, LEFT)
        eq_step1 = MathTex("0 = -\\frac{1}{2}(9.8)t^2 + 20t + 1.5").next_to(eq_formulation_header, DOWN, buff=0.3).align_to(eq_formulation_header, LEFT)
        eq_final = MathTex("0 = -4.9t^2 + 20t + 1.5", font_size=0.8).next_to(eq_step1, DOWN, buff=0.3).align_to(eq_step1, LEFT).set_color(COLOR_FORMULA)

        self.play(Write(eq_formulation_header))
        self.play(Write(eq_step1))
        self.play(TransformMatchingTex(eq_step1, eq_final))
        self.wait(1.5)

        # Identify a, b, c
        abc_id = MathTex("a = -4.9", ", ", "b = 20", ", ", "c = 1.5", font_size=0.6).next_to(eq_final, DOWN, buff=0.5).align_to(eq_final, LEFT)
        abc_id[0].set_color(COLOR_A)
        abc_id[2].set_color(COLOR_B)
        abc_id[4].set_color(COLOR_C)
        self.play(Write(abc_id))
        self.wait(1)

        # Quadratic formula reminder
        quadratic_formula_small = MathTex(
            "t = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}",
            font_size=0.6, color=COLOR_FORMULA
        ).next_to(abc_id, DOWN, buff=0.5).align_to(abc_id, LEFT)
        self.play(Write(quadratic_formula_small))
        self.wait(1)

        # Substitute and solve
        sub_proj = MathTex(
            "t = \\frac{-(20) \\pm \\sqrt{(20)^2 - 4(-4.9)(1.5)}}{2(-4.9)}",
            font_size=0.55
        ).next_to(quadratic_formula_small, DOWN, buff=0.5).align_to(quadratic_formula_small, LEFT)
        self.play(TransformFromCopy(VGroup(abc_id, quadratic_formula_small), sub_proj))
        self.wait(2)

        disc_calc_1 = MathTex("\\Delta = 400 - (-29.4) = 429.4", font_size=0.55).next_to(sub_proj, DOWN, buff=0.3).align_to(sub_proj, LEFT)
        self.play(Write(disc_calc_1))
        self.wait(1.5)

        sol_proj_1 = MathTex("t = \\frac{-20 \\pm \\sqrt{429.4}}{-9.8}", font_size=0.55).next_to(disc_calc_1, DOWN, buff=0.3).align_to(disc_calc_1, LEFT)
        self.play(TransformMatchingTex(VGroup(sub_proj, disc_calc_1), sol_proj_1))
        self.wait(1)

        sol_proj_2 = MathTex("t \\approx \\frac{-20 \\pm 20.72}{-9.8}", font_size=0.55).next_to(sol_proj_1, DOWN, buff=0.3).align_to(sol_proj_1, LEFT)
        self.play(TransformMatchingTex(sol_proj_1, sol_proj_2))
        self.wait(1)

        t1 = MathTex("t_1 \\approx \\frac{0.72}{-9.8} \\approx -0.07 \\text{ s (ignore)}", font_size=0.5).next_to(sol_proj_2, DOWN, buff=0.5).align_to(sol_proj_2, LEFT).set_color(RED)
        t2 = MathTex("t_2 \\approx \\frac{-40.72}{-9.8} \\approx 4.16 \\text{ s}", font_size=0.5).next_to(t1, DOWN, buff=0.3).align_to(t1, LEFT).set_color(GREEN)

        self.play(Write(t1))
        self.play(Write(t2))
        self.wait(2)

        conclusion_proj = Text("Conclusion: The ball hits the ground at approx. 4.16 seconds.", font_size=0.45, color=TEAL).next_to(t2, DOWN, buff=0.7).align_to(t2, LEFT)
        self.play(Write(conclusion_proj))
        self.wait(3)
        self.play(FadeOut(VGroup(problem_text_1, problem_text_2, problem_text_3, eq_formulation_header, eq_final,
                                abc_id, quadratic_formula_small, sol_proj_2, t1, t2, conclusion_proj)))

    def optimization_application(self):
        """Shows how quadratic equations are used for optimization problems, like maximizing area."""
        heading = Text("Section 5: Real-World Application:", font_size=HEADING_SIZE, color=COLOR_HIGHLIGHT).to_edge(UP)
        sub_heading = Text("Optimization & Area", font_size=SUBHEADING_SIZE).next_to(heading, DOWN)
        self.play(Write(heading), Write(sub_heading))
        self.wait(1)

        # Rectangular garden diagram
        garden = Rectangle(width=6, height=3, color=GREEN, fill_opacity=0.2, stroke_width=4).center().shift(DOWN*0.5)
        L_label = MathTex("L", font_size=0.6).next_to(garden.get_top(), UP)
        W_label = MathTex("W", font_size=0.6).next_to(garden.get_right(), RIGHT)

        self.play(Create(garden), Write(L_label), Write(W_label))
        self.wait(1)

        perimeter_formula = MathTex("P = 2L + 2W", font_size=0.6).to_edge(LEFT).shift(UP*1)
        area_formula = MathTex("A = L \\times W", font_size=0.6).next_to(perimeter_formula, DOWN, buff=0.3).align_to(perimeter_formula, LEFT)

        self.play(Write(perimeter_formula), Write(area_formula))
        self.wait(1.5)

        self.play(VGroup(heading, sub_heading).animate.to_corner(UL).shift(DOWN*0.5))
        self.play(VGroup(garden, L_label, W_label).animate.to_corner(DR).scale(0.7))
        self.play(VGroup(perimeter_formula, area_formula).animate.to_corner(UR).scale(0.7))

        # Problem: 100 feet of fencing, max area
        problem_opt_1 = Text("Problem: 100 feet of fencing for a rectangular garden.", font_size=0.45).to_edge(LEFT).shift(UP*1.5)
        problem_opt_2 = Text("What dimensions give the maximum area?", font_size=0.45, color=COLOR_HIGHLIGHT).next_to(problem_opt_1, DOWN)
        self.play(Write(VGroup(problem_opt_1, problem_opt_2)))
        self.wait(1)

        # Formulate Area in terms of one variable
        perimeter_given = MathTex("P = 100 \\implies 2L + 2W = 100", font_size=0.6).next_to(problem_opt_2, DOWN, buff=0.5).align_to(problem_opt_2, LEFT)
        simplify_P = MathTex("L + W = 50 \\implies L = 50 - W", font_size=0.6).next_to(perimeter_given, DOWN, buff=0.3).align_to(perimeter_given, LEFT)
        self.play(Write(perimeter_given))
        self.play(Write(simplify_P))
        self.wait(1.5)

        area_sub = MathTex("A = (50 - W)W", font_size=0.6).next_to(simplify_P, DOWN, buff=0.5).align_to(simplify_P, LEFT)
        area_quadratic = MathTex("A = -W^2 + 50W", font_size=0.8).next_to(area_sub, DOWN, buff=0.3).align_to(area_sub, LEFT).set_color(COLOR_FORMULA)
        self.play(Write(area_sub))
        self.play(TransformMatchingTex(area_sub.copy(), area_quadratic))
        self.wait(1.5)

        # Find vertex for max area
        vertex_text = Text("To find maximum area, find the vertex of the parabola:", font_size=0.4, color=BLUE).next_to(area_quadratic, DOWN, buff=0.5).align_to(area_quadratic, LEFT)
        vertex_formula = MathTex("W = \\frac{-b}{2a}", font_size=0.6, color=TEAL).next_to(vertex_text, DOWN, buff=0.3).align_to(vertex_text, LEFT)
        self.play(Write(vertex_text))
        self.play(Write(vertex_formula))
        self.wait(1.5)

        # Identify a, b from A = -W^2 + 50W
        a_b_ident = MathTex("a = -1", ", ", "b = 50", font_size=0.5).next_to(vertex_formula, DOWN, buff=0.5).align_to(vertex_formula, LEFT)
        a_b_ident[0].set_color(COLOR_A)
        a_b_ident[2].set_color(COLOR_B)
        self.play(Write(a_b_ident))
        self.wait(0.5)

        calc_W = MathTex("W = \\frac{-50}{2(-1)} = 25 \\text{ feet}", font_size=0.6).next_to(a_b_ident, DOWN, buff=0.3).align_to(a_b_ident, LEFT).set_color(COLOR_SOLUTION)
        calc_L = MathTex("L = 50 - W = 50 - 25 = 25 \\text{ feet}", font_size=0.6).next_to(calc_W, DOWN, buff=0.3).align_to(calc_W, LEFT).set_color(COLOR_SOLUTION)

        self.play(Write(calc_W))
        self.play(Write(calc_L))
        self.wait(1.5)

        max_area_text = Text("Maximum Area: 25 x 25 = 625 sq ft", font_size=0.5, color=GREEN).next_to(calc_L, DOWN, buff=0.7).align_to(calc_L, LEFT)
        self.play(Write(max_area_text))
        self.wait(3)
        self.play(FadeOut(VGroup(heading, sub_heading, garden, L_label, W_label, perimeter_formula, area_formula,
                                problem_opt_1, problem_opt_2, perimeter_given, simplify_P, area_sub, area_quadratic,
                                vertex_text, vertex_formula, a_b_ident, calc_W, calc_L, max_area_text)))

    def the_discriminant(self):
        """Explains the discriminant and its implications for the nature of roots, with visual examples."""
        heading = Text("Section 6: The Discriminant", font_size=HEADING_SIZE, color=COLOR_HIGHLIGHT).to_edge(UP)
        self.play(Write(heading))
        self.wait(1)

        disc_def_text = Text("The term under the square root in the quadratic formula:", font_size=0.45).next_to(heading, DOWN, buff=0.5)
        disc_formula = MathTex("\\Delta = b^2 - 4ac", font_size=EQUATION_SIZE, color=COLOR_DISCRIMINANT).next_to(disc_def_text, DOWN, buff=0.3)
        self.play(Write(disc_def_text))
        self.play(Write(disc_formula))
        self.wait(1.5)

        tells_us_text = Text("Its value tells us about the nature of the solutions:", font_size=0.45, color=BLUE).next_to(disc_formula, DOWN, buff=0.7)
        self.play(Write(tells_us_text))
        self.wait(1.5)

        self.play(FadeOut(disc_def_text), heading.animate.to_corner(UL).shift(DOWN*0.5),
                  disc_formula.animate.to_corner(UL).shift(DOWN*1.5 + RIGHT*2))
        self.play(tells_us_text.animate.to_corner(UL).shift(DOWN*2.5 + RIGHT*0.5))

        # Case 1: Delta > 0 (Two distinct real roots)
        case1_text = MathTex("\\Delta > 0 \\implies", "\\text{Two distinct real roots}", color=GREEN).next_to(tells_us_text, DOWN, buff=0.7).align_to(tells_us_text, LEFT)
        case1_text[1].set_color(GREEN)
        self.play(Write(case1_text))
        self.wait(1)

        axes1 = Axes(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1],
            x_length=4, y_length=4, axis_config={"color": GREY}, tips=False
        ).to_corner(DR).shift(LEFT*1.5 + UP*1)
        parabola1 = axes1.get_graph(lambda x: x**2 - 2, color=PURPLE)
        root1_1 = Dot(axes1.c2p(-np.sqrt(2), 0), color=GREEN, radius=0.08)
        root1_2 = Dot(axes1.c2p(np.sqrt(2), 0), color=GREEN, radius=0.08)
        self.play(Create(axes1))
        self.play(Create(parabola1), FadeIn(root1_1, root1_2))
        self.play(Circumscribe(VGroup(root1_1, root1_2)))
        self.wait(2)

        # Case 2: Delta = 0 (One real root)
        case2_text = MathTex("\\Delta = 0 \\implies", "\\text{One real root (repeated)}", color=YELLOW).next_to(case1_text, DOWN, buff=0.7).align_to(case1_text, LEFT)
        case2_text[1].set_color(YELLOW)
        self.play(Write(case2_text))
        self.wait(1)

        axes2 = Axes(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1],
            x_length=4, y_length=4, axis_config={"color": GREY}, tips=False
        ).next_to(axes1, DOWN, buff=0.5).align_to(axes1, LEFT)
        parabola2 = axes2.get_graph(lambda x: x**2, color=PURPLE)
        root2_1 = Dot(axes2.c2p(0, 0), color=YELLOW, radius=0.08)
        self.play(Create(axes2))
        self.play(Create(parabola2), FadeIn(root2_1))
        self.play(Circumscribe(root2_1))
        self.wait(2)

        # Case 3: Delta < 0 (Two distinct complex conjugate roots)
        case3_text = MathTex("\\Delta < 0 \\implies", "\\text{Two distinct complex conjugate roots}", color=RED).next_to(case2_text, DOWN, buff=0.7).align_to(case2_text, LEFT)
        case3_text[1].set_color(RED)
        self.play(Write(case3_text))
        self.wait(1)

        axes3 = Axes(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1],
            x_length=4, y_length=4, axis_config={"color": GREY}, tips=False
        ).next_to(axes2, DOWN, buff=0.5).align_to(axes2, LEFT)
        parabola3 = axes3.get_graph(lambda x: x**2 + 2, color=PURPLE)
        no_roots_text = Text("No real x-intercepts", font_size=0.3, color=RED).next_to(parabola3, UP)
        self.play(Create(axes3))
        self.play(Create(parabola3), Write(no_roots_text))
        self.wait(3)
        self.play(FadeOut(VGroup(heading, disc_formula, tells_us_text, case1_text, axes1, parabola1, root1_1, root1_2,
                                case2_text, axes2, parabola2, root2_1,
                                case3_text, axes3, parabola3, no_roots_text)))

    def common_misunderstandings(self):
        """Highlights common errors and pitfalls when using the quadratic equation."""
        heading = Text("Common Misunderstandings & Pitfalls", font_size=HEADING_SIZE, color=COLOR_HIGHLIGHT).to_edge(UP)
        self.play(Write(heading))
        self.wait(1)

        # Misconception 1: Forgetting +/-
        miscon1_head = Text("1. Forgetting the '±' sign", font_size=SUBHEADING_SIZE, color=RED).next_to(heading, DOWN, buff=0.7).to_edge(LEFT)
        miscon1_corr = Text("Always yields two potential answers.", font_size=0.4).next_to(miscon1_head, RIGHT, buff=0.5)
        self.play(Write(miscon1_head))
        self.play(Write(miscon1_corr))
        self.wait(1.5)

        # Misconception 2: Incorrectly identifying a, b, or c
        miscon2_head = Text("2. Incorrectly identifying a, b, or c", font_size=SUBHEADING_SIZE, color=RED).next_to(miscon1_head, DOWN, buff=0.7).align_to(miscon1_head, LEFT)
        miscon2_corr_1 = Text("Rearrange to ax² + bx + c = 0 FIRST.", font_size=0.4).next_to(miscon2_head, RIGHT, buff=0.5)
        example_eq_bad = MathTex("3x^2 = 5x - 2", font_size=0.4).next_to(miscon2_corr_1, DOWN, buff=0.3).align_to(miscon2_corr_1, LEFT)
        example_eq_good = MathTex("3x^2 - 5x + 2 = 0", font_size=0.4).next_to(example_eq_bad, RIGHT)
        self.play(Write(miscon2_head))
        self.play(Write(miscon2_corr_1))
        self.play(Write(example_eq_bad))
        self.play(TransformMatchingTex(example_eq_bad.copy(), example_eq_good))
        self.wait(2)

        # Pitfall 1: Sign errors
        pitfall1_head = Text("3. Sign errors (e.g., (-b)² vs -b²)", font_size=SUBHEADING_SIZE, color=RED).next_to(miscon2_head, DOWN, buff=1.0).align_to(miscon2_head, LEFT)
        pitfall1_corr = Text("Be meticulous with parentheses and negative numbers.", font_size=0.4).next_to(pitfall1_head, RIGHT, buff=0.5)
        self.play(Write(pitfall1_head))
        self.play(Write(pitfall1_corr))
        self.wait(1.5)

        # Pitfall 2: Division by zero (a=0)
        pitfall2_head = Text("4. Division by zero (a ≠ 0 condition)", font_size=SUBHEADING_SIZE, color=RED).next_to(pitfall1_head, DOWN, buff=0.7).align_to(pitfall1_head, LEFT)
        pitfall2_corr = Text("If a=0, it's a linear equation, not quadratic.", font_size=0.4).next_to(pitfall2_head, RIGHT, buff=0.5)
        self.play(Write(pitfall2_head))
        self.play(Write(pitfall2_corr))
        self.wait(1.5)

        # Pitfall 3: Interpreting roots
        pitfall3_head = Text("5. Interpreting roots (real-world context)", font_size=SUBHEADING_SIZE, color=RED).next_to(pitfall2_head, DOWN, buff=0.7).align_to(pitfall2_head, LEFT)
        pitfall3_corr = Text("Some mathematical roots might be physically meaningless (e.g., negative time).", font_size=0.4).next_to(pitfall3_head, RIGHT, buff=0.5)
        self.play(Write(pitfall3_head))
        self.play(Write(pitfall3_corr))
        self.wait(2.5)
        self.play(FadeOut(VGroup(heading, miscon1_head, miscon1_corr, miscon2_head, miscon2_corr_1, example_eq_bad, example_eq_good,
                                pitfall1_head, pitfall1_corr, pitfall2_head, pitfall2_corr, pitfall3_head, pitfall3_corr)))

    def recap_and_conclusion(self):
        """Summarizes the key concepts and provides a call to action."""
        # Recap / Summary
        recap_heading = Text("Recap & Summary", font_size=HEADING_SIZE, color=COLOR_HIGHLIGHT).to_edge(UP)
        self.play(Write(recap_heading))
        self.wait(1)

        recap_eq = MathTex("ax^2 + bx + c = 0", font_size=EQUATION_SIZE).next_to(recap_heading, DOWN, buff=0.5)
        recap_formula = MathTex("x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}", font_size=EQUATION_SIZE+0.1, color=COLOR_FORMULA).next_to(recap_eq, DOWN, buff=0.7)
        self.play(Write(recap_eq))
        self.play(Write(recap_formula))
        self.wait(1.5)

        recap_text1 = Text("Powerful tools for solving unknowns with squared variables.", font_size=0.45).next_to(recap_formula, DOWN, buff=1.0)
        recap_text2 = Text("Models parabolic curves, calculates trajectories, optimizes areas.", font_size=0.45).next_to(recap_text1, DOWN, buff=0.3)
        self.play(Write(recap_text1))
        self.play(Write(recap_text2))
        self.wait(3)
        self.play(FadeOut(VGroup(recap_heading, recap_eq, recap_formula, recap_text1, recap_text2)))

        # Closing / Call to Action
        closing_heading = Text("Keep Exploring!", font_size=HEADING_SIZE, color=GREEN).to_edge(UP)
        self.play(Write(closing_heading))
        self.wait(1)

        closing_text_1 = Text("Remember the quadratic equation next time you see a parabola!", font_size=0.45).next_to(closing_heading, DOWN, buff=0.7)
        closing_text_2 = Text("It's working behind the scenes, helping us understand and shape our world.", font_size=0.45).next_to(closing_text_1, DOWN, buff=0.3)
        closing_text_3 = Text("This fundamental concept lays the groundwork for more advanced math and science.", font_size=0.45).next_to(closing_text_2, DOWN, buff=0.3)

        self.play(FadeIn(closing_text_1, shift=UP))
        self.play(Write(closing_text_2))
        self.play(Write(closing_text_3))
        self.wait(3)
        self.play(FadeOut(VGroup(closing_heading, closing_text_1, closing_text_2, closing_text_3)))