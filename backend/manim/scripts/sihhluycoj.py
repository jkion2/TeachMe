from manim import *

# --- Constants & Colors ---
WHEEL_RADIUS = 2.0
WHEEL_COLOR = BLUE_D
GROUND_COLOR = GREEN_D
TRANSLATIONAL_VELOCITY_COLOR = YELLOW
ROTATIONAL_VELOCITY_COLOR = RED
RESULTANT_VELOCITY_COLOR = GREEN
POINT_COLOR = WHITE
TEXT_COLOR = WHITE
EQUATION_COLOR = YELLOW
HIGHLIGHT_COLOR = ORANGE
VELOCITY_MAGNITUDE = 1.5  # Represents V and R*omega magnitude for arrow length


class SolutionAnimation(Scene):
    def construct(self):
        # Define ground_y once for consistency across sections
        ground_y = Line(LEFT, RIGHT).to_edge(DOWN).get_y()

        # --- 1. Introduction ---
        self.introduction_section()

        # --- 2. Mathematical Foundation ---
        self.mathematical_foundation_section(WHEEL_RADIUS, ground_y)

        # --- 3. Step-by-Step Breakdown (Visualizing Components) ---
        self.show_translational_motion(WHEEL_RADIUS, ground_y)
        self.show_rotational_motion(WHEEL_RADIUS, ground_y)
        self.show_no_slip_condition(WHEEL_RADIUS, ground_y)
        self.show_combined_velocity_at_point_M(WHEEL_RADIUS, ground_y)

        # --- 4. Common Misunderstandings ---
        self.common_misunderstandings_section(WHEEL_RADIUS, ground_y)

        # --- 5. Recap / Summary ---
        self.recap_summary_section(WHEEL_RADIUS, ground_y)

        # --- 6. Closing ---
        self.closing_section()

    # --- Helper Methods for Animation Sections ---

    def introduction_section(self):
        """Introduces the video title, hook, and the core idea."""
        title = Text("The Mystery of Flying Mud: Rolling Without Slipping", font_size=48).to_edge(UP)
        hook_text = Text(
            "Where does a detached particle *initially* go?",
            font_size=36, color=YELLOW
        ).next_to(title, DOWN)
        self.play(Write(title), FadeIn(hook_text, shift=DOWN))
        self.wait(1.5)

        intro_text1 = Text(
            "Understanding the initial trajectory of a particle detaching from a wheel.",
            font_size=30
        ).to_edge(UP).shift(DOWN * 0.8)
        intro_text2 = Text(
            "It's about how translational and rotational motions combine.",
            font_size=30
        ).next_to(intro_text1, DOWN)
        intro_text3 = Text(
            "The core idea: Vector Addition!",
            font_size=36, color=GREEN
        ).next_to(intro_text2, DOWN * 2)

        self.play(FadeOut(title, hook_text, shift=UP))
        self.play(Write(intro_text1), Write(intro_text2))
        self.wait(1)
        self.play(Write(intro_text3))
        self.wait(2)
        self.play(FadeOut(intro_text1, intro_text2, intro_text3))

    def mathematical_foundation_section(self, wheel_radius, ground_y):
        """Lays out the mathematical framework for velocity on a rolling wheel."""
        formula_title = Text("Mathematical Foundation: Velocity on a Rolling Wheel", font_size=40).to_edge(UP)
        self.play(Write(formula_title))
        self.wait(1)

        # Setup wheel and ground
        ground = Line(LEFT * FRAME_WIDTH / 2, RIGHT * FRAME_WIDTH / 2, color=GROUND_COLOR).move_to(ground_y * UP)
        wheel_center_pos = UP * wheel_radius + ground_y * UP
        wheel = Circle(radius=wheel_radius, color=WHEEL_COLOR, fill_opacity=0.3).move_to(wheel_center_pos)
        center_dot = Dot(wheel.get_center(), color=POINT_COLOR)
        radius_line = Line(wheel.get_center(), wheel.get_center() + UP * wheel_radius, color=POINT_COLOR)
        radius_label = MathTex("R", font_size=30).next_to(radius_line, RIGHT)

        v_c_text = MathTex(r"\vec{v}_C = (v_C, 0)", font_size=36).next_to(wheel, RIGHT, buff=1)
        omega_text = MathTex(r"\omega", font_size=36).next_to(wheel, UP + RIGHT * 0.5)
        self.play(Create(ground), Create(wheel), Create(center_dot), Create(radius_line), Write(radius_label))
        self.play(Write(v_c_text), Write(omega_text))
        self.wait(1)

        no_slip_cond = MathTex(r"\text{No-slip condition: } v_C = R\omega", font_size=36).next_to(v_c_text, DOWN)
        self.play(Write(no_slip_cond))
        self.wait(1)

        v_m_formula_title = MathTex(r"\vec{v}_M = \vec{v}_C + \vec{v}_{M/C}", font_size=36).next_to(no_slip_cond, DOWN, buff=0.5)
        v_m_formula_rot = MathTex(r"\vec{v}_{M/C} = (R\omega\sin\alpha, -R\omega\cos\alpha)", font_size=36).next_to(v_m_formula_title, DOWN)
        v_m_formula_general = MathTex(
            r"\vec{v}_M = R\omega(1 + \sin\alpha, -\cos\alpha)", font_size=36, color=EQUATION_COLOR
        ).next_to(v_m_formula_rot, DOWN, buff=0.5)

        self.play(Write(v_m_formula_title))
        self.wait(1)
        self.play(Write(v_m_formula_rot))
        self.wait(1)
        self.play(Write(v_m_formula_general))
        self.wait(2)

        formula_group = VGroup(formula_title, ground, wheel, center_dot, radius_line, radius_label,
                               v_c_text, omega_text, no_slip_cond, v_m_formula_title,
                               v_m_formula_rot, v_m_formula_general)
        self.play(FadeOut(formula_group))

    def show_translational_motion(self, wheel_radius, ground_y):
        """Visualizes the translational velocity of the entire wheel."""
        title = Text("1. Translational Motion: Wheel as a Whole", font_size=40).to_edge(UP)
        self.play(Write(title))

        wheel_center_start = LEFT * 4 + UP * wheel_radius + ground_y * UP
        wheel_center_end = RIGHT * 4 + UP * wheel_radius + ground_y * UP
        
        wheel_trans = Circle(radius=wheel_radius, color=WHEEL_COLOR, fill_opacity=0.3).move_to(wheel_center_start)
        center_dot_trans = Dot(wheel_trans.get_center(), color=POINT_COLOR)

        v_label_text = MathTex(r"\vec{v}_{trans} = V\hat{i}", color=TRANSLATIONAL_VELOCITY_COLOR, font_size=36).to_corner(UL).shift(RIGHT*2)

        # Arrows for translational velocity at different points
        points_on_wheel = [wheel_trans.get_center() + v for v in [LEFT*wheel_radius*0.7, RIGHT*wheel_radius*0.7, UP*wheel_radius*0.7, DOWN*wheel_radius*0.7, ORIGIN]]
        v_arrows = VGroup()
        for p in points_on_wheel:
            arrow = Arrow(p, p + RIGHT * VELOCITY_MAGNITUDE, buff=0, max_stroke_width_to_length_ratio=0.1, max_tip_length_to_length_ratio=0.3, color=TRANSLATIONAL_VELOCITY_COLOR)
            v_arrows.add(arrow)

        self.play(Create(wheel_trans), Create(center_dot_trans), Create(v_arrows))
        self.play(Write(v_label_text))
        self.wait(1)

        # Animate wheel moving without rotation
        self.play(
            wheel_trans.animate.shift(wheel_center_end - wheel_center_start),
            center_dot_trans.animate.shift(wheel_center_end - wheel_center_start),
            v_arrows.animate.shift(wheel_center_end - wheel_center_start),
            run_time=3, rate_func=linear
        )
        self.wait(1)
        self.play(FadeOut(wheel_trans, center_dot_trans, v_arrows, v_label_text, title))

    def show_rotational_motion(self, wheel_radius, ground_y):
        """Visualizes the rotational/tangential velocity of points on the rim."""
        title = Text("2. Rotational Motion: Spinning in Place", font_size=40).to_edge(UP)
        self.play(Write(title))

        wheel_center = ORIGIN + UP * wheel_radius + ground_y * UP
        wheel_rot = Circle(radius=wheel_radius, color=WHEEL_COLOR, fill_opacity=0.3).move_to(wheel_center)
        center_dot_rot = Dot(wheel_rot.get_center(), color=POINT_COLOR)

        omega_label = MathTex(r"|\vec{v}_{rot}| = R\omega", color=ROTATIONAL_VELOCITY_COLOR, font_size=36).to_corner(UL).shift(RIGHT*2)

        # Points on the rim for rotational velocity
        points_on_rim_angles = [0, PI/2, PI, 3*PI/2] # Right, Top, Left, Bottom
        
        v_rot_arrows = VGroup()
        for angle in points_on_rim_angles:
            p = wheel_rot.point_at_angle(angle)
            # For clockwise rotation, tangent direction is (sin(angle), -cos(angle))
            direction = np.array([np.sin(angle), -np.cos(angle), 0])
            arrow = Arrow(p, p + direction * VELOCITY_MAGNITUDE * 0.8, buff=0, max_stroke_width_to_length_ratio=0.1, max_tip_length_to_length_ratio=0.3, color=ROTATIONAL_VELOCITY_COLOR)
            v_rot_arrows.add(arrow)
        
        self.play(Create(wheel_rot), Create(center_dot_rot), Create(v_rot_arrows))
        self.play(Write(omega_label))
        
        # Animate rotation (arrows rotate with wheel)
        self.play(Rotate(VGroup(wheel_rot, v_rot_arrows), angle=-2*PI, about_point=wheel_center, run_time=3, rate_func=linear))
        self.wait(1)
        self.play(FadeOut(wheel_rot, center_dot_rot, v_rot_arrows, omega_label, title))

    def show_no_slip_condition(self, wheel_radius, ground_y):
        """Demonstrates the 'rolling without slipping' condition at the contact point."""
        title = Text("3. Rolling Without Slipping: The Critical Link", font_size=40).to_edge(UP)
        self.play(Write(title))

        wheel_center = ORIGIN + UP * wheel_radius + ground_y * UP
        wheel_ns = Circle(radius=wheel_radius, color=WHEEL_COLOR, fill_opacity=0.3).move_to(wheel_center)
        center_dot_ns = Dot(wheel_ns.get_center(), color=POINT_COLOR)
        
        point_p = Dot(wheel_ns.point_at_angle(-PI/2), color=HIGHLIGHT_COLOR)
        p_label = Text("Point P (Contact)", font_size=24, color=HIGHLIGHT_COLOR).next_to(point_p, DOWN)
        
        # Translational velocity at P
        v_trans_at_p = Arrow(point_p.get_center() + LEFT * VELOCITY_MAGNITUDE / 2, point_p.get_center() + RIGHT * VELOCITY_MAGNITUDE / 2,
                             buff=0, color=TRANSLATIONAL_VELOCITY_COLOR, max_stroke_width_to_length_ratio=0.1, max_tip_length_to_length_ratio=0.3)
        v_trans_label = MathTex("V", color=TRANSLATIONAL_VELOCITY_COLOR, font_size=30).next_to(v_trans_at_p, UP)

        # Rotational velocity at P (clockwise rotation means to the left at the bottom)
        v_rot_at_p = Arrow(point_p.get_center() + RIGHT * VELOCITY_MAGNITUDE / 2, point_p.get_center() + LEFT * VELOCITY_MAGNITUDE / 2,
                           buff=0, color=ROTATIONAL_VELOCITY_COLOR, max_stroke_width_to_length_ratio=0.1, max_tip_length_to_length_ratio=0.3)
        v_rot_label = MathTex("R\omega", color=ROTATIONAL_VELOCITY_COLOR, font_size=30).next_to(v_rot_at_p, UP)
        
        self.play(Create(wheel_ns), Create(center_dot_ns))
        self.play(Create(point_p), Write(p_label))
        self.wait(0.5)
        
        self.play(Create(v_trans_at_p), Write(v_trans_label))
        self.wait(0.5)
        self.play(Create(v_rot_at_p), Write(v_rot_label))
        self.wait(1)

        # Show cancellation and condition
        no_slip_eq = MathTex(r"V = R\omega", font_size=40, color=GREEN).to_corner(UL).shift(RIGHT*2)
        zero_vel_text = Text("Point P: Instantaneously at Rest", font_size=30, color=HIGHLIGHT_COLOR).next_to(no_slip_eq, DOWN, buff=0.5)
        self.play(
            v_trans_at_p.animate.set_opacity(0),
            v_rot_at_p.animate.set_opacity(0),
            FadeOut(v_trans_label, v_rot_label),
            Transform(point_p.copy(), Dot(point_p.get_center(), radius=0.05, color=GREEN)) # Representing zero velocity visually
        )
        self.play(Write(no_slip_eq), Write(zero_vel_text))
        self.wait(1.5)

        self.play(FadeOut(wheel_ns, center_dot_ns, point_p, p_label, no_slip_eq, zero_vel_text, title))

    def show_combined_velocity_at_point_M(self, wheel_radius, ground_y):
        """Combines translational and rotational velocities at a specific point M."""
        title = Text("4. Combining Velocities: Where Does the Mud Go?", font_size=40).to_edge(UP)
        self.play(Write(title))

        wheel_center = ORIGIN + UP * wheel_radius + ground_y * UP
        wheel_main = Circle(radius=wheel_radius, color=WHEEL_COLOR, fill_opacity=0.3).move_to(wheel_center)
        center_dot_main = Dot(wheel_main.get_center(), color=POINT_COLOR)
        ground_main = Line(LEFT * FRAME_WIDTH / 2, RIGHT * FRAME_WIDTH / 2, color=GROUND_COLOR).move_to(ground_y * UP)

        self.play(Create(ground_main), Create(wheel_main), Create(center_dot_main))
        self.wait(0.5)

        # Point M definition (alpha = 2*PI/3 for upper-left quadrant)
        alpha = 2 * PI / 3 
        point_m = Dot(wheel_main.point_at_angle(alpha), color=HIGHLIGHT_COLOR)
        m_label = Text("Point M", font_size=24, color=HIGHLIGHT_COLOR).next_to(point_m, UP+LEFT)
        radius_to_m = Line(wheel_main.get_center(), point_m.get_center(), color=POINT_COLOR, stroke_width=2)
        alpha_arc = Arc(radius=0.5, start_angle=0, angle=alpha, arc_center=wheel_main.get_center())
        alpha_label = MathTex(r"\alpha = 2\pi/3", font_size=24).next_to(alpha_arc, RIGHT, buff=0.1)

        self.play(Create(point_m), Write(m_label), Create(radius_to_m), Create(alpha_arc), Write(alpha_label))
        self.wait(1)

        # 1. Translational Velocity at M
        current_step_text = Text("1. Translational Velocity", font_size=30).to_corner(UL)
        self.play(Write(current_step_text))

        v_trans_m = Arrow(point_m.get_center(), point_m.get_center() + RIGHT * VELOCITY_MAGNITUDE,
                          buff=0, color=TRANSLATIONAL_VELOCITY_COLOR, max_stroke_width_to_length_ratio=0.1, max_tip_length_to_length_ratio=0.3)
        v_trans_m_label = MathTex(r"\vec{v}_C = V\hat{i}", font_size=30, color=TRANSLATIONAL_VELOCITY_COLOR).next_to(v_trans_m, DOWN)
        
        self.play(Create(v_trans_m), Write(v_trans_m_label))
        self.wait(1)

        # 2. Rotational Velocity at M (tangential, clockwise rotation)
        self.play(FadeOut(current_step_text), run_time=0.5)
        current_step_text = Text("2. Rotational Velocity", font_size=30).to_corner(UL)
        self.play(Write(current_step_text))

        # Tangent vector for clockwise rotation at angle alpha (CCW from positive x-axis)
        tangent_direction = np.array([np.sin(alpha), -np.cos(alpha), 0])
        v_rot_m = Arrow(point_m.get_center(), point_m.get_center() + tangent_direction * VELOCITY_MAGNITUDE,
                        buff=0, color=ROTATIONAL_VELOCITY_COLOR, max_stroke_width_to_length_ratio=0.1, max_tip_length_to_length_ratio=0.3)
        v_rot_m_label = MathTex(r"\vec{v}_{M/C} = R\omega (\sin\alpha, -\cos\alpha)", font_size=30, color=ROTATIONAL_VELOCITY_COLOR).next_to(v_rot_m, LEFT)

        self.play(Create(v_rot_m), Write(v_rot_m_label))
        self.wait(1)
        
        # 3. Vector Addition
        self.play(FadeOut(current_step_text), run_time=0.5)
        current_step_text = Text("3. Vector Sum: Initial Trajectory", font_size=30).to_corner(UL)
        self.play(Write(current_step_text))

        v_rot_m_shifted = v_rot_m.copy().move_to(v_trans_m.get_end(), aligned_edge=v_rot_m.get_start())
        v_m_resultant = Arrow(point_m.get_center(), v_rot_m_shifted.get_end(),
                              buff=0, color=RESULTANT_VELOCITY_COLOR, max_stroke_width_to_length_ratio=0.1, max_tip_length_to_length_ratio=0.3)
        v_m_resultant_label = MathTex(r"\vec{v}_M", font_size=30, color=RESULTANT_VELOCITY_COLOR).next_to(v_m_resultant, UP+RIGHT)

        self.play(Transform(v_rot_m, v_rot_m_shifted))
        self.play(Create(v_m_resultant), Write(v_m_resultant_label))
        self.wait(1.5)

        # Calculation
        self.play(FadeOut(current_step_text), run_time=0.5)
        current_step_text = Text("Calculation for Point M (α=120°)", font_size=30).to_corner(UL)
        self.play(Write(current_step_text))

        calculation_group = VGroup()
        calculation_group.add(MathTex(r"\sin(2\pi/3) = \sqrt{3}/2", font_size=30))
        calculation_group.add(MathTex(r"\cos(2\pi/3) = -1/2", font_size=30))
        calculation_group.add(MathTex(r"\vec{v}_M = R\omega(1 + \sin\alpha, -\cos\alpha)", font_size=30, color=EQUATION_COLOR))
        calculation_group.add(MathTex(r"\vec{v}_M = R\omega(1 + \sqrt{3}/2, -(-1/2))", font_size=30))
        calculation_group.add(MathTex(r"\vec{v}_M = R\omega(1 + \sqrt{3}/2, 1/2)", font_size=30, color=RESULTANT_VELOCITY_COLOR))
        
        calculation_group.arrange(DOWN, center=False, aligned_edge=LEFT).to_edge(RIGHT).shift(LEFT*2 + UP*1.5)
        
        self.play(Write(calculation_group[0]))
        self.play(Write(calculation_group[1]))
        self.play(Write(calculation_group[2]))
        self.play(Write(calculation_group[3]))
        self.play(Write(calculation_group[4]))
        self.wait(2)

        final_dir_text = Text("Result: Upwards and Right (Matches Arrow D)", font_size=36, color=GREEN).next_to(calculation_group, DOWN, buff=1).to_edge(RIGHT)
        self.play(Write(final_dir_text))
        self.wait(2)

        # Optional: Top point for comparison
        self.play(FadeOut(current_step_text, calculation_group, final_dir_text))
        current_step_text = Text("Special Case: Top of the Wheel", font_size=30).to_corner(UL)
        self.play(Write(current_step_text))

        point_top = Dot(wheel_main.point_at_angle(PI/2), color=HIGHLIGHT_COLOR)
        v_trans_top = Arrow(point_top.get_center(), point_top.get_center() + RIGHT * VELOCITY_MAGNITUDE,
                            buff=0, color=TRANSLATIONAL_VELOCITY_COLOR, max_stroke_width_to_length_ratio=0.1)
        v_rot_top = Arrow(point_top.get_center(), point_top.get_center() + RIGHT * VELOCITY_MAGNITUDE,
                          buff=0, color=ROTATIONAL_VELOCITY_COLOR, max_stroke_width_to_length_ratio=0.1)
        v_total_top = Arrow(point_top.get_center(), point_top.get_center() + RIGHT * VELOCITY_MAGNITUDE * 2,
                            buff=0, color=RESULTANT_VELOCITY_COLOR, max_stroke_width_to_length_ratio=0.1)
        top_formula = MathTex(r"\vec{v}_{top} = V\hat{i} + V\hat{i} = 2V\hat{i}", font_size=30).next_to(v_total_top, UP)

        self.play(Create(point_top), Create(v_trans_top))
        self.play(TransformFromCopy(v_trans_top, v_rot_top)) # Show v_rot appears at the same location/direction
        self.play(Create(v_total_top), Write(top_formula))
        self.wait(2)

        # Fade out all mobjects from this section
        self.play(FadeOut(VGroup(title, wheel_main, center_dot_main, ground_main, point_m, m_label, radius_to_m, alpha_arc, alpha_label,
                                 v_trans_m, v_trans_m_label, v_rot_m, v_rot_m_label, v_m_resultant, v_m_resultant_label,
                                 current_step_text, point_top, v_trans_top, v_rot_top, v_total_top, top_formula)))

    def common_misunderstandings_section(self, wheel_radius, ground_y):
        """Highlights common errors in determining particle trajectory."""
        title_miscon = Text("Common Misunderstandings", font_size=40).to_edge(UP)
        self.play(Write(title_miscon))
        
        wheel_center = ORIGIN + UP * wheel_radius + ground_y * UP
        wheel_miscon = Circle(radius=wheel_radius, color=WHEEL_COLOR, fill_opacity=0.3).move_to(wheel_center)
        center_dot_miscon = Dot(wheel_miscon.get_center(), color=POINT_COLOR)
        self.play(Create(wheel_miscon), Create(center_dot_miscon))

        alpha_miscon = PI/4 # A generic point for demonstrating errors
        point_miscon = Dot(wheel_miscon.point_at_angle(alpha_miscon), color=HIGHLIGHT_COLOR)
        self.play(Create(point_miscon))

        # Misconception 1: Purely tangential (relative to center, not ground)
        miscon1_text = Text("Misconception 1: Purely tangential to rim (relative to center)", font_size=28).to_corner(UL)
        tangent_direction_pure = np.array([np.sin(alpha_miscon), -np.cos(alpha_miscon), 0]) # tangent for CW
        v_miscon1 = Arrow(point_miscon.get_center(), point_miscon.get_center() + tangent_direction_pure * VELOCITY_MAGNITUDE,
                          buff=0, color=RED, max_stroke_width_to_length_ratio=0.1, max_tip_length_to_length_ratio=0.3)
        self.play(Write(miscon1_text), Create(v_miscon1))
        self.wait(2)
        self.play(FadeOut(v_miscon1, miscon1_text))

        # Misconception 2: Purely horizontal (ignoring rotational)
        miscon2_text = Text("Misconception 2: Only translational velocity considered", font_size=28).to_corner(UL)
        v_miscon2 = Arrow(point_miscon.get_center(), point_miscon.get_center() + RIGHT * VELOCITY_MAGNITUDE,
                          buff=0, color=RED, max_stroke_width_to_length_ratio=0.1, max_tip_length_to_length_ratio=0.3)
        self.play(Write(miscon2_text), Create(v_miscon2))
        self.wait(2)
        self.play(FadeOut(v_miscon2, miscon2_text))

        always_sum_text = Text("Always sum BOTH translational and rotational components!", font_size=32, color=GREEN).next_to(point_miscon, DOWN*2)
        self.play(Write(always_sum_text))
        self.wait(2)

        self.play(FadeOut(title_miscon, wheel_miscon, center_dot_miscon, point_miscon, always_sum_text))

    def recap_summary_section(self, wheel_radius, ground_y):
        """Summarizes the key concept of vector addition for rolling without slipping."""
        title_recap = Text("Recap: Vector Sum is Key", font_size=40).to_edge(UP)
        self.play(Write(title_recap))

        summary_eq = MathTex(r"\vec{v}_{point} = \vec{v}_{trans} + \vec{v}_{rot}", font_size=48, color=GREEN).shift(UP*1)
        self.play(Write(summary_eq))
        self.wait(1)

        wheel_center_recap = ORIGIN + UP * wheel_radius + ground_y * UP
        wheel_recap = Circle(radius=wheel_radius, color=WHEEL_COLOR, fill_opacity=0.3).move_to(wheel_center_recap)
        center_dot_recap = Dot(wheel_recap.get_center(), color=POINT_COLOR)
        ground_recap = Line(LEFT * FRAME_WIDTH / 2, RIGHT * FRAME_WIDTH / 2, color=GROUND_COLOR).move_to(ground_y * UP)
        self.play(Create(ground_recap), Create(wheel_recap), Create(center_dot_recap))

        alpha_recap = 2 * PI / 3 
        point_m_recap = Dot(wheel_recap.point_at_angle(alpha_recap), color=HIGHLIGHT_COLOR)
        m_label_recap = Text("Point M", font_size=24, color=HIGHLIGHT_COLOR).next_to(point_m_recap, UP+LEFT)
        
        # Redraw the combined vector for Point M
        # Using the formula v_M = R*omega*(1 + sin(alpha), -cos(alpha))
        # With V = R*omega, this is V*(1 + sin(alpha), -cos(alpha))
        # Assuming VELOCITY_MAGNITUDE = V
        calculated_x = VELOCITY_MAGNITUDE * (1 + np.sin(alpha_recap))
        calculated_y = VELOCITY_MAGNITUDE * (-np.cos(alpha_recap))
        
        v_m_resultant_recap = Arrow(point_m_recap.get_center(), 
                                    point_m_recap.get_center() + np.array([calculated_x, calculated_y, 0]),
                                    buff=0, color=RESULTANT_VELOCITY_COLOR, max_stroke_width_to_length_ratio=0.1, max_tip_length_to_length_ratio=0.3)
        v_m_resultant_label_recap = MathTex(r"\vec{v}_M", font_size=30, color=RESULTANT_VELOCITY_COLOR).next_to(v_m_resultant_recap, UP+RIGHT)

        self.play(Create(point_m_recap), Write(m_label_recap))
        self.play(Create(v_m_resultant_recap), Write(v_m_resultant_label_recap))
        self.wait(2)

        self.play(FadeOut(VGroup(title_recap, summary_eq, wheel_recap, center_dot_recap, ground_recap,
                                 point_m_recap, m_label_recap, v_m_resultant_recap, v_m_resultant_label_recap)))

    def closing_section(self):
        """Concludes the video with a call to action or future concepts."""
        closing_text1 = Text("This vector addition is fundamental in physics!", font_size=36, color=BLUE).to_edge(UP).shift(DOWN*0.5)
        closing_text2 = Text("Understanding complex motion from simple components.", font_size=30).next_to(closing_text1, DOWN)
        closing_text3 = Text("What's next? Slipping wheels or parabolic trajectories?", font_size=30, color=YELLOW).next_to(closing_text2, DOWN*2)
        
        self.play(Write(closing_text1))
        self.play(Write(closing_text2))
        self.wait(1)
        self.play(Write(closing_text3))
        self.wait(2)
        self.play(FadeOut(VGroup(closing_text1, closing_text2, closing_text3)))
