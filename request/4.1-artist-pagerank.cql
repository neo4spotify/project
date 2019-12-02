// Without writing pageRank to Artist
CALL algo.pageRank.stream('Artist', 'IS_RELATED_TO', {iterations:40, dampingFactor:0.85})
YIELD nodeId, score

RETURN algo.asNode(nodeId).artist_name AS Artist,score
ORDER BY score DESC
LIMIT 50

// Writing pageRank to Artist
CALL algo.pageRank('Artist', 'IS_RELATED_TO',
  {iterations:40, dampingFactor:0.85, write: true,writeProperty:"pagerank"})
YIELD nodes, iterations, loadMillis, computeMillis, writeMillis, dampingFactor, write, writeProperty