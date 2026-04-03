from robot import Robot
import time

def simulate_day():
    print("--- Starting Factory Robot Simulation (A Day in the Life) ---")

    # Initialize our robot, OTTO, at its charging base (0, 0)
    otto = Robot("OTTO-2026", battery_level=90, position=(0, 0))
    print(otto.report_status())

    # Task 1: Move to Station A (10, 5) to pick up parts
    print("\nTask 1: Moving to Station A...")
    if otto.move(10, 5):
        print("OTTO has arrived at Station A. Picking up parts...")
        time.sleep(0.5) # Simulate picking up parts
        # Let's say performing the task consumes some extra battery
        otto.battery_level -= 5
        print(f"Task complete! {otto.report_status()}")

    # Task 2: Move to Station B (-5, 15) to deliver parts
    print("\nTask 2: Moving to Station B...")
    # Calculating displacement from current position (10, 5) to (-5, 15)
    dx = -15
    dy = 10
    if otto.move(dx, dy):
        print("OTTO has arrived at Station B. Delivering parts...")
        time.sleep(0.5) # Simulate delivering parts
        otto.battery_level -= 8
        print(f"Task complete! {otto.report_status()}")

    # Task 3: Return to Charging Base (0, 0)
    print("\nTask 3: Returning to Base for Recharge...")
    # Calculating displacement from current position (-5, 15) to (0, 0)
    dx = 5
    dy = -15
    if otto.move(dx, dy):
        print("OTTO has returned to base.")
        otto.recharge(50)
        print(f"Ready for the next shift! {otto.report_status()}")
    else:
        print("Oh no! OTTO is stranded and needs manual assistance.")

    print("\n--- Simulation Complete ---")

if __name__ == "__main__":
    simulate_day()
