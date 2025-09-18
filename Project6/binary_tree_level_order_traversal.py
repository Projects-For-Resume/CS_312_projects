from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        


def levelOrder(self, root:TreeNode) -> list[list[int]]:
    if not root:
        return[]
    
    ans:list[list[int]] = []
    queue:deque = deque([root])

    while queue:

        lvl_len:int = len(queue)
        current_lvl:list = []

        for _ in range(lvl_len):
            node:TreeNode = queue.popleft()
            current_lvl.append(node.val)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        ans.append(current_lvl)

    return ans