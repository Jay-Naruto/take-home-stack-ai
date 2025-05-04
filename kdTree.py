import numpy as np

class KDTreeNode:
    def __init__(self, point, left=None, right=None, index=None):
        self.point = point

        self.left = left

        self.right = right
        self.index = index

class KDTree:
    def __init__(self, data,ids):
        self.data = np.array(data)
        self.ids = ids
        self.tree = self.build_tree(data, ids)

    def build_tree(self, points, ids, depth=0):
        if not points:
            return None
            
        if len(points) <= 1:
            return KDTreeNode(points[0], index=ids[0])

        axis = depth %len(points[0])
        sorted_points = sorted(zip(points, ids),key=lambda x:x[0][axis])
        median_index = len(sorted_points) // 2
        median_point, median_id = sorted_points[median_index]

        left_points= [p[0] for p in sorted_points[:median_index]]
        right_points= [p[0] for p in sorted_points[median_index+1:]]

        left_ids= [p[1] for p in sorted_points[:median_index]]
        right_ids= [p[1] for p in sorted_points[median_index+1:]]

        left = self.build_tree(left_points, left_ids, depth + 1)
        right = self.build_tree(right_points, right_ids, depth + 1)

        return KDTreeNode(median_point, left, right, index=median_id)

    def knn_search(self, query, k, node=None, best_list=None, depth=0):
        if node is None:
            node = self.tree
            if node is None:
                return []
                
        if best_list is None:
            best_list = []

        distance = np.linalg.norm(query - node.point)

        if len(best_list) < k:
            best_list.append((node, distance))
            best_list.sort(key=lambda x: x[1])
        else:
            if distance < best_list[-1][1]:
                best_list[-1] = (node, distance)
                best_list.sort(key=lambda x: x[1])

        axis = depth % len(query)
        next_branch = node.left if query[axis] <node.point[axis] else node.right
        opposite_branch = node.right if query[axis] <node.point[axis] else node.left

        if next_branch is not None:
            self.knn_search(query, k, next_branch,best_list, depth+1)

        if opposite_branch is not None and (len(best_list)<k or abs(query[axis] -node.point[axis]) < best_list[-1][1]):
            
            self.knn_search(query, k, opposite_branch, best_list,depth + 1)

        return [(node.index, dist) for node, dist in best_list]