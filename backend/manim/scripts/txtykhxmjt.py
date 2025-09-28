from manim import *

class SolutionAnimation(Scene):
    def construct(self):
        # Create a simple circle centered at the origin
        # Manim's Circle defaults to radius=1 and center=ORIGIN
        circle = Circle(color=BLUE)

        # Animate the drawing of the circle
        self.play(Create(circle))

        # Keep the circle on screen for a moment
        self.wait(1)

        # Optionally, fade out the circle at the end
        self.play(FadeOut(circle))