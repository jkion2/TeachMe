from manim import *

class SolutionAnimation(Scene):
    def construct(self):
        # Set background color
        self.camera.background_color = "#363636" # Neutral dark gray

        # Define circle properties
        circle_color = BLUE
        circle_radius = self.camera.frame_height * 0.2 # 40% of screen height for diameter, so 20% for radius
        
        # Create the solid blue circle
        circle = Circle(
            radius=circle_radius,
            color=circle_color,
            fill_opacity=1,
            stroke_width=0 # No border, just solid fill
        )
        
        # Place the circle in the center of the screen
        circle.move_to(ORIGIN)

        # Fade in the circle over 0.5 seconds
        self.play(FadeIn(circle, run_time=0.5))

        # Keep the circle static for the remaining 1.5 seconds
        self.wait(1.5)