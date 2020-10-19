import cv2 as cv
import numpy as np

DENSITY = 14


class PathPlanning():
    def __init__(self):
        self.neighbour_map = self._gen_neighbours_map()

    def _gen_points(self):
        points = []
        for y in range(DENSITY):
            for x in range(DENSITY):
                points.append([x, y])
        return points

    def _gen_neighbours(self, point):
        [x, y] = point
        neighbours = np.unique([
            [max(0, x-1), max(0, y-1)],
            [x, max(0, y-1)],
            [min(DENSITY-1, x+1), max(0, y-1)],
            [max(0, x-1), y],
            [min(DENSITY-1, x+1), y],
            [max(0, x-1), min(DENSITY-1, y+1)],
            [x, min(DENSITY-1, y+1)],
            [min(DENSITY-1, x+1), min(DENSITY-1, y+1)],
        ], axis=0)
        neighbours = (e.tolist()
                      for e in neighbours if np.any(np.not_equal(e, point)))
        return list(neighbours)

    def _gen_neighbours_map(self):
        neighbour_map = {}
        for [x, y] in self._gen_points():
            key = '[{},{}]'.format(x, y)
            neighbour_map[key] = self._gen_neighbours([x, y])
        return neighbour_map

    def draw_bitmap(self, mask):
        bitmap = cv.resize(mask, (DENSITY, DENSITY))
        centroid = int(DENSITY/2)
        bitmap[centroid:, (centroid-1):(centroid+1)] = 0
        return np.ceil(bitmap)

    def _distance(self, source, destination):
        return np.linalg.norm(np.array(source)-np.array(destination))

    def neighbours(self, point):
        [x, y] = point
        key = '[{},{}]'.format(x, y)
        return self.neighbour_map[key]

    def dijkstra(self, bitmap, source, detination):
        visited_nodes = []
        unvisited_nodes = [source]
        histogram = np.full((DENSITY, DENSITY), np.inf)
        histogram[source[1], source[0]] = 0.
        # Compute distances
        while len(unvisited_nodes) > 0:
            current_node = unvisited_nodes.pop(0)
            visited_nodes.append(current_node)
            for neighbour in self.neighbours(current_node):
                [x, y] = neighbour
                current_value = histogram[current_node[1], current_node[0]]
                visited = neighbour in visited_nodes
                waiting = neighbour in unvisited_nodes
                occupied = bitmap[y, x] != 0
                if not visited and not waiting:
                    unvisited_nodes.append(neighbour)
                if not visited and not occupied:
                    histogram[y, x] = min(
                        histogram[y, x], current_value + self._distance(current_node, neighbour))
        # Trace the path
        if not histogram[detination[1], detination[0]] < np.inf:
            return None
        trajectory = [detination]
        reached = False
        while not reached:
            min_node = None
            min_distance = np.inf
            for neighbour in self.neighbours(detination):
                [x, y] = neighbour
                distance = histogram[y, x]
                if distance < min_distance:
                    min_node = neighbour
                    min_distance = distance
            detination = min_node
            trajectory.append(detination)
            reached = source in trajectory
        # Return trajectory
        return trajectory
