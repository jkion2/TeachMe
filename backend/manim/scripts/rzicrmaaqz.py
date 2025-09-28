from manim import *

class SolutionAnimation(Scene):
    def construct(self):
        # Create a perfect white circle
        # Set radius to 1 unit (default for Circle) for a perfect circle
        # Set fill_color to WHITE and fill_opacity to 1 for a solid white circle
        circle = Circle(radius=1.0, color=WHITE, fill_opacity=1.0)
        
        # Ensure the circle is perfectly centered on the screen
        circle.move_to(ORIGIN)
        
        # Add the circle to the scene without any animation
        # This makes it appear instantly and static
        self.add(circle)
        
        # Keep the circle on screen for 5 seconds
        self.wait(5)