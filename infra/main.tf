provider "google" {
  project = "filemon-355819"
  region  = "europe-central2"
}

terraform {
  backend "gcs" {
      bucket = "filemon-tf-state"
    prefix = "terraform/state"
  }

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}