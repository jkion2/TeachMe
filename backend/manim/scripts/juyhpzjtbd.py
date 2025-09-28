from manim import *

class SolutionAnimation(Scene):
    def construct(self):
        # Create a simple circle
        circle = Circle(radius=1.5, color=BLUE, fill_opacity=0.5)

        # Animation: Create the circle, display it, then fade it out
        self.play(Create(circle))  # Draw the circle on screen
        self.wait(2)               # Wait for 2 seconds
        self.play(FadeOut(circle)) # Remove the circle from screen