from manim import *

# Define colors for consistency
BLUE_LIGHT = "#5DADE2"
GREEN_DARK = "#28B463"
YELLOW_BRIGHT = "#F4D03F"
RED_DARK = "#CB4335"
PURPLE_MEDIUM = "#8E44AD"

class SolutionAnimation(Scene):
    def construct(self):
        self.intro_the_circle()
        self.geometric_definition()
        self.key_components()
        self.standard_form_equation()
        self.measuring_the_circle()
        self.example_walkthrough()
        self.common_misunderstandings()
        self.recap_summary()
        self.closing_remarks()

    def intro_the_circle(self):
        # Title and Hook
        title = Text("The Perfect Shape: Understanding the Circle", font_size=50).to_edge(UP)
        hook_text = Text(
            "Defined by constant distance and symmetry.",
            font_size=32, color=YELLOW_BRIGHT
        ).next_to(title, DOWN, buff=0.5)

        self.play(Write(title))
        self.play(FadeIn(hook_text, shift=UP))
        self.wait(1.5)

        intro_context = Paragraph(
            "The circle is a fundamental shape, foundational to trigonometry,",
            "engineering, physics, and advanced concepts. We work in the",
            "two-dimensional Euclidean plane ($\\mathbb{R}^2$), representing",
            "points by Cartesian coordinates $(x,y)$.",
            font_size=28, alignment="center"
        ).next_to(hook_text, DOWN, buff=0.8)

        self.play(Write(intro_context))
        self.wait(2.5)
        self.play(FadeOut(title, hook_text, intro_context))

        key_idea_text = Text(
            "A circle: perfect symmetry and constant distance.",
            font_size=40, color=GREEN_DARK
        ).to_edge(UP, buff=1)
        sub_key_idea = Text(
            "Explore its components and translate its geometric definition",
            "into an algebraic equation using the distance formula.",
            font_size=28
        ).next_to(key_idea_text, DOWN, buff=0.5)

        self.play(Write(key_idea_text))
        self.play(FadeIn(sub_key_idea, shift=UP))
        self.wait(3)
        self.play(FadeOut(key_idea_text, sub_key_idea))

    def geometric_definition(self):
        # Section 1: Geometric Definition
        section_title = Text("1. Geometric Definition of a Circle", font_size=40, color=BLUE_LIGHT).to_edge(UP)
        self.play(Write(section_title))
        self.wait(0.5)

        # Center point
        center_dot = Dot(point=ORIGIN, color=RED_DARK)
        center_label = MathTex("(h,k)").next_to(center_dot, DOWN)
        center_group = VGroup(center_dot, center_label)

        self.play(FadeIn(center_group, scale=0.8))
        self.wait(0.5)
        self.play(center_label.animate.next_to(center_dot, UR, buff=0.1))

        narration1 = Text(
            "Imagine a single point, the center (h,k).",
            font_size=28
        ).to_corner(DR).shift(LEFT*0.5)
        self.play(Write(narration1))
        self.wait(1.5)

        # Tracing point and circle
        radius_val = 2.5
        tracing_point_start = center_dot.get_center() + RIGHT * radius_val
        tracing_dot = Dot(tracing_point_start, color=YELLOW_BRIGHT)
        tracing_label = MathTex("(x,y)").next_to(tracing_dot, UP + RIGHT)

        self.play(FadeIn(tracing_dot, scale=0.5))
        self.play(Write(tracing_label))
        self.wait(0.5)

        narration2 = Text(
            "Now, draw every point (x,y) that is exactly",
            "the same distance, r, away from it.",
            font_size=28
        ).next_to(narration1, UP, aligned_edge=LEFT)
        self.play(FadeTransform(narration1, narration2))
        self.wait(1)

        path = Circle(radius=radius_val, color=GREEN_DARK, stroke_width=4)
        radius_line = Line(center_dot.get_center(), tracing_dot.get_center(), color=PURPLE_MEDIUM)
        radius_label = MathTex("r", font_size=32).next_to(radius_line, UR, buff=0.1)

        self.play(Create(radius_line), Write(radius_label))
        self.wait(0.5)

        def update_tracing_dot(mob, alpha):
            point_on_circle = path.point_from_proportion(alpha)
            mob.move_to(point_on_circle)
            tracing_label.next_to(mob, UP + RIGHT)
            radius_line.put_start_and_end_on(center_dot.get_center(), mob.get_center())

        self.play(
            UpdateFromAlphaFunc(tracing_dot, update_tracing_dot),
            Create(path),
            rate_func=linear,
            run_time=3
        )
        self.play(FadeOut(tracing_label))
        self.wait(0.5)

        narration3 = Text(
            "This constant distance, r, is the radius.",
            "The shape you get? A circle!",
            font_size=28
        ).next_to(narration2, UP, aligned_edge=LEFT)
        self.play(FadeTransform(narration2, narration3))
        self.wait(1)

        radius_label_final = MathTex("\\text{Radius } r").next_to(radius_line, UP, buff=0.2).set_color(PURPLE_MEDIUM)
        center_label_final = MathTex("\\text{Center }(h,k)").next_to(center_dot, UL, buff=0.2).set_color(RED_DARK)
        self.play(FadeOut(radius_label), Transform(center_label, center_label_final), Write(radius_label_final))

        definition_text = Paragraph(
            "A circle is the set of all points $(x,y)$ in a plane",
            "that are equidistant from a given fixed point $(h,k)$",
            "called the center. The constant distance is the radius $r$.",
            font_size=26
        ).to_corner(DL).shift(RIGHT*0.5)
        self.play(Write(definition_text))

        self.play(
            Indicate(center_dot), Indicate(center_label),
            Indicate(path),
            Indicate(radius_line), Indicate(radius_label_final),
            run_time=2
        )
        self.wait(2)
        self.play(FadeOut(section_title, center_group, radius_line, radius_label_final,
                           path, definition_text, narration3))

    def key_components(self):
        # Section 2: Key Components: Radius & Diameter
        section_title = Text("2. Key Components: Radius & Diameter", font_size=40, color=BLUE_LIGHT).to_edge(UP)
        self.play(Write(section_title))
        self.wait(0.5)

        circle = Circle(radius=2.5, color=GREEN_DARK, stroke_width=4).shift(LEFT*2.5)
        center_dot = Dot(circle.get_center(), color=RED_DARK)
        center_label = MathTex("(h,k)").next_to(center_dot, DL)
        self.play(Create(circle), FadeIn(center_dot), Write(center_label))
        self.wait(0.5)

        radius_line = Line(center_dot.get_center(), circle.point_at_angle(PI/4), color=PURPLE_MEDIUM)
        radius_label = MathTex("r").next_to(radius_line, UP)
        narration1 = Text(
            "The radius (r) connects the center to any point on the circle.",
            font_size=28
        ).to_corner(DR)
        self.play(Create(radius_line), Write(radius_label), Write(narration1))
        self.wait(1.5)

        diameter_line = Line(circle.point_at_angle(3*PI/4), circle.point_at_angle(-PI/4), color=YELLOW_BRIGHT)
        diameter_label = MathTex("d").next_to(diameter_line, DOWN)
        narration2 = Text(
            "The diameter (d) passes through the center,",
            "connecting two points on the circle.",
            font_size=28
        ).next_to(narration1, UP, aligned_edge=LEFT)
        self.play(FadeTransform(narration1, narration2))
        self.play(Create(diameter_line), Write(diameter_label))
        self.wait(1.5)

        equation_d2r = MathTex("d = 2r", color=YELLOW_BRIGHT).next_to(circle, RIGHT, buff=1.5)
        narration3 = Text(
            "The diameter is simply twice the radius!",
            font_size=28
        ).next_to(narration2, UP, aligned_edge=LEFT)
        self.play(FadeTransform(narration2, narration3))
        self.play(Write(equation_d2r))
        self.play(Circumscribe(equation_d2r))
        self.wait(2)

        self.play(FadeOut(section_title, circle, center_dot, center_label,
                           radius_line, radius_label, diameter_line,
                           diameter_label, equation_d2r, narration3))

    def standard_form_equation(self):
        # Section 3: Standard Form (Center-Radius Form) of the Equation of a Circle
        section_title = Text("3. Standard Form Equation", font_size=40, color=BLUE_LIGHT).to_edge(UP)
        self.play(Write(section_title))
        self.wait(0.5)

        narration = Text(
            "How to express this geometrically using algebra?",
            font_size=28
        ).to_corner(DR)
        self.play(Write(narration))
        self.wait(1)

        distance_formula_text = MathTex(
            "\\text{Distance Formula: } d = \\sqrt{(x_2-x_1)^2 + (y_2-y_1)^2}",
            font_size=36
        ).to_corner(UL).shift(RIGHT*0.5)
        self.play(Write(distance_formula_text))
        self.wait(2)

        narration2 = Text(
            "The distance between any point (x,y) on the circle",
            "and the center (h,k) must be equal to the radius r.",
            font_size=28
        ).next_to(narration, UP, aligned_edge=LEFT)
        self.play(FadeTransform(narration, narration2))
        self.wait(1)

        eq1 = MathTex(
            "\\sqrt{(x-h)^2 + (y-k)^2} = r",
            font_size=44
        ).next_to(distance_formula_text, DOWN, buff=1).align_to(distance_formula_text, LEFT)
        self.play(Write(eq1))
        self.wait(2)

        eq2_step1_text = MathTex(
            "\\left(\\sqrt{(x-h)^2 + (y-k)^2}\\right)^2 = r^2",
            font_size=44
        ).next_to(eq1, DOWN, buff=0.8).align_to(eq1, LEFT)
        narration3 = Text(
            "Squaring both sides gives us the standard form:",
            font_size=28
        ).next_to(narration2, UP, aligned_edge=LEFT)
        self.play(FadeTransform(narration2, narration3))
        self.play(TransformMatchingTex(eq1.copy(), eq2_step1_text))
        self.wait(1.5)

        eq3_final = MathTex(
            "(x-h)^2 + (y-k)^2 = r^2",
            font_size=50, color=YELLOW_BRIGHT
        ).next_to(eq2_step1_text, DOWN, buff=0.8).align_to(eq2_step1_text, LEFT)
        self.play(TransformMatchingTex(eq2_step1_text, eq3_final))
        self.wait(1.5)

        final_label = Text("Standard Form Equation of a Circle", font_size=32).next_to(eq3_final, DOWN, buff=0.5)
        self.play(Write(final_label))
        self.play(Circumscribe(eq3_final, color=GREEN_DARK, time_width=2))
        self.wait(2.5)

        self.play(FadeOut(section_title, distance_formula_text, eq3_final, final_label, narration3))

    def measuring_the_circle(self):
        # Section 4: Measuring the Circle: Circumference & Area
        section_title = Text("4. Measuring the Circle: Circumference & Area", font_size=40, color=BLUE_LIGHT).to_edge(UP)
        self.play(Write(section_title))
        self.wait(0.5)

        circle = Circle(radius=2, color=GREEN_DARK, stroke_width=5)
        center_dot = Dot(circle.get_center(), color=RED_DARK)
        self.play(Create(circle), FadeIn(center_dot))
        self.wait(0.5)

        radius_line = Line(center_dot.get_center(), circle.point_at_angle(0), color=PURPLE_MEDIUM)
        radius_label = MathTex("r").next_to(radius_line, UP)
        self.play(Create(radius_line), Write(radius_label))
        self.wait(0.5)

        narration1 = Text(
            "Circumference (C) is the total distance around its edge.",
            font_size=28
        ).to_corner(DR)
        self.play(Write(narration1))
        self.wait(1)

        # Circumference animation
        circumference_path = circle.copy().set_color(YELLOW_BRIGHT).set_stroke_width(8)
        self.play(ShowPassingFlash(circumference_path, run_time=1.5, time_width=0.5))

        # "Unrolling" animation (simplified)
        straight_line = Line(LEFT * PI * radius_line.get_length(), RIGHT * PI * radius_line.get_length(), color=YELLOW_BRIGHT, stroke_width=6)
        c_label = MathTex("C").next_to(straight_line, UP)
        
        self.play(
            circle.animate.shift(LEFT*3),
            center_dot.animate.shift(LEFT*3),
            radius_line.animate.shift(LEFT*3),
            radius_label.animate.shift(LEFT*3),
            run_time=1
        )
        self.play(
            FadeIn(straight_line.next_to(circle, RIGHT, buff=2)),
            Write(c_label.next_to(straight_line, UP)),
        )
        self.wait(0.5)

        circumference_eq = MathTex("C = 2\\pi r", "=", "\\pi d", font_size=44, color=YELLOW_BRIGHT).next_to(straight_line, DOWN, buff=0.8)
        self.play(Write(circumference_eq))
        self.wait(1.5)

        narration2 = Text(
            "Area (A) is the amount of flat space it encloses.",
            font_size=28
        ).next_to(narration1, UP, aligned_edge=LEFT)
        self.play(FadeTransform(narration1, narration2))
        self.wait(1)

        # Area animation
        area_fill = circle.copy().set_fill(GREEN_DARK, opacity=0.7).set_stroke_width(0)
        a_label = MathTex("A").move_to(area_fill.get_center())
        self.play(FadeIn(area_fill), Write(a_label))
        self.wait(1)

        area_eq = MathTex("A = \\pi r^2", font_size=44, color=GREEN_DARK).next_to(circumference_eq, DOWN, buff=0.8)
        self.play(Write(area_eq))
        self.wait(1.5)

        pi_note = MathTex("\\pi \\approx 3.14159", font_size=32).to_corner(DR).shift(LEFT*0.5)
        self.play(Write(pi_note))
        self.play(Circumscribe(VGroup(circumference_eq, area_eq), color=BLUE_LIGHT))
        self.wait(3)

        self.play(FadeOut(section_title, circle, center_dot, radius_line, radius_label,
                           straight_line, c_label, circumference_eq,
                           area_fill, a_label, area_eq, pi_note, narration2))

    def example_walkthrough(self):
        # Section 5: Example: Putting it all Together
        section_title = Text("5. Example: Putting it all Together", font_size=40, color=BLUE_LIGHT).to_edge(UP)
        self.play(Write(section_title))
        self.wait(0.5)

        example_intro = Text(
            "Given: Center (h,k) = (2,1), Radius r = 3 units.",
            font_size=32
        ).to_corner(UL).shift(RIGHT*0.5)
        self.play(Write(example_intro))
        self.wait(1)

        # Setup Axes
        axes = Axes(
            x_range=[-1, 5, 1],
            y_range=[-2, 4, 1],
            x_length=6,
            y_length=6,
            axis_config={"color": GRAY, "stroke_width": 2},
            x_axis_config={"numbers_with_elongated_ticks": [0,1,2,3,4,5]},
            y_axis_config={"numbers_with_elongated_ticks": [-2,-1,0,1,2,3,4]},
        ).scale(0.7).to_edge(LEFT, buff=0.5)
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")

        self.play(Create(axes), Write(axes_labels))
        self.wait(0.5)

        # Plotting the circle
        center_coords = axes.coords_to_point(2,1)
        example_center_dot = Dot(center_coords, color=RED_DARK, radius=0.08)
        center_label_ex = MathTex("(2,1)").next_to(example_center_dot, DOWN)
        example_circle = Circle(
            radius=axes.x_axis.get_unit_size() * 3, # Map 3 units to axes scale
            color=GREEN_DARK,
            stroke_width=4
        ).move_to(center_coords)
        
        self.play(FadeIn(example_center_dot, scale=0.5), Write(center_label_ex))
        self.play(Create(example_circle))
        self.wait(1)

        # Calculations
        calculations_group = VGroup().to_edge(RIGHT).shift(UP*1.5)

        eq_text = Text("Standard Equation:", font_size=28).to_corner(UR).shift(DOWN*0.5)
        eq_val = MathTex("(x-2)^2 + (y-1)^2 = 3^2 = 9", color=YELLOW_BRIGHT, font_size=36).next_to(eq_text, DOWN, buff=0.2).align_to(eq_text, LEFT)
        calculations_group.add(eq_text, eq_val)
        self.play(Write(eq_text), Write(eq_val))
        self.wait(1.5)

        diam_text = Text("Diameter (d):", font_size=28).next_to(eq_val, DOWN, buff=0.5).align_to(eq_text, LEFT)
        diam_val = MathTex("d = 2r = 2 \\times 3 = 6 \\text{ units}", color=PURPLE_MEDIUM, font_size=36).next_to(diam_text, DOWN, buff=0.2).align_to(eq_text, LEFT)
        calculations_group.add(diam_text, diam_val)
        self.play(Write(diam_text), Write(diam_val))

        radius_line_ex = Line(example_center_dot.get_center(), axes.coords_to_point(2,4), color=PURPLE_MEDIUM, stroke_width=3)
        radius_label_ex = MathTex("r=3").next_to(radius_line_ex, LEFT, buff=0.1)
        diameter_line_ex = Line(axes.coords_to_point(-1,1), axes.coords_to_point(5,1), color=YELLOW_BRIGHT, stroke_width=3)
        diameter_label_ex = MathTex("d=6").next_to(diameter_line_ex, DOWN, buff=0.1)
        self.play(Create(radius_line_ex), Write(radius_label_ex))
        self.play(Create(diameter_line_ex), Write(diameter_label_ex))
        self.wait(1.5)


        circ_text = Text("Circumference (C):", font_size=28).next_to(diam_val, DOWN, buff=0.5).align_to(eq_text, LEFT)
        circ_val = MathTex("C = 2\\pi r = 2\\pi(3) = 6\\pi \\approx 18.85 \\text{ units}", color=BLUE_LIGHT, font_size=36).next_to(circ_text, DOWN, buff=0.2).align_to(eq_text, LEFT)
        calculations_group.add(circ_text, circ_val)
        self.play(Write(circ_text), Write(circ_val))
        self.play(ShowPassingFlash(example_circle.copy().set_color(BLUE_LIGHT).set_stroke_width(8), run_time=1.5, time_width=0.5))
        self.wait(1.5)

        area_text = Text("Area (A):", font_size=28).next_to(circ_val, DOWN, buff=0.5).align_to(eq_text, LEFT)
        area_val = MathTex("A = \\pi r^2 = \\pi(3)^2 = 9\\pi \\approx 28.27 \\text{ sq. units}", color=GREEN_DARK, font_size=36).next_to(area_text, DOWN, buff=0.2).align_to(eq_text, LEFT)
        calculations_group.add(area_text, area_val)
        self.play(Write(area_text), Write(area_val))
        example_circle_fill = example_circle.copy().set_fill(GREEN_DARK, opacity=0.7).set_stroke_width(0)
        self.play(FadeIn(example_circle_fill))
        self.wait(1.5)
        
        # Verification
        verify_point = MathTex("(2,4)", color=YELLOW_BRIGHT).next_to(axes.coords_to_point(2,4), UR)
        verify_dot = Dot(axes.coords_to_point(2,4), color=YELLOW_BRIGHT)
        verify_equation = MathTex("(2-2)^2 + (4-1)^2 = 0^2 + 3^2 = 9", font_size=32).next_to(area_val, DOWN, buff=0.5).align_to(area_text, LEFT)
        
        self.play(FadeIn(verify_dot, verify_point))
        self.play(Write(verify_equation))
        self.play(Circumscribe(verify_equation, color=YELLOW_BRIGHT))
        self.wait(2)

        self.play(FadeOut(section_title, example_intro, axes, axes_labels,
                           example_center_dot, center_label_ex, example_circle,
                           radius_line_ex, radius_label_ex, diameter_line_ex, diameter_label_ex,
                           calculations_group, verify_dot, verify_point, verify_equation, example_circle_fill))

    def common_misunderstandings(self):
        # Common Misunderstandings & Tips
        section_title = Text("Common Misunderstandings & Tips", font_size=40, color=BLUE_LIGHT).to_edge(UP)
        self.play(Write(section_title))
        self.wait(0.5)

        misconception1_title = Text("Circumference vs. Area", font_size=36, color=RED_DARK).to_corner(UL)
        self.play(Write(misconception1_title))
        self.wait(0.5)

        circumference_def = MathTex("C = 2\\pi r \\quad (\\text{Length, e.g., meters})", font_size=32).next_to(misconception1_title, DOWN, buff=0.5).align_to(misconception1_title, LEFT)
        area_def = MathTex("A = \\pi r^2 \\quad (\\text{Space, e.g., square meters})", font_size=32).next_to(circumference_def, DOWN, buff=0.2).align_to(misconception1_title, LEFT)
        self.play(Write(circumference_def), Write(area_def))
        self.wait(2)

        misconception2_title = Text("Standard Equation: Signs of (h,k) and r²", font_size=36, color=RED_DARK).next_to(area_def, DOWN, buff=1).align_to(misconception1_title, LEFT)
        self.play(Write(misconception2_title))
        self.wait(0.5)

        eq_template = MathTex("(x-h)^2 + (y-k)^2 = r^2", font_size=44).next_to(misconception2_title, DOWN, buff=0.5).align_to(misconception1_title, LEFT)
        self.play(Write(eq_template))
        self.wait(1)

        h_k_highlight = MathTex("(x\\underline{-h})^2 + (y\\underline{-k})^2 = r^2", font_size=44).move_to(eq_template).set_color_by_tex_to_color_map({"{-h}": YELLOW_BRIGHT, "{-k}": YELLOW_BRIGHT})
        r_sq_highlight = MathTex("(x-h)^2 + (y-k)^2 = \\underline{r^2}", font_size=44).move_to(eq_template).set_color_by_tex_to_color_map({"r^2": GREEN_DARK})
        
        self.play(TransformMatchingTex(eq_template, h_k_highlight))
        narration1 = Text(
            "Center (h,k) coordinates are subtracted.",
            "e.g., (x+3)^2 means h = -3.",
            font_size=28
        ).to_corner(DR).shift(LEFT*0.5)
        self.play(Write(narration1))
        self.wait(2)

        self.play(TransformMatchingTex(h_k_highlight, r_sq_highlight))
        narration2 = Text(
            "The term on the right is radius squared ($r^2$).",
            "Remember to take the square root for r.",
            font_size=28
        ).next_to(narration1, UP, aligned_edge=LEFT)
        self.play(FadeTransform(narration1, narration2))
        self.wait(2.5)

        self.play(FadeOut(section_title, misconception1_title, circumference_def, area_def,
                           misconception2_title, r_sq_highlight, narration2))

    def recap_summary(self):
        # Recap / Summary
        section_title = Text("Recap: The Circle", font_size=40, color=BLUE_LIGHT).to_edge(UP)
        self.play(Write(section_title))
        self.wait(0.5)

        summary_points = VGroup(
            MathTex("\\bullet \\text{ Definition: Locus of points equidistant from a center } (h,k) \\text{ by radius } r.", font_size=34),
            MathTex("\\bullet \\text{ Standard Equation: } (x-h)^2 + (y-k)^2 = r^2", font_size=34),
            MathTex("\\bullet \\text{ Diameter: } d=2r", font_size=34),
            MathTex("\\bullet \\text{ Circumference: } C=2\\pi r", font_size=34),
            MathTex("\\bullet \\text{ Area: } A=\\pi r^2", font_size=34)
        ).arrange(DOWN, buff=0.8, alignment=LEFT).center().shift(UP*0.5)

        summary_points[0][0].set_color(BLUE_LIGHT)
        summary_points[1][2].set_color(YELLOW_BRIGHT) # (x-h)^2 + (y-k)^2 = r^2
        summary_points[2][2].set_color(PURPLE_MEDIUM) # d=2r
        summary_points[3][2].set_color(YELLOW_BRIGHT) # C=2\pi r
        summary_points[4][2].set_color(GREEN_DARK)   # A=\pi r^2

        self.play(LaggedStart(*[Write(point) for point in summary_points], lag_ratio=0.7))
        self.wait(4)

        self.play(FadeOut(section_title, summary_points))

    def closing_remarks(self):
        # Closing / Call to Action
        final_text = Text(
            "The circle's perfect symmetry and predictable properties",
            "make it an indispensable concept.",
            font_size=38
        ).to_edge(UP, buff=1)

        self.play(Write(final_text))
        self.wait(1.5)

        # Final graphic: a stylized circle animation
        final_circle = Circle(radius=2, color=BLUE_LIGHT, stroke_width=8)
        inner_circle = Circle(radius=1.5, color=GREEN_DARK, stroke_width=6)
        outer_ring = Annulus(inner_radius=2.5, outer_radius=2.8, color=YELLOW_BRIGHT, stroke_width=4)

        circle_group = VGroup(final_circle, inner_circle, outer_ring).center()

        self.play(
            Create(final_circle),
            GrowFromCenter(inner_circle),
            FadeIn(outer_ring, shift=UP),
            run_time=2
        )
        self.play(Rotate(circle_group, angle=TAU/4, run_time=3, rate_func=linear))

        call_to_action = Text(
            "Mastering these basics sets the stage for more complex ideas.",
            "Spot circles around you and appreciate their mathematical elegance!",
            font_size=30
        ).next_to(final_circle, DOWN, buff=1)
        self.play(Write(call_to_action))
        self.wait(3)

        self.play(FadeOut(final_text, circle_group, call_to_action))