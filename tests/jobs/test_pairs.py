from nose.tools import eq_, ok_

from odetta.jobs.pairs import *
from tests import *


disable_mrjob_loggers()


@dummytest(DistanceStatistics(), 'distance_stats')
def test_distance_stats(out):
    eq_([('Gaps', 'Mean: 470.0, Standard Deviation: 509.411425078, Variance: 259500.0, N: 5.0'), ('Overlaps', 'Mean: 378.333333333, Standard Deviation: 560.119034968, Variance: 313733.333333, N: 3.0')], out)


@dummytest(ToSplat(), 'combine_splats')
def test_ToSplat(out):
    eq_(2, len(out))
    a = '\t'.join(['ChrD', 'AT-GT', '10', '11', '13', '21', '22', '23', '24',
                   'ATCG', '2', 'bay1,bay2', '-'])
    b = '\t'.join(['ChrC', 'AT-GT', '50', '51', '53', '61', '62', '63', '64',
                   'ATTT', '2', 'foo1,foo2', '-'])
    ok_([b, a], sorted([x[1] for x in out]))


@dummytest(DistanceFilter(args=['--min-distance', '100', '--max-distance', '1000']), 
           'distance_filter')
def test_ValidFilter_by_distance(out):
    eq_(['bar', 'bas'], sorted([x[0] for x in out]))


@dummytest(UnambiguousFilter(), 'unambiguous')
def test_unambiguous_filter(out):
    eq_([('foo\\1', 'foo\\2'), ('foo\\2', 'foo\\1')], 
        sorted([(x[1][0]['ID'], x[1][1]['ID']) for x in out]))


@dummytest(UnambiguousFilter(args=['--invert']), 'unambiguous')
def test_inverted_unambiguous_filter(out):
    eq_([('bar\\1', 'bar\\2'), ('bar\\1', 'bar\\2')], 
        sorted([(x[1][0]['ID'], x[1][1]['ID']) for x in out]))


@dummytest(ReferenceCounts(), 'reference_counts')
def test_reference_counts(out):
    eq_(3, len(out))
    d = dict(x for x in out)
    eq_({'one-one': 1, 'one-two': 2}, d['ChrC'])
    eq_({'one-one': 3}, d['ChrD'])
    eq_({'one-one': 1}, d['ChrR'])


@dummytest(Combiner(), 'combiner')
def test_combiner(out):
    eq_([('foo:7:1:1:1#0/1', 'foo:7:1:1:1#0/2'), 
         ('foo:7:1:1:5#0/1', 'foo:7:1:1:5#0/2'), 
         ('foo:7:1:1:5#0/1', 'foo:7:1:1:5#0/2')], 
        sorted([(x[1][0]['ID'], x[1][1]['ID']) for x in out]))


@dummytest(Combiner(args=['--unambiguous-only']), 'combiner')
def test_unambiguous_combiner(out):
    eq_([('foo:7:1:1:1#0/1', 'foo:7:1:1:1#0/2')], 
        [(x[1][0]['ID'], x[1][1]['ID']) for x in out])
