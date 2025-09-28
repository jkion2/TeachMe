from manim import *

class SolutionAnimation(Scene):
    def construct(self):
        # Create a static circle
        # By default, Circle is centered at the origin (0,0,0)
        circle = Circle(radius=1.5, color=BLUE, fill_opacity=0.8)

        # Add the circle to the scene instantly
        # It will appear and remain static
        self.add(circle)

        # Keep the circle on screen for 10 seconds
        self.wait(10)