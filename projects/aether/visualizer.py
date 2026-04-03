import matplotlib.pyplot as plt
import numpy as np
import os

def render_grid(world, filename="visual/aether_v1.png"):
    """Renders the WorldGrid state using matplotlib and saves it."""
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 8))

    # Grid background
    grid_data = np.zeros((world.height, world.width))
    ax.imshow(grid_data, cmap='Greys', extent=[0, world.width, 0, world.height], origin='lower')

    # Draw grid lines
    ax.set_xticks(np.arange(0, world.width + 1, 1))
    ax.set_yticks(np.arange(0, world.height + 1, 1))
    ax.grid(which='both', color='black', linestyle='-', linewidth=1)

    for y in range(world.height):
        for x in range(world.width):
            # Check for agents
            agent = world.grid[y][x]
            if agent:
                ax.text(x + 0.5, y + 0.5, 'R', ha='center', va='center',
                        fontsize=20, color='blue', fontweight='bold')
                ax.add_patch(plt.Circle((x + 0.5, y + 0.5), 0.3, color='blue', alpha=0.3))

            # Check for items
            item = world.get_item((x, y))
            if item == 'obstacle':
                 ax.text(x + 0.5, y + 0.5, 'X', ha='center', va='center',
                         fontsize=20, color='red', fontweight='bold')
                 ax.add_patch(plt.Rectangle((x, y), 1, 1, color='red', alpha=0.2))
            elif item == 'charger':
                 ax.text(x + 0.5, y + 0.5, 'C', ha='center', va='center',
                         fontsize=20, color='green', fontweight='bold')
                 ax.add_patch(plt.Circle((x + 0.5, y + 0.5), 0.2, color='green', alpha=0.3))

    ax.set_title("AETHER Simulation State", fontsize=16)
    ax.set_xlim(0, world.width)
    ax.set_ylim(0, world.height)

    plt.savefig(filename)
    plt.close()
    print(f"Visualization saved to {filename}")

if __name__ == "__main__":
    # Internal test
    from world.grid import WorldGrid
    w = WorldGrid(10, 10)
    w.place_item('obstacle', (2, 2))
    w.place_item('obstacle', (2, 3))
    w.place_item('charger', (8, 8))

    class FakeAgent: pass
    w.place_agent(FakeAgent(), (5, 5))

    render_grid(w, "visual/aether_test.png")
    # Also save as v1 as per plan
    render_grid(w, "visual/aether_v1.png")
