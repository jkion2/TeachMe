from manim import *

# Constants for consistent styling
DEFAULT_FONT_SIZE = 0.7
TITLE_COLOR = BLUE_A
EQUATION_COLOR = BLUE
HIGHLIGHT_COLOR = YELLOW
AXES_COLOR = WHITE
GRAPH_COLOR = GREEN
VERTEX_COLOR = RED
FOCAL_POINT_COLOR = ORANGE
GRID_COLOR = GREY_BROWN

class SolutionAnimation(Scene):
    def construct(self):
        self.introduce_quadratics()
        self.section_parabola()
        self.section_projectile_motion()
        self.section_optimization()
        self.section_engineering_design()
        self.common_misunderstandings()
        self.recap_summary()
        self.closing_call_to_action()

    def introduce_quadratics(self):
        # Video Title and Hook
        title = Text("Why Quadratics Rule the World", font_size=DEFAULT_FONT_SIZE * 1.2).to_edge(UP)
        hook_text = Text(
            "The math behind everyday marvels: quadratic equations.",
            font_size=DEFAULT_FONT_SIZE * 0.8,
            color=HIGHLIGHT_COLOR
        ).next_to(title, DOWN)
        
        self.play(Write(title), FadeIn(hook_text, shift=DOWN))
        self.wait(1.5)
        self.play(FadeOut(title, shift=UP), FadeOut(hook_text, shift=UP))
        self.wait(0.5)

        # Introduction (Context + Why It Matters)
        intro_narration = Text(
            "A quadratic equation is a polynomial of degree two.",
            font_size=DEFAULT_FONT_SIZE * 0.7
        ).to_edge(UP)

        quadratic_eq = MathTex(r"ax^2 + bx + c = 0", r", \text{ where } a \neq 0", font_size=DEFAULT_FONT_SIZE).move_to(ORIGIN)
        quadratic_eq[0].set_color(EQUATION_COLOR)

        self.play(FadeIn(intro_narration, shift=UP))
        self.play(Write(quadratic_eq[0]))
        self.play(Write(quadratic_eq[1]))
        self.wait(1.5)

        quadratic_formula = MathTex(
            r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}",
            font_size=DEFAULT_FONT_SIZE
        ).next_to(quadratic_eq, DOWN, buff=0.7).set_color(HIGHLIGHT_COLOR)

        self.play(Write(quadratic_formula))
        self.wait(2)

        why_it_matters = Text(
            "Their real power lies in describing a fundamental shape: the parabola.",
            font_size=DEFAULT_FONT_SIZE * 0.6
        ).next_to(quadratic_formula, DOWN, buff=0.5).set_color(GREEN)

        self.play(FadeIn(why_it_matters, shift=UP))
        self.wait(2)

        self.play(FadeOut(intro_narration, shift=UP),
                  FadeOut(quadratic_eq),
                  FadeOut(quadratic_formula),
                  FadeOut(why_it_matters, shift=DOWN))
        self.wait(1)

    def section_parabola(self):
        section_title = Text("1. The Parabola - Nature's Favorite Curve", font_size=DEFAULT_FONT_SIZE * 0.9, color=TITLE_COLOR).to_edge(UP)
        self.play(Write(section_title))
        self.wait(0.5)

        eq_y_form = MathTex(r"y = ax^2 + bx + c", font_size=DEFAULT_FONT_SIZE).move_to(UP*1.5).set_color(EQUATION_COLOR)
        self.play(Write(eq_y_form))
        self.wait(1)

        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 5, 1],
            x_length=6,
            y_length=5,
            axis_config={"color": AXES_COLOR},
        ).to_edge(DOWN)
        labels = axes.get_axis_labels(x_label="x", y_label="y")

        parabola = axes.plot(lambda x: x**2, color=GRAPH_COLOR)
        vertex_dot = Dot(axes.c2p(0, 0), color=VERTEX_COLOR)
        vertex_label = MathTex(r"\text{Vertex: } (0,0)", font_size=DEFAULT_FONT_SIZE * 0.5).next_to(vertex_dot, DR, buff=0.1)
        
        self.play(Create(axes), Create(labels), Create(parabola))
        self.play(FadeIn(vertex_dot), Write(vertex_label))
        self.wait(1)

        axis_of_symmetry = DashedLine(axes.c2p(0, -2), axes.c2p(0, 5), color=HIGHLIGHT_COLOR)
        symmetry_label = Text("Axis of Symmetry", font_size=DEFAULT_FONT_SIZE * 0.4, color=HIGHLIGHT_COLOR).next_to(axis_of_symmetry, UL, buff=0.1)
        self.play(Create(axis_of_symmetry), Write(symmetry_label))
        self.wait(1.5)

        # Animate changing 'a'
        a_text = MathTex(r"a", font_size=DEFAULT_FONT_SIZE * 0.6).next_to(eq_y_form, RIGHT, buff=0.5)
        self.play(Circumscribe(eq_y_form[2], color=HIGHLIGHT_COLOR), Write(Text("Changing 'a'", font_size=DEFAULT_FONT_SIZE * 0.5).to_corner(UL)))
        self.wait(0.5)

        parabola_a_group = VGroup(parabola, vertex_dot, vertex_label)
        self.play(parabola_a_group.animate.become(axes.plot(lambda x: 2*x**2, color=GRAPH_COLOR)),
                  Transform(vertex_label, MathTex(r"\text{Vertex: } (0,0)", font_size=DEFAULT_FONT_SIZE * 0.5).next_to(vertex_dot, DR, buff=0.1)))
        self.wait(0.7)
        self.play(parabola_a_group.animate.become(axes.plot(lambda x: 0.5*x**2, color=GRAPH_COLOR)),
                  Transform(vertex_label, MathTex(r"\text{Vertex: } (0,0)", font_size=DEFAULT_FONT_SIZE * 0.5).next_to(vertex_dot, DR, buff=0.1)))
        self.wait(0.7)
        self.play(parabola_a_group.animate.become(axes.plot(lambda x: -x**2, color=GRAPH_COLOR)),
                  Transform(vertex_label, MathTex(r"\text{Vertex: } (0,0)", font_size=DEFAULT_FONT_SIZE * 0.5).next_to(vertex_dot, DR, buff=0.1)))
        self.wait(1)
        self.play(parabola_a_group.animate.become(axes.plot(lambda x: x**2, color=GRAPH_COLOR)),
                  Transform(vertex_label, MathTex(r"\text{Vertex: } (0,0)", font_size=DEFAULT_FONT_SIZE * 0.5).next_to(vertex_dot, DR, buff=0.1)))
        self.wait(0.7)
        
        # Animate changing 'c'
        self.play(Circumscribe(eq_y_form[6], color=HIGHLIGHT_COLOR), Write(Text("Changing 'c'", font_size=DEFAULT_FONT_SIZE * 0.5).to_corner(UL)))
        parabola_c_group = VGroup(parabola, vertex_dot, vertex_label)
        self.play(parabola_c_group.animate.become(axes.plot(lambda x: x**2 + 2, color=GRAPH_COLOR)),
                  Transform(vertex_dot, Dot(axes.c2p(0, 2), color=VERTEX_COLOR)),
                  Transform(vertex_label, MathTex(r"\text{Vertex: } (0,2)", font_size=DEFAULT_FONT_SIZE * 0.5).next_to(axes.c2p(0,2), DR, buff=0.1)))
        self.wait(0.7)
        self.play(parabola_c_group.animate.become(axes.plot(lambda x: x**2 - 2, color=GRAPH_COLOR)),
                  Transform(vertex_dot, Dot(axes.c2p(0, -2), color=VERTEX_COLOR)),
                  Transform(vertex_label, MathTex(r"\text{Vertex: } (0,-2)", font_size=DEFAULT_FONT_SIZE * 0.5).next_to(axes.c2p(0,-2), DR, buff=0.1)))
        self.wait(1)
        self.play(parabola_c_group.animate.become(axes.plot(lambda x: x**2, color=GRAPH_COLOR)),
                  Transform(vertex_dot, Dot(axes.c2p(0, 0), color=VERTEX_COLOR)),
                  Transform(vertex_label, MathTex(r"\text{Vertex: } (0,0)", font_size=DEFAULT_FONT_SIZE * 0.5).next_to(axes.c2p(0,0), DR, buff=0.1)))
        self.wait(0.7)
        
        # Discriminant
        discriminant_eq = MathTex(r"D = b^2 - 4ac", font_size=DEFAULT_FONT_SIZE * 0.7).next_to(eq_y_form, DOWN, buff=0.5).set_color(HIGHLIGHT_COLOR)
        discriminant_cases = VGroup(
            MathTex(r"D > 0 \implies \text{2 distinct real roots}", font_size=DEFAULT_FONT_SIZE * 0.5),
            MathTex(r"D = 0 \implies \text{1 repeated real root}", font_size=DEFAULT_FONT_SIZE * 0.5),
            MathTex(r"D < 0 \implies \text{2 complex conjugate roots}", font_size=DEFAULT_FONT_SIZE * 0.5)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(discriminant_eq, DOWN, buff=0.3)
        discriminant_cases.set_color_by_tex("real roots", GREEN)
        discriminant_cases.set_color_by_tex("complex", RED)

        self.play(Write(discriminant_eq))
        self.wait(1)
        self.play(FadeIn(discriminant_cases, shift=DOWN))
        self.wait(2)

        self.play(FadeOut(VGroup(section_title, eq_y_form, axes, labels, parabola_a_group, axis_of_symmetry, symmetry_label, 
                                 Text("Changing 'a'", font_size=DEFAULT_FONT_SIZE * 0.5).to_corner(UL), Text("Changing 'c'", font_size=DEFAULT_FONT_SIZE * 0.5).to_corner(UL),
                                 discriminant_eq, discriminant_cases)))
        self.wait(0.5)

    def section_projectile_motion(self):
        section_title = Text("2. Projectile Motion - Predicting the Path", font_size=DEFAULT_FONT_SIZE * 0.9, color=TITLE_COLOR).to_edge(UP)
        self.play(Write(section_title))
        self.wait(0.5)

        # Set up axes for projectile motion
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 15, 2.5],
            x_length=9,
            y_length=6,
            axis_config={"color": AXES_COLOR},
            tips=True
        ).to_edge(DL)
        labels = axes.get_axis_labels(x_label="Time (s)", y_label="Height (m)")

        # Projectile motion equation
        physics_eq = MathTex(
            r"h(t) = -\frac{1}{2}gt^2 + v_0 t + h_0",
            font_size=DEFAULT_FONT_SIZE * 0.7
        ).next_to(section_title, DOWN, buff=0.5).to_edge(RIGHT)
        
        self.play(Create(axes), Create(labels), Write(physics_eq))
        self.wait(1.5)

        # Draw a simple projectile trajectory
        projectile_path = axes.plot(lambda t: -4.9*t**2 + 20*t + 5, x_range=[0, 4.318], color=GRAPH_COLOR)
        initial_point = Dot(axes.c2p(0, 5), color=RED)
        max_height_point = Dot(axes.c2p(20/9.8, -4.9*(20/9.8)**2 + 20*(20/9.8) + 5), color=YELLOW)
        end_point = Dot(axes.c2p(4.318, 0), color=RED)
        
        self.play(Create(projectile_path), FadeIn(initial_point), FadeIn(max_height_point), FadeIn(end_point))
        self.play(Circumscribe(projectile_path, color=HIGHLIGHT_COLOR))
        self.wait(1)

        # Worked Example: Set up specific values
        example_title = Text("Worked Example: Projectile Launch", font_size=DEFAULT_FONT_SIZE * 0.6, color=HIGHLIGHT_COLOR).next_to(physics_eq, DOWN, buff=0.5)
        self.play(Write(example_title))

        given_values = VGroup(
            MathTex(r"v_0 = 20 \text{ m/s}", font_size=DEFAULT_FONT_SIZE * 0.5),
            MathTex(r"h_0 = 5 \text{ m}", font_size=DEFAULT_FONT_SIZE * 0.5),
            MathTex(r"g = 9.8 \text{ m/s}^2", font_size=DEFAULT_FONT_SIZE * 0.5)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(example_title, DOWN, buff=0.3)
        self.play(FadeIn(given_values, shift=DOWN))
        self.wait(1)

        # Substitute into equation
        substituted_eq1 = MathTex(r"h(t) = -\frac{1}{2}(9.8)t^2 + 20t + 5", font_size=DEFAULT_FONT_SIZE * 0.6).next_to(given_values, DOWN, buff=0.5)
        substituted_eq2 = MathTex(r"h(t) = -4.9t^2 + 20t + 5", font_size=DEFAULT_FONT_SIZE * 0.6).next_to(substituted_eq1, DOWN, buff=0.2)
        
        self.play(TransformMatchingTex(physics_eq.copy(), substituted_eq1))
        self.wait(0.5)
        self.play(TransformMatchingTex(substituted_eq1, substituted_eq2))
        self.wait(1)

        # Find time to impact (h(t)=0)
        set_to_zero = MathTex(r"-4.9t^2 + 20t + 5 = 0", font_size=DEFAULT_FONT_SIZE * 0.6).next_to(substituted_eq2, DOWN, buff=0.5).set_color(EQUATION_COLOR)
        self.play(Write(Text("To find time to impact (h(t)=0):", font_size=DEFAULT_FONT_SIZE * 0.4).next_to(substituted_eq2, DOWN, buff=0.2)))
        self.play(Write(set_to_zero))
        self.wait(1)

        quadratic_formula_mini = MathTex(r"t = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}", font_size=DEFAULT_FONT_SIZE * 0.5).next_to(set_to_zero, DOWN, buff=0.3).set_color(HIGHLIGHT_COLOR)
        self.play(Write(quadratic_formula_mini))
        self.wait(1)

        # Step-by-step solution
        solve_step1 = MathTex(r"t = \frac{-20 \pm \sqrt{20^2 - 4(-4.9)(5)}}{2(-4.9)}", font_size=DEFAULT_FONT_SIZE * 0.5).next_to(quadratic_formula_mini, DOWN, buff=0.3)
        solve_step2 = MathTex(r"t = \frac{-20 \pm \sqrt{400 + 98}}{-9.8}", font_size=DEFAULT_FONT_SIZE * 0.5).next_to(solve_step1, DOWN, buff=0.2)
        solve_step3 = MathTex(r"t = \frac{-20 \pm \sqrt{498}}{-9.8}", font_size=DEFAULT_FONT_SIZE * 0.5).next_to(solve_step2, DOWN, buff=0.2)
        solve_step4 = MathTex(r"t \approx \frac{-20 \pm 22.3159}{-9.8}", font_size=DEFAULT_FONT_SIZE * 0.5).next_to(solve_step3, DOWN, buff=0.2)
        
        self.play(Write(solve_step1))
        self.play(Write(solve_step2))
        self.play(Write(solve_step3))
        self.play(Write(solve_step4))
        self.wait(1)

        solution_t1 = MathTex(r"t_1 \approx -0.236 \text{ s}", font_size=DEFAULT_FONT_SIZE * 0.5).next_to(solve_step4, DOWN, buff=0.3, aligned_edge=LEFT).set_color(RED)
        solution_t2 = MathTex(r"t_2 \approx 4.318 \text{ s}", font_size=DEFAULT_FONT_SIZE * 0.5).next_to(solution_t1, RIGHT, buff=0.5).set_color(GREEN)
        self.play(FadeIn(solution_t1, shift=LEFT), FadeIn(solution_t2, shift=RIGHT))
        self.play(Circumscribe(solution_t2, color=GREEN))
        self.wait(1.5)

        conclusion_text = Text(
            "Projectile hits the ground in approx. 4.318 seconds.",
            font_size=DEFAULT_FONT_SIZE * 0.5,
            color=GREEN
        ).next_to(solution_t1, DOWN, buff=0.5)
        self.play(FadeIn(conclusion_text, shift=UP))
        self.wait(2)

        self.play(FadeOut(VGroup(*self.mobjects)))
        self.wait(0.5)

    def section_optimization(self):
        section_title = Text("3. Optimization Problems - Finding the Best Outcome", font_size=DEFAULT_FONT_SIZE * 0.9, color=TITLE_COLOR).to_edge(UP)
        self.play(Write(section_title))
        self.wait(0.5)

        # Graph of a parabola showing max/min
        axes = Axes(
            x_range=[0, 60, 10],
            y_range=[0, 1500, 250],
            x_length=7,
            y_length=6,
            axis_config={"color": AXES_COLOR},
            tips=True
        ).to_edge(DR)
        labels = axes.get_axis_labels(x_label="x", y_label="Area (A)")

        optimization_parabola = axes.plot(lambda x: -2*x**2 + 100*x, x_range=[0, 50], color=GRAPH_COLOR)
        
        vertex_x = 100/(2*2) # -b/(2a) = -100/(2*-2) = 25
        vertex_y = -2*(vertex_x**2) + 100*vertex_x # -2(25^2) + 100(25) = -1250 + 2500 = 1250
        
        vertex_opt_dot = Dot(axes.c2p(vertex_x, vertex_y), color=VERTEX_COLOR)
        vertex_opt_label = Text("Maximum", font_size=DEFAULT_FONT_SIZE * 0.5, color=HIGHLIGHT_COLOR).next_to(vertex_opt_dot, UL)
        
        self.play(Create(axes), Create(labels), Create(optimization_parabola), FadeIn(vertex_opt_dot), FadeIn(vertex_opt_label, shift=UP))
        self.wait(1.5)

        vertex_formula_text = MathTex(r"\text{Vertex } x\text{-coordinate: } x = -\frac{b}{2a}", font_size=DEFAULT_FONT_SIZE * 0.7).to_edge(UL).set_color(EQUATION_COLOR)
        self.play(Write(vertex_formula_text))
        self.wait(1)

        # Worked Example: Fencing Problem
        example_title = Text("Worked Example: Maximizing Fenced Area", font_size=DEFAULT_FONT_SIZE * 0.6, color=HIGHLIGHT_COLOR).next_to(vertex_formula_text, DOWN, buff=0.5, aligned_edge=LEFT)
        self.play(Write(example_title))

        problem_description = Text(
            "Farmer has 100m fencing for a field next to a barn.",
            font_size=DEFAULT_FONT_SIZE * 0.45
        ).next_to(example_title, DOWN, buff=0.3, aligned_edge=LEFT)
        self.play(FadeIn(problem_description, shift=DOWN))
        self.wait(1)

        # Diagram of field
        barn = Rectangle(width=3, height=0.5, color=BROWN, fill_opacity=0.8).next_to(axes.c2p(0, 0), UL, buff=1)
        barn.shift(LEFT*2.5 + UP*1.5)
        field_rect = Rectangle(width=5, height=2.5, color=GREEN_B, fill_opacity=0.5).next_to(barn, RIGHT, buff=0)
        field_rect.move_to(axes.c2p(25, 625)) # Approximate center for visualization
        field_rect.stretch_to_fit_width(axes.x_axis.get_unit_size() * 50)
        field_rect.stretch_to_fit_height(axes.y_axis.get_unit_size() * 25)
        field_rect.set_color(GREEN)

        x_label_field = MathTex("x", font_size=DEFAULT_FONT_SIZE * 0.5).next_to(field_rect, LEFT)
        y_label_field = MathTex("y", font_size=DEFAULT_FONT_SIZE * 0.5).next_to(field_rect, UP)
        
        # self.add(barn, field_rect, x_label_field, y_label_field) # Add temporarily for position
        # self.play(ShowPassingFlash(barn.copy().set_color(RED), run_time=1), ShowPassingFlash(field_rect.copy().set_color(RED), run_time=1))
        # self.wait()


        equations_fencing = VGroup(
            MathTex(r"\text{Perimeter: } 2x + y = 100", font_size=DEFAULT_FONT_SIZE * 0.5),
            MathTex(r"\text{Area: } A = xy", font_size=DEFAULT_FONT_SIZE * 0.5)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(problem_description, DOWN, buff=0.3)
        self.play(Write(equations_fencing))
        self.wait(1)

        derive_A1 = MathTex(r"y = 100 - 2x", font_size=DEFAULT_FONT_SIZE * 0.5).next_to(equations_fencing[1], DOWN, buff=0.3, aligned_edge=LEFT)
        derive_A2 = MathTex(r"A(x) = x(100 - 2x)", font_size=DEFAULT_FONT_SIZE * 0.5).next_to(derive_A1, DOWN, buff=0.2, aligned_edge=LEFT)
        derive_A3 = MathTex(r"A(x) = 100x - 2x^2", font_size=DEFAULT_FONT_SIZE * 0.5).next_to(derive_A2, DOWN, buff=0.2, aligned_edge=LEFT)
        derive_A4 = MathTex(r"A(x) = -2x^2 + 100x", font_size=DEFAULT_FONT_SIZE * 0.5).next_to(derive_A3, DOWN, buff=0.2, aligned_edge=LEFT)
        
        self.play(Write(derive_A1))
        self.play(TransformMatchingTex(derive_A1.copy(), derive_A2))
        self.play(TransformMatchingTex(derive_A2.copy(), derive_A3))
        self.play(TransformMatchingTex(derive_A3.copy(), derive_A4))
        self.wait(1.5)

        # Apply vertex formula
        calc_x = MathTex(r"x = \frac{-100}{2(-2)} = \frac{-100}{-4} = 25", font_size=DEFAULT_FONT_SIZE * 0.6).next_to(derive_A4, DOWN, buff=0.5).set_color(EQUATION_COLOR)
        self.play(Write(Text("Using vertex formula:", font_size=DEFAULT_FONT_SIZE * 0.4).next_to(derive_A4, DOWN, buff=0.2)))
        self.play(Write(calc_x))
        self.wait(1)

        calc_y_A = VGroup(
            MathTex(r"y = 100 - 2(25) = 50 \text{ m}", font_size=DEFAULT_FONT_SIZE * 0.5),
            MathTex(r"\text{Max Area } A = 25 \times 50 = 1250 \text{ m}^2", font_size=DEFAULT_FONT_SIZE * 0.5)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(calc_x, DOWN, buff=0.3)
        
        self.play(Write(calc_y_A[0]))
        self.play(Write(calc_y_A[1]))
        self.wait(2)

        self.play(FadeOut(VGroup(*self.mobjects)))
        self.wait(0.5)

    def section_engineering_design(self):
        section_title = Text("4. Engineering & Design - Shaping Our World", font_size=DEFAULT_FONT_SIZE * 0.9, color=TITLE_COLOR).to_edge(UP)
        self.play(Write(section_title))
        self.wait(0.5)

        # Architectural Arches (Bridge)
        arch_text = Text("Architectural Arches (Bridges)", font_size=DEFAULT_FONT_SIZE * 0.6, color=HIGHLIGHT_COLOR).to_corner(UL)
        bridge_arch = Arc(radius=2, start_angle=PI, angle=PI, color=GREY_B).shift(DOWN*0.5)
        bridge_base = Line(LEFT*2, RIGHT*2, color=GREY_B).shift(DOWN*0.5)
        bridge_posts = VGroup(*[Line(bridge_base.get_point_at_percent(i/6), bridge_arch.get_point_at_percent(i/6), color=GREY_B) for i in range(1, 6)])
        bridge = VGroup(bridge_arch, bridge_base, bridge_posts).center().shift(LEFT*3)

        self.play(Write(arch_text), Create(bridge))
        self.wait(1.5)

        # Satellite Dish (Reflectors)
        reflector_text = Text("Reflectors (Satellite Dishes)", font_size=DEFAULT_FONT_SIZE * 0.6, color=HIGHLIGHT_COLOR).to_corner(UR)
        
        parabolic_reflector = Arc(start_angle=PI*0.75, angle=PI*0.5, radius=3, color=BLUE_B).rotate(PI/2).flip(UP).set_height(4) # A parabolic shape
        parabolic_reflector.shift(RIGHT*3)

        focus_point = Dot(parabolic_reflector.get_center() + LEFT*1.5, color=FOCAL_POINT_COLOR) # Approximate focal point
        
        # Incoming parallel rays
        rays = VGroup(*[
            Line(parabolic_reflector.get_boundary_point(UP) + UP*i*0.5, parabolic_reflector.get_boundary_point(DOWN) + DOWN*i*0.5 + RIGHT*0.5, color=WHITE)
            for i in np.linspace(-1.5, 1.5, 7)
        ])
        rays_in = VGroup()
        for i, ray in enumerate(rays):
            p = parabolic_reflector.get_points_along_curve_closest_to_points([ray.get_end()])[0]
            if p is None: continue # Skip if no intersection
            
            # Create a line segment from outside the parabola to the intersection point
            intersection_point = parabolic_reflector.get_points_from_proportion(
                parabolic_reflector.get_point_mobject_from_proportion(
                    ray.get_projection_along_line(parabolic_reflector.get_start_point(), parabolic_reflector.get_end_point())[0]
                ).get_proportion()
            )[0]
            
            # This is hard to get right dynamically, use simplified parallel lines hitting the curve and reflecting to a point
            # Simpler approach: Draw parallel lines towards the parabola, then draw lines from intersection to focal point.
            
            start_y = np.linspace(parabolic_reflector.get_y(parabolic_reflector.get_x_range()[0] + 0.1), 
                                  parabolic_reflector.get_y(parabolic_reflector.get_x_range()[1] - 0.1), 7)
            
            ray_start_x = parabolic_reflector.get_x(parabolic_reflector.get_y(0.1)) - 3 # arbitrary x far left
            ray_end_x_on_parabola = parabolic_reflector.get_x(start_y[i])
            
            ray_in = Line(RIGHT*ray_start_x + UP*start_y[i], RIGHT*ray_end_x_on_parabola + UP*start_y[i], color=WHITE)
            rays_in.add(ray_in)
            
            # The actual reflection requires tangential calculations, simplifying for visual.
            # Just draw lines to the focal point
        
        self.play(Write(reflector_text), Create(parabolic_reflector), Create(focus_point))
        
        # Simplified incoming rays and reflection to focal point
        incoming_lines = VGroup()
        reflected_lines = VGroup()
        for y_val in np.linspace(-1.5, 1.5, 5):
            x_on_parabola = 0.5 * y_val**2 + parabolic_reflector.get_center()[0] - 1.5 # simple x=ky^2 shifted
            
            incoming_line = Line(parabolic_reflector.get_center() + LEFT*2 + UP*y_val, parabolic_reflector.get_center() + UP*y_val + LEFT*1.5 + RIGHT*0.5 * y_val**2, color=WHITE)
            incoming_lines.add(incoming_line)
            
            point_on_parabola_for_ray = incoming_line.get_end()
            
            reflected_line = Line(point_on_parabola_for_ray, focus_point.get_center(), color=FOCAL_POINT_COLOR)
            reflected_lines.add(reflected_line)
        
        # This is a bit of a hack to simulate a parabola and its focal point for visual explanation.
        # A more accurate parabola for Manim would be axes.plot(lambda y: k*y**2)
        
        parabola_curve_obj = ParametricFunction(
            lambda t: parabolic_reflector.get_center() + np.array([0.5*t**2 - 1.5, t, 0]),
            t_range=[-1.5, 1.5], color=BLUE_B
        )
        self.play(Transform(parabolic_reflector, parabola_curve_obj)) # Replace placeholder Arc with a better parabola
        
        self.play(Create(incoming_lines))
        self.play(LaggedStart(*[Create(line) for line in reflected_lines], lag_ratio=0.2))
        self.wait(2)

        # Resonant Frequency
        resonant_text = Text("Resonant Frequency in Circuits", font_size=DEFAULT_FONT_SIZE * 0.6, color=HIGHLIGHT_COLOR).next_to(bridge, DOWN, buff=1.5, aligned_edge=LEFT)
        resonant_eq = MathTex(r"\omega^2 = \frac{1}{LC}", font_size=DEFAULT_FONT_SIZE * 0.7).next_to(resonant_text, DOWN, buff=0.5, aligned_edge=LEFT).set_color(EQUATION_COLOR)
        
        self.play(Write(resonant_text), Write(resonant_eq))
        self.wait(2)

        self.play(FadeOut(VGroup(*self.mobjects)))
        self.wait(0.5)

    def common_misunderstandings(self):
        section_title = Text("Common Misunderstandings", font_size=DEFAULT_FONT_SIZE * 0.9, color=TITLE_COLOR).to_edge(UP)
        self.play(Write(section_title))
        self.wait(0.5)

        misconception1 = Text(
            "1. Quadratics are only about 'solutions' (roots).",
            font_size=DEFAULT_FONT_SIZE * 0.6, color=RED
        ).to_edge(UL).shift(DOWN*0.5)
        
        clarification1 = Text(
            "The *entire curve* shows continuous behavior (e.g., height over time).",
            font_size=DEFAULT_FONT_SIZE * 0.5, color=GREEN
        ).next_to(misconception1, DOWN, aligned_edge=LEFT)

        self.play(Write(misconception1))
        self.wait(1)
        self.play(Write(clarification1))
        self.wait(1.5)

        misconception2 = Text(
            "2. All mathematical solutions are physically relevant.",
            font_size=DEFAULT_FONT_SIZE * 0.6, color=RED
        ).next_to(clarification1, DOWN, buff=0.8, aligned_edge=LEFT)

        clarification2 = Text(
            "Negative time or length might be mathematically valid but physically irrelevant.",
            font_size=DEFAULT_FONT_SIZE * 0.5, color=GREEN
        ).next_to(misconception2, DOWN, aligned_edge=LEFT)

        self.play(Write(misconception2))
        self.wait(1)
        self.play(Write(clarification2))
        self.wait(2)

        self.play(FadeOut(VGroup(*self.mobjects)))
        self.wait(0.5)

    def recap_summary(self):
        section_title = Text("Recap & Summary", font_size=DEFAULT_FONT_SIZE * 0.9, color=TITLE_COLOR).to_edge(UP)
        self.play(Write(section_title))
        self.wait(0.5)

        summary_points = VGroup(
            Text("- Quadratic equations describe parabolas.", font_size=DEFAULT_FONT_SIZE * 0.6),
            Text("- Model projectile motion, trajectories.", font_size=DEFAULT_FONT_SIZE * 0.6),
            Text("- Optimize solutions (max/min).", font_size=DEFAULT_FONT_SIZE * 0.6),
            Text("- Fundamental in engineering & design (arches, reflectors).", font_size=DEFAULT_FONT_SIZE * 0.6)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).center().shift(UP*0.5)
        summary_points.set_color_by_tex("parabolas", GRAPH_COLOR)
        summary_points.set_color_by_tex("projectile motion", HIGHLIGHT_COLOR)
        summary_points.set_color_by_tex("Optimize", VERTEX_COLOR)
        summary_points.set_color_by_tex("engineering", BLUE_B)
        
        self.play(FadeIn(summary_points[0], shift=LEFT))
        self.play(FadeIn(summary_points[1], shift=LEFT))
        self.play(FadeIn(summary_points[2], shift=LEFT))
        self.play(FadeIn(summary_points[3], shift=LEFT))
        self.wait(3)

        self.play(FadeOut(VGroup(*self.mobjects)))
        self.wait(0.5)

    def closing_call_to_action(self):
        closing_text1 = Text(
            "Next time you see an arched bridge or a fountain's arc,",
            font_size=DEFAULT_FONT_SIZE * 0.7, color=HIGHLIGHT_COLOR
        ).center().shift(UP*1)
        
        closing_text2 = Text(
            "remember the humble quadratic equation at play.",
            font_size=DEFAULT_FONT_SIZE * 0.8, color=EQUATION_COLOR
        ).next_to(closing_text1, DOWN, buff=0.8)

        self.play(FadeIn(closing_text1, shift=UP))
        self.play(Write(closing_text2))
        self.wait(2)

        call_to_action = Text(
            "Keep exploring, and you'll find math everywhere!",
            font_size=DEFAULT_FONT_SIZE * 0.6, color=GREEN
        ).next_to(closing_text2, DOWN, buff=1)

        self.play(FadeIn(call_to_action, shift=UP))
        self.wait(2)
        self.play(FadeOut(VGroup(closing_text1, closing_text2, call_to_action)))
        self.wait(1)
