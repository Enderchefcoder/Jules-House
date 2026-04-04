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
            elif item == 'Metal':
                 ax.text(x + 0.5, y + 0.5, 'M', ha='center', va='center',
                         fontsize=16, color='gray', fontweight='bold')
            elif item == 'Data':
                 ax.text(x + 0.5, y + 0.5, 'D', ha='center', va='center',
                         fontsize=16, color='cyan', fontweight='bold')
            elif item == 'market_hub':
                 ax.text(x + 0.5, y + 0.5, 'H', ha='center', va='center',
                         fontsize=16, color='orange', fontweight='bold')

    ax.set_title("AETHER Simulation State", fontsize=16)
    ax.set_xlim(0, world.width)
    ax.set_ylim(0, world.height)

    plt.savefig(filename)
    plt.close()
    print(f"Visualization saved to {filename}")

def render_grid_3d(world, filename="visual/aether_3d_v1.png"):
    """Renders the World3D state using matplotlib 3D and saves it."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Render obstacles
    if world.obstacles:
        obs_x, obs_y, obs_z = zip(*world.obstacles)
        ax.scatter(obs_x, obs_y, obs_z, c='red', marker='s', s=100, label='Obstacle', alpha=0.5)

    # Render items
    items_by_type = {}
    for pos, itype in world.items.items():
        if itype not in items_by_type: items_by_type[itype] = []
        items_by_type[itype].append(pos)

    color_map = {
        'charger': ('green', 'o', 'Charger'),
        'Metal': ('gray', 'h', 'Metal Resource'),
        'Data': ('cyan', 'D', 'Data Resource'),
        'market_hub': ('orange', 'P', 'Market Hub')
    }

    for itype, positions in items_by_type.items():
        if positions and itype in color_map:
            color, marker, label = color_map[itype]
            x, y, z = zip(*positions)
            ax.scatter(x, y, z, c=color, marker=marker, s=100, label=label, alpha=0.8)

    # Render agents
    if world.agents:
        ag_pos = list(world.agents.keys())
        ag_x, ag_y, ag_z = zip(*ag_pos)
        ax.scatter(ag_x, ag_y, ag_z, c='blue', marker='^', s=200, label='Humanoid', alpha=1.0)

        for pos, agent in world.agents.items():
            ax.text(pos[0], pos[1], pos[2] + 0.5, agent.name, color='blue', fontsize=8)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title("AETHER Integrated Simulation (AETHER + CHRONOS)", fontsize=16)
    ax.legend(loc='upper left', bbox_to_anchor=(1.05, 1))

    ax.set_xlim(0, world.width)
    ax.set_ylim(0, world.height)
    ax.set_zlim(0, world.depth)

    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    print(f"3D Visualization saved to {filename}")

if __name__ == "__main__":
    print("Visualizer updated.")
