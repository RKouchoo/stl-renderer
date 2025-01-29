import sys
from stl import mesh
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def load_stl(file_path):
    """Load an STL file."""
    return mesh.Mesh.from_file(file_path)

def calculate_dimensions(stl_mesh):
    """Calculate the bounding box dimensions of the mesh."""
    points = np.vstack((stl_mesh.v0, stl_mesh.v1, stl_mesh.v2))
    min_point = np.min(points, axis=0)
    max_point = np.max(points, axis=0)
    return min_point, max_point

def render_stl_with_dimensions(stl_mesh, dimensions):
    """Render the STL mesh with bounding box dimensions as text."""
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot the mesh
    tris = Poly3DCollection(stl_mesh.vectors)
    tris.set_edgecolor('k')
    
    # Calculate center for text placement
    min_point, max_point = dimensions
    center_point = (min_point + max_point) / 2.0
    
    ax.add_collection3d(tris)

    # Auto scale to the mesh size
    scale = np.concatenate([stl_mesh.points]).flatten()
    ax.auto_scale_xyz(scale, scale, scale)

    # Display dimensions as text
    dim_text = f"Min: {dimensions[0]}\nMax: {dimensions[1]}"
    ax.text(center_point[0], center_point[1], center_point[2],
            dim_text, color='red', fontsize=12, ha="center")

    plt.show()

def main(stl_file_path):
    # Load the STL file
    stl_mesh = load_stl(stl_file_path)

    # Calculate dimensions
    min_point, max_point = calculate_dimensions(stl_mesh)
    dimensions = (min_point, max_point)
    print(f"Dimensions: Min: {min_point}, Max: {max_point}")

    # Render the mesh with dimensions
    render_stl_with_dimensions(stl_mesh, dimensions)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_stl_file>")
        sys.exit(1)
    
    stl_file_path = sys.argv[1]
    main(stl_file_path)
