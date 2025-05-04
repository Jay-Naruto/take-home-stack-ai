
import numpy as np

class BallTreeNode:
    def __init__(self, center, radius, left=None, right=None, points=None, indices=None):
        self.center = center
        self.radius = radius
        self.left = left

        self.right = right

        self.points = points  
        self.indices = indices 

class BallTree:
    def __init__(self, data, ids, leaf_size= 1):
        self.data = np.array(data,dtype =np.float64)
        self.ids = np.array(ids)

        self.leaf_size = leaf_size
        self.tree = self.build_tree(np.arange(len(data)))
    
    def build_tree(self, indices):

        points = self.data[indices]
        
        if len(points)<=self.leaf_size:
            return BallTreeNode(
                center=np.mean(points, axis=0), 
                radius=0 if len(points) == 1 else np.max(np.linalg.norm(points - np.mean(points, axis=0), axis=1)),
                points=points,
                indices=self.ids[indices]
            )
        
        center = np.mean(points,axis=0)
        distances = np.linalg.norm(points -center, axis=1)
        radius = np.max(distances)
        
        variances = np.var(points,axis=0)
        split_dim = np.argmax(variances)
        
        sorted_indices = np.argsort(points[:,split_dim])
        mid_idx = len(sorted_indices) // 2
        
        left_indices = indices[sorted_indices[:mid_idx]]
        right_indices = indices[sorted_indices[mid_idx:]]
        
        left = self.build_tree(left_indices)
        right = self.build_tree(right_indices)
        
        return BallTreeNode(center=center, radius=radius,left=left, right=right)
    
    def knn_search(self, query, k):
        query = np.array(query,dtype=np.float64)
        
        candidates = []
        results = []
        root_dist = np.linalg.norm(query - self.tree.center)
        candidates.append((root_dist, self.tree))
        
        while candidates and (len(results) < k or candidates[0][0] < results[0][0]):
            candidates.sort(key=lambda x: x[0],reverse=True)  
            dist, node = candidates.pop()
            
            if node.points is not None:
                for i, point_idx in enumerate(node.indices):
                    point_dist = np.linalg.norm(query-node.points[i])
                    results.append((point_dist, point_idx))
                    results.sort(key=lambda x: x[0])  
                    if len(results) > k:
                        results.pop()
            else:
                if node.left:
                    left_dist = np.linalg.norm(query- node.left.center)
                    if len(results) < k or left_dist - node.left.radius <results[0][0]:
                        candidates.append((left_dist, node.left))
                
                if node.right:
                    right_dist = np.linalg.norm(query- node.right.center)
                    if len(results) < k or right_dist - node.right.radius <results[0][0]:
                        candidates.append((right_dist, node.right))
        
        return [(id_val, dist) for dist, id_val in results]