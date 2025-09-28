from manim import *

# Constants for consistent styling and values
WHEEL_RADIUS = 2
WHEEL_CENTER_Y = -1.5
VELOCITY_MAG = 2  # Represents v_C and R*omega
MUD_POINT_ANGLE_DEG = 45  # Angle from positive x-axis, counter-clockwise, for upper-right quadrant
MUD_POINT_ANGLE_RAD = MUD_POINT_ANGLE_DEG * DEGREES

# Colors
GROUND_COLOR = WHITE
WHEEL_COLOR = WHITE
HUB_COLOR = RED
MUD_POINT_COLOR = BROWN
V_CM_COLOR = BLUE_C      # Translational velocity of center of mass
V_ROT_COLOR = GREEN_C    # Rotational velocity relative to center
V_TOTAL_COLOR = YELLOW_C # Absolute instantaneous velocity
CORRECT_ARROW_COLOR = GREEN_B
INCORRECT_ARROW_COLOR = RED_B

class SolutionAnimation(Scene):
    def construct(self):
        self.intro_hook()
        self.section1_dual_motion()
        self.section2_velocity_any_point()
        self.section3_velocity_at_detachment()
        self.section4_moment_of_detachment()
        self.common_misunderstandings()
        self.recap_summary()
        self.closing_call_to_action()

    def intro_hook(self):
        # Video Title and Hook
        title = Title("The Physics of Flying Mud: Why Your Bike Splashes *That* Way!", font_size=48)
        hook_text = Text(
            "Ever wondered exactly how mud flies off your tires?",
            font_size=36, color=YELLOW_C
        ).next_to(title, DOWN, buff=0.8)
        
        intro_text = Text(
            "We'll explore a mud particle detaching from a rolling wheel.",
            font_size=32
        ).next_to(hook_text, DOWN, buff=0.5)

        self.play(Write(title), FadeIn(hook_text))
        self.wait(1.5)
        self.play(Write(intro_text))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(hook_text), FadeOut(intro_text))

    def section1_dual_motion(self):
        # Section 1: The Dual Motion of a Rolling Wheel
        section_title = Title("1. The Dual Motion of a Rolling Wheel").to_edge(UP)
        self.play(Write(section_title))

        # Create ground line
        ground = Line(LEFT * 7, RIGHT * 7, color=GROUND_COLOR).shift(DOWN * (WHEEL_RADIUS + 0.5))

        # Initial positions for rolling wheel animation
        wheel_center_start = [-5, WHEEL_CENTER_Y, 0]

        # Mobjects for the rolling animation
        wheel_anim = Circle(radius=WHEEL_RADIUS, color=WHEEL_COLOR).move_to(wheel_center_start)
        hub_anim = Dot(wheel_anim.get_center(), color=HUB_COLOR)
        p_dot_anim = Dot(wheel_anim.get_bottom(), color=RED, radius=0.08)
        p_label_anim = MathTex("P").next_to(p_dot_anim, DOWN, buff=0.2)

        v_cm_arrow_anim = Arrow(hub_anim.get_center(), hub_anim.get_center() + RIGHT * VELOCITY_MAG, buff=0, color=V_CM_COLOR)
        v_cm_label_anim = MathTex(r"\vec{v}_C").next_to(v_cm_arrow_anim, UP, buff=0.2)

        omega_arrow_anim = CurvedArrow(
            wheel_anim.get_center() + RIGHT * 0.5 + UP * 0.5,
            wheel_anim.get_center() + RIGHT * 0.5 + DOWN * 0.5,
            radius=-0.5, color=WHITE
        )
        omega_label_anim = MathTex(r"\omega").next_to(omega_arrow_anim, RIGHT, buff=0.2)

        self.play(Create(ground), Create(wheel_anim), FadeIn(hub_anim))
        self.play(Write(p_label_anim), Create(p_dot_anim))
        self.play(FadeIn(v_cm_arrow_anim), Write(v_cm_label_anim), FadeIn(omega_arrow_anim), Write(omega_label_anim))
        self.wait(1)

        # Group all animatable mobjects for the rolling motion
        rolling_group = VGroup(
            wheel_anim, hub_anim, p_dot_anim, p_label_anim,
            v_cm_arrow_anim, v_cm_label_anim, omega_arrow_anim, omega_label_anim
        )

        # Update function for rolling motion
        def update_rolling_group(group, dt):
            wheel_obj, hub_obj, p_dot_obj, p_label_obj, v_cm_arrow_obj, v_cm_label_obj, omega_arrow_obj, omega_label_obj = group

            # Translate wheel and hub
            wheel_obj.shift(RIGHT * VELOCITY_MAG * dt)
            hub_obj.shift(RIGHT * VELOCITY_MAG * dt)

            # Rotate wheel around its new center
            angle = -VELOCITY_MAG * dt / WHEEL_RADIUS  # Clockwise rotation
            wheel_obj.rotate(angle, about_point=wheel_obj.get_center())

            # Update point P position (always at the bottom of the wheel)
            p_dot_obj.move_to(wheel_obj.get_bottom())
            p_label_obj.next_to(p_dot_obj, DOWN, buff=0.2)

            # Update V_CM arrow and label relative to new hub center
            v_cm_arrow_obj.put_start_and_end_on(hub_obj.get_center(), hub_obj.get_center() + RIGHT * VELOCITY_MAG)
            v_cm_label_obj.next_to(v_cm_arrow_obj, UP, buff=0.2)

            # Update Omega arrow and label relative to new hub center
            omega_arrow_obj.move_to(hub_obj.get_center() + RIGHT * 0.5 + DOWN * 0.5)
            omega_label_obj.next_to(omega_arrow_obj, RIGHT, buff=0.2)

        self.add(rolling_group) # Add the group to the scene for animation
        self.play(
            UpdateFromFunc(rolling_group, update_rolling_group),
            run_time=3,
            rate_func=linear
        )
        self.wait(1)

        # Equation: v_C = R*omega
        equation1 = MathTex(r"v_C = R\omega").to_edge(RIGHT).shift(UP*1.5)
        keyword = Text("Rolling Without Slipping", font_size=30, color=YELLOW_C).next_to(equation1, DOWN, buff=0.5)
        self.play(Write(equation1), Write(keyword))
        self.wait(1.5)

        # Fade out rolling group and ground for point velocity demo
        self.play(FadeOut(rolling_group), FadeOut(ground), FadeOut(keyword), FadeOut(equation1))

        # Static wheel to demonstrate point velocities (P=0, Top=2v_C)
        wheel_static = Circle(radius=WHEEL_RADIUS, color=WHEEL_COLOR).move_to(ORIGIN + UP * WHEEL_RADIUS) # Place wheel slightly higher
        hub_static = Dot(wheel_static.get_center(), color=HUB_COLOR)
        
        # Redraw ground for context with static wheel
        ground_static = Line(LEFT * 7, RIGHT * 7, color=GROUND_COLOR).shift(DOWN * 0) # Aligned to bottom of wheel_static

        self.play(Create(ground_static), Create(wheel_static), FadeIn(hub_static))

        point_bottom_static = Dot(wheel_static.get_bottom(), color=RED, radius=0.08)
        v_bottom_label_static = MathTex(r"\vec{v}_P = \mathbf{0}").next_to(point_bottom_static, DOWN, buff=0.2)
        self.play(Create(point_bottom_static), Write(v_bottom_label_static))
        self.wait(1.5)

        point_top_static = Dot(wheel_static.get_top(), color=RED, radius=0.08)
        v_top_arrow_static = Arrow(
            start=point_top_static.get_center(),
            end=point_top_static.get_center() + RIGHT * VELOCITY_MAG * 2,
            buff=0, color=V_TOTAL_COLOR
        )
        v_top_label_static = MathTex(r"2\vec{v}_C").next_to(v_top_arrow_static, UP, buff=0.2)
        self.play(Create(point_top_static), Create(v_top_arrow_static), Write(v_top_label_static))
        self.wait(2)

        self.play(FadeOut(section_title), FadeOut(wheel_static), FadeOut(hub_static), FadeOut(point_bottom_static),
                  FadeOut(v_bottom_label_static), FadeOut(point_top_static), FadeOut(v_top_arrow_static), FadeOut(v_top_label_static), FadeOut(ground_static))

    def section2_velocity_any_point(self):
        # Section 2: Velocity of Any Point on the Wheel
        section_title = Title("2. Velocity of Any Point on the Wheel").to_edge(UP)
        self.play(Write(section_title))

        # Equation for total velocity
        eq_total_v = MathTex(
            r"\vec{v}_P = \vec{v}_C + \vec{v}_{P/C}"
        ).to_edge(RIGHT).shift(UP*1.5)
        self.play(Write(eq_total_v))
        self.wait(1)

        # Create static wheel with point M at origin for vector addition clarity
        wheel = Circle(radius=WHEEL_RADIUS, color=WHEEL_COLOR).move_to(ORIGIN)
        hub = Dot(wheel.get_center(), color=HUB_COLOR)
        
        # Calculate M's position in upper-right quadrant
        # MUD_POINT_ANGLE_RAD is CCW from positive x-axis
        mud_x_rel = WHEEL_RADIUS * np.cos(MUD_POINT_ANGLE_RAD)
        mud_y_rel = WHEEL_RADIUS * np.sin(MUD_POINT_ANGLE_RAD)
        mud_point_pos = wheel.get_center() + [mud_x_rel, mud_y_rel, 0]
        
        mud_dot = Dot(mud_point_pos, color=MUD_POINT_COLOR, radius=0.1)
        mud_label = MathTex("M").next_to(mud_dot, UP + RIGHT, buff=0.3)
        
        self.play(Create(wheel), FadeIn(hub), Create(mud_dot), Write(mud_label))
        self.wait(1)

        # Vectors at M
        # v_CM (translational velocity)
        v_cm_arrow = Arrow(
            start=mud_point_pos,
            end=mud_point_pos + RIGHT * VELOCITY_MAG,
            buff=0, color=V_CM_COLOR
        )
        v_cm_label = MathTex(r"\vec{v}_C").next_to(v_cm_arrow, UP, buff=0.2)

        # v_rot (rotational velocity relative to center)
        # Angle of v_rot is MUD_POINT_ANGLE_RAD - PI/2 for clockwise wheel rotation
        rot_vel_x = VELOCITY_MAG * np.cos(MUD_POINT_ANGLE_RAD - PI/2)
        rot_vel_y = VELOCITY_MAG * np.sin(MUD_POINT_ANGLE_RAD - PI/2)
        
        v_rot_arrow = Arrow(
            start=mud_point_pos,
            end=mud_point_pos + [rot_vel_x, rot_vel_y, 0],
            buff=0, color=V_ROT_COLOR
        )
        v_rot_label = MathTex(r"\vec{v}_{M/C}").next_to(v_rot_arrow, RIGHT, buff=0.2)

        self.play(Create(v_cm_arrow), Write(v_cm_label))
        self.wait(1)
        self.play(Create(v_rot_arrow), Write(v_rot_label))
        self.wait(1)

        # Highlight equality of magnitudes
        mag_equality = MathTex(
            r"|\vec{v}_C| = |\vec{v}_{M/C}| = R\omega"
        ).next_to(eq_total_v, DOWN, buff=0.5)
        self.play(Write(mag_equality))
        self.wait(1.5)

        # Vector addition (head-to-tail)
        v_rot_arrow_moved = v_rot_arrow.copy().move_to(v_cm_arrow.get_end(), aligned_edge=v_rot_arrow.get_start())
        
        v_total_arrow = Arrow(
            start=mud_point_pos,
            end=v_rot_arrow_moved.get_end(),
            buff=0, color=V_TOTAL_COLOR
        )
        v_total_label = MathTex(r"\vec{v}_M").next_to(v_total_arrow, DOWN, buff=0.2)

        self.play(Transform(v_rot_arrow, v_rot_arrow_moved))
        self.play(Create(v_total_arrow), Write(v_total_label))
        self.wait(2)
        
        self.play(
            FadeOut(section_title), FadeOut(eq_total_v), FadeOut(mag_equality), FadeOut(wheel), FadeOut(hub),
            FadeOut(mud_dot), FadeOut(mud_label), FadeOut(v_cm_arrow), FadeOut(v_cm_label),
            FadeOut(v_rot_arrow), FadeOut(v_rot_label), FadeOut(v_total_arrow), FadeOut(v_total_label)
        )

    def section3_velocity_at_detachment(self):
        # Section 3: Velocity at the Detachment Point M
        section_title = Title("3. Velocity at the Detachment Point M").to_edge(UP)
        self.play(Write(section_title))

        # Re-create static wheel and point M
        wheel = Circle(radius=WHEEL_RADIUS, color=WHEEL_COLOR).move_to(ORIGIN)
        hub = Dot(wheel.get_center(), color=HUB_COLOR)
        
        mud_x_rel = WHEEL_RADIUS * np.cos(MUD_POINT_ANGLE_RAD)
        mud_y_rel = WHEEL_RADIUS * np.sin(MUD_POINT_ANGLE_RAD)
        mud_point_pos = wheel.get_center() + [mud_x_rel, mud_y_rel, 0]
        
        mud_dot = Dot(mud_point_pos, color=MUD_POINT_COLOR, radius=0.1)
        mud_label = MathTex("M").next_to(mud_dot, UP + RIGHT, buff=0.3)
        
        self.add(wheel, hub, mud_dot, mud_label)

        # v_CM (translational velocity)
        v_cm_arrow = Arrow(
            start=mud_point_pos,
            end=mud_point_pos + RIGHT * VELOCITY_MAG,
            buff=0, color=V_CM_COLOR
        )
        v_cm_label = MathTex(r"\vec{v}_C").next_to(v_cm_arrow, UP, buff=0.2)

        # v_rot (rotational velocity relative to center)
        rot_vel_x = VELOCITY_MAG * np.cos(MUD_POINT_ANGLE_RAD - PI/2)
        rot_vel_y = VELOCITY_MAG * np.sin(MUD_POINT_ANGLE_RAD - PI/2)
        
        v_rot_arrow = Arrow(
            start=mud_point_pos,
            end=mud_point_pos + [rot_vel_x, rot_vel_y, 0],
            buff=0, color=V_ROT_COLOR
        )
        v_rot_label = MathTex(r"\vec{v}_{M/C}").next_to(v_rot_arrow, RIGHT, buff=0.2)

        self.play(Create(v_cm_arrow), Write(v_cm_label), Create(v_rot_arrow), Write(v_rot_label))
        self.wait(1)

        # Resultant vector, which should be tangential
        v_total_end_point = mud_point_pos + [VELOCITY_MAG + rot_vel_x, rot_vel_y, 0] # Sum of v_C and v_rot components
        v_total_arrow = Arrow(
            start=mud_point_pos,
            end=v_total_end_point,
            buff=0, color=V_TOTAL_COLOR
        )
        v_total_label = MathTex(r"\vec{v}_M").next_to(v_total_arrow, DOWN, buff=0.2)

        self.play(Create(v_total_arrow), Write(v_total_label))
        self.wait(1)

        # Show that v_total is tangential to the wheel at M
        tangent_line = Line(
            v_total_arrow.get_start() - normalize(v_total_arrow.get_vector()) * 1,
            v_total_arrow.get_end() + normalize(v_total_arrow.get_vector()) * 1,
            color=YELLOW_B, stroke_width=2
        )
        highlight_tangent = Text("Instantaneous velocity is tangential!", font_size=30, color=YELLOW_B).to_edge(DOWN)
        self.play(Create(tangent_line), Write(highlight_tangent)) 
        self.wait(2)

        self.play(
            FadeOut(section_title), FadeOut(wheel), FadeOut(hub), FadeOut(mud_label),
            FadeOut(v_cm_arrow), FadeOut(v_cm_label), FadeOut(v_rot_arrow), FadeOut(v_rot_label),
            FadeOut(tangent_line), FadeOut(highlight_tangent)
        )
        # Keep mud_dot, v_total_arrow, v_total_label for the next section's animation
        self.add(mud_dot, v_total_arrow, v_total_label) 

    def section4_moment_of_detachment(self):
        # Section 4: The Moment of Detachment and Predicting Trajectory
        section_title = Title("4. The Moment of Detachment and Predicting Trajectory").to_edge(UP)
        self.play(Write(section_title))

        # Re-create wheel (as it was just faded out) for context
        wheel = Circle(radius=WHEEL_RADIUS, color=WHEEL_COLOR).move_to(ORIGIN)
        hub = Dot(wheel.get_center(), color=HUB_COLOR)
        
        mud_x_rel = WHEEL_RADIUS * np.cos(MUD_POINT_ANGLE_RAD)
        mud_y_rel = WHEEL_RADIUS * np.sin(MUD_POINT_ANGLE_RAD)
        mud_point_pos = wheel.get_center() + [mud_x_rel, mud_y_rel, 0]
        
        mud_dot = Dot(mud_point_pos, color=MUD_POINT_COLOR, radius=0.1)
        mud_label = MathTex("M").next_to(mud_dot, UP + RIGHT, buff=0.3)

        # The v_total_arrow and label should still be in the scene from previous section
        self.add(wheel, hub, mud_dot, mud_label) 

        # Newton's First Law
        newton_text = Text("Newton's First Law of Motion:", font_size=32).to_edge(LEFT).shift(UP*1.5)
        newton_desc = Text("Object continues with instantaneous velocity unless acted upon by a force.", font_size=28).next_to(newton_text, DOWN, aligned_edge=LEFT, buff=0.3)
        self.play(Write(newton_text), Write(newton_desc))
        self.wait(2)

        # Centripetal force explanation
        force_equation = MathTex(r"F_c = m\omega^2 R").next_to(wheel, RIGHT).shift(RIGHT*1)
        force_text = Text("Adhesive force provides centripetal force.", font_size=28).next_to(force_equation, DOWN, buff=0.3)
        self.play(Write(force_equation), Write(force_text))
        self.wait(2)

        # Animation of detachment
        initial_mud_pos = mud_dot.get_center()
        # Trajectory just follows the instantaneous velocity vector
        trajectory_end_point = initial_mud_pos + v_total_arrow.get_vector() * 3 
        
        def update_mud_trajectory(mobject, alpha):
            new_pos = initial_mud_pos + (trajectory_end_point - initial_mud_pos) * alpha
            mobject.move_to(new_pos)

        # Fade out wheel parts, mud flies off
        self.play(
            FadeOut(wheel), FadeOut(hub), FadeOut(mud_label), FadeOut(newton_text), FadeOut(newton_desc),
            FadeOut(force_equation), FadeOut(force_text)
        )
        self.play(
            UpdateFromFunc(mud_dot, update_mud_trajectory),
            run_time=2,
            rate_func=linear
        )
        self.play(FadeOut(v_total_arrow), FadeOut(v_total_label)) # Fade out the guiding arrow
        self.wait(1)

        # Reset mud_dot to its initial detachment point for arrow comparison
        mud_dot.move_to(mud_point_pos)
        self.add(wheel, hub, mud_dot, mud_label) # Bring back the wheel and mud dot for context
        self.play(FadeIn(wheel), FadeIn(hub), FadeIn(mud_label))

        # Possible arrows at M (A-E)
        arrow_length = WHEEL_RADIUS * 0.7
        arrows = VGroup()
        labels = VGroup()

        # Arrow A: Horizontal right (pure v_C)
        arrow_A = Arrow(mud_point_pos, mud_point_pos + RIGHT * arrow_length, color=INCORRECT_ARROW_COLOR)
        label_A = MathTex("A").next_to(arrow_A, UP, buff=0.2).set_color(INCORRECT_ARROW_COLOR)
        arrows.add(arrow_A); labels.add(label_A)

        # Arrow B: Horizontal left (opposite v_C)
        arrow_B = Arrow(mud_point_pos, mud_point_pos + LEFT * arrow_length, color=INCORRECT_ARROW_COLOR)
        label_B = MathTex("B").next_to(arrow_B, UP, buff=0.2).set_color(INCORRECT_ARROW_COLOR)
        arrows.add(arrow_B); labels.add(label_B)

        # Arrow C: Tangential (correct v_total) - Re-calculate direction based on fixed MUD_POINT_ANGLE_RAD
        rot_vel_x_dir = np.cos(MUD_POINT_ANGLE_RAD - PI/2)
        rot_vel_y_dir = np.sin(MUD_POINT_ANGLE_RAD - PI/2)
        v_total_dir = normalize(np.array([1 + rot_vel_x_dir, rot_vel_y_dir, 0])) # Simplified directional vector (v_C component = 1)
        arrow_C = Arrow(mud_point_pos, mud_point_pos + v_total_dir * arrow_length, color=CORRECT_ARROW_COLOR)
        label_C = MathTex("C").next_to(arrow_C, DOWN, buff=0.2).set_color(CORRECT_ARROW_COLOR)
        arrows.add(arrow_C); labels.add(label_C)

        # Arrow D: Vertical up
        arrow_D = Arrow(mud_point_pos, mud_point_pos + UP * arrow_length, color=INCORRECT_ARROW_COLOR)
        label_D = MathTex("D").next_to(arrow_D, LEFT, buff=0.2).set_color(INCORRECT_ARROW_COLOR)
        arrows.add(arrow_D); labels.add(label_D)

        # Arrow E: Radially outward
        radial_vec = normalize(mud_point_pos - wheel.get_center())
        arrow_E = Arrow(mud_point_pos, mud_point_pos + radial_vec * arrow_length, color=INCORRECT_ARROW_COLOR)
        label_E = MathTex("E").next_to(arrow_E, UP, buff=0.2).set_color(INCORRECT_ARROW_COLOR)
        arrows.add(arrow_E); labels.add(label_E)

        self.play(Create(arrows), Write(labels))
        self.wait(2)

        correct_text = Text("The initial direction is C, tangential to the wheel.", font_size=32, color=CORRECT_ARROW_COLOR).to_edge(DOWN)
        self.play(Circumscribe(arrow_C, color=CORRECT_ARROW_COLOR), Write(correct_text))
        self.wait(2.5)

        self.play(
            FadeOut(section_title), FadeOut(wheel), FadeOut(hub), FadeOut(mud_dot), FadeOut(mud_label),
            FadeOut(arrows), FadeOut(labels), FadeOut(correct_text)
        )

    def common_misunderstandings(self):
        title = Title("Common Misunderstandings").to_edge(UP)
        self.play(Write(title))

        # Re-create wheel and mud dot for context
        wheel = Circle(radius=WHEEL_RADIUS, color=WHEEL_COLOR).move_to(ORIGIN)
        hub = Dot(wheel.get_center(), color=HUB_COLOR)
        mud_x_rel = WHEEL_RADIUS * np.cos(MUD_POINT_ANGLE_RAD)
        mud_y_rel = WHEEL_RADIUS * np.sin(MUD_POINT_ANGLE_RAD)
        mud_point_pos = wheel.get_center() + [mud_x_rel, mud_y_rel, 0]
        mud_dot = Dot(mud_point_pos, color=MUD_POINT_COLOR, radius=0.1)
        mud_label = MathTex("M").next_to(mud_dot, UP + RIGHT, buff=0.3)
        self.add(wheel, hub, mud_dot, mud_label)

        # Misconception 1
        miscon1_text = Text("Misconception 1: Mud flies straight up or horizontally.", font_size=32).to_edge(LEFT).shift(UP*1.5)
        arrow_up = Arrow(mud_point_pos, mud_point_pos + UP*1, color=INCORRECT_ARROW_COLOR)
        arrow_horiz = Arrow(mud_point_pos, mud_point_pos + RIGHT*1, color=INCORRECT_ARROW_COLOR)
        self.play(Write(miscon1_text), Create(arrow_up), Create(arrow_horiz))
        correction1_text = Text("Correction: It ignores combined translational and rotational motion.", font_size=28, color=CORRECT_ARROW_COLOR).next_to(miscon1_text, DOWN, aligned_edge=LEFT, buff=0.3)
        self.play(Write(correction1_text))
        self.wait(2)
        self.play(FadeOut(arrow_up), FadeOut(arrow_horiz))

        # Misconception 2
        miscon2_text = Text("Misconception 2: Mud immediately falls straight down.", font_size=32).next_to(miscon1_text, DOWN*3, aligned_edge=LEFT)
        arrow_down = Arrow(mud_point_pos, mud_point_pos + DOWN*1, color=INCORRECT_ARROW_COLOR)
        self.play(Write(miscon2_text), Create(arrow_down))
        correction2_text = Text("Correction: Initial direction is set by instantaneous velocity.", font_size=28, color=CORRECT_ARROW_COLOR).next_to(miscon2_text, DOWN, aligned_edge=LEFT, buff=0.3)
        self.play(Write(correction2_text))
        self.wait(2)
        self.play(FadeOut(arrow_down))

        # Misconception 3
        miscon3_text = Text("Misconception 3: Mud flies radially outward.", font_size=32).next_to(miscon2_text, DOWN*3, aligned_edge=LEFT)
        radial_vec = normalize(mud_point_pos - wheel.get_center())
        arrow_radial = Arrow(mud_point_pos, mud_point_pos + radial_vec*1, color=INCORRECT_ARROW_COLOR)
        self.play(Write(miscon3_text), Create(arrow_radial))
        correction3_text = Text("Correction: Inertia dictates tangential motion at detachment.", font_size=28, color=CORRECT_ARROW_COLOR).next_to(miscon3_text, DOWN, aligned_edge=LEFT, buff=0.3)
        self.play(Write(correction3_text))
        self.wait(2)
        self.play(FadeOut(arrow_radial))

        self.play(FadeOut(title), FadeOut(wheel), FadeOut(hub), FadeOut(mud_dot), FadeOut(mud_label),
                  FadeOut(miscon1_text), FadeOut(correction1_text),
                  FadeOut(miscon2_text), FadeOut(correction2_text),
                  FadeOut(miscon3_text), FadeOut(correction3_text))

    def recap_summary(self):
        title = Title("Recap: Why the Mud Flies That Way").to_edge(UP)
        self.play(Write(title))

        summary_points = VGroup(
            Text("1. Rolling wheel has dual motion: translation + rotation.", font_size=30).to_edge(LEFT).shift(UP*1.5),
            Text("2. Velocity of any point = sum of translational and rotational velocities.", font_size=30).next_to(summary_points[0], DOWN, aligned_edge=LEFT, buff=0.5),
            Text("3. Detachment occurs when adhesive force fails.", font_size=30).next_to(summary_points[1], DOWN, aligned_edge=LEFT, buff=0.5),
            Text("4. Initial trajectory is tangential due to inertia.", font_size=30, color=V_TOTAL_COLOR).next_to(summary_points[2], DOWN, aligned_edge=LEFT, buff=0.5)
        )
        # Re-arrange to make sure next_to works correctly if summary_points is empty initially.
        summary_points = VGroup(
            Text("1. Rolling wheel has dual motion: translation + rotation.", font_size=30).to_edge(LEFT).shift(UP*1.5),
            Text("2. Velocity of any point = sum of translational and rotational velocities.", font_size=30),
            Text("3. Detachment occurs when adhesive force fails.", font_size=30),
            Text("4. Initial trajectory is tangential due to inertia.", font_size=30, color=V_TOTAL_COLOR)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).to_edge(LEFT).shift(UP*1.5)


        self.play(FadeIn(summary_points[0]), run_time=1)
        self.wait(0.5)
        self.play(FadeIn(summary_points[1]), run_time=1)
        self.wait(0.5)
        self.play(FadeIn(summary_points[2]), run_time=1)
        self.wait(0.5)
        self.play(FadeIn(summary_points[3]), run_time=1)
        self.wait(2.5)
        self.play(FadeOut(title), FadeOut(summary_points))

    def closing_call_to_action(self):
        closing_text = Text(
            "This principle extends far beyond mud! It's fundamental to understanding projectile motion from any rotating system.",
            font_size=36, text_to_color_map={"fundamental": YELLOW_C}
        ).to_center()
        
        call_to_action = Text(
            "What other real-world examples of combined motion can you spot? Let us know in the comments!",
            font_size=30, color=BLUE
        ).next_to(closing_text, DOWN, buff=0.7)

        self.play(Write(closing_text))
        self.wait(2.5)
        self.play(FadeIn(call_to_action))
        self.wait(3.5)
        self.play(FadeOut(closing_text), FadeOut(call_to_action))
