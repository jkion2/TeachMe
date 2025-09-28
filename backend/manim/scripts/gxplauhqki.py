from manim import *

class SolutionAnimation(Scene):
    def construct(self):
        # Constants for consistency
        CIRCLE_COLOR = WHITE
        DOT_COLOR = WHITE
        CIRCLE_RADIUS = 2.0
        CIRCLE_STROKE_WIDTH = 3 # "thin white line"
        PULSE_SCALE_FACTOR = 1.05 # 5% larger for subtle pulse
        PULSE_CYCLE_DURATION = 3.0 # seconds for one full pulse cycle (scale up and down)

        # --- 1. The Emergence (0-8 seconds) ---
        # 1.1 Brief moment of black screen (default background)
        self.wait(0.5) # Start at 0.5s

        # 1.2 A single, bright white point appears at the center.
        center_dot = Dot(ORIGIN, color=DOT_COLOR, radius=0.08)
        self.play(FadeIn(center_dot, scale=0.5), run_time=0.8) # 0.5 + 0.8 = 1.3s
        self.wait(0.2) # 1.3 + 0.2 = 1.5s

        # 1.3 A thin white line extends from the center, rotating 360 degrees to trace a perfect circle.
        # Manim's Create(Circle) visually traces the circumference, starting from the rightmost point.
        circle = Circle(
            radius=CIRCLE_RADIUS,
            color=CIRCLE_COLOR,
            stroke_width=CIRCLE_STROKE_WIDTH
        ).move_to(ORIGIN) # Ensure it's perfectly centered
        self.play(Create(circle), run_time=5.8) # 1.5 + 5.8 = 7.3s

        # 1.4 The center dot fades, leaving only the pure, static white circle.
        self.play(FadeOut(center_dot), run_time=0.5) # 7.3 + 0.5 = 7.8s
        self.wait(0.5) # 7.8 + 0.5 = 8.3s. This concludes the emergence phase.

        # --- 2. The Stillness (8-18 seconds) ---
        # The fully formed, static white circle remains. It gently pulsates.
        # This phase should last approximately 9.7 seconds (18s - 8.3s).
        # We'll use 3 full pulse cycles. Each cycle scales up and then back down.
        num_pulse_cycles = 3
        for _ in range(num_pulse_cycles):
            self.play(
                circle.animate.scale(PULSE_SCALE_FACTOR),
                run_time=PULSE_CYCLE_DURATION,
                rate_func=there_and_back # Scales up to factor, then back to original size
            )
        # Total pulse animation time: 3 cycles * 3.0s/cycle = 9.0 seconds.
        # Current time: 8.3s + 9.0s = 17.3s
        self.wait(0.7) # Add a short wait to bring total time to 17.3 + 0.7 = 18.0s

        # --- 3. Closing (18-20 seconds) ---
        # The circle slowly and smoothly fades to black.
        self.play(FadeOut(circle), run_time=2.0) # 18.0 + 2.0 = 20.0s

        # End screen black.
        self.wait(0.5) # A final brief wait to ensure the screen is fully black before ending.