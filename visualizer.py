from tree import Node, NodeType

class Visualizer:
    @staticmethod
    def visualize(node):
        lines, _, _ = Visualizer._display(node)
        for line in lines:
            print(line)
    
    @staticmethod
    def _display(node):
        if node is None:
            return [], 0, 0
        
        label = str(node.value) if node.value != 'u-' else '-'
        width = len(label)
        
        if node.type == NodeType.NUMBER:
            return [label], width, width // 2
        
        if node.value == 'u-':
            # Унарный оператор
            child_lines, cw, cm = Visualizer._display(node.right)
            
            if cm >= 0:
                first = " " * cm + label + " " * (cw - cm - 1)
                second = " " * cm + "\\" + " " * (cw - cm - 1)
            else:
                first = label + " " * (cw - 1)
                second = "\\" + " " * (cw - 1)
            
            return [first, second] + child_lines, cw, 0
        
        # БИНАРНЫЙ ОПЕРАТОР
        left_lines, lw, lm = Visualizer._display(node.left)
        right_lines, rw, rm = Visualizer._display(node.right)
        
        spacing = 2
        total_width = lw + spacing + rw
        
        left_center = lm
        right_center = lw + spacing + rm
        operator_pos = (left_center + right_center) // 2
        
        label_start = operator_pos - width // 2
        label_line = list(" " * total_width)
        for i in range(width):
            pos = label_start + i
            if 0 <= pos < total_width:
                label_line[pos] = label[i]
        label_line = "".join(label_line)
        
        branch_line = list(" " * total_width)
        
        if lw > 0 and lm >= 0 and lm < len(branch_line):
            if operator_pos > lm:
                branch_line[lm] = "/"
        
        right_branch_pos = lw + spacing + rm
        if rw > 0 and rm >= 0 and right_branch_pos < len(branch_line):
            if operator_pos < right_branch_pos:
                branch_line[right_branch_pos] = "\\"
        
        branch_line = "".join(branch_line)
        
        max_h = max(len(left_lines), len(right_lines))
        left_lines += [" " * lw] * (max_h - len(left_lines))
        right_lines += [" " * rw] * (max_h - len(right_lines))
        
        merged = []
        for i in range(max_h):
            merged.append(left_lines[i] + " " * spacing + right_lines[i])
        
        return [label_line, branch_line] + merged, total_width, operator_pos