# frozen_string_literal: true

Gem::Specification.new do |spec|
  spec.name        = "billing"
  spec.version     = "4.11.0"
  spec.authors     = ["Meridian Platform"]
  spec.summary     = "Billing engine: client, posting, and settlement primitives."
  spec.files       = Dir["lib/**/*.rb", "app/**/*.rb"]
  spec.required_ruby_version = ">= 3.3"
end
