from pathlib import Path
from byu_pytest_utils import with_import, max_score, test_files

@max_score(5)
@with_import('alignment')
def test_initialize_matrix(initialize_matrix_unrestricted):
    seq1 = "seq1"
    seq2 = "seq2"
    indel_penalty = 5
    
    matrix = initialize_matrix_unrestricted(seq1, seq2, indel_penalty)
    
    assert len(matrix) == len(seq2) + 1
    assert len(matrix[0]) == len(seq1) + 1
    
    assert matrix[0][0] == (0.0, 0)
    
    for j in range(1, len(seq1) + 1):
        assert matrix[0][j] == (j * indel_penalty, 1)
    
    for i in range(1, len(seq2) + 1):
        assert matrix[i][0] == (i * indel_penalty, 2)
    
    print(matrix)

def test_needleman_wunsch():
    from alignment import NeedleMan_Wunsch, initialize_matrix_unrestricted
    
    seq1 = "AT"
    seq2 = "AG"
    
    matrix = initialize_matrix_unrestricted(seq1, seq2)
    
    filled_matrix = NeedleMan_Wunsch(matrix, seq1, seq2)
    
    assert len(filled_matrix) == len(seq2) + 1
    assert len(filled_matrix[0]) == len(seq1) + 1
    
    assert filled_matrix[0][0] == (0.0, 0)
    
    assert filled_matrix[1][1][0] == -3  # Match reward
    assert filled_matrix[1][1][1] == 0   # Diagonal direction
    
    assert filled_matrix[1][2][0] == 2
    assert filled_matrix[1][2][1] == 1
    
    assert filled_matrix[2][2][0] == -2
    assert filled_matrix[2][2][1] == 0

def test_unrestricted_algorithm():
    from alignment import align
    
    seq1 = "AT"
    seq2 = "AG"
    
    score, aligned_seq1, aligned_seq2 = align(seq1, seq2)
    
    assert score == -2
    assert aligned_seq1 == "AT"
    assert aligned_seq2 == "AG"
   
def test_initialize_matrix_banded():
    from alignment import initialize_matrix_banded
    import math
    
    # Test case 1: Sequences that can be aligned within the band
    seq1 = "ACTG"
    seq2 = "ACGG"
    banded_width = 2
    indel_penalty = 5
    
    matrix = initialize_matrix_banded(seq1, seq2, banded_width, indel_penalty)
    
    # Check matrix dimensions
    assert len(matrix) == len(seq2) + 1
    assert len(matrix[0]) == len(seq1) + 1
    
    # Check (0,0) initialization
    assert matrix[0][0] == (0.0, 0)
    
    # Check first row initialization within band
    assert matrix[0][1] == (5.0, 1)
    assert matrix[0][2] == (10.0, 1)
    assert matrix[0][3] == (15.0, 1)
    
    # Check first column initialization within band
    assert matrix[1][0] == (5.0, 2)
    assert matrix[2][0] == (10.0, 2)
    
    # Check cells outside the band are (inf, None)
    assert matrix[4][1] == (math.inf, None)
    
    # Test case 2: Sequences that cannot be aligned within the band
    seq1 = "ACTGACTG"
    seq2 = "AC"
    banded_width = 2
    
    matrix = initialize_matrix_banded(seq1, seq2, banded_width, indel_penalty)
    
    # Should create a 1x1 matrix with (0, 0) at position (0,0)
    assert len(matrix) == 1
    assert len(matrix[0]) == 1
    assert matrix[0][0] == (math.inf, None)


def test_needleman_wunsch_banded():
    from alignment import NeedleMan_Wunsch, initialize_matrix_banded
    import math
    
    # Test with small sequences
    seq1 = "ACTG"
    seq2 = "ACGG"
    banded_width = 2
    
    # Create a matrix with proper initialization
    matrix = [[(math.inf, None) for j in range(len(seq1)+1)] for i in range(len(seq2)+1)]
    matrix[0][0] = (0.0, 0)
    
    # Initialize first row and column within band
    for j in range(1, min(banded_width+1, len(seq1)+1)):
        matrix[0][j] = (matrix[0][j-1][0] + 5, 1)
    
    for i in range(1, min(banded_width+1, len(seq2)+1)):
        matrix[i][0] = (matrix[i-1][0][0] + 5, 2)
    
    # Run the algorithm
    filled_matrix = NeedleMan_Wunsch(matrix, seq1, seq2, banded_width=banded_width)
    
    # Check dimensions
    assert len(filled_matrix) == len(seq2) + 1
    assert len(filled_matrix[0]) == len(seq1) + 1
    
    # Check specific cells within the band
    assert filled_matrix[1][1][0] == -3  # Match reward
    assert filled_matrix[1][1][1] == 0   # Diagonal direction
    
    # Check cells outside the band remain infinity
    assert filled_matrix[4][1][0] == math.inf
    
    # Check bottom-right cell (final score)
    assert filled_matrix[4][4][0] != math.inf  # Should have a valid score

def test_compare_diagonal_top_left_banded():
    from alignment import compare_diagonal_top_left_banded
    import math
    
    # Create a test matrix
    matrix = [[(math.inf, None) for j in range(5)] for i in range(5)]
    
    # Set up some known values
    matrix[1][1] = (-3.0, 0)  # Diagonal from (2,2)
    matrix[1][2] = (2.0, 1)   # Top from (2,2)
    matrix[2][1] = (2.0, 2)   # Left from (2,2)
    
    # Test within band
    banded_width = 2
    result = compare_diagonal_top_left_banded(2, 2, banded_width, matrix)
    
    # Should choose diagonal (lowest score with tie-breaking)
    assert result[0] == -2.0  # -3.0 + 1 (sub_penalty)
    assert result[1] == 0     # Diagonal direction
    
    # Test with cell outside band
    matrix[3][0] = (10.0, 1)  # Outside band for position (4,1)
    result = compare_diagonal_top_left_banded(4, 1, banded_width, matrix)
    
    # All options should be infinity, default to diagonal
    assert result[0] == math.inf
    assert result[1] == 0
    
    # Test with only one valid direction
    matrix[2][3] = (5.0, 1)
    result = compare_diagonal_top_left_banded(3, 3, banded_width, matrix)
    
    # Only top direction is within band
    assert result[0] == 10.0  # 5.0 + 5 (indel_penalty)
    assert result[1] == 2     # Top direction

