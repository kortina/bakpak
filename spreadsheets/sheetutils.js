function quarterFromString(datestring) {
  var parts = datestring.split("-");
  var m = parseInt(parts[1], 10);
  var q;
  if (m <= 3) q = 1;
  else if (m <= 6) q = 2;
  else if (m <= 9) q = 3;
  else if (m <= 12) q = 4;
  return parts[0] + "-Q" + q.toString();
}
