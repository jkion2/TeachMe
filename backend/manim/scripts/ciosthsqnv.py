from manim import *

# Define constants for consistency and easy modification
WHEEL_RADIUS = 2.0
WHEEL_COLOR = BLUE_D
GROUND_COLOR = GREEN_D
TEXT_COLOR = WHITE
VELOCITY_COLOR = YELLOW
ROTATIONAL_COLOR = RED_C
RESULTANT_COLOR = GREEN_C
ANGULAR_VELOCITY = 0.5  # radians per second
LINEAR_VELOCITY = WHEEL_RADIUS * ANGULAR_VELOCITY  # V = R*omega for rolling without slipping

class SolutionAnimation(Scene):
    def construct(self):
        # 1. Rolling Without Slipping: The Basics
        self.intro_rolling_without_slipping()
        self.wait(1)

        # 2. Velocity of a Point on a Rolling Wheel
        self.velocity_of_a_point()
        self.wait(1)

        # 3. The Moment of Detachment: Inertia and Initial Direction
        self.moment_of_detachment()
        self.wait(1)

        # 4. Problem Solving: Identifying the Correct Direction for Point M
        self.problem_solving_point_m()
        self.wait(1)

        # 5. Common Misunderstandings & Recap
        self.common_misunderstandings_and_recap()
        self.wait(2) # Final pause for recap

    def intro_rolling_without_slipping(self):
        """Explains rolling without slipping and shows velocities."""
        title = Text("1. Rolling Without Slipping: The Basics", font_size=40).to_edge(UP).set_color(BLUE_C)
        self.play(Write(title))
        self.wait(0.5)

        # Ground line
        ground = Line(LEFT * FRAME_WIDTH / 2, RIGHT * FRAME_WIDTH / 2).shift(DOWN * WHEEL_RADIUS * 1.5)
        self.play(Create(ground))

        # Wheel setup
        wheel = Circle(radius=WHEEL_RADIUS, color=WHEEL_COLOR, fill_opacity=0.2)
        wheel.move_to(ORIGIN + UP * WHEEL_RADIUS + ground.get_y()) # Place wheel on ground
        
        center_dot = Dot(wheel.get_center(), color=WHITE)
        center_label = MathTex("O").next_to(center_dot, UP + LEFT * 0.5)

        point_p_loc = wheel.get_bottom()
        point_p_dot = Dot(point_p_loc, color=RED)
        point_p_label = MathTex("P").next_to(point_p_dot, DOWN)

        radius_line = Line(center_dot.get_center(), point_p_dot.get_center(), color=WHITE)
        radius_label = MathTex("R").next_to(radius_line, RIGHT, buff=0.1)

        wheel_group = VGroup(wheel, center_dot, center_label, point_p_dot, point_p_label, radius_line, radius_label)
        
        # Initial display
        self.play(
            Create(wheel_group[0]),
            FadeIn(wheel_group[1:]),
            run_time=1.5
        )
        self.wait(0.5)

        # Center velocity V
        v_cm_arrow = Arrow(center_dot.get_center() + LEFT * 0.5, center_dot.get_center() + RIGHT * 0.5, color=VELOCITY_COLOR)
        v_cm_label = MathTex("V").next_to(v_cm_arrow, UP)

        # Angular velocity omega
        omega_arc = Arc(start_angle=PI/2, end_angle=0, radius=0.5, arc_center=center_dot.get_center(), color=ROTATIONAL_COLOR)
        omega_arrow = Arrow(omega_arc.get_end(), omega_arc.point_at_angle(-PI/6), color=ROTATIONAL_COLOR) # Arrow pointing clockwise
        omega_label = MathTex("\\omega").next_to(omega_arc, RIGHT, buff=0.1)

        self.play(
            GrowArrow(v_cm_arrow), Write(v_cm_label),
            Create(omega_arc), GrowArrow(omega_arrow), Write(omega_label)
        )
        self.wait(0.5)

        # Rolling without slipping equation
        eq_rolling = MathTex("V = R\\omega").next_to(ground, UP * 2, buff=0.5).set_color(RESULTANT_COLOR)
        self.play(Write(eq_rolling))
        self.wait(1)

        # Animate wheel rolling and show velocities at key points
        description_text = Text("Point P (contact point) is momentarily at rest.", font_size=28).next_to(eq_rolling, UP, buff=0.5)
        self.play(FadeIn(description_text))

        # Velocity vectors at specific points for static illustration
        self.play(FadeOut(v_cm_arrow, v_cm_label, omega_arc, omega_arrow, omega_label)) # Temporarily hide

        v_center = Arrow(center_dot.get_center(), center_dot.get_center() + RIGHT * LINEAR_VELOCITY, color=VELOCITY_COLOR)
        v_center_label = MathTex("V").next_to(v_center, UP)
        
        v_top_loc = wheel.get_top()
        v_top = Arrow(v_top_loc, v_top_loc + RIGHT * LINEAR_VELOCITY * 2, color=VELOCITY_COLOR) # V_CM + v_rot (V+V = 2V)
        v_top_label = MathTex("2V").next_to(v_top, UP)

        v_bottom_loc = wheel.get_bottom()
        v_bottom = Arrow(v_bottom_loc, v_bottom_loc + RIGHT * LINEAR_VELOCITY * 0.1, color=VELOCITY_COLOR) # Emphasize 0 velocity, tiny arrow
        v_bottom_label = MathTex("0").next_to(v_bottom, DOWN)

        self.play(
            GrowArrow(v_center), Write(v_center_label),
            GrowArrow(v_top), Write(v_top_label),
            GrowArrow(v_bottom), Write(v_bottom_label)
        )
        self.wait(1.5)

        self.play(
            FadeOut(description_text, v_center, v_center_label, v_top, v_top_label, v_bottom, v_bottom_label)
        )

        # Animate rolling
        rolling_text = Text("Wheel rolling to the right", font_size=30).next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(rolling_text))

        def update_wheel_group(mobject, dt):
            mobject.shift(RIGHT * LINEAR_VELOCITY * dt)
            # Rotate around its own center, which is the center_dot's current position (mobject[1])
            mobject.rotate(-ANGULAR_VELOCITY * dt, about_point=mobject[1].get_center()) 
            # Update P's position and label
            mobject[3].move_to(mobject[0].get_bottom()) # point_p_dot
            mobject[4].next_to(mobject[3], DOWN) # point_p_label
            # Update radius line
            mobject[5].put_start_and_end_on(mobject[1].get_center(), mobject[3].get_center())
            mobject[6].next_to(mobject[5], RIGHT, buff=0.1)

        wheel_group.add_updater(update_wheel_group)
        self.add(wheel_group) # Add the group with updater
        self.wait(4)
        wheel_group.clear_updaters() # Stop the animation
        self.play(FadeOut(wheel_group, rolling_text, eq_rolling, title, ground))

    def velocity_of_a_point(self):
        """Illustrates vector addition for velocity of a point on the rim."""
        title = Text("2. Velocity of a Point on a Rolling Wheel", font_size=40).to_edge(UP).set_color(BLUE_C)
        self.play(Write(title))
        self.wait(0.5)

        ground = Line(LEFT * FRAME_WIDTH / 2, RIGHT * FRAME_WIDTH / 2).shift(DOWN * WHEEL_RADIUS * 1.5)
        self.add(ground)

        # Wheel setup (static for vector demonstration)
        wheel = Circle(radius=WHEEL_RADIUS, color=WHEEL_COLOR, fill_opacity=0.2)
        wheel.move_to(ORIGIN + UP * WHEEL_RADIUS + ground.get_y())
        center_dot = Dot(wheel.get_center(), color=WHITE)
        center_label = MathTex("O").next_to(center_dot, UP + LEFT * 0.5)
        
        # Mud particle M in the upper-right quadrant
        mud_angle_ccw = PI/4 # Counter-clockwise from positive x-axis (45 degrees)
        mud_point_loc = wheel.point_at_angle(mud_angle_ccw)
        mud_dot = Dot(mud_point_loc, color=YELLOW)
        mud_label = MathTex("M").next_to(mud_dot, UP + RIGHT * 0.5)
        
        self.play(
            Create(wheel),
            FadeIn(center_dot, center_label),
            FadeIn(mud_dot, mud_label)
        )
        self.wait(0.5)

        # Velocity vectors at M
        # Translational velocity V_CM (same as wheel center, to the right)
        v_display_length = LINEAR_VELOCITY * 1.5 # Scale for visual clarity
        v_cm_particle_arrow = Arrow(mud_point_loc, mud_point_loc + RIGHT * v_display_length, color=VELOCITY_COLOR)
        v_cm_particle_label = MathTex("\\vec{V}_{CM}").next_to(v_cm_particle_arrow, DOWN * 0.5)

        # Rotational velocity v_rot (tangential to wheel, clockwise rotation)
        # Manim's get_tangent_at_angle gives CCW tangent. For CW, it's the same direction.
        # E.g., at top (PI/2), get_tangent_at_angle gives LEFT. If CW, v_rot is also LEFT.
        # At right (0), get_tangent_at_angle gives UP. If CW, v_rot is DOWN.
        # So, the unit tangent vector for CW rotation:
        # If angle is `a` (CCW from positive x), then radial vector is (cos a, sin a).
        # Tangential vector for CW is (sin a, -cos a) in standard coordinates.
        # Manim's `get_tangent_at_angle(a)` returns `(-sin a, cos a)`.
        # So, the component for CW rotation must be `-1 * (Manim's default CCW tangent rotated by PI)`
        # Or more simply, if we want clockwise rotation, and angle is CCW:
        # at PI/4 (top-right), rotation is clockwise, so v_rot is UP-LEFT.
        # get_tangent_at_angle(PI/4) -> (-0.707, 0.707) which is UP-LEFT. So Manim's default is correct.
        v_rot_direction_unit = wheel.get_tangent_at_angle(mud_angle_ccw)
        v_rot_particle_arrow = Arrow(mud_point_loc, mud_point_loc + v_rot_direction_unit * v_display_length, color=ROTATIONAL_COLOR)
        v_rot_particle_label = MathTex("\\vec{v}_{rot}").next_to(v_rot_particle_arrow, LEFT * 0.5 + UP * 0.5)

        self.play(
            GrowArrow(v_cm_particle_arrow), Write(v_cm_particle_label),
            GrowArrow(v_rot_particle_arrow), Write(v_rot_particle_label)
        )
        self.wait(1)

        # Vector addition equation
        eq_vector_sum = MathTex("\\vec{v}_{particle} = \\vec{V}_{CM} + \\vec{v}_{rot}").next_to(ground, UP * 2, buff=0.5).set_color(RESULTANT_COLOR)
        self.play(Write(eq_vector_sum))
        self.wait(0.5)

        # Show resultant vector using parallelogram rule
        resultant_vector = v_cm_particle_arrow.get_vector() + v_rot_particle_arrow.get_vector()
        resultant_arrow = Arrow(mud_point_loc, mud_point_loc + resultant_vector, color=RESULTANT_COLOR)
        resultant_label = MathTex("\\vec{v}_{particle}").next_to(resultant_arrow, RIGHT * 0.5)

        # Dashed lines for parallelogram
        dashed_line_1 = DashedLine(
            mud_point_loc + v_cm_particle_arrow.get_vector(),
            mud_point_loc + resultant_vector,
            color=GRAY_A
        )
        dashed_line_2 = DashedLine(
            mud_point_loc + v_rot_particle_arrow.get_vector(),
            mud_point_loc + resultant_vector,
            color=GRAY_A
        )

        self.play(
            Create(dashed_line_1), Create(dashed_line_2),
            GrowArrow(resultant_arrow), Write(resultant_label)
        )
        self.wait(2)
        self.play(FadeOut(
            title, ground, wheel, center_dot, center_label, mud_dot, mud_label,
            v_cm_particle_arrow, v_cm_particle_label,
            v_rot_particle_arrow, v_rot_particle_label,
            eq_vector_sum, resultant_arrow, resultant_label, dashed_line_1, dashed_line_2
        ))

    def moment_of_detachment(self):
        """Explains that detached mud follows instantaneous velocity due to inertia."""
        title = Text("3. The Moment of Detachment: Inertia", font_size=40).to_edge(UP).set_color(BLUE_C)
        self.play(Write(title))
        self.wait(0.5)

        ground = Line(LEFT * FRAME_WIDTH / 2, RIGHT * FRAME_WIDTH / 2).shift(DOWN * WHEEL_RADIUS * 1.5)
        self.add(ground)
        wheel = Circle(radius=WHEEL_RADIUS, color=WHEEL_COLOR, fill_opacity=0.2)
        wheel.move_to(ORIGIN + UP * WHEEL_RADIUS + ground.get_y())
        center_dot = Dot(wheel.get_center(), color=WHITE)
        center_label = MathTex("O").next_to(center_dot, UP + LEFT * 0.5)
        
        # Mud particle M
        mud_angle_ccw = PI/4 # Counter-clockwise from positive x-axis
        mud_point_loc = wheel.point_at_angle(mud_angle_ccw)
        mud_dot = Dot(mud_point_loc, color=YELLOW)
        mud_label = MathTex("M").next_to(mud_dot, UP + RIGHT * 0.5)

        self.play(
            Create(wheel), FadeIn(center_dot, center_label), FadeIn(mud_dot, mud_label)
        )
        self.wait(0.5)

        # Calculate the resultant velocity vector direction for M
        v_cm_direction_unit = RIGHT
        v_rot_direction_unit = wheel.get_tangent_at_angle(mud_angle_ccw)
        # Magnitudes are equal (V=R*omega), so vector sum is simple
        resultant_direction_unit = normalize(v_cm_direction_unit + v_rot_direction_unit)
        
        resultant_arrow = Arrow(mud_point_loc, mud_point_loc + resultant_direction_unit * 2, color=RESULTANT_COLOR)
        resultant_label = MathTex("\\vec{v}_{initial}").next_to(resultant_arrow, RIGHT * 0.5 + UP * 0.5)

        self.play(GrowArrow(resultant_arrow), Write(resultant_label))
        self.wait(0.5)

        # Detachment animation
        detachment_path = Line(mud_point_loc, mud_point_loc + resultant_direction_unit * 3, color=RESULTANT_COLOR)
        
        detachment_text_1 = Text("Detachment = Instantaneous Velocity", font_size=30).to_edge(LEFT).shift(UP * 1.5)
        detachment_text_2 = Text("Newton's First Law (Inertia)", font_size=30).next_to(detachment_text_1, DOWN, aligned_edge=LEFT)
        detachment_text_group = VGroup(detachment_text_1, detachment_text_2)

        mud_dot_detaching = mud_dot.copy().set_color(YELLOW)
        self.play(
            Transform(mud_dot_detaching, Dot(detachment_path.get_end(), color=YELLOW)), # Final position of the mud particle
            MoveAlongPath(mud_dot_detaching, detachment_path),
            Write(detachment_text_group)
        )
        self.wait(1)

        self.play(FadeOut(
            title, ground, wheel, center_dot, center_label, mud_label, mud_dot,
            resultant_arrow, resultant_label, mud_dot_detaching, detachment_text_group
        ))

    def problem_solving_point_m(self):
        """Applies the vector addition to determine the flight path for point M."""
        title = Text("4. Problem Solving: Detachment at Point M", font_size=40).to_edge(UP).set_color(BLUE_C)
        self.play(Write(title))
        self.wait(0.5)

        ground = Line(LEFT * FRAME_WIDTH / 2, RIGHT * FRAME_WIDTH / 2).shift(DOWN * WHEEL_RADIUS * 1.5)
        self.add(ground)

        wheel = Circle(radius=WHEEL_RADIUS, color=WHEEL_COLOR, fill_opacity=0.2)
        wheel.move_to(ORIGIN + UP * WHEEL_RADIUS + ground.get_y())
        self.add(wheel)

        center_dot = Dot(wheel.get_center(), color=WHITE)
        center_label = MathTex("O").next_to(center_dot, UP + LEFT * 0.5)
        self.add(center_dot, center_label)

        # Mud particle M (same location as previous sections)
        mud_angle_ccw = PI/4 # Counter-clockwise from positive x-axis
        mud_point_loc = wheel.point_at_angle(mud_angle_ccw)
        mud_dot = Dot(mud_point_loc, color=YELLOW)
        mud_label = MathTex("M").next_to(mud_dot, UP + RIGHT * 0.5)
        self.add(mud_dot, mud_label)
        self.wait(0.5)

        v_display_length = LINEAR_VELOCITY * 1.5 # Consistent display length

        # 1. Translational Velocity (V_CM)
        step_1_text = Text("1. Translational Velocity ", font_size=30).to_edge(LEFT).shift(UP * 1.5)
        v_cm_label_text = MathTex("\\vec{V}_{CM}").next_to(step_1_text, RIGHT)
        step_1_group = VGroup(step_1_text, v_cm_label_text).to_edge(LEFT)
        self.play(Write(step_1_group))

        v_cm_particle_arrow = Arrow(mud_point_loc, mud_point_loc + RIGHT * v_display_length, color=VELOCITY_COLOR)
        v_cm_particle_label = MathTex("\\vec{V}_{CM}").next_to(v_cm_particle_arrow, DOWN * 0.5)
        self.play(GrowArrow(v_cm_particle_arrow), Write(v_cm_particle_label))
        self.wait(1)
        self.play(FadeOut(step_1_group))

        # 2. Rotational Velocity (v_rot)
        step_2_text = Text("2. Rotational Velocity ", font_size=30).to_edge(LEFT).shift(UP * 1.5)
        v_rot_label_text = MathTex("\\vec{v}_{rot}").next_to(step_2_text, RIGHT)
        step_2_group = VGroup(step_2_text, v_rot_label_text).to_edge(LEFT)
        self.play(Write(step_2_group))

        v_rot_direction_unit = wheel.get_tangent_at_angle(mud_angle_ccw)
        v_rot_particle_arrow = Arrow(mud_point_loc, mud_point_loc + v_rot_direction_unit * v_display_length, color=ROTATIONAL_COLOR)
        v_rot_particle_label = MathTex("\\vec{v}_{rot}").next_to(v_rot_particle_arrow, LEFT * 0.5 + UP * 0.5)
        self.play(GrowArrow(v_rot_particle_arrow), Write(v_rot_particle_label))
        self.wait(1)
        self.play(FadeOut(step_2_group))

        # 3. Vector Sum
        step_3_text = Text("3. Vector Sum", font_size=30).to_edge(LEFT).shift(UP * 1.5)
        self.play(Write(step_3_text))

        # Dashed lines for parallelogram
        resultant_vector_sum = v_cm_particle_arrow.get_vector() + v_rot_particle_arrow.get_vector()
        dashed_line_1 = DashedLine(
            mud_point_loc + v_cm_particle_arrow.get_vector(),
            mud_point_loc + resultant_vector_sum,
            color=GRAY_A
        )
        dashed_line_2 = DashedLine(
            mud_point_loc + v_rot_particle_arrow.get_vector(),
            mud_point_loc + resultant_vector_sum,
            color=GRAY_A
        )
        self.play(Create(dashed_line_1), Create(dashed_line_2))

        resultant_arrow = Arrow(mud_point_loc, mud_point_loc + resultant_vector_sum, color=RESULTANT_COLOR)
        self.play(GrowArrow(resultant_arrow))
        self.wait(1)

        # "Arrow E" representation
        arrow_e_label = MathTex("\\text{Arrow E}").next_to(resultant_arrow, RIGHT * 0.5 + UP * 0.5).set_color(RESULTANT_COLOR)
        self.play(Write(arrow_e_label))
        self.wait(1)

        self.play(FadeOut(
            title, ground, wheel, center_dot, center_label, mud_dot, mud_label,
            v_cm_particle_arrow, v_cm_particle_label,
            v_rot_particle_arrow, v_rot_particle_label,
            dashed_line_1, dashed_line_2,
            resultant_arrow, arrow_e_label, step_3_text
        ))

    def common_misunderstandings_and_recap(self):
        """Highlights common errors and recaps the main points."""
        title = Text("5. Common Misunderstandings & Recap", font_size=40).to_edge(UP).set_color(BLUE_C)
        self.play(Write(title))
        self.wait(0.5)

        ground = Line(LEFT * FRAME_WIDTH / 2, RIGHT * FRAME_WIDTH / 2).shift(DOWN * WHEEL_RADIUS * 1.5)
        self.add(ground)

        wheel = Circle(radius=WHEEL_RADIUS, color=WHEEL_COLOR, fill_opacity=0.2)
        wheel.move_to(ORIGIN + UP * WHEEL_RADIUS + ground.get_y())
        self.add(wheel)

        mud_angle_ccw = PI/4 # Counter-clockwise from positive x-axis
        mud_point_loc = wheel.point_at_angle(mud_angle_ccw)
        mud_dot = Dot(mud_point_loc, color=YELLOW)
        mud_label = MathTex("M").next_to(mud_dot, UP + RIGHT * 0.5)
        self.add(mud_dot, mud_label)

        # Correct direction (Arrow E)
        v_cm_direction_unit = RIGHT
        v_rot_direction_unit = wheel.get_tangent_at_angle(mud_angle_ccw)
        resultant_direction_unit = normalize(v_cm_direction_unit + v_rot_direction_unit)
        correct_arrow = Arrow(mud_point_loc, mud_point_loc + resultant_direction_unit * 2.5, color=RESULTANT_COLOR)
        correct_label = Text("Correct: Tangential to Path", font_size=28).next_to(correct_arrow, UP + RIGHT).set_color(GREEN)

        self.play(GrowArrow(correct_arrow), Write(correct_label))
        self.wait(1)

        # Incorrect: Radial path
        radial_direction_unit = normalize(mud_point_loc - wheel.get_center())
        incorrect_radial_arrow = Arrow(mud_point_loc, mud_point_loc + radial_direction_unit * 2, color=RED)
        incorrect_radial_label = Text("Incorrect: Radial!", font_size=28).next_to(incorrect_radial_arrow, RIGHT).set_color(RED)
        
        self.play(
            FadeOut(correct_arrow, correct_label), # Hide correct to show incorrect
            GrowArrow(incorrect_radial_arrow), Write(incorrect_radial_label)
        )
        self.wait(1)
        self.play(FadeOut(incorrect_radial_arrow, incorrect_radial_label))

        # Incorrect: Just translational
        incorrect_translational_arrow = Arrow(mud_point_loc, mud_point_loc + RIGHT * 2, color=RED)
        incorrect_translational_label = Text("Incorrect: Just Translational!", font_size=28).next_to(incorrect_translational_arrow, DOWN).set_color(RED)
        
        self.play(GrowArrow(incorrect_translational_arrow), Write(incorrect_translational_label))
        self.wait(1)
        self.play(FadeOut(incorrect_translational_arrow, incorrect_translational_label))

        # Bring back correct path
        self.play(GrowArrow(correct_arrow), Write(correct_label))
        self.wait(1)

        # Recap points
        recap_title = Text("Key Takeaways:", font_size=36).to_edge(LEFT).shift(UP * 1.5).set_color(BLUE_C)
        bullet_1 = MathTex("\\bullet ", "V = R\\omega").next_to(recap_title, DOWN, aligned_edge=LEFT)
        bullet_2 = MathTex("\\bullet ", "\\vec{v}_{particle} = \\vec{V}_{CM} + \\vec{v}_{rot}").next_to(bullet_1, DOWN, aligned_edge=LEFT)
        bullet_3 = MathTex("\\bullet ", "\\text{Detachment direction: Tangent to the actual path}").next_to(bullet_2, DOWN, aligned_edge=LEFT)
        bullet_4 = MathTex("\\bullet ", "\\text{For point M, the correct direction is Arrow E.}").next_to(bullet_3, DOWN, aligned_edge=LEFT)
        
        recap_group = VGroup(recap_title, bullet_1, bullet_2, bullet_3, bullet_4).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(LEFT)
        
        self.play(
            FadeOut(title, correct_arrow, correct_label, mud_dot, mud_label, wheel, ground),
            Write(recap_group, run_time=2)
        )
        self.wait(3)

        self.play(FadeOut(recap_group))
