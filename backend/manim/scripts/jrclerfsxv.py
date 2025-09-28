from manim import *

class SolutionAnimation(Scene):
    def construct(self):
        # Define the circle centered at the origin with a radius of 2 units
        # Default color for Circle is BLUE, and default center is ORIGIN,
        # but specifying for clarity.
        circle = Circle(radius=2, color=BLUE, fill_opacity=0)

        # Animate the drawing of the circle
        self.play(Create(circle))

        # Pause at the end of the animation
        self.wait(1)