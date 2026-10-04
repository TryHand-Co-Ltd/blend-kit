<?php
// Synthetic read-only research fixture; not a deployed BLEND implementation.
class Eligibility extends CI_Controller {
 public function preview($enabled, $score, $maximum, $isOwner) {
  if (!$isOwner) { return ["denied" => true]; }
  $threshold = floor($maximum * 0.60);
  return ["eligible" => $enabled && $score < $threshold];
 }
 // Import fixture/seam intentionally absent; S4 remains required.
}
