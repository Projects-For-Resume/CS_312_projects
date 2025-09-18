from byu_pytest_utils import max_score

from test_utils import is_convex_hull

from convex_hull import compute_hull
from generate import generate_random_points


@max_score(5)
def test_uniform_distribution_small():
    points = generate_random_points('uniform', 10, 312)
    candidate_hull = compute_hull(points)
    assert is_convex_hull(candidate_hull, points)


@max_score(15)
def test_uniform_distribution_large():
    points = generate_random_points('uniform', 20000, 312)
    candidate_hull = compute_hull(points)
    assert is_convex_hull(candidate_hull, points)


@max_score(5)
def test_guassian_distribution_small():
    points = generate_random_points('guassian', 10, 312)
    candidate_hull = compute_hull(points)
    assert is_convex_hull(candidate_hull, points)


@max_score(15)
def test_guassian_distribution_large():
    points = generate_random_points('guassian', 20000, 312)
    candidate_hull = compute_hull(points)
    assert is_convex_hull(candidate_hull, points)


def test_uniform_distribution_base_case():
    points:list[tuple] = [(1,2),(3,3),(4,2)]
    candidate_hull = compute_hull(points)
    assert is_convex_hull(candidate_hull, points)

def test_a_little_more_complicated():
    points:list[tuple] = [(1,2),(3,3),(4,2), (0,0)]
    candidate_hull = compute_hull(points)
    assert is_convex_hull(candidate_hull, points)

def test_even_more_difficult():
    points:list[tuple] = [(1,2),(3,2),(4,1), (0,0), (2, 3), (5,4)]
    candidate_hull:list[tuple[float, float]] = compute_hull(points)
    assert is_convex_hull(candidate_hull, points)

def test_uniform_distribution_100():
    points_100 = generate_random_points('uniform', 100, 123)
    candidate_hull_100 = compute_hull(points_100)
    assert is_convex_hull(candidate_hull_100, points_100)

def test_uniform_distribution_10000():
    points_10000 = generate_random_points('uniform', 1000, 123)
    candidate_hull_10000 = compute_hull(points_10000)
    assert is_convex_hull(candidate_hull_10000, points_10000)