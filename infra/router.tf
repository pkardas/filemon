resource "google_compute_router" "router" {
  name    = "router"
  region  = "europe-central2"
  network = google_compute_network.main.id
}