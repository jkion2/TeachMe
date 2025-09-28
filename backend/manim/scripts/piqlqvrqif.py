from manim import *

class SolutionAnimation(Scene):
    def construct(self):
        # Create a simple circle
        circle = Circle(radius=1.0, color=BLUE, fill_opacity=0.8)

        # Make the circle appear quickly (e.g., FadeIn)
        self.play(FadeIn(circle), run_time=0.5)

        # Keep the circle visible for the remaining duration to total 2 seconds
        self.wait(1.5)