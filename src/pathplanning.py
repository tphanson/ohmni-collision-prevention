import cv2 as cv
import numpy as np


class PathPlanning():
    def __init__(self, density=(14, 14)):
        self.density = density
        self.neighbour_map = self._gen_neighbours_map()

    def _gen_points(self):
        points = []
        for y in range(self.density[0]):
            for x in range(self.density[1]):
                points.append([y, x])
        return points

    def _gen_neighbours(self, point):
        [y, x] = point
        neighbours = np.unique([
            [max(0, y-1), max(0, x-1)],
            [max(0, y-1), x],
            [max(0, y-1), min(13, x+1)],
            [y, max(0, x-1)],
            [y, min(13, x+1)],
            [min(13, y+1), max(0, x-1)],
            [min(13, y+1), x],
            [min(13, y+1), min(13, x+1)],
        ], axis=0)
        neighbours = (e.tolist()
                      for e in neighbours if np.any(np.not_equal(e, point)))
        return list(neighbours)

    def _gen_neighbours_map(self):
        neighbour_map = {}
        for [y, x] in self._gen_points():
            key = '[{},{}]'.format(y, x)
            neighbour_map[key] = self._gen_neighbours([y, x])
        return neighbour_map

    def draw_bitmap(self, mask):
        bitmap = cv.resize(mask, self.density)
        bitmap[6:8, 6:8] = np.zeros((2, 2))
        return np.ceil(bitmap)

    def _distance(self, source, destination):
        return np.linalg.norm(np.array(source)-np.array(destination))

    def neighbours(self, point):
        [y, x] = point
        key = '[{},{}]'.format(y, x)
        return self.neighbour_map[key]

    def a_star(self, bitmap):
        return None

    def dijkstra(self, bitmap, source, detination):
        visited_nodes = []
        unvisited_nodes = [source]
        histogram = np.full(self.density, np.inf)
        histogram[source[0], source[1]] = 0.
        # Compute distances
        while len(unvisited_nodes) > 0:
            current_node = unvisited_nodes.pop(0)
            visited_nodes.append(current_node)
            for neighbour in self.neighbours(current_node):
                [y, x] = neighbour
                current_value = histogram[current_node[0], current_node[1]]
                visited = neighbour in visited_nodes
                waiting = neighbour in unvisited_nodes
                occupied = bitmap[y, x] != 0
                if not visited and not waiting:
                    unvisited_nodes.append(neighbour)
                if not visited and not occupied:
                    histogram[y, x] = min(
                        histogram[y, x], current_value + self._distance(current_node, neighbour))
        # Trace the path
        trajectory = [detination]
        existed = histogram[detination[0], detination[1]] < np.inf
        reached = False
        while existed and not reached:
            min_node = None
            min_distance = np.inf
            for neighbour in self.neighbours(detination):
                [y, x] = neighbour
                distance = histogram[y, x]
                if distance < min_distance:
                    min_node = neighbour
                    min_distance = distance
            detination = min_node
            trajectory.append(min_node)
            reached = source in trajectory
        # Return trajectory
        return trajectory
