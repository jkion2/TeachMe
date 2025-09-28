from manim import *

class SolutionAnimation(Scene):
    def construct(self):
        # Set the background color to black
        self.camera.background_color = BLACK

        # Calculate the final radius for the circle
        # Diameter is 30% of screen height, so radius is 15% of screen height
        screen_height = self.camera.frame_height
        final_radius = 0.15 * screen_height

        # Create the circle mobject
        # It should be white, have a stroke width of 5, and no fill
        circle_outline = Circle(
            radius=final_radius,
            color=WHITE,
            stroke_width=5,
            fill_opacity=0  # No fill
        )
        # Ensure the circle is perfectly centered (which is default for Circle)
        circle_outline.move_to(ORIGIN)

        # --- Animation Sequence ---

        # 0 to 0.5 seconds: Screen is completely black
        self.wait(0.5)

        # 0.5 to 1.5 seconds: White circular outline grows from the center
        # The Create animation draws the circle path smoothly
        self.play(
            Create(circle_outline),
            run_time=1.0  # Duration of the growth animation
        )

        # 1.5 to 2 seconds: The fully formed white circular outline holds static
        self.wait(0.5)