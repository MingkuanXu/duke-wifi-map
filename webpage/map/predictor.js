
var numNeighbors = 3;  // Number of nearest neighbors (dummy for now; will use value from training later)
//var decayConstant = 1;  // Since signal strengths between

// Allow a maximum distance of 250m for the nearest neighbors with measurements.
// This translates to the following latitude/longitude boundaries.
// (Measurements at the corner of the boundary will still be far away - we'll finetune them later.)
var maxDist = 250;
var maxLatDelta = 0.0023;
var maxLonDelta = 0.0028;

// Return -1: Ignore this point
function getSignal(lat, lon) {
  return 3;
}
