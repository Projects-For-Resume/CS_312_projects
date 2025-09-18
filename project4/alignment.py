import math

def align(
        seq1: str,
        seq2: str,
        match_award=-3,
        indel_penalty=5,
        sub_penalty=1,
        banded_width=-1,
        gap='-'
) -> tuple[float, str | None, str | None]:
    """
        Align seq1 against seq2 using Needleman-Wunsch
        Put seq1 on left (j) and seq2 on top (i)
        => matrix[i][j]
        :param seq1: the first sequence to align; should be on the "left" of the matrix
        :param seq2: the second sequence to align; should be on the "top" of the matrix
        :param match_award: how many points to award a match
        :param indel_penalty: how many points to award a gap in either sequence
        :param sub_penalty: how many points to award a substitution
        :param banded_width: banded_width * 2 + 1 is the width of the banded alignment; -1 indicates full alignment
        :param gap: the character to use to represent gaps in the alignment strings
        :return: alignment cost, alignment 1, alignment 2
    """
    return_tuple: tuple[float, str | None, str | None] = (0.0, "","")

    if banded_width == -1:
        matrix_cost_traceback_list: list[list[tuple[float, int|None]]] = initialize_matrix_unrestricted(seq1, seq2, indel_penalty)
        matrix_cost_traceback_list = NeedleMan_Wunsch_unrestricted(matrix_cost_traceback_list, seq1, seq2, match_award, indel_penalty, sub_penalty, banded_width)
        return_tuple = traceback_unrestricted(matrix_cost_traceback_list, seq1, seq2, gap)
    else:
        matrix_cost_traceback_dict: dict[tuple[int,int], tuple[float,int|None]] = initialize_matrix_banded(seq1, seq2, banded_width,indel_penalty)
        matrix_cost_traceback_dict = NeedleMan_Wunsch_banded(matrix_cost_traceback_dict, seq1, seq2, match_award, indel_penalty, sub_penalty, banded_width)
        return_tuple = traceback_banded(matrix_cost_traceback_dict, seq1, seq2, gap)
    return return_tuple

def initialize_matrix_unrestricted(seq1: str, seq2: str, indel_penalty=5) -> list[list[tuple[float, int|None]]]:

    zero_matrix:list[list[tuple[float, int|None]]] = [[(0.0, 0) for j in range(len(seq1)+1)] for i in range(len(seq2)+1)]

    for m in range(len(zero_matrix[0])):
        if m == 0:
            continue
        else:
            zero_matrix[0][m] = (zero_matrix[0][m - 1][0] + float(indel_penalty), 1)
    
    for n in range(len(zero_matrix)):
        if n == 0:
            continue
        else:
            zero_matrix[n][0] = (zero_matrix[n-1][0][0] + float(indel_penalty), 2)

    return zero_matrix

def initialize_matrix_banded(seq1: str, seq2: str, banded_width:int, indel_penalty=5)->dict[tuple[int,int], tuple[float,int|None]]:
    if abs(len(seq1) - len(seq2)) > banded_width:
        return {(0,0): (math.inf, None)}

    matrix:dict[tuple[int,int], tuple[float,int|None]] = {}
    
    matrix[(0,0)] = (0.0, 0)
    
    for j in range(1, min(banded_width+1, len(seq1)+1)):
        matrix[(0,j)] = (matrix[(0,j-1)][0] + indel_penalty, 1)
    
    for i in range(1, min(banded_width+1, len(seq2)+1)):
        matrix[(i,0)] = (matrix[(i-1,0)][0] + indel_penalty, 2)

    return matrix

def NeedleMan_Wunsch_unrestricted(
        matrix_cost_traceback_list: list[list[tuple[float, int|None]]],
        seq1: str,
        seq2: str,
        match_award=-3,
        indel_penalty=5,
        sub_penalty=1,
        banded_width=-1
        ) -> list[list[tuple[float, int|None]]]:
    
   
    for i in range(1,len(matrix_cost_traceback_list)):
        for j in range(1,len(matrix_cost_traceback_list[0])):
            
            # if seq1[j-1] == seq2[i-1]:
            #     matrix_cost_traceback_list[i][j] = (matrix_cost_traceback_list[i-1][j-1][0] + match_award, 0)
            # else:
                matrix_cost_traceback_list[i][j] = compare_diagonal_top_left_unrestricted(i,j, seq1, seq2, matrix_cost_traceback_list, indel_penalty, sub_penalty, match_award)

    return matrix_cost_traceback_list
    
def NeedleMan_Wunsch_banded(
        matrix_cost_traceback_dict: dict[tuple[int,int], tuple[float,int|None]],
        seq1: str,
        seq2: str,
        match_award=-3,
        indel_penalty=5,
        sub_penalty=1,
        banded_width=-1
        ) -> dict[tuple[int,int], tuple[float,int|None]]:
    
   
    for i in range(1, len(seq2)+1):
        for j in range(max(1, i-banded_width), min(len(seq1)+1, i+banded_width+1)):
            # if seq1[j-1] == seq2[i-1]:
            #     matrix_cost_traceback_dict[(i,j)] = (matrix_cost_traceback_dict[(i-1,j-1)][0] + match_award, 0)
            # else:
                matrix_cost_traceback_dict[(i,j)] = compare_diagonal_top_left_banded(i, j, seq1, seq2, matrix_cost_traceback_dict, indel_penalty, sub_penalty, match_award)
    
    return matrix_cost_traceback_dict

def compare_diagonal_top_left_unrestricted(i:int, j:int, seq1:str, seq2:str, matrix_cost_traceback: list[list[tuple[float, int|None]]]|dict,
                              indel_penalty=5, sub_penalty=1, match_award = -3) -> tuple[float, int|None]:

    if seq1[j-1] == seq2[i-1]:
        diagonal:tuple[float, int|None] = (matrix_cost_traceback[i-1][j-1][0] + match_award, 0)
    
    else:
        diagonal = (matrix_cost_traceback[i-1][j-1][0] + sub_penalty, 0)

    left:tuple[float, int|None] = (matrix_cost_traceback[i][j-1][0] + indel_penalty, 1)
    top:tuple[float, int|None] = (matrix_cost_traceback[i-1][j][0] + indel_penalty, 2)


    if diagonal[0] <= left[0] and diagonal[0] <= top[0]: 
        return diagonal
    elif left[0] >= top[0]:
        return top
    else:
        return left

def compare_diagonal_top_left_banded(i:int, j:int, seq1:str, seq2:str, matrix_cost_traceback: dict[tuple[int,int], tuple[float,int|None]],
                              indel_penalty=5, sub_penalty=1, match_award = -3):
    
    diagonal = (math.inf, 0)
    top = (math.inf, 2)
    left = (math.inf, 1)
    
    if (i-1, j-1) in matrix_cost_traceback:
        if seq1[j-1] == seq2[i-1]:
            diagonal = (matrix_cost_traceback[(i-1,j-1)][0] + match_award, 0)
        else:
            diagonal = (matrix_cost_traceback[(i-1,j-1)][0] + sub_penalty, 0)
        
    
    if (i-1, j) in matrix_cost_traceback:
        top = (matrix_cost_traceback[(i-1,j)][0] + indel_penalty, 2)
    
    if (i, j-1) in matrix_cost_traceback:
        left = (matrix_cost_traceback[(i,j-1)][0] + indel_penalty, 1)
    
    if diagonal[0] <= top[0] and diagonal[0] <= left[0]:
        return diagonal
    elif left[0] >= top[0]:
        return top
    else:
        return left

def traceback_unrestricted(matrix: list[list[tuple[float, int|None]]]|dict, seq1: str, seq2: str, gap='-') -> tuple[float, str | None, str | None]:
    i = len(seq2)
    j = len(seq1)

    seq1_aligned = ""
    seq2_aligned = ""
    
    cost: float = matrix[i][j][0]
    
    while i > 0 or j > 0:
        
        direction: int|None = matrix[i][j][1]
    #   Diagonal
        if direction == 0: 
            seq1_aligned = seq1[j-1] + seq1_aligned
            seq2_aligned = seq2[i-1] + seq2_aligned
            i -= 1
            j -= 1
#       Left
        elif direction == 1:  

            seq1_aligned = seq1[j-1] + seq1_aligned
            seq2_aligned = gap + seq2_aligned
            j -= 1
#       Top
        else:
            
            seq1_aligned = gap + seq1_aligned
            seq2_aligned = seq2[i-1] + seq2_aligned
            i -= 1
    
    return (cost, seq1_aligned, seq2_aligned)

def traceback_banded(matrix: dict[tuple[int,int], tuple[float,int|None]], seq1: str, seq2: str, gap='-') -> tuple[float, str | None, str | None]:
    i = len(seq2)
    j = len(seq1)
    
    if (0,0) in matrix and matrix[(0,0)][0] == math.inf:
        return (math.inf, None, None)
    
    if (i, j) not in matrix:
        best_score = math.inf
        best_pos = None
        
        for pos in matrix:
            if (pos[0] == i or pos[1] == j) and matrix[pos][0] < best_score:
                best_score = matrix[pos][0]
                best_pos = pos
        
        if best_pos is None:
            return (math.inf, None, None)
        
        i, j = best_pos
    
    seq1_aligned = ""
    seq2_aligned = ""
    
    cost: float = matrix[(i,j)][0]
    
    while i > 0 or j > 0:
        if (i, j) not in matrix:
            return (math.inf, None, None)
        
        direction: int|None = matrix[(i,j)][1]
        
        match direction:
            case 0:  
                seq1_aligned = seq1[j-1] + seq1_aligned
                seq2_aligned = seq2[i-1] + seq2_aligned
                i -= 1
                j -= 1
            case 1:  
                seq1_aligned = seq1[j-1] + seq1_aligned
                seq2_aligned = gap + seq2_aligned
                j -= 1
            case 2:  
                seq1_aligned = gap + seq1_aligned
                seq2_aligned = seq2[i-1] + seq2_aligned
                i -= 1
            case None:
                return (math.inf, None, None)
    
    return (cost, seq1_aligned, seq2_aligned)
